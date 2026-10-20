"""Build every screenshot for one version of the Lab 6 report.

    python3 shots.py A      light Wireshark theme, my own shell prompt
    python3 shots.py B      dark Wireshark theme, anonymous '$' prompt

It also prints the measured numbers that the reports quote.
"""
import sys
from ws6 import *

V = sys.argv[1].upper() if len(sys.argv) > 1 else "A"
A = V == "A"
T = LIGHT if A else DARK
TH = TERM_A if A else TERM_B
LOG = f"logs{V}/"
SH = f"../shots/{V.lower()}_"
MSG = f"../captures/lab6{'' if A else 'b'}_msg.pcapng"
FILES = f"../captures/lab6{'' if A else 'b'}_files.pcapng"
MSGNAME = MSG.split("/")[-1]
FILENAME = FILES.split("/")[-1]


def log(name, keep=None, skip=0):
    lines = [l.rstrip("\n") for l in open(LOG + name)][skip:]
    if keep and len(lines) > keep:
        lines = lines[:keep - 1] + [f"... ({len(lines) - keep + 1} more lines)"]
    return lines


def cmd(c, *logs, keep=None):
    """One pane body: the command the student typed, then its real output."""
    out = ["$ " + c]
    for name in logs:
        out += log(name, keep)
    return out


ip = open(LOG + "ts_ip.txt").read().strip()
notes = []

# ================================================================ terminals
if A:
    run = lambda s: "python3 " + s
    E1S, E1C = run("tcp_server.py"), run("tcp_client.py")
    E2S, E2C = run("udp_server.py"), run("udp_client.py")
    E4S, E4C, E4C2 = run("boundary_server.py"), run("boundary_client.py"), run("boundary_client.py --split")
    E5S, E5C = run("share_server.py"), run("share_client.py")
    E6S, E6C = run("share_server.py --lan"), run(f"share_client.py {ip}")
    A5S, A5C = run("calc_server.py"), run("calc_client.py")
    A6S, A6C = run("echo_server.py"), run("echo_client.py")
    E8S, E8C = run("tcp_file_server.py"), run("tcp_file_client.py sensor_log.txt")
    E8C2 = run("tcp_file_client.py notes_log.txt")
    E8E = [run("tcp_file_client.py missing.txt"), run("tcp_file_client.py ../secret.txt"),
           run("tcp_file_client.py sensor_log.txt")]
    E8SLOW = run("tcp_file_server.py --slow")
    E9S, E9C = run("udp_file_server.py"), run("udp_file_client.py sensor_log.txt")
    E9DUP, E9DROP = run("udp_file_server.py --dup"), run("udp_file_server.py --drop")
else:
    run = lambda s: "python3 " + s
    E1S, E1C = run("messaging.py server"), run('messaging.py client "Hello Server" "Computer Networks" ...')
    E2S, E2C = run("udp_messaging.py server --mode upper"), run('udp_messaging.py client "Hello Server" ...')
    E4S, E4C, E4C2 = None, run("stream_boundaries.py"), run("stream_boundaries.py --split")
    E5S, E5C = run("tcp_share.py server"), run("tcp_share.py client")
    E6S, E6C = run("tcp_share.py server --lan"), run(f"tcp_share.py client --host {ip}")
    A5S, A5C = run("calculator.py server"), run("calculator.py client")
    A6S, A6C = run("udp_messaging.py server --mode echo"), run('udp_messaging.py client "Echo this back" ...')
    E8S, E8C = run("tcp_file_server.py"), run("tcp_file_client.py sensor_log.txt")
    E8C2 = run("tcp_file_client.py notes_log.txt")
    E8E = [run("tcp_file_client.py missing.txt"), run("tcp_file_client.py ../secret.txt"),
           run("tcp_file_client.py sensor_log.txt")]
    E8SLOW = run("tcp_file_server.py --slow")
    E9S, E9C = run("udp_file_server.py"), run("udp_file_client.py sensor_log.txt")
    E9DUP, E9DROP = run("udp_file_server.py --dup"), run("udp_file_server.py --drop 7")

terminal(SH + "exp1.png", [("Terminal 1: TCP server (port 5000)", cmd(E1S, "exp1_server.log")),
                           ("Terminal 2: TCP client", cmd(E1C, "exp1_client.log"))], TH=TH)

terminal(SH + "exp2.png", [("Terminal 1: UDP server (port 5001)", cmd(E2S, "exp2_server.log")),
                           ("Terminal 2: UDP client", cmd(E2C, "exp2_client.log"))], TH=TH)

if A:
    terminal(SH + "exp4.png", [("Terminal 1: one recv(1024) for three send() calls",
                                cmd(E4S, "exp4_server.log") + cmd(E4C, "exp4_client.log")),
                               ("Terminal 2: the same data read with recv(5) three times",
                                cmd(E4C2, "exp4_client_split.log"))], TH=TH)
else:
    terminal(SH + "exp4.png", [("One recv(1024) for three sendall() calls", cmd(E4C, "exp4_one.log")),
                               ("The same data read with recv(5) three times", cmd(E4C2, "exp4_split.log"))], TH=TH)

terminal(SH + "exp5.png", [("Terminal 1: file server (port 5002)", cmd(E5S, "exp5_server.log")),
                           ("Terminal 2: client", cmd(E5C, "exp5_client.log")),
                           ("Terminal 2: size, byte compare and SHA-256", log("ts_exp5_verify.log"))], TH=TH)

terminal(SH + "exp6.png", [("Finding the interface address and testing reachability", log("ts_exp6.log")),
                           ("Terminal 1: server bound to 0.0.0.0", cmd(E6S, "exp6_server.log")),
                           ("Terminal 2: client using the interface IP", cmd(E6C, "exp6_client.log"))], TH=TH)

terminal(SH + "exp7.png", [("Building the test files and fingerprinting them", log("ts_exp7.log"))], TH=TH)

terminal(SH + "taskA5.png", [("Terminal 1: calculator server (port 5005)", cmd(A5S, "taskA5_server.log")),
                             ("Terminal 2: client", cmd(A5C, "taskA5_client.log"))], TH=TH)

terminal(SH + "taskA6.png", [("Terminal 1: UDP echo server", cmd(A6S, "taskA6_server.log")),
                             ("Terminal 2: client (reply compared with what was sent)",
                              cmd(A6C, "taskA6_client.log"))], TH=TH)

terminal(SH + "exp8.png", [("Terminal 1: TCP file server (port 6000)", cmd(E8S, "exp8_server.log", keep=12)),
                           ("Terminal 2: 300 KB file", cmd(E8C, "exp8_client.log")),
                           ("Terminal 2: 100 KB file", cmd(E8C2, "exp8_client_small.log"))], TH=TH)

terminal(SH + "exp8_err.png", [
    ("Error 1: file that does not exist", cmd(E8E[0], "exp8_err_missing.log")),
    ("Error 2: filename that tries to leave the shared folder", cmd(E8E[1], "exp8_err_invalid.log")),
    ("Error 3: no server listening", cmd(E8E[2], "exp8_err_refused.log")),
    ("Error 4: server stopped in the middle of a slow transfer",
     ["$ " + E8SLOW] + log("exp8_slow_server.log", keep=4) + ["^C"] + cmd(E8C, "exp8_err_closed.log"))], TH=TH)

terminal(SH + "exp9.png", [("Terminal 1: UDP file server (port 6001)", cmd(E9S, "exp9_server.log", keep=10)),
                           ("Terminal 2: client", cmd(E9C, "exp9_client.log"))], TH=TH)

if A:
    terminal(SH + "exp9_tests.png", [
        ("Duplicate and out-of-order test (server --dup)",
         cmd(E9DUP, "exp9_dup_server.log", keep=8) + cmd(E9C, "exp9_dup_client.log")),
        ("Packet-loss test (server --drop, chunk 7 never sent)",
         cmd(E9DROP, "exp9_drop_server.log", keep=8) + cmd(E9C, "exp9_drop_client.log")),
        ("Error tests", cmd(run("udp_file_client.py missing.txt"), "exp9_err_missing.log") +
                        cmd(run("udp_file_client.py ../secret.txt"), "exp9_err_invalid.log") +
                        cmd(E9C, "exp9_err_noserver.log"))], TH=TH)
else:
    terminal(SH + "exp9_tests.png", [
        ("Duplicate and out-of-order test (server --dup)",
         cmd(E9DUP, "exp9_dup_server.log", keep=8) + cmd(E9C, "exp9_dup_client.log")),
        ("Loss test with the repair switched off",
         cmd(E9DROP, "exp9_drop_server.log", keep=6) + cmd(E9C + " --no-repair", "exp9_drop_norepair.log")),
        ("The same loss, repaired by one RESEND request", cmd(E9C, "exp9_drop_repair.log")),
        ("Error tests", cmd(run("udp_file_client.py missing.txt"), "exp9_err_missing.log") +
                        cmd(run("udp_file_client.py ../secret.txt"), "exp9_err_invalid.log") +
                        cmd(E9C, "exp9_err_noserver.log"))], TH=TH)

if A:
    tcp_times = [float(log(f"exp10_tcp_{i}.log")[3].split(":")[1].strip().split()[0]) for i in (1, 2, 3)]
    udp_times = [float(log(f"exp10_udp_{i}.log")[6].split(":")[1].strip().split()[0]) for i in (1, 2, 3)]
    size = 307224
    avg_t, avg_u = sum(tcp_times) / 3, sum(udp_times) / 3
    import subprocess
    body = []
    for i in (1, 2, 3):
        body += cmd(run("tcp_file_client.py sensor_log.txt"), f"exp10_tcp_{i}.log")
    body2 = []
    for i in (1, 2, 3):
        body2 += cmd(run("udp_file_client.py sensor_log.txt"), f"exp10_udp_{i}.log")
    avg_pane = ["$ python3 average.py 307224 " + " ".join(f"{t:.4f}" for t in tcp_times),
                "Runs         : " + ", ".join(f"{t:.4f} s" for t in tcp_times),
                "Average time : {:.4f} s".format(avg_t),
                "Throughput   : {:.2f} KB/s".format((size / 1024) / avg_t),
                "$ python3 average.py 307224 " + " ".join(f"{t:.4f}" for t in udp_times),
                "Runs         : " + ", ".join(f"{t:.4f} s" for t in udp_times),
                "Average time : {:.4f} s".format(avg_u),
                "Throughput   : {:.2f} KB/s".format((size / 1024) / avg_u)]
    terminal(SH + "exp10.png", [("Three TCP runs", body), ("Three UDP runs", body2),
                                ("Averages and throughput", avg_pane)], TH=TH, line_h=21, size=14)
    notes.append(("exp10 tcp", tcp_times, avg_t, (size / 1024) / avg_t))
    notes.append(("exp10 udp", udp_times, avg_u, (size / 1024) / avg_u))
else:
    terminal(SH + "exp10.png", [("Automated benchmark, three runs of each protocol",
                                 cmd(run("benchmark.py sensor_log.txt"), "exp10_benchmark.log")),
                                ("The same for the 100 KB file",
                                 cmd(run("benchmark.py notes_log.txt"), "exp10_benchmark_small.log"))], TH=TH)
    notes.append(("exp10 benchmark", log("exp10_benchmark.log")))
    notes.append(("exp10 benchmark small", log("exp10_benchmark_small.log")))

terminal(SH + "final.png", [("Both received copies compared with the original", log("ts_final.log"))], TH=TH)
print("terminals done")

# ================================================================ Wireshark: messaging capture
msg = Cap(MSG)
TOT = len(msg.pk)
st = lambda nums: (MSGNAME, f"Packets: {TOT} · Displayed: {len(nums)} ({100 * len(nums) / TOT:.1f}%)")
tcp5000 = msg.tcp_frames(5000)
udp5001 = msg.udp_frames(5001)
hs = tcp5000[:3]
first_data = next(n for n in tcp5000 if msg.info[n]["len"] and msg.pk[n - 1][TCP].dport == 5000)
first_ack = next(n for n in tcp5000 if n > first_data and msg.info[n]["len"] == 0
                 and msg.pk[n - 1][TCP].sport == 5000)
fins = [n for n in tcp5000 if msg.pk[n - 1][TCP].flags & 1]
close = fins + [n for n in tcp5000 if n > fins[-1]]
req = next(n for n in udp5001 if msg.pk[n - 1][UDP].dport == 5001)
TS = msg.info[tcp5000[0]]["stream"]          # the capture also caught background DNS,
US = msg.info[req]["stream"]                 # so the stream indexes are not always 0
rep = next(n for n in udp5001 if n > req and msg.pk[n - 1][UDP].sport == 5001)

t = head(msg, first_data) + tcp_tree(msg, first_data) + \
    [(0, False, f"Data ({msg.info[first_data]['len']} bytes)")]
render(SH + "w_tcp.png", msg, MSGNAME, "tcp.port == 5000", tcp5000, sel=first_data, tree=t, tree_sel=3,
       raw=bytes(msg.pk[first_data - 1]), hl=(34, 32), status=st(tcp5000), T=T,
       list_h=250, bytes_h=96, box_tree=ix(t, ("Source Port", "Destination Port")) if not A else ())

t = head(msg, hs[0]) + tcp_tree(msg, hs[0], flags_open=True)
render(SH + "w_handshake.png", msg, MSGNAME, f"tcp.stream eq {TS}", tcp5000, sel=hs[0], tree=t,
       tree_sel=at(t, ".... .... ..1. = Syn"), raw=bytes(msg.pk[hs[0] - 1]), hl=(46, 2),
       status=st(tcp5000), T=T, list_h=170, bytes_h=96, box_rows=[tuple(hs)],
       box_tree=ix(t, ("Sequence Number:", "Sequence Number (raw)")))

rtt = float(msg.pk[first_ack - 1].time) - float(msg.pk[first_data - 1].time)
irtt = float(msg.pk[hs[2] - 1].time) - float(msg.pk[hs[0] - 1].time)
t = head(msg, first_ack) + seqack(tcp_tree(msg, first_ack),
                                  [f"[This is an ACK to the segment in frame: {first_data}]",
                                   f"[The RTT to ACK the segment was: {rtt:.9f} seconds]",
                                   f"[iRTT: {irtt:.9f} seconds]"])
render(SH + "w_seqack.png", msg, MSGNAME, f"tcp.stream eq {TS}", tcp5000, sel=first_ack, tree=t,
       tree_sel=at(t, "[SEQ/ACK analysis]"), raw=bytes(msg.pk[first_ack - 1]), hl=(42, 4),
       status=st(tcp5000), T=T, list_h=190, bytes_h=78,
       box_rows=[(first_data,), (first_ack,)],
       box_tree=ix(t, ("Acknowledgment Number:", "Acknowledgment number (raw)")))

fa = follow(SH + "w_follow_tcp.png", msg, TS, tcp5000, MSGNAME, proto=TCP, T=T)

t = head(msg, close[0]) + tcp_tree(msg, close[0], flags_open=True)
render(SH + "w_fin.png", msg, MSGNAME, "tcp.flags.fin == 1", close, sel=close[0], tree=t,
       tree_sel=at(t, ".... .... ...1 = Fin"), raw=bytes(msg.pk[close[0] - 1]), hl=(46, 2),
       status=st(fins), T=T, list_h=110, bytes_h=78, box_rows=[tuple(close)])

t = head(msg, req) + udp_tree(msg, req, data_label=f"Data ({msg.info[req]['len']} bytes)")
render(SH + "w_udp.png", msg, MSGNAME, "udp.port == 5001", udp5001, sel=req, tree=t, tree_sel=3,
       raw=bytes(msg.pk[req - 1]), hl=(34, 8), status=st(udp5001), T=T, list_h=250, bytes_h=96,
       box_tree=ix(t, ("Length:", "Checksum:")))

udp0 = msg.stream_frames(US, UDP)
fu = follow(SH + "w_follow_udp.png", msg, US, udp0, MSGNAME, proto=UDP, T=T, H=520)

if not A:                                   # the echo conversation is only in version B's capture
    last = next(n for n in reversed(udp5001) if msg.pk[n - 1][UDP].dport == 5001)
    ES = msg.info[last]["stream"]            # the echo test is the second conversation on 5001
    echo = msg.stream_frames(ES, UDP)
    if echo and ES != US:
        follow(SH + "w_follow_udp_echo.png", msg, ES, echo, MSGNAME, proto=UDP, T=T, H=420)
        notes.append(("echo frames", echo, "stream", ES))

notes.append(("msg capture", MSGNAME, "total", TOT, "tcp5000", len(tcp5000), "udp5001", len(udp5001)))
notes.append(("streams tcp/udp", TS, US))
notes.append(("handshake", hs, "first data", first_data, "ack", first_ack, "rtt", rtt, "irtt", irtt))
notes.append(("close", close, "udp req/rep", req, rep))
notes.append(("follow tcp", fa, "follow udp", fu))
notes.append(("ports", msg.pk[hs[0] - 1][TCP].sport, 5000, msg.pk[req - 1][UDP].sport, 5001))
notes.append(("udp lens", [(n, msg.pk[n - 1][UDP].len, hex(msg.pk[n - 1][UDP].chksum)) for n in udp5001[:4]]))

# ================================================================ Wireshark: file-transfer capture
files = Cap(FILES)
FTOT = len(files.pk)
fst = lambda nums: (FILENAME, f"Packets: {FTOT} · Displayed: {len(nums)} ({100 * len(nums) / FTOT:.1f}%)")
tcp6000 = files.tcp_frames(6000)
udp6001 = files.udp_frames(6001)
first6000 = tcp6000[0]
FS = files.info[first6000]["stream"]
stream0 = files.stream_frames(FS, TCP)

hdr = next(n for n in stream0 if files.info[n]["len"] and files.pk[n - 1][TCP].sport == 6000)
data_seg = next(n for n in stream0 if n > hdr and files.info[n]["len"] > 1000)
t = head(files, data_seg) + tcp_tree(files, data_seg) + [(0, False, f"Data ({files.info[data_seg]['len']} bytes)")]
render(SH + "w_file_tcp.png", files, FILENAME, "tcp.port == 6000", stream0, sel=data_seg, tree=t, tree_sel=3,
       raw=bytes(files.pk[data_seg - 1])[:160], hl=(34, 32), status=fst(tcp6000), T=T,
       list_h=250, bytes_h=96)

getf = next(n for n in udp6001 if bytes(files.pk[n - 1][UDP].payload).startswith(b"GET"))
chunk = getf + 2
t = head(files, chunk) + udp_tree(files, chunk, data_label=f"Data ({files.info[chunk]['len']} bytes)")
render(SH + "w_file_udp.png", files, FILENAME, "udp.port == 6001", udp6001[udp6001.index(getf):], sel=chunk,
       tree=t, tree_sel=at(t, "UDP payload"), raw=bytes(files.pk[chunk - 1])[:112], hl=(42, 4),
       status=fst(udp6001), T=T, list_h=250, bytes_h=96,
       box_tree=ix(t, ("Length:", "Length:")))

# Statistics -> Conversations, for the runs measured in Experiment 10
def conv_row(frames, proto):
    pk = files.pk
    a = pk[frames[0] - 1][proto]
    first, last = float(pk[frames[0] - 1].time), float(pk[frames[-1] - 1].time)
    total = sum(len(pk[n - 1]) for n in frames)
    dur = max(last - first, 1e-6)
    return [pk[frames[0] - 1][IP].src, a.sport, pk[frames[0] - 1][IP].dst, a.dport,
            len(frames), f"{total:,}", f"{dur:.4f}", f"{total * 8 / dur / 1000:,.0f} k"]

i0 = udp6001.index(getf)
udp_run = udp6001[i0:i0 + 303]          # GET + OK + 301 chunks
conversations(SH + "w_conv_tcp.png", [conv_row(stream0, TCP)], FILENAME, tab="TCP", T=T,
              note="One TCP transfer of sensor_log.txt (Experiment 8): every data segment is acknowledged.")
conversations(SH + "w_conv_udp.png", [conv_row(udp_run, UDP)], FILENAME, tab="UDP", T=T,
              note="One UDP transfer of the same file (Experiment 9): request, header and 301 data datagrams, no ACKs.")

notes.append(("files capture", FILENAME, "total", FTOT, "tcp6000", len(tcp6000), "udp6001", len(udp6001)))
notes.append(("tcp stream0", len(stream0), stream0[0], stream0[-1], "hdr", hdr, "seg", data_seg))
notes.append(("tcp conv", conv_row(stream0, TCP)))
notes.append(("udp conv", conv_row(udp_run, UDP)))
notes.append(("tcp seg sizes", sorted({files.info[n]["len"] for n in stream0 if files.info[n]["len"]})[-4:]))
notes.append(("udp get/ok", repr(bytes(files.pk[getf - 1][UDP].payload)),
              repr(bytes(files.pk[getf][UDP].payload))))

print("\n--- numbers for the report ---")
for n in notes:
    print(n)
