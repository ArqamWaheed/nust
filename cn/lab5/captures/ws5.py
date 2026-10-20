"""Render Wireshark-style screenshots from the real lab5 capture (adapted from lab4 ws.py)."""
import warnings; warnings.filterwarnings("ignore")
from scapy.all import rdpcap, IP, IPv6, UDP, TCP, DNS
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/"
UI = ImageFont.truetype(FD + "dejavu/DejaVuSans.ttf", 13)
UIB = ImageFont.truetype(FD + "dejavu/DejaVuSans-Bold.ttf", 13)
TITLE = ImageFont.truetype(FD + "ubuntu/Ubuntu-B.ttf", 15)
MONO = ImageFont.truetype(FD + "dejavu/DejaVuSansMono.ttf", 13)

MANUF = {}
for line in open("/usr/share/wireshark/manuf", encoding="utf-8", errors="ignore"):
    if line.startswith("#") or "\t" not in line: continue
    pre, short = line.split("\t")[:2]
    if len(pre) == 8: MANUF[pre.upper()] = short.strip()

def macname(m):
    v = MANUF.get(m[:8].upper())
    return f"{v}_{m[9:]}" if v else m

QT = {1: "A", 28: "AAAA", 5: "CNAME", 65: "HTTPS"}
FLAGN = ["FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR"]
TLSHS = {1: "Client Hello", 2: "Server Hello", 4: "New Session Ticket"}

def ipl(p): return p[IP] if IP in p else p[IPv6]
def flagstr(f): return ", ".join(FLAGN[b] for b in range(8) if int(f) >> b & 1)
def opts(t): return dict((k, v) for k, v in t.options if k != "NOP")

def tls_records(pl):
    out, o = [], 0
    while o + 5 <= len(pl) and pl[o] in (0x14, 0x15, 0x16, 0x17) and pl[o + 1] == 3:
        L = int.from_bytes(pl[o + 3:o + 5], "big")
        if pl[o] == 0x16: out.append(TLSHS.get(pl[o + 5], "Handshake") if o + 5 < len(pl) else "Handshake")
        else: out.append({0x14: "Change Cipher Spec", 0x15: "Alert", 0x17: "Application Data"}[pl[o]])
        o += 5 + L
    return out

# ---------------------------------------------------------------- per-packet analysis
class Cap:
    def __init__(self, path):
        self.pk = rdpcap(path); self.t0 = float(self.pk[0].time)
        self.stream, self.base, self.ws, self.rows = {}, {}, {}, {}
        self.info = {}
        pending = set()
        for n, p in enumerate(self.pk, 1):
            if TCP not in p: continue
            l, t = ipl(p), p[TCP]
            k, r = (l.src, t.sport, l.dst, t.dport), (l.dst, t.dport, l.src, t.sport)
            sk = tuple(sorted([k[:2], k[2:]]))
            self.stream.setdefault(sk, len(self.stream))
            self.base.setdefault(k, t.seq if t.flags & 2 else t.seq - 1)
            if t.flags & 16: self.base.setdefault(r, t.ack - 1)
            if t.flags & 2: self.ws[k] = opts(t).get("WScale", -1)
            pl = bytes(t.payload)
            rel_s = (t.seq - self.base[k]) % 2**32
            rel_a = (t.ack - self.base[r]) % 2**32 if r in self.base else 0
            sc = self.ws.get(k) if (r in self.ws and k in self.ws and not t.flags & 2) else None
            win = t.window << sc if sc not in (None, -1) else t.window
            proto, extra = "TCP", ""
            if 80 in (t.sport, t.dport):
                if pl.startswith((b"GET ", b"POST ", b"HEAD ")): proto = "HTTP"
                elif pl.startswith(b"HTTP/") and b"\r\n0\r\n\r\n" not in pl: pending.add(sk); extra = " [TCP segment of a reassembled PDU]"
                elif pl == b"0\r\n\r\n" and sk in pending: proto = "HTTP"
            recs = tls_records(pl) if 443 in (t.sport, t.dport) else []
            if recs: proto = "TLSv1.3"
            info = f"{t.sport} → {t.dport} [{flagstr(t.flags)}] Seq={rel_s}"
            if t.flags & 16: info += f" Ack={rel_a}"
            info += f" Win={win} Len={len(pl)}"
            o = opts(t)
            if t.flags & 2:
                if "MSS" in o: info += f" MSS={o['MSS']}"
                if "SAckOK" in o: info += " SACK_PERM=1"
            if "Timestamp" in o: info += f" TSval={o['Timestamp'][0]} TSecr={o['Timestamp'][1]}"
            if t.flags & 2 and "WScale" in o: info += f" WS={2 ** o['WScale']}"
            info += extra
            if proto == "HTTP":
                info = pl.split(b"\r\n")[0].decode() if not pl.startswith(b"0") else "HTTP/1.1 200 OK  (text/html)"
            if recs: info = ", ".join(recs)
            self.info[n] = dict(stream=self.stream[sk], rs=rel_s, ra=rel_a, win=win, scale=sc, len=len(pl), proto=proto)
            self.rows[n] = [proto, info]

    def row(self, n):
        p = self.pk[n - 1]; l = ipl(p)
        t = f"{float(p.time) - self.t0:.6f}"
        if n in self.rows: proto, info = self.rows[n]
        elif DNS in p:
            d = p[DNS]; proto = "DNS"
            qs = [f"{QT.get(q.qtype, q.qtype)} {q.qname.decode().rstrip('.')}" for q in (d.qd or [])]
            ans = []
            for a in (d.an or []):
                rd = a.rdata.decode().rstrip(".") if isinstance(a.rdata, bytes) else str(a.rdata)
                ans.append(f"{QT.get(a.type, a.type)} {rd}")
            info = ("Standard query response " if d.qr else "Standard query ") + f"0x{d.id:04x} " + " ".join(qs + ans)
        else: proto, info = "UDP", ""
        return [str(n), t, l.src, l.dst, proto, str(len(p)), info]

    def color(self, n):
        p = self.pk[n - 1]
        if TCP not in p: return "#daeeff", "#12272e"
        t = p[TCP]
        if t.flags & 4: return "#a40000", "#fffc9c"
        if 80 in (t.sport, t.dport): return "#e4ffc7", "#12272e"
        if t.flags & 3: return "#a0a0a0", "#12272e"
        return "#e7e6ff", "#12272e"

# ---------------------------------------------------------------- detail-tree helpers
def frame_line(n, p, iface="wlp0s20f3"):
    L = len(p); return f"Frame {n}: {L} bytes on wire ({L*8} bits), {L} bytes captured ({L*8} bits) on interface {iface}, id 0"
def eth_line(p): return f"Ethernet II, Src: {macname(p.src)} ({p.src}), Dst: {macname(p.dst)} ({p.dst})"
def ip_line(p): return f"Internet Protocol Version 4, Src: {p[IP].src}, Dst: {p[IP].dst}"

def tcp_tree(cap, n, flags_open=False, opts_open=False, seqack=True):
    p = cap.pk[n - 1]; t = p[TCP]; i = cap.info[n]; hl = t.dataofs * 4
    nxt = i["rs"] + i["len"] + (1 if t.flags & 3 else 0)
    tr = [(0, True, f"Transmission Control Protocol, Src Port: {t.sport}, Dst Port: {t.dport}, Seq: {i['rs']}" +
           (f", Ack: {i['ra']}" if t.flags & 16 else "") + f", Len: {i['len']}"),
          (1, None, f"Source Port: {t.sport}"), (1, None, f"Destination Port: {t.dport}"),
          (1, None, f"[Stream index: {i['stream']}]"), (1, None, f"[TCP Segment Len: {i['len']}]"),
          (1, None, f"Sequence Number: {i['rs']}    (relative sequence number)"),
          (1, None, f"Sequence Number (raw): {t.seq}")]
    if i["len"] or t.flags & 3: tr.append((1, None, f"[Next Sequence Number: {nxt}    (relative sequence number)]"))
    tr += [(1, None, f"Acknowledgment Number: {i['ra'] if t.flags & 16 else 0}" + ("    (relative ack number)" if t.flags & 16 else "")),
           (1, None, f"Acknowledgment number (raw): {t.ack}"),
           (1, None, f"{hl // 4:04b} .... = Header Length: {hl} bytes ({hl // 4})"),
           (1, flags_open, f"Flags: 0x{int(t.flags):03x} ({flagstr(t.flags).replace(', ', ', ')})")]
    if flags_open:
        f = int(t.flags); bit = lambda b: "Set" if f >> b & 1 else "Not set"
        tr += [(2, None, "000. .... .... = Reserved: Not set"), (2, None, "...0 .... .... = Nonce: Not set"),
               (2, None, f".... {f>>7&1}... .... = Congestion Window Reduced (CWR): {bit(7)}"),
               (2, None, f".... .{f>>6&1}.. .... = ECN-Echo: {bit(6)}"),
               (2, None, f".... ..{f>>5&1}. .... = Urgent: {bit(5)}"),
               (2, None, f".... ...{f>>4&1} .... = Acknowledgment: {bit(4)}"),
               (2, None, f".... .... {f>>3&1}... = Push: {bit(3)}"),
               (2, None, f".... .... .{f>>2&1}.. = Reset: {bit(2)}"),
               (2, None, f".... .... ..{f>>1&1}. = Syn: {bit(1)}"),
               (2, None, f".... .... ...{f&1} = Fin: {bit(0)}"),
               (2, None, "[TCP Flags: ····" + "".join(c if f >> (7 - k) & 1 else "·" for k, c in enumerate("CEUAPRSF")) + "]")]
    tr.append((1, None, f"Window: {t.window}"))
    if i["scale"] is not None:
        tr.append((1, None, f"[Calculated window size: {i['win']}]"))
        tr.append((1, None, f"[Window size scaling factor: {2 ** i['scale']}]"))
    elif t.flags & 2: tr.append((1, None, f"[Calculated window size: {t.window}]"))
    tr += [(1, None, f"Checksum: 0x{t.chksum:04x} [unverified]"), (1, None, "[Checksum Status: Unverified]"),
           (1, None, "Urgent Pointer: 0")]
    o = opts(t)
    if hl > 20:
        names = []
        for k, v in t.options:
            names.append({"MSS": "Maximum segment size", "SAckOK": "SACK permitted", "Timestamp": "Timestamps",
                          "NOP": "No-Operation (NOP)", "WScale": "Window scale"}.get(k, k))
        tr.append((1, opts_open, f"Options: ({hl - 20} bytes), " + ", ".join(names)))
        if opts_open:
            for k, v in t.options:
                if k == "MSS": tr.append((2, False, f"TCP Option - Maximum segment size: {v} bytes"))
                elif k == "SAckOK": tr.append((2, False, "TCP Option - SACK permitted"))
                elif k == "Timestamp": tr.append((2, False, f"TCP Option - Timestamps: TSval {v[0]}, TSecr {v[1]}"))
                elif k == "NOP": tr.append((2, False, "TCP Option - No-Operation (NOP)"))
                elif k == "WScale": tr.append((2, False, f"TCP Option - Window scale: {v} (multiply by {2 ** v})"))
    if seqack and not t.flags & 2: tr.append((1, False, "[SEQ/ACK analysis]"))
    tr.append((1, False, "[Timestamps]"))
    if i["len"]: tr.append((1, None, f"TCP payload ({i['len']} bytes)"))
    return tr

# ---------------------------------------------------------------- themes
LIGHT = dict(bg="#ffffff", chrome="#ebebeb", title="#2c2c2c", titlefg="#f0f0f0", border="#c0c0c0", text="#1e1e1e",
             sel="#308cc6", ok="#afffaf", field="#ffffff", head="#f4f4f4", hint="#9a9a9a", icon="#555555", scroll="#b8b8b8")
DARK = dict(bg="#232323", chrome="#2f2f2f", title="#1b1b1b", titlefg="#e6e6e6", border="#4a4a4a", text="#e3e3e3",
            sel="#2a6ab0", ok="#2e5f2e", field="#1a1a1a", head="#353535", hint="#8a8a8a", icon="#c8c8c8", scroll="#5a5a5a")

def clip(d, s, font, w):
    if d.textlength(s, font=font) <= w: return s
    while s and d.textlength(s + "…", font=font) > w: s = s[:-1]
    return s + "…"

def icons(d, y, T):
    x = 12; ic = T["icon"]
    d.polygon([(x, y+20), (x+10, y+4), (x+18, y+20)], fill="#3b7bd4"); x += 30
    d.rectangle([x, y+5, x+14, y+19], fill="#d63c3c"); x += 30
    d.polygon([(x, y+20), (x+10, y+4), (x+18, y+20)], fill="#56a64b"); x += 30
    d.ellipse([x, y+4, x+16, y+20], outline=ic, width=3); d.ellipse([x+5, y+9, x+11, y+15], fill=ic); x += 34
    d.line([x-8, y+2, x-8, y+22], fill=T["border"])
    for _ in range(3): d.rectangle([x, y+5, x+16, y+19], outline=ic, width=2); x += 28
    d.line([x-4, y+2, x-4, y+22], fill=T["border"]); x += 6
    d.ellipse([x, y+4, x+14, y+18], outline=ic, width=2); d.line([x+12, y+16, x+18, y+22], fill=ic, width=2); x += 30
    for k in range(5):
        if k == 0: d.polygon([(x+14, y+5), (x+14, y+19), (x+3, y+12)], fill=ic)
        elif k == 1: d.polygon([(x+3, y+5), (x+3, y+19), (x+14, y+12)], fill=ic)
        else:
            d.line([(x+8, y+5), (x+8, y+19)], fill=ic, width=2)
            d.polygon([(x+3, y+13), (x+13, y+13), (x+8, y+19)] if k != 3 else [(x+3, y+10), (x+13, y+10), (x+8, y+4)], fill=ic)
        x += 28
    d.line([x-4, y+2, x-4, y+22], fill=T["border"]); x += 6
    for k in range(4):
        if k == 0:
            for j in range(4): d.line([(x+2, y+6+j*4), (x+16, y+6+j*4)], fill=ic, width=2)
        else:
            d.ellipse([x+1, y+3, x+17, y+19], outline=ic, width=2)
            if k in (1, 2): d.line([(x+5, y+11), (x+13, y+11)], fill=ic, width=2)
            if k == 1: d.line([(x+9, y+7), (x+9, y+15)], fill=ic, width=2)
        x += 28

def titlebar(d, W, title, T):
    d.rectangle([0, 0, W, 36], fill=T["title"])
    tw = d.textlength(title, font=TITLE); d.text(((W - tw) / 2, 9), title, font=TITLE, fill=T["titlefg"])
    for i, c in enumerate(("#e95420", "#7a7a7a", "#7a7a7a")):
        cx = W - 22 - i * 28; d.ellipse([cx - 9, 9, cx + 9, 27], fill=c)
    d.text((W - 27, 8), "×", font=UIB, fill="white")

COLS = [("No.", 56), ("Time", 88), ("Source", 150), ("Destination", 150), ("Protocol", 76), ("Length", 58), ("Info", None)]

def render(out, cap, title, filt, nums, sel=None, tree=(), tree_sel=None, raw=b"", hl=(0, 0), status=("", ""),
           W=1280, list_h=330, tree_h=None, bytes_h=150, T=LIGHT, box_rows=(), box_tree=(), chrome=True):
    tree_h = tree_h or max(110, 22 * len(tree) + 12)
    top = (36 + 26 + 34) if chrome else 0
    H = top + 32 + list_h + 6 + tree_h + (6 + bytes_h if bytes_h else 0) + 26
    im = Image.new("RGB", (W, H), T["bg"]); d = ImageDraw.Draw(im)
    y = 0
    if chrome:
        titlebar(d, W, title, T); y = 36
        d.rectangle([0, y, W, y + 26], fill=T["chrome"]); x = 10
        for m in "File Edit View Go Capture Analyze Statistics Telephony Wireless Tools Help".split():
            d.text((x, y + 4), m, font=UI, fill=T["text"]); x += d.textlength(m, font=UI) + 18
        y += 26; d.rectangle([0, y, W, y + 34], fill=T["chrome"]); icons(d, y + 4, T); y += 34
    # filter bar
    d.rectangle([0, y, W, y + 32], fill=T["chrome"])
    d.rectangle([8, y + 4, W - 120, y + 28], fill=T["ok"] if filt else T["field"], outline="#8a8a8a")
    d.polygon([(14, y + 9), (24, y + 9), (24, y + 23), (19, y + 19), (14, y + 23)], fill="#777")
    if filt: d.text((34, y + 8), filt, font=MONO, fill="#000" if T is LIGHT else "#f0f0f0")
    else: d.text((34, y + 8), "Apply a display filter … <Ctrl-/>", font=UI, fill=T["hint"])
    d.line([(W - 142, y + 16), (W - 128, y + 16)], fill=T["icon"], width=2); d.polygon([(W - 130, y + 11), (W - 124, y + 16), (W - 130, y + 21)], fill=T["icon"])
    d.text((W - 92, y + 7), "Expression…   +", font=UI, fill=T["text"])
    y += 32
    # packet list
    d.rectangle([0, y, W, y + 22], fill=T["head"]); d.line([0, y + 22, W, y + 22], fill=T["border"])
    xs = []; x = 0
    for name, w in COLS:
        xs.append(x); d.text((x + 6, y + 3), name, font=UI, fill=T["text"])
        if w: x += w; d.line([x, y, x, y + 22], fill=T["border"])
    ly = y + 23; rh = 20; rowy = {}
    for n in nums:
        if ly + rh > y + list_h: break
        r = cap.row(n); bg, fg = cap.color(n)
        if n == sel: bg, fg = T["sel"], "#ffffff"
        d.rectangle([0, ly, W - 14, ly + rh - 1], fill=bg)
        for i, (name, w) in enumerate(COLS):
            cw = (w or (W - 14 - xs[i])) - 10
            txt = clip(d, r[i], UI, cw)
            if name in ("No.", "Length"): d.text((xs[i] + (w - 6) - d.textlength(txt, font=UI), ly + 2), txt, font=UI, fill=fg)
            else: d.text((xs[i] + 6, ly + 2), txt, font=UI, fill=fg)
        if n == sel: d.polygon([(3, ly + 6), (3, ly + 14), (9, ly + 10)], fill="white")
        rowy[n] = ly; ly += rh
    d.rectangle([W - 14, y + 23, W, y + list_h], fill=T["chrome"])
    d.rounded_rectangle([W - 11, y + 40, W - 3, y + 80], 3, fill=T["scroll"])
    for grp in box_rows:
        ys = [rowy[n] for n in grp if n in rowy]
        if ys: d.rectangle([2, min(ys) - 1, W - 16, max(ys) + rh], outline="#e53935", width=3)
    y += list_h
    d.rectangle([0, y, W, y + 6], fill=T["chrome"]); y += 6
    # details
    ty = y + 4; treey = []
    for i, (lvl, exp, txt) in enumerate(tree):
        if i == tree_sel: d.rectangle([0, ty, W, ty + 21], fill=T["sel"])
        fg = "white" if i == tree_sel else T["text"]
        tx = 8 + 22 * lvl
        if exp is not None:
            cx, cy = tx + 5, ty + 11
            d.polygon([(cx - 5, cy - 3), (cx + 5, cy - 3), (cx, cy + 3)] if exp else [(cx - 3, cy - 5), (cx - 3, cy + 5), (cx + 3, cy)], fill=fg)
        d.text((tx + 16, ty + 2), clip(d, txt, UI, W - tx - 30), font=UI, fill=fg)
        treey.append((tx, ty, d.textlength(clip(d, txt, UI, W - tx - 30), font=UI))); ty += 22
    for a, b in box_tree:
        x0 = min(treey[k][0] for k in range(a, b + 1)) + 10
        x1 = max(treey[k][0] + treey[k][2] for k in range(a, b + 1)) + 26
        d.rectangle([x0, treey[a][1] - 1, min(x1, W - 4), treey[b][1] + 22], outline="#e53935", width=3)
    y += tree_h
    if bytes_h:
        d.rectangle([0, y, W, y + 6], fill=T["chrome"]); y += 6
        by = y + 4
        for off in range(0, min(len(raw), 16 * ((bytes_h - 8) // 18)), 16):
            chunk = raw[off:off + 16]
            d.text((8, by), f"{off:04x}", font=MONO, fill=T["text"])
            for j, b in enumerate(chunk):
                bx = 64 + j * 24 + (8 if j >= 8 else 0); ax = 480 + j * 9 + (9 if j >= 8 else 0)
                on = hl[0] <= off + j < hl[0] + hl[1]
                if on: d.rectangle([bx - 2, by, bx + 18, by + 16], fill=T["sel"]); d.rectangle([ax, by, ax + 8, by + 16], fill=T["sel"])
                col = "white" if on else T["text"]
                d.text((bx, by), f"{b:02x}", font=MONO, fill=col)
                d.text((ax, by), chr(b) if 32 <= b < 127 else "·", font=MONO, fill=col)
            by += 18
        y += bytes_h
    d.rectangle([0, y, W, H], fill=T["chrome"]); d.line([0, y, W, y], fill=T["border"])
    d.ellipse([8, y + 7, 20, y + 19], fill="#5cb85c")
    d.text((30, y + 5), status[0], font=UI, fill=T["text"])
    d.text((W / 2 - 120, y + 5), status[1], font=UI, fill=T["text"])
    d.text((W - 130, y + 5), "Profile: Default", font=UI, fill=T["text"])
    im.save(out)

# ---------------------------------------------------------------- follow tcp stream dialog
def follow(out, cap, stream, nums, title_file, T=LIGHT, W=1000, H=620):
    im = Image.new("RGB", (W, H), T["chrome"]); d = ImageDraw.Draw(im)
    titlebar(d, W, f"Wireshark · Follow TCP Stream (tcp.stream eq {stream}) · {title_file}", T)
    x0, y0, x1, y1 = 10, 46, W - 10, H - 150
    d.rectangle([x0, y0, x1, y1], fill=T["field"], outline=T["border"])
    first = None; cpk = spk = turns = 0; last = None; tot = 0
    lines = []  # (text, side)
    for n in nums:
        p = cap.pk[n - 1]; pl = bytes(p[TCP].payload)
        if not pl: continue
        side = ipl(p).src if first is None else ("c" if ipl(p).src == first else "s")
        if first is None: first = ipl(p).src; side = "c"
        cpk += side == "c"; spk += side == "s"; tot += len(pl)
        if side != last: turns += last is not None; last = side
        txt = "".join(c if c == "\n" or 32 <= ord(c) < 127 else "." for c in pl.decode("latin-1").replace("\r\n", "\n"))
        for seg in txt.split("\n"):
            while len(seg) > 118: lines.append((seg[:118], side)); seg = seg[118:]
            lines.append((seg, side))
    ly = y0 + 4
    cbg, cfg, sbg, sfg = ("#fbeded", "#7f0000", "#ededfb", "#00007f") if T is LIGHT else ("#4a2020", "#ffb3b3", "#20284a", "#b3c6ff")
    for txt, side in lines:
        if ly + 17 > y1 - 2: break
        d.rectangle([x0 + 2, ly, x1 - 16, ly + 16], fill=cbg if side == "c" else sbg)
        d.text((x0 + 6, ly), txt, font=MONO, fill=cfg if side == "c" else sfg); ly += 17
    d.rectangle([x1 - 14, y0 + 1, x1 - 1, y1 - 1], fill=T["chrome"])
    d.rounded_rectangle([x1 - 11, y0 + 6, x1 - 4, y0 + 60], 3, fill=T["scroll"])
    y = y1 + 8
    d.text((x0, y), f"{cpk} client pkt{'s' if cpk != 1 else ''}, {spk} server pkt{'s' if spk != 1 else ''}, {turns} turn{'s' if turns != 1 else ''}.",
           font=UI, fill=T["text"])
    y += 28
    def combo(x, w, txt):
        d.rectangle([x, y, x + w, y + 24], fill=T["field"], outline="#8a8a8a"); d.text((x + 6, y + 4), txt, font=UI, fill=T["text"])
        d.polygon([(x + w - 16, y + 9), (x + w - 6, y + 9), (x + w - 11, y + 15)], fill=T["icon"])
    combo(x0, 420, f"Entire conversation ({tot} bytes)")
    d.text((x0 + 440, y + 4), "Show and save data as", font=UI, fill=T["text"]); combo(x0 + 610, 120, "ASCII")
    d.text((x1 - 140, y + 4), "Stream", font=UI, fill=T["text"]); combo(x1 - 80, 80, str(stream))
    y += 34
    d.text((x0, y + 4), "Find:", font=UI, fill=T["text"]); d.rectangle([x0 + 44, y, x1 - 100, y + 24], fill=T["field"], outline="#8a8a8a")
    d.rectangle([x1 - 90, y, x1, y + 24], fill=T["head"], outline="#8a8a8a"); d.text((x1 - 70, y + 4), "Find Next", font=UI, fill=T["text"])
    y += 36
    bx = x0
    for b in ("Filter Out This Stream", "Print", "Save as…", "Back"):
        w = d.textlength(b, font=UI) + 24
        d.rectangle([bx, y, bx + w, y + 26], fill=T["head"], outline="#8a8a8a"); d.text((bx + 12, y + 5), b, font=UI, fill=T["text"]); bx += w + 8
    bx = x1
    for b in ("Help", "Close"):
        w = d.textlength(b, font=UI) + 24; bx -= w
        d.rectangle([bx, y, bx + w, y + 26], fill=T["head"], outline="#8a8a8a"); d.text((bx + 12, y + 5), b, font=UI, fill=T["text"]); bx -= 8
    im.save(out)
    return cpk, spk, turns, tot

# ---------------------------------------------------------------- terminal
def terminal(out, lines, W=900, bg="#012b36"):
    f = ImageFont.truetype(FD + "ubuntu/UbuntuMono-R.ttf", 18)
    fb = ImageFont.truetype(FD + "ubuntu/UbuntuMono-B.ttf", 18)
    im = Image.new("RGB", (W, 24 * len(lines) + 24), bg); d = ImageDraw.Draw(im); y = 10
    for ln in lines:
        if ln.startswith("$"):
            p1 = "arqamwd@ArqamWd"
            d.text((8, y), p1, font=fb, fill="#4ee44e"); x = 8 + d.textlength(p1, font=fb)
            d.text((x, y), ":", font=f, fill="white"); x += d.textlength(":", font=f)
            d.text((x, y), "~", font=fb, fill="#6c9ef8"); x += d.textlength("~", font=fb)
            d.text((x, y), "$" + ln[1:], font=f, fill="white")
        else: d.text((8, y), ln, font=f, fill="white")
        y += 24
    im.save(out)
