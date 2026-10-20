"""Apply the humanizer pass to the prose of both report scripts (prose only; code blocks untouched)."""
import re, sys

A = [
 # titles and captions: a dash standing in for a colon
 ('para("Lab 6: Socket Programming — Client-Server Communication Using TCP and UDP in Python"',
  'para("Lab 6: Socket Programming (Client-Server Communication Using TCP and UDP in Python)"'),
 ('head("Lab Tasks — Group A: Messaging")', 'head("Lab Tasks: Group A (Messaging)")'),
 ('head("Lab Tasks — Group B and C")', 'head("Lab Tasks: Groups B and C")'),
 ('["Acknowledgment number", "13 — the next byte the server expects"]',
  '["Acknowledgment number", "13 (the next byte the server expects)"]'),
 ('["Chunk 7 dropped", "Transfer incomplete. Missing chunks: [7] — 300 of 301 received"]',
  '["Chunk 7 dropped", "Transfer incomplete. Missing chunks: [7] (300 of 301 received)"]'),
 # UDP header sentence
 ('has only four fields — source port 59016', 'has only four fields: source port 59016'),
 ('"Length 20 (8 header + 12 data) and Checksum 0xfe27 — and there is no handshake before it and no close after it.")',
  '"Length 20 (8 bytes of header plus 12 of data) and Checksum 0xfe27. Nothing was sent before it and nothing is "\n     "sent after the last one.")'),
 # byte stream
 ("b'AAAABBBBCCCC' — 12 bytes from one recv()", "b'AAAABBBBCCCC', 12 bytes from a single recv()"),
 ('"the bytes but not the boundaries between send() calls. That is exactly why the file client in Experiment 8 has "',
  '"the bytes, but the boundaries between send() calls are gone. The file client in Experiment 8 therefore has "'),
 # hash vs length
 ('"contents match and not just the length. Throughput is the file size in KB divided by the elapsed seconds, and "',
  '"contents are the same, which the length on its own cannot. Throughput is the file size in KB divided by the "'),
 ('"time.perf_counter() is used because it is a high-resolution clock.")',
  '"elapsed seconds, and time.perf_counter() is used for the timing because it is a high-resolution clock.")'),
 # closer after the error table
 ('para("The last one is the important one: without the size header the client would have saved those 40960 bytes and "\n     "called it a complete file.")',
  'para("Without the size header the client would have saved those 40960 bytes and treated them as the whole file.")'),
 # comparison paragraph
 ('para("**Comparison.** On this machine', 'sub("Comparison")\npara("On this machine'),
 ('"start retransmitting and backing off while UDP would simply keep sending. What TCP gave me for free — ordering, "',
  '"start retransmitting and backing off while UDP would simply keep sending. TCP handed me ordering, "'),
 ('"retransmission, flow control and a clear end of file — is exactly what I had to build by hand with sequence "',
  '"retransmission, flow control and a clear end of file for nothing, and over UDP I built the same things by hand "'),
 ('"numbers, a chunk count, duplicate detection and a timeout.")',
  '"out of sequence numbers, a chunk count, duplicate detection and a timeout.")'),
 ('"packet per application chunk — on a real network TCP would be limited to about 1500 bytes per segment and the "',
  '"packet per application chunk. On a real network TCP would be limited to about 1500 bytes per segment, so the "'),
 # echo
 ('para("The echo server sends back exactly the bytes it received — nothing is added and nothing is changed — and the "\n     "client compares the reply with what it sent.")',
  'para("The echo server sends back exactly the bytes it received, with nothing added and nothing changed, and the "\n     "client compares the reply with what it sent.")'),
 # UDP messaging close
 ('"The client used port 59016. Nothing is exchanged before the first message and nothing is exchanged at the end: "\n     "the client simply stops.")',
  '"The client used port 59016. Nothing is exchanged before the first message or after the last one; the client "\n     "just stops.")'),
 # review answers
 ('"afterwards, and the protocol guarantees ordered, reliable delivery — TCP, as used by my file server on port "\n     "6000. Connectionless means every message is sent on its own with no setup and no guarantee — UDP, as used by "\n     "my messaging server on port 5001."',
  '"afterwards, and the protocol guarantees ordered, reliable delivery. TCP works this way, and my file server on "\n     "port 5000 uses it. Connectionless means every message is sent on its own with no setup and no guarantee, "\n     "which is UDP, as used by my messaging server on port 5001."'),
 ('"system pick an ephemeral one — 38014 and 59016 in my captures."',
  '"system pick an ephemeral one, which was 38014 and 59016 in my captures."'),
 ('"0.0.0.0 in bind() means every interface on the machine, so other computers can reach the server too — that is "\n     "the change Experiment 6 asks for."',
  '"0.0.0.0 in bind() means every interface on the machine, so other computers can reach the server too, which is "\n     "the change Experiment 6 asks for."'),
 ('"throw away a repeat and list exactly which ones never arrived — my tests produced Duplicates ignored: 1 and "\n     "Missing chunks: [7]."',
  '"throw away a repeat and list exactly which ones never arrived. My tests produced Duplicates ignored: 1 and "\n     "Missing chunks: [7]."'),
 ('"wrong the value changes completely — size only proves that the right number of bytes arrived, not the right "\n     "bytes."',
  '"wrong the value changes completely. The size tells you how many bytes arrived and the hash tells you which "\n     "ones they were."'),
 ('"A single run is noisy because of scheduling, caching and other processes — my three TCP runs ranged from "\n     "0.0014 s to 0.0025 s — so the average is a fairer number."',
  '"A single run is noisy because of scheduling, caching and other processes; my three TCP runs ranged from "\n     "0.0014 s to 0.0025 s, so the average is a fairer number."'),
]

B = [
 ('p = para("Lab Report — Lab 6: Socket Programming"', 'p = para("Lab 6 Report: Socket Programming"'),
 ('head("Experiments 1 and 2 — Messaging over TCP and UDP")', 'head("Experiments 1 and 2: messaging over TCP and UDP")'),
 ('head("Experiment 3 — The traffic in Wireshark")', 'head("Experiment 3: the traffic in Wireshark")'),
 ('head("Experiment 4 — TCP is a byte stream")', 'head("Experiment 4: TCP is a byte stream")'),
 ('head("Experiments 5 and 6 — Sharing a file over TCP")', 'head("Experiments 5 and 6: sharing a file over TCP")'),
 ('head("Experiment 7 — Test file, integrity and timing")', 'head("Experiment 7: test file, integrity and timing")'),
 ('head("Experiment 8 — Request-response file server over TCP")', 'head("Experiment 8: request-response file server over TCP")'),
 ('head("Experiment 9 — File transfer over UDP, with loss repair")', 'head("Experiment 9: file transfer over UDP, with loss repair")'),
 ('head("Experiment 10 — Performance comparison")', 'head("Experiment 10: performance comparison")'),
 ('head("Lab tasks — Group A")', 'head("Lab tasks: Group A")'),
 ('sub("Task 5 — calculator (port 5005)")', 'sub("Task 5: calculator (port 5005)")'),
 ('sub("Task 6 — UDP echo")', 'sub("Task 6: UDP echo")'),
 ('"**udp.port == 5001** matches 16 — the extra five are the echo test of task 6.")',
  '"**udp.port == 5001** matches 16: the extra five are the echo test of task 6.")'),
 ('"Filter udp.port == 5001: four header fields only — ports, Length 20 and Checksum 0xfe27"',
  '"Filter udp.port == 5001: only four header fields, the two ports, Length 20 and Checksum 0xfe27"'),
 ('["Chunk 7 dropped, repair off", "Transfer incomplete. Missing chunks: [7] — 300 of 301"]',
  '["Chunk 7 dropped, repair off", "Transfer incomplete. Missing chunks: [7] (300 of 301)"]'),
 ('"1 repair round, 301 of 301 chunks, MATCH (2.0103 s — the 2 s timeout)"',
  '"1 repair round, 301 of 301 chunks, MATCH (2.0103 s, which is the 2 s timeout)"'),
 ('"chunk is the real difference between the protocols: with the repair switched off the file simply stays "',
  '"chunk shows where the two protocols differ: with the repair switched off the file simply stays "'),
 ('para("**Comparison.** TCP was about five times faster', 'sub("Comparison")\npara("TCP was about five times faster'),
 ('"itself guarantees ordered and reliable delivery — TCP, used by my file server on port 6000. Connectionless "\n     "means each datagram travels on its own with no set-up and no guarantee — UDP, used by the messaging server on "\n     "port 5001."',
  '"itself guarantees ordered and reliable delivery. TCP works this way, and my file server on port 6000 uses it. "\n     "Connectionless means each datagram travels on its own with no set-up and no guarantee, which is UDP, used by "\n     "the messaging server on port 5001."'),
 ('"needs some free port for the answers, so the operating system assigns an ephemeral one — 48110 and 45601 in "\n     "my captures."',
  '"needs some free port for the answers, so the operating system assigns an ephemeral one, which was 48110 and "\n     "45601 in my captures."'),
 ('"broken transfer into a clear error — Connection closed early: got 40960 of 307224 bytes — rather than a "\n     "silently truncated file."',
  '"broken transfer into a clear error, Connection closed early: got 40960 of 307224 bytes, instead of a silently "\n     "truncated file."'),
 ('"— my tests produced Duplicates ignored: 1 and Missing chunks: [7]."',
  '". My tests produced Duplicates ignored: 1 and Missing chunks: [7]."'),
 ('"The size only says how many bytes arrived. The hash depends on every byte, so one wrong byte changes the "\n     "whole value — it proves the content, not just the length."',
  '"The size only says how many bytes arrived. The hash depends on every byte, so one wrong byte changes the "\n     "whole value: the size counts the bytes and the hash identifies them."'),
 ('"before the first message and three more closing down, and gave back an ordered, acknowledged byte stream — "\n     "but a stream with no message boundaries, which is why the file client is built around a size header and an "\n     "exact-length loop."',
  '"before the first message and three more closing down, and gave back an ordered, acknowledged byte stream with "\n     "no message boundaries left in it, which is why the file client is built around a size header and an "\n     "exact-length loop."'),
]

for path, edits in (("report_a.py", A), ("report_b.py", B)):
    s = open(path).read()
    missed = []
    for old, new in edits:
        if old not in s:
            missed.append(old[:70])
            continue
        s = s.replace(old, new, 1)
    # remaining dashes in code-block captions: "name.py — text"  ->  "name.py: text"
    s = re.sub(r'(\w+\.py) — ', r'\1: ', s)
    open(path, "w").write(s)
    print(path, "applied", len(edits) - len(missed), "of", len(edits))
    for m in missed:
        print("   MISSED:", m)
