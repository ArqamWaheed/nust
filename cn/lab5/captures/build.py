from ws5 import *

cap = Cap("lab5_tcp.pcapng"); pk = cap.pk; TOT = len(pk)
tcp = [n for n in range(1, TOT + 1) if TCP in pk[n - 1]]
F = lambda m: [n for n in tcp if pk[n - 1][TCP].flags & m]
st = lambda name, nums: (name, f"Packets: {TOT} · Displayed: {len(nums)} ({100 * len(nums) / TOT:.1f}%)")
s25 = [n for n in tcp if cap.info[n]["stream"] == 25]
s34 = [n for n in tcp if cap.info[n]["stream"] == 34]
p443 = [n for n in tcp if 443 in (pk[n - 1][TCP].sport, pk[n - 1][TCP].dport)]
T = lambda n: float(pk[n - 1].time)
NAME = "lab5_tcp.pcapng"

def head(n): p = pk[n - 1]; return [(0, False, frame_line(n, p)), (0, False, eth_line(p)), (0, False, ip_line(p))]
def at(tree, pre): return next(i for i, x in enumerate(tree) if x[2].startswith(pre))
def ix(tree, *pairs):
    f = lambda pre: next(i for i, x in enumerate(tree) if x[2].startswith(pre))
    return [(f(a), f(b)) for a, b in pairs]
def win(nums, around, before=6): i = nums.index(around); return nums[max(0, i - before):]
def seqack(tree, lines):
    k = next(i for i, x in enumerate(tree) if x[2] == "[SEQ/ACK analysis]")
    return tree[:k] + [(1, True, "[SEQ/ACK analysis]")] + [(2, None, l) for l in lines] + tree[k + 1:]

irtt25, irtt34 = T(200) - T(198), T(344) - T(342)

# ================================================================ Version A (light, full window, like lab 4)
terminal("../shots/a0_terminal.png", [
    "$ curl -4 -s -o /dev/null -w \"http %{http_code}\\n\" --http1.1 http://example.com/", "http 200",
    "$ curl -4 -s -o /dev/null -w \"https %{http_code}\\n\" https://example.com/", "https 200",
    "$ exec 3<>/dev/tcp/192.168.18.1/81", "bash: connect: Connection refused", "$ "], W=980)

render("../shots/a1_tcp.png", cap, NAME, "tcp", win(tcp, 201, 4), sel=201,
       tree=head(201) + tcp_tree(cap, 201) + [(0, False, "Hypertext Transfer Protocol")], tree_sel=3,
       raw=bytes(pk[200]), hl=(34, 32), status=st(NAME, tcp), list_h=250, bytes_h=96)

render("../shots/a2_handshake.png", cap, NAME, "tcp.stream eq 25", s25, sel=198,
       tree=(t := head(198) + tcp_tree(cap, 198, flags_open=True)), tree_sel=at(t, ".... .... ..1. = Syn"),
       raw=bytes(pk[197]), hl=(46, 2), status=st(NAME, s25), list_h=270, bytes_h=96)

render("../shots/a3_seqack.png", cap, NAME, "tcp.stream eq 25", s25, sel=202,
       tree=head(202) + seqack(tcp_tree(cap, 202), ["[This is an ACK to the segment in frame: 201]",
            f"[The RTT to ACK the segment was: {T(202) - T(201):.9f} seconds]", f"[iRTT: {irtt25:.9f} seconds]"]),
       tree_sel=10, raw=bytes(pk[201]), hl=(42, 4), status=st(NAME, s25), list_h=270, bytes_h=96)

rst = F(4)
render("../shots/a4_rst.png", cap, NAME, "tcp.flags.reset == 1", rst, sel=717,
       tree=(t := head(717) + tcp_tree(cap, 717, flags_open=True)), tree_sel=at(t, ".... .... .1.. = Reset"),
       raw=bytes(pk[716]), hl=(46, 2), status=st(NAME, rst), list_h=140, bytes_h=78)

fa = follow("../shots/a5_follow.png", cap, 25, s25, NAME)

fin = F(1)
render("../shots/a6_fin.png", cap, NAME, "tcp.flags.fin == 1", fin, sel=207,
       tree=(t := head(207) + tcp_tree(cap, 207, flags_open=True)), tree_sel=at(t, ".... .... ...1 = Fin"),
       raw=bytes(pk[206]), hl=(46, 2), status=st(NAME, fin), list_h=270, bytes_h=78)

render("../shots/a7_443.png", cap, NAME, "tcp.port == 443", win(p443, 342, 3), sel=342,
       tree=head(342) + tcp_tree(cap, 342, opts_open=True), tree_sel=3,
       raw=bytes(pk[341]), hl=(34, 40), status=st(NAME, p443), list_h=250, bytes_h=96)

# ================================================================ Version B (dark, cropped panes, red boxes)
terminal("../shots/b0_terminal.png", [
    "$ curl -4 -s -o /dev/null -w \"http %{http_code}\\n\" --http1.1 http://example.com/", "http 200",
    "$ curl -4 -s -o /dev/null -w \"https %{http_code}\\n\" https://example.com/", "https 200",
    "$ exec 3<>/dev/tcp/192.168.18.1/81", "bash: connect: Connection refused", "$ "], W=980, bg="#300a24")

t = head(349) + tcp_tree(cap, 349) + [(0, False, "Transport Layer Security")]
render("../shots/b1_tcp.png", cap, NAME, "tcp", win(tcp, 349, 5), sel=349, tree=t, tree_sel=3,
       status=st(NAME, tcp), list_h=230, bytes_h=0, T=DARK, box_tree=ix(t, ("Source Port", "Destination Port"), ("Sequence Number:", "Acknowledgment number (raw)"), ("Flags", "[Checksum Status")))

t = head(343) + tcp_tree(cap, 343)
render("../shots/b2_handshake.png", cap, NAME, "tcp.stream eq 34", s34, sel=343, tree=t, tree_sel=3,
       status=st(NAME, s34), list_h=300, bytes_h=0, T=DARK, chrome=False, box_rows=[(342, 343, 344)], box_tree=ix(t, ("Sequence Number:", "Acknowledgment number (raw)")))

t = head(354) + seqack(tcp_tree(cap, 354), ["[This is an ACK to the segment in frame: 349]",
        f"[The RTT to ACK the segment was: {T(354) - T(349):.9f} seconds]", f"[iRTT: {irtt34:.9f} seconds]"])
render("../shots/b3_seqack.png", cap, NAME, "tcp.stream eq 34", s34, sel=354, tree=t, tree_sel=3,
       status=st(NAME, s34), list_h=300, bytes_h=0, T=DARK, chrome=False, box_rows=[(349,), (354,)], box_tree=ix(t, ("Sequence Number:", "Acknowledgment number (raw)"), ("[SEQ/ACK", "[The RTT")))

fb = follow("../shots/b5_follow.png", cap, 34, s34, NAME, T=DARK)

t = head(368) + tcp_tree(cap, 368, flags_open=True)
render("../shots/b6_close.png", cap, NAME, "tcp.stream eq 34", s34, sel=368, tree=t, tree_sel=3,
       status=st(NAME, s34), list_h=300, bytes_h=0, T=DARK, chrome=False, box_rows=[(368, 369, 370, 371)], box_tree=ix(t, (".... .... ...1 = Fin", ".... .... ...1 = Fin")))

finrst = sorted(set(F(1)) | set(F(4)))
t = head(717) + tcp_tree(cap, 717)
render("../shots/b6_rst.png", cap, NAME, "tcp.flags.fin == 1 || tcp.flags.reset == 1", win(finrst, 717, 3), sel=717, tree=t[:13] + t[15:16],
       tree_sel=3, status=st(NAME, finrst), list_h=200, bytes_h=0, T=DARK, chrome=False, box_rows=[(717,), (887,), (905,)])

syn443 = [n for n in p443 if pk[n - 1][TCP].flags & 2]
t = head(342) + tcp_tree(cap, 342, opts_open=True)
render("../shots/b7_443.png", cap, NAME, "tcp.port == 443 && tcp.flags.syn == 1", syn443, sel=342, tree=t, tree_sel=3,
       status=st(NAME, syn443), list_h=200, bytes_h=0, T=DARK, chrome=False, box_rows=[(342, 343)], box_tree=ix(t, ("Destination Port", "Destination Port")))

# ================================================================ numbers used in the reports
print("counts tcp", len(tcp), "syn", len(F(2)), "ack", len(F(16)), "fin", len(fin), "rst", len(rst), "443", len(p443), "syn443", len(syn443))
print("follow A", fa, "follow B", fb)
for n in (198, 199, 200, 201, 202, 207, 225, 226, 342, 343, 344, 349, 354, 368, 369, 370, 371, 717):
    print(cap.row(n), cap.info[n]["win"], hex(pk[n - 1][TCP].chksum), pk[n - 1][TCP].dataofs * 4)
print("rtt 201->202", T(202) - T(201), "349->354", T(354) - T(349), "irtt", irtt25, irtt34)
