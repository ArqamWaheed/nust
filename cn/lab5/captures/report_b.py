from PIL import Image
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SH = "../shots/"
BLUE = RGBColor(0x1F, 0x38, 0x64)
doc = Document()
s = doc.sections[0]
s.page_width, s.page_height = Inches(8.27), Inches(11.69)
s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(0.75)
doc.styles["Normal"].font.name = "Arial"
doc.styles["Normal"].font.size = Pt(10.5)
fig = [0]

def para(text="", size=10.5, bold=False, italic=False, center=False, after=6, color=None):
    p = doc.add_paragraph()
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(after)
    for i, t in enumerate(text.split("**")):
        if not t: continue
        r = p.add_run(t); r.font.size = Pt(size); r.bold = bold or (i % 2 == 1); r.italic = italic
        if color: r.font.color.rgb = color
    return p

def shade(cell, hexcol):
    tc = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcol); tc.append(sh)

def rule(p):
    b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "8"), ("space", "1"), ("color", "1F3864")): bt.set(qn("w:" + k), v)
    b.append(bt); p._p.get_or_add_pPr().append(b)

def head(t):
    p = para(t, 13, True, after=4, color=BLUE); p.paragraph_format.space_before = Pt(10); p.paragraph_format.keep_with_next = True
def img(f, caption, w=6.6, maxh=5.8):
    W, H = Image.open(SH + f).size; w = min(w, maxh * W / H)
    doc.add_picture(SH + f, width=Inches(w)); doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.keep_with_next = True
    fig[0] += 1; para(f"Figure {fig[0]}: {caption}", 9, italic=True, center=True, after=10)
def qa(q, a):
    para(f"**Q: {q}**", after=0).paragraph_format.keep_with_next = True
    para(a, after=6)

def table(rows, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = t.cell(i, j); c.text = ""
            run = c.paragraphs[0].add_run(v); run.font.size = Pt(9.5); run.bold = i == 0
            if i == 0: shade(c, "D9E2F3")
            if widths: c.width = Inches(widths[j])
            c.paragraphs[0].paragraph_format.keep_with_next = i < len(rows) - 1
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ------------------------------------------------------------------ title block
para("Lab 5: TCP Traffic Analysis using Wireshark", 17, True, after=0, color=BLUE)
rule(para("EE353 Computer Networks  |  Department of Computing", 10.5, after=8))
t = doc.add_table(rows=2, cols=4); t.style = "Table Grid"
for i, (k, v) in enumerate([("Name", "Arqam Waheed"), ("Reg No.", "553514"), ("Class", "BSDS 3A"), ("Date", "8 October 2026")]):
    a, b = t.cell(i // 2, (i % 2) * 2), t.cell(i // 2, (i % 2) * 2 + 1)
    a.text = ""; r = a.paragraphs[0].add_run(k); r.bold = True; shade(a, "D9E2F3"); b.text = v
doc.add_paragraph().paragraph_format.space_after = Pt(2)

head("Setup")
para("Wireshark 3.6.2 on Ubuntu, capturing on wlp0s20f3 (192.168.18.55). File: lab5_tcp.pcapng, 1519 packets, 1511 of them TCP. "
     "I used curl to load example.com over HTTP and HTTPS and then connected to a closed port on my router. "
     "This report mostly follows the HTTPS connection (stream 34).")
img("b0_terminal.png", "Commands run during the capture", 5.6)

# ------------------------------------------------------------------ 1
head("1. Identify TCP Traffic")
img("b1_tcp.png", "Filter tcp, frame 349 (TLS Client Hello) with the TCP header expanded")
table([["Field", "Observation"],
       ["Source IP", "192.168.18.55"], ["Destination IP", "104.20.23.154"],
       ["Source Port", "43358"], ["Destination Port", "443"],
       ["Sequence Number", "1 (raw 1817588855)"], ["Acknowledgment Number", "1 (raw 3351956361)"],
       ["Flags", "0x018 (PSH, ACK)"], ["Window Size", "502, scaled ×128 = 64256 bytes"],
       ["TCP Header Length", "32 bytes"], ["Checksum / Status", "0x54b9, unverified"],
       ["Higher Layer Protocol", "TLS (Client Hello)"]], [2.3, 4.6])
para("Outgoing packets from my laptop show unverified checksums because the Wi-Fi card fills them in after capture (checksum offload).")

# ------------------------------------------------------------------ 2
head("2. Three-Way Handshake")
img("b2_handshake.png", "tcp.stream eq 34, handshake in frames 342 to 344")
table([["Step", "Frame", "Ports", "Seq (raw)", "Ack (raw)"],
       ["SYN", "342", "43358 → 443", "1817588854", "0"],
       ["SYN/ACK", "343", "443 → 43358", "3351956360", "1817588855"],
       ["ACK", "344", "43358 → 443", "1817588855", "3351956361"]], [0.9, 0.7, 1.4, 1.9, 1.9])
qa("What is the purpose of SYN?", "It requests a new connection and tells the server the client's initial sequence number.")
qa("What does SYN/ACK acknowledge?", "The client's SYN. Ack 1817588855 is the client's ISN plus one.")
qa("Why is the final ACK required?", "The server also sent a SYN, so it needs an acknowledgment too. After this both directions are open.")
qa("Which endpoint initiated the connection?", "My laptop, 192.168.18.55, port 43358.")

# ------------------------------------------------------------------ 3
head("3. Sequence and Acknowledgment Analysis")
img("b3_seqack.png", "Frame 354 acknowledges the 517-byte Client Hello in frame 349")
table([["Item", "Value"],
       ["Data packet", "Frame 349, Seq = 1, Len = 517"],
       ["Next sequence number", "518"],
       ["ACK packet", "Frame 354, Ack = 518"],
       ["Time difference", "4.108323 − 4.100747 = 7.6 ms"]], [2.3, 4.6])
qa("How do sequence and acknowledgment numbers support reliable, ordered delivery?",
   "Sequence numbers count bytes, not packets. The receiver uses them to reorder segments and find missing ones. "
   "The ACK says which byte it wants next: Ack 518 means bytes 1 to 517 arrived. If no ACK comes back the sender retransmits.")

# ------------------------------------------------------------------ 4
head("4. TCP Flags")
table([["Filter", "Seen?", "Count", "Explanation"],
       ["tcp.flags.syn == 1", "Yes", "13", "SYN and SYN/ACK packets that open connections"],
       ["tcp.flags.ack == 1", "Yes", "1501", "Ack field is valid; on everything except plain SYNs and RSTs"],
       ["tcp.flags.fin == 1", "Yes", "11", "Sender is done sending and is closing its side"],
       ["tcp.flags.reset == 1", "Yes", "5", "Connection refused or aborted"]], [1.6, 0.6, 0.6, 4.1])

# ------------------------------------------------------------------ 5
head("5. Follow TCP Stream")
img("b5_follow.png", "Follow TCP Stream on stream 34 (HTTPS)", 5.8)
para("Stream 34 is between 192.168.18.55:43358 (client) and 104.20.23.154:443 (server). Wireshark set the filter to "
     "tcp.stream eq 34 and showed only its 22 packets (6239 bytes of payload).")
qa("What does a TCP stream represent?", "One TCP connection: a single pair of IP addresses and ports.")
qa("Why is stream-level analysis useful?", "A capture has many connections mixed together. One stream shows a single conversation in order.")
qa("Why may application data not be readable when HTTPS/TLS is used?",
   "TLS encrypts everything after the handshake. Only example.com in the Client Hello is readable. "
   "The HTTP stream (25) showed the full GET and 200 OK in plain text.")

# ------------------------------------------------------------------ 6
head("6. Connection Termination")
img("b6_close.png", "Four-packet close of stream 34 (frames 368 to 371)")
table([["Frame", "Direction", "Flags", "Seq", "Ack"],
       ["368", "client → server", "FIN, ACK", "842", "5399"],
       ["369", "server → client", "ACK", "5399", "842"],
       ["370", "server → client", "FIN, ACK", "5399", "843"],
       ["371", "client → server", "ACK", "843", "5400"]], [0.7, 1.7, 1.3, 1.5, 1.5])
img("b6_rst.png", "RST packets: router refusing port 81 (717) and Ubuntu's connectivity check (887, 905)")
para("Frame 717 is a RST, ACK from my router because nothing listens on port 81. Frames 887 and 905 are resets from "
     "connectivity-check.ubuntu.com, which aborted its connection after sending a FIN.")
qa("Why can TCP connection termination involve multiple packets in both directions?",
   "Each direction is closed separately. Both sides send a FIN and both FINs need an ACK, so a close takes 4 packets "
   "(3 if one side puts its ACK and FIN together).")

# ------------------------------------------------------------------ 7
head("7. TCP Port 443")
img("b7_443.png", "tcp.port == 443 && tcp.flags.syn == 1")
para("TCP/443 traffic was present (1482 packets). The connection to example.com used port 443 and did the "
     "SYN (342) → SYN/ACK (343) → ACK (344) handshake before TLS started. Port 443 is usually HTTPS, but any program can use any port. "
     "Wireshark only shows it as TLS after reading the payload.")

# ------------------------------------------------------------------ 8
head("8. TCP vs UDP")
table([["Feature", "TCP", "UDP"],
       ["Connection setup", "3-way handshake", "None"],
       ["Reliability", "ACKs + retransmission", "None"],
       ["Ordering", "Yes, using sequence numbers", "No"],
       ["Acknowledgments", "Yes", "No"],
       ["Flow control", "Receive window", "No"],
       ["Minimum transport header", "20 bytes", "8 bytes"],
       ["Examples", "HTTP, HTTPS, SSH", "DNS, DHCP, QUIC"]], [2.3, 2.3, 2.3])
para("From my captures:", after=2)
para("•  TCP spent 3 packets (342–344) on the handshake before any data. The Lab 4 DNS lookup was just a query and a response.", after=2)
para("•  TCP headers here were 32 bytes (with options) vs 8 bytes for every UDP packet in Lab 4.", after=2)
para("•  Every TCP data segment got an ACK (349 → 354). UDP packets were never acknowledged.", after=6)

# ------------------------------------------------------------------ viva
head("Viva Questions")
for q, a in [("What is TCP and why is it connection-oriented?", "A reliable transport layer protocol. It sets up a connection with a handshake before data is sent."),
             ("Explain the three-way handshake.", "SYN from client, SYN/ACK from server, ACK from client."),
             ("What is the purpose of SYN?", "To start a connection and synchronise initial sequence numbers."),
             ("Sequence number vs acknowledgment number?", "Seq numbers the data being sent. Ack is the next byte expected from the other side."),
             ("Why does TCP use acknowledgments?", "To confirm delivery so lost data can be retransmitted."),
             ("What is the receive window?", "Free buffer space at the receiver, which limits how much unacknowledged data the sender can send."),
             ("Flow control vs congestion control?", "Flow control stops the receiver from being overloaded. Congestion control stops the network from being overloaded."),
             ("FIN vs RST?", "FIN is a normal, graceful close. RST ends the connection immediately and drops any pending data."),
             ("What does Follow TCP Stream do?", "Isolates one connection and shows its data as a conversation."),
             ("Why might a website not produce TCP/443?", "It may use HTTP/3 over QUIC (UDP/443) instead."),
             ("What is a TCP segment?", "One TCP header plus its payload."),
             ("How does TCP differ from UDP?", "TCP is reliable, ordered and connection-based. UDP is fast with no guarantees."),
             ("What can a retransmission or duplicate ACK indicate?", "A lost or out-of-order segment, usually from congestion.")]:
    qa(q, a)

doc.save("../ArqamWaheed553514_Lab5_B.docx")
print("saved")
