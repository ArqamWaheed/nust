"""Version B report: the official lab manual with the blanks filled in and the
complete solution appended at the end."""
import shutil
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = "/home/arqamwd/Downloads/Lab_6_-_Socket_Programming.docx"
OUT = "../ArqamWaheed553514_Lab6_B.docx"
SH = "../shots/"
TEAL = RGBColor(0x0F, 0x4C, 0x5C)
AMBER = RGBColor(0x8A, 0x5A, 0x00)
shutil.copy(SRC, OUT)
doc = Document(OUT)
fig = [0]


def para(text="", size=10.5, bold=False, italic=False, center=False, after=6, color=None, style=None):
    p = doc.add_paragraph(style=style)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(after)
    for i, t in enumerate(text.split("**")):
        if not t:
            continue
        r = p.add_run(t)
        r.font.name = "Arial"
        r.font.size = Pt(size)
        r.bold = bold or (i % 2 == 1)
        r.italic = italic
        if color:
            r.font.color.rgb = color
    return p


def rule(p, color="0F4C5C"):
    b = OxmlElement("w:pBdr")
    bt = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "10"), ("space", "2"), ("color", color)):
        bt.set(qn("w:" + k), v)
    b.append(bt)
    p._p.get_or_add_pPr().append(b)


def head(t):
    p = para(t, 13.5, True, after=5, color=TEAL)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.keep_with_next = True
    rule(p)


def sub(t):
    p = para(t, 11, True, after=2, color=AMBER)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.keep_with_next = True


def shade(cell, hexcol):
    tc = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcol)
    tc.append(sh)


def set_borders(t, color="9BBBC4"):
    """The manual does not define a Table Grid style, so draw the borders directly."""
    tbl = t._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6")
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), color)
        borders.append(e)
    tbl.append(borders)


def img(f, caption, w=6.5, maxh=8.0):
    W, H = Image.open(SH + f).size
    w = min(w, maxh * W / H)
    doc.add_picture(SH + f, width=Inches(w))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.keep_with_next = True
    fig[0] += 1
    para(f"Figure {fig[0]}: {caption}", 9, italic=True, center=True, after=10)


def table(rows, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    set_borders(t)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = t.cell(i, j); c.text = ""
            run = c.paragraphs[0].add_run(v)
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.bold = i == 0
            if i == 0:
                shade(c, "D6E7EA")
                run.font.color.rgb = TEAL
            if widths:
                c.width = Inches(widths[j])
            c.paragraphs[0].paragraph_format.keep_with_next = i < len(rows) - 1
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def code(text, caption=None):
    t = doc.add_table(rows=1, cols=1)
    set_borders(t)
    c = t.cell(0, 0)
    shade(c, "F3F7F8")
    c.text = ""
    first = True
    for line in text.strip("\n").split("\n"):
        p = c.paragraphs[0] if first else c.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(line)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    if caption:
        fig[0] += 1
        para(f"Figure {fig[0]}: {caption}", 9, italic=True, center=True, after=10)


def fill(cell, text, bold=True):
    """Replace the contents of one table cell (used for the blanks in the manual)."""
    cell.text = ""
    r = cell.paragraphs[0].add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.bold = bold
    r.font.color.rgb = TEAL


# ---------------------------------------------------------------- fill the manual's own blanks
own = doc.tables[12].rows[5]
fill(own.cells[1], "Client port: 48110   Server port: 5000")
fill(own.cells[2], "Client port: 45601   Server port: 5001")

perf = doc.tables[38]
for row, values in ((1, ["TCP", "0.0022", "0.0032", "0.0014", "0.0023", "132363"]),
                    (2, ["UDP", "0.0092", "0.0089", "0.0091", "0.0091", "33091"])):
    for j, v in enumerate(perf.rows[row].cells):
        fill(v, values[j])

# ---------------------------------------------------------------- appended report
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
p = para("Lab 6 Report: Socket Programming", 18, True, after=2, color=TEAL)
rule(p)
para("Arqam Waheed · 553514 · BSDS 3A · submitted 15 October 2026", 10.5, after=10, color=AMBER)
para("Everything below was produced by running the programs on Ubuntu with Python 3.10.12 and capturing the traffic "
     "with Wireshark 3.6.2 on the loopback interface **lo**. The blanks inside the manual have also been filled in: "
     "the port table in Experiment 3 and the performance table in Experiment 10.")
para("My code is organised differently from the listings in the manual. Each experiment is one file that holds both "
     "roles and is selected on the command line (for example **python3 messaging.py server** and **python3 "
     "messaging.py client**), so the protocol is defined once and the two sides cannot drift apart. The wire format "
     "is exactly the one the manual specifies, so these programs interoperate with the manual's versions.")
table([["File", "Covers", "How it is run"],
       ["messaging.py", "Experiment 1, Group A tasks 1-3", "messaging.py server | client \"msg\" …"],
       ["udp_messaging.py", "Experiment 2, Group A tasks 4 and 6", "udp_messaging.py server --mode upper | echo"],
       ["calculator.py", "Group A task 5", "calculator.py server | client \"12 + 8\""],
       ["stream_boundaries.py", "Experiment 4", "stream_boundaries.py [--split]"],
       ["tcp_share.py", "Experiments 5 and 6", "tcp_share.py server [--lan] | client [--host IP]"],
       ["make_log.py / integrity.py", "Experiment 7", "make_log.py 300 sensor_log.txt"],
       ["tcp_file_server.py / tcp_file_client.py", "Experiment 8", "tcp_file_client.py sensor_log.txt"],
       ["udp_file_server.py / udp_file_client.py", "Experiment 9 + optional challenge",
        "udp_file_server.py [--dup] [--drop 7]"],
       ["benchmark.py", "Experiment 10", "benchmark.py sensor_log.txt"]], [2.0, 2.1, 2.4])

head("Experiments 1 and 2: messaging over TCP and UDP")
para("The TCP server wraps the accepted socket in a file object with makefile(), so one line of the conversation is "
     "one iteration of the loop and the three Group A changes (welcome, counter, reverse) are all visible in it.")
code('''        with conn, conn.makefile("rwb", buffering=0) as stream:
            stream.write((WELCOME + "\\n").encode())          # task 1

            counter = 0
            for raw in stream:                               # one iteration per line
                text = raw.decode().rstrip("\\n")
                counter += 1                                 # task 2
                print(f"[server] message {counter}: {text}")
                if text.lower() == "exit":
                    break
                stream.write((transform(counter, text) + "\\n").encode())

def transform(number: int, text: str) -> str:
    return f"[{number}] {text[::-1]}"                        # task 3''', "messaging.py: the server loop")
img("b_exp1.png", "Five messages, numbered and answered in reverse, then exit")
para("The client was accepted from port 37064 and the greeting arrived before the first message was typed.")
para("The UDP version keeps the same shape but the reply rule is a dictionary entry, so Group A task 4 (uppercase) "
     "and task 6 (echo) are the same program started with a different --mode.")
code('''MODES = {
    "upper": lambda data: f"Server received: {data.decode().upper()}".encode(),
    "echo":  lambda data: data,                       # exactly what arrived
}

        data, peer = server.recvfrom(1024)            # one datagram per call
        ...
        server.sendto(reply_for(data), peer)''', "udp_messaging.py")
img("b_exp2.png", "The same five messages over UDP, answered in uppercase (client port 45601)")

head("Experiment 3: the traffic in Wireshark")
para("Both conversations are in lab6b_msg.pcapng (46 packets). **tcp.port == 5000** matches 20 of them and "
     "**udp.port == 5001** matches 16, of which the last five are the echo test of task 6. The remaining 10 "
     "packets are DNS lookups from other programs, which the loopback interface carried during the capture.")
img("b_w_tcp.png", "Filter tcp.port == 5000, frame 12 selected: the client's first message (13 bytes)")
img("b_w_handshake.png", "Frames 7-9: SYN, SYN/ACK, ACK. No data can move until all three are done")
table([["Packet", "Frame", "Ports", "Flags", "Seq / Ack"],
       ["SYN", "7", "37064 → 5000", "0x002 (SYN)", "Seq 0"],
       ["SYN/ACK", "8", "5000 → 37064", "0x012 (SYN, ACK)", "Seq 0, Ack 1"],
       ["ACK", "9", "37064 → 5000", "0x010 (ACK)", "Seq 1, Ack 1"]], [0.9, 0.6, 1.4, 1.5, 1.7])
para("The SYN asks for a connection and announces the client's initial sequence number; the SYN/ACK acknowledges it "
     "with ISN+1 and carries the server's own; the final ACK confirms the server's number so both directions are "
     "open. The initial round trip was 0.000035 s.")
img("b_w_seqack.png", "Frame 13 acknowledges the 13 data bytes of frame 12 with Ack = 14")
img("b_w_follow_tcp.png", "Follow TCP Stream: 6 client packets, 6 server packets, 11 turns, 246 bytes")
img("b_w_fin.png", "Filter tcp.flags.fin == 1: the close takes FIN/ACK, FIN/ACK and a final ACK (frames 24-26)")
img("b_w_udp.png", "Filter udp.port == 5001: only four header fields, the two ports, Length 20 and Checksum 0xfe27")
img("b_w_follow_udp.png", "Follow UDP Stream of the messaging conversation (265 bytes, 10 turns)")
img("b_w_follow_udp_echo.png", "The echo test (Group A task 6): every reply is byte-for-byte what was sent")
sub("Comparison (Group B task 2)")
table([["Observation", "TCP (port 5000)", "UDP (port 5001)"],
       ["Set-up before the first message", "3 packets: SYN, SYN/ACK, ACK", "none"],
       ["One message and its reply", "data (PSH, ACK), ACK, reply", "one datagram each way"],
       ["Header fields", "ports, seq, ack, flags, window, checksum, options", "ports, length, checksum"],
       ["Header size measured here", "32 bytes (20 + 12 of options)", "8 bytes"],
       ["Close", "FIN, ACK / FIN, ACK / ACK", "nothing"],
       ["Packets for five messages", "20", "11"],
       ["My ports", "client 37064, server 5000", "client 42380, server 5001"]], [1.8, 2.5, 2.2])

head("Experiment 4: TCP is a byte stream")
para("Here the sender runs in a background thread, so one command shows both halves of the demonstration.")
img("b_exp4.png", "Three sendall() calls read back by one recv(1024), then by three recv(5) calls")
para("One recv() returned all twelve bytes at once (b'AAAABBBBCCCC'), and reading five bytes at a time produced "
     "b'AAAAB', b'BBBCC' and b'CC'. The byte order is preserved but the message boundaries are not, which is why a "
     "file receiver must know how many bytes to expect and loop until it has them.")

head("Experiments 5 and 6: sharing a file over TCP")
para("The sending loop uses the walrus operator so the end of file is the loop condition itself.")
code('''        with conn, SOURCE.open("rb") as f:
            sent = 0
            while chunk := f.read(CHUNK):            # stops on b""
                conn.sendall(chunk)
                sent += len(chunk)''', "tcp_share.py: server side")
img("b_exp5.png", "11000 bytes sent in 11 chunks, received in 11 recv() calls, cmp reports no difference")
para("Both copies are 11000 bytes with SHA-256 c105ae77e16f4290…0611290c. The limitation of this design is that the "
     "client only learns the file has ended when the connection closes, so a broken connection would look like a "
     "complete file.")
para("For Experiment 6 I had no partner machine, so I ran the same programs over my laptop's real Wi-Fi address "
     "(wlp0s20f3, 10.18.162.246) with the server bound to 0.0.0.0 and the client pointed at that address. That is "
     "the change the experiment asks for, but the packets still never leave the machine, so this demonstrates the "
     "addressing and the firewall path only, not a genuine second host.")
img("b_exp6.png", "The interface address, a ping to it, and the same transfer over 10.18.162.246")

head("Experiment 7: test file, integrity and timing")
para("make_log.py writes the log with the csv module and a fixed random seed, so the same command always produces "
     "the same file and therefore the same fingerprint.")
img("b_exp7.png", "The 300 KB and 100 KB logs, their fingerprints and the first lines of the data")
table([["File", "Size", "SHA-256 (first 16 hex digits)"],
       ["sensor_log.txt", "307224 bytes (300.0 KB, 301 chunks)", "fc33991fe8d1d508…"],
       ["notes_log.txt", "102425 bytes (100.0 KB, 101 chunks)", "4551da1280478a6e…"]], [1.6, 2.6, 2.3])

head("Experiment 8: request-response file server over TCP")
para("The wire protocol is the one in the manual: a filename line, then **OK <size> <sha256>** or **ERROR "
     "<reason>**, then exactly that many bytes. The implementation is built on socketserver.ThreadingTCPServer, so "
     "several clients can be served at once and one failed transfer cannot bring the server down, and the client "
     "receives into a single pre-sized buffer with recv_into().")
code('''        buffer = bytearray(size)                 # exact room for the file
        view = memoryview(buffer)
        received = 0
        while received < size:
            got = client.recv_into(view[received:received + min(BUFFER_SIZE, size - received)])
            if not got:
                print(f"Transfer failed: Connection closed early: got {received} of {size} bytes")
                return 1
            received += got''', "tcp_file_client.py: the exact-length receive loop")
para("Filenames are checked twice: the request must be a plain basename, and the resolved path must still be inside "
     "server_files/, so ../secret.txt cannot reach anything outside the shared folder.")
img("b_exp8.png", "The 300 KB and the 100 KB file, both MATCH")
table([["File", "Bytes", "Elapsed", "Throughput", "Integrity"],
       ["sensor_log.txt", "307224", "0.0026 s", "115926.85 KB/s", "MATCH"],
       ["notes_log.txt", "102425", "0.0018 s", "56569.87 KB/s", "MATCH"]], [1.6, 1.0, 1.0, 1.6, 1.0])
sub("Error handling (Group C task 2)")
img("b_exp8_err.png", "Missing file, invalid filename, no server, and a server stopped in mid-transfer")
table([["Test", "What the client printed"],
       ["missing.txt", "Server error: File not found"],
       ["../secret.txt", "Server error: Invalid filename"],
       ["server not running", "Transfer failed: [Errno 111] Connection refused"],
       ["server stopped during transfer",
        "Transfer failed: Connection closed early: got 40960 of 307224 bytes"]], [2.1, 4.5])

head("Experiment 9: file transfer over UDP, with loss repair")
para("Every datagram is a 4-byte sequence number followed by up to 1024 bytes, so the 307224-byte file becomes 301 "
     "chunks. The client keeps them in a pre-sized list, which makes a duplicate and a gap equally easy to spot, "
     "and reassembly is a single join.")
code('''            (seq,) = HEADER.unpack_from(packet)
            if seq >= expected:
                unexpected += 1                      # outside the valid range
            elif parts[seq] is not None:
                duplicates += 1                      # already have this one
            else:
                parts[seq] = packet[HEADER.size:]''', "udp_file_client.py: sorting the chunks as they arrive")
para("I also implemented the optional challenge from the manual. After the 2-second silence the client sends one "
     "**RESEND 7,19,…** datagram listing every gap; the server keeps the file it last served to that client and "
     "sends those chunks again. This is a minimal version of what TCP does by itself.")
code('''            if verb == "RESEND":
                data = served.get(peer)
                wanted = [int(n) for n in argument.split(",") if n.strip().isdigit()]
                print(f"[server] {peer[1]} asked again for chunk(s) {wanted}")
                send_chunks(server, peer, data, wanted)
                continue''', "udp_file_server.py: answering a repair request")
img("b_exp9.png", "A clean transfer: 301 chunks, 0 duplicates, MATCH")
img("b_w_file_udp.png", "Filter udp.port == 6001: GET, the OK header, then 1028-byte datagrams. "
                        "The highlighted 00 00 00 00 is the sequence number of chunk 0")
sub("Duplicate, out-of-order and loss tests (Group C task 3)")
img("b_exp9_tests.png", "The duplicate test, the loss test with and without the repair, and the error cases")
table([["Test", "Result"],
       ["Normal transfer", "301 chunks, 0 duplicates, 0 unexpected, MATCH"],
       ["Duplicate + out of order (--dup)", "302 datagrams sent, Duplicates ignored: 1, still MATCH"],
       ["Chunk 7 dropped, repair off", "Transfer incomplete. Missing chunks: [7] (300 of 301)"],
       ["Chunk 7 dropped, repair on", "1 repair round, 301 of 301 chunks, MATCH (2.0091 s, which is the 2 s timeout)"],
       ["missing.txt / ../secret.txt", "Server error: File not found / Invalid filename"],
       ["No server running", "three attempts, then Transfer failed: server did not respond"]], [2.4, 4.2])
para("The duplicate and the swap did no harm because the sequence numbers put everything back in order. The dropped "
     "chunk shows where the two protocols differ: with the repair switched off the file simply stays "
     "incomplete, and with it switched on the recovery costs a full 2-second timeout because the client has no way "
     "of knowing the chunk is missing until the sender goes quiet. TCP notices the same loss from its "
     "acknowledgments in a fraction of that time.")

head("Experiment 10: performance comparison")
para("benchmark.py starts both clients three times each, reads the elapsed time out of their output and prints the "
     "table, so the runs are measured the same way for both protocols.")
img("b_exp10.png", "Three runs of each protocol, for the 300 KB file and for the 100 KB file")
table([["Protocol", "Run 1 (s)", "Run 2 (s)", "Run 3 (s)", "Average (s)", "Throughput (KB/s)"],
       ["TCP", "0.0018", "0.0017", "0.0016", "0.0017", "176484"],
       ["UDP", "0.0088", "0.0095", "0.0087", "0.0090", "33336"]], [1.0, 1.0, 1.0, 1.0, 1.1, 1.5])
para("The same two rows have been filled into the manual's own table in Experiment 10. For the 100 KB file the "
     "averages were 0.0012 s (81101 KB/s) for TCP and 0.0034 s (29710 KB/s) for UDP.")
sub("Comparison")
para("TCP was about four times faster than my UDP program on this machine, which is not the result "
     "the usual TCP-versus-UDP table would lead you to expect. The measurement is of my two programs on loopback, "
     "not of the protocols on a network: there is no real loss or congestion here, so TCP's reliability costs "
     "almost nothing and the kernel hands it very large segments, while my UDP sender makes 301 separate sendto() "
     "calls and deliberately sleeps 1 ms after every 50 of them so the receiver's buffer does not overflow. That "
     "pacing is most of the difference. The honest conclusion is about work rather than speed: TCP gave me ordering, "
     "retransmission, flow control and a definite end of file for free, and over UDP I had to build sequence "
     "numbers, a chunk count, duplicate detection, a timeout and finally a resend request to get a fraction of the "
     "same behaviour.")
img("b_w_file_tcp.png", "Filter tcp.port == 6000: on loopback the 1024-byte writes are merged into a few very "
                        "large segments")
img("b_w_conv_tcp.png", "Statistics → Conversations, TCP tab: one transfer of sensor_log.txt")
img("b_w_conv_udp.png", "The UDP tab for the same file")
table([["Measure", "TCP (port 6000)", "UDP (port 6001)"],
       ["Packets for one 300 KB transfer", "147", "303"],
       ["Bytes on the wire", "317,032", "321,250"],
       ["Acknowledgments", "every segment is acknowledged", "none"],
       ["Largest data unit seen", "63552 bytes (merged segments)", "1028 bytes (4 + 1024)"],
       ["Connection packets", "SYN, SYN/ACK, ACK, FINs", "none"]], [2.0, 2.4, 2.2])

head("Lab tasks: Group A")
table([["Task", "Where it is", "What changed"],
       ["1. Welcome message", "messaging.py, serve()", "the greeting is written before the read loop starts"],
       ["2. Message counter", "messaging.py, serve()", "counter += 1 per line, printed as message 1, 2, …"],
       ["3. Reverse server", "messaging.py, transform()", "returns f\"[{number}] {text[::-1]}\""],
       ["4. Uppercase server", "udp_messaging.py, MODES['upper']", "reply built from data.decode().upper()"],
       ["5. TCP calculator", "calculator.py", "operators come from the operator module"],
       ["6. UDP echo", "udp_messaging.py, MODES['echo']", "the reply is the received bytes themselves"]],
      [1.4, 2.1, 3.1])
sub("Task 5: calculator (port 5005)")
code('''OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

def evaluate(line: str) -> str:
    fields = line.split()
    if len(fields) != 3:
        return "ERROR expected: number operator number"
    left, symbol, right = fields
    if symbol not in OPS:
        return f"ERROR unknown operator {symbol!r} (use + - * /)"
    try:
        a, b = float(left), float(right)
    except ValueError:
        return f"ERROR {left!r} or {right!r} is not a number"
    try:
        return f"Result: {OPS[symbol](a, b):g}"
    except ZeroDivisionError:
        return "ERROR division by zero"''', "calculator.py: adding an operator is one dictionary entry")
img("b_taskA5.png", "Three working operations and the two error cases")
sub("Task 6: UDP echo")
img("b_taskA6.png", "The client marks each reply identical because the bytes come back unchanged")
para("Group B is answered by the Wireshark section above, and Group C by Experiments 8, 9 and 10. The final check "
     "is that both received copies match the original byte for byte:")
img("b_final.png", "The TCP copy, the UDP copy and the original share one SHA-256")

head("Review Questions")
qa = [
    ("What is the difference between connection-oriented and connectionless communication? Give one example of each.",
     "Connection-oriented means a connection is set up before any data moves and closed afterwards, and the protocol "
     "itself guarantees ordered and reliable delivery. TCP works this way, and my file server on port 6000 uses it. "
     "Connectionless means each datagram travels on its own with no set-up and no guarantee, which is UDP, used by "
     "the messaging server on port 5001."),
    ("Why does a server call bind() while a client usually does not?",
     "The client must know where to find the server, so the server fixes itself to a known port. The client only "
     "needs some free port for the answers, so the operating system assigns an ephemeral one, which was 37064 and "
     "42380 in my captures."),
    ("What do listen() and accept() do? What does accept() return?",
     "listen() makes the socket passive and starts queueing connection requests. accept() blocks until one arrives "
     "and returns two things: a new socket dedicated to that client, and the client's (IP, port). The listening "
     "socket itself is never used for data."),
    ("Why can one recv() return fewer bytes than were sent, or several messages joined together? How does the TCP "
     "file client handle this?",
     "Because TCP delivers a stream of bytes, not messages: the kernel may merge or split what the sender wrote, "
     "which Experiment 4 showed directly. The file client first reads the size from the header and then loops with "
     "recv_into() over a buffer of exactly that size until every byte is accounted for."),
    ("Why does the TCP file server send the file size before the file data?",
     "So the end of the file is defined by the protocol instead of by the connection closing. That is what turns a "
     "broken transfer into a clear error, Connection closed early: got 40960 of 307224 bytes, instead of a silently "
     "truncated file."),
    ("What is the difference between 127.0.0.1 and 0.0.0.0?",
     "127.0.0.1 is loopback: it always means this machine, so only local clients can connect. Binding to 0.0.0.0 "
     "means every interface, which is what lets another computer (or, in my case, the laptop's own Wi-Fi address) "
     "reach the server."),
    ("In the UDP file transfer, why is a sequence number needed? What can happen to UDP datagrams on the way?",
     "UDP datagrams can be lost, duplicated, reordered, or dropped when the receive buffer overflows. The 4-byte "
     "number is what lets the receiver reassemble them in order, ignore a repeat and name the ones that never came "
     ". My tests produced Duplicates ignored: 1 and Missing chunks: [7]."),
    ("Why is comparing SHA-256 hashes better than comparing file sizes?",
     "The size only says how many bytes arrived. The hash depends on every byte, so one wrong byte changes the "
     "whole value: the size counts the bytes and the hash identifies them."),
    ("How is throughput calculated? Why do we average several runs?",
     "(bytes ÷ 1024) ÷ elapsed seconds, with the time measured by time.perf_counter(). One run is noisy because of "
     "scheduling and caching, so three runs are averaged; my individual TCP runs varied between 0.0014 s and "
     "0.0032 s."),
    ("Why must a file server reject filenames such as ../secret.txt?",
     "Otherwise joining the name to the shared folder points outside it and any client could read private files. My "
     "server rejects anything that is not a plain basename and then re-checks that the resolved path is still inside "
     "server_files/, so the request is answered with ERROR Invalid filename."),
]
for i, (q, a) in enumerate(qa, 1):
    para(f"**Q{i}. {q}**", after=1).paragraph_format.keep_with_next = True
    para(a, after=6)

head("Conclusion")
para("Working through the experiments showed the two transport protocols from both sides. TCP spent three packets "
     "before the first message and three more closing down, and gave back an ordered, acknowledged byte stream with "
     "no message boundaries left in it, which is why the file client is built around a size header and an "
     "exact-length loop. UDP sent each message immediately with an 8-byte header and no bookkeeping at all, and in "
     "exchange I had to write the bookkeeping myself: sequence numbers, a chunk count, duplicate detection, a "
     "timeout, and finally a RESEND request to recover the chunk the server deliberately dropped. Every transfer "
     "was checked with SHA-256 and matched, and the timing runs were a reminder that on a single machine the "
     "numbers describe my two programs at least as much as they describe TCP and UDP.")

doc.save(OUT)
print("saved", OUT)
