#!/bin/bash
# Runs every Experiment / Lab Task of version B for real and stores the terminal
# transcripts in logsB/ and the loopback captures in ../captures/.
set -u
CODE=/home/arqamwd/nust/cn/lab6/codeB
WORK=/home/arqamwd/nust/cn/lab6/runB
LOG=/home/arqamwd/nust/cn/lab6/build/logsB
CAPDIR=/home/arqamwd/nust/cn/lab6/captures
PY="python3 -u"

rm -rf "$WORK" "$LOG"; mkdir -p "$WORK" "$LOG" "$CAPDIR"
cp "$CODE"/*.py "$WORK"/            # the manual asks for every lab file in one folder
cd "$WORK" || exit 1
run() { local out=$1; shift; "$@" > "$LOG/$out" 2>&1; }

echo "### prep"
$PY -c "open('share_me.txt','w').write('Hello from the server\n' * 500)"
run exp7_make.log $PY make_log.py 300 sensor_log.txt
mkdir -p server_files && cp sensor_log.txt server_files/
run exp7_make_small.log $PY make_log.py 100 notes_log.txt
cp notes_log.txt server_files/
run exp7_integrity.log $PY integrity.py sensor_log.txt notes_log.txt
echo "secret admin password" > secret.txt

echo "### capture 1: messaging"
dumpcap -i lo -q -w "$CAPDIR/lab6b_msg.pcapng" -a duration:60 > /dev/null 2>&1 &
CAP=$!
sleep 2

echo "--- Experiment 1 + tasks 1-3 (TCP 5000)"
$PY messaging.py server > "$LOG/exp1_server.log" 2>&1 &
S=$!
sleep 1
run exp1_client.log $PY messaging.py client \
  "Hello Server" "Computer Networks" "Socket programming lab" "Reliable byte stream" "Ordered delivery"
wait $S 2>/dev/null
sleep 1

echo "--- Experiment 2 + task 4 (UDP 5001, uppercase)"
$PY udp_messaging.py server --mode upper > "$LOG/exp2_server.log" 2>&1 &
S=$!
sleep 1
run exp2_client.log $PY udp_messaging.py client \
  "Hello Server" "No handshake here" "One datagram per recvfrom" "Boundaries preserved" "Lower overhead"
wait $S 2>/dev/null
sleep 1

echo "--- task 6 (UDP echo, same file, --mode echo)"
$PY udp_messaging.py server --mode echo > "$LOG/taskA6_server.log" 2>&1 &
S=$!
sleep 1
run taskA6_client.log $PY udp_messaging.py client "Echo this back" "MiXeD CaSe 123"
wait $S 2>/dev/null
sleep 1
kill $CAP 2>/dev/null; wait $CAP 2>/dev/null
sleep 1

echo "--- task 5 (calculator 5005)"
$PY calculator.py server > "$LOG/taskA5_server.log" 2>&1 &
S=$!
sleep 1
run taskA5_client.log $PY calculator.py client
wait $S 2>/dev/null
sleep 1

echo "--- Experiment 4 (byte stream, 5004)"
run exp4_one.log $PY stream_boundaries.py
sleep 1
run exp4_split.log $PY stream_boundaries.py --split
sleep 1

echo "--- Experiment 5 (file sharing, 5002)"
$PY tcp_share.py server > "$LOG/exp5_server.log" 2>&1 &
S=$!
sleep 1
run exp5_client.log $PY tcp_share.py client
wait $S 2>/dev/null
{ stat -c "%10s bytes  %n" share_me.txt received_share_me.txt
  cmp share_me.txt received_share_me.txt && echo "cmp: no differences"
  sha256sum share_me.txt received_share_me.txt; } > "$LOG/exp5_verify.log" 2>&1
sleep 1

echo "--- Experiment 6 (real interface IP, same machine)"
IP=$(ip -4 -o addr show wlp0s20f3 | awk '{print $4}' | cut -d/ -f1)
{ ip -4 -o addr show wlp0s20f3; ping -c 3 "$IP"; } > "$LOG/exp6_setup.log" 2>&1
$PY tcp_share.py server --lan > "$LOG/exp6_server.log" 2>&1 &
S=$!
sleep 1
run exp6_client.log $PY tcp_share.py client --host "$IP"
wait $S 2>/dev/null
run exp6_verify.log $PY integrity.py share_me.txt received_share_me.txt
sleep 1

echo "### capture 2: file transfer"
dumpcap -i lo -q -w "$CAPDIR/lab6b_files.pcapng" -a duration:120 > /dev/null 2>&1 &
CAP2=$!
sleep 2

echo "--- Experiment 8 (TCP file server 6000)"
$PY tcp_file_server.py > "$LOG/exp8_server.log" 2>&1 &
SRV=$!
sleep 1
run exp8_client.log $PY tcp_file_client.py sensor_log.txt
sleep 1
run exp8_client_small.log $PY tcp_file_client.py notes_log.txt
sleep 1
run exp8_err_missing.log $PY tcp_file_client.py missing.txt
sleep 1
run exp8_err_invalid.log $PY tcp_file_client.py ../secret.txt
sleep 1
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1
run exp8_err_refused.log $PY tcp_file_client.py sensor_log.txt
sleep 1

echo "--- Experiment 8 premature closure"
$PY tcp_file_server.py --slow > "$LOG/exp8_slow_server.log" 2>&1 &
SRV=$!
sleep 1
$PY tcp_file_client.py sensor_log.txt > "$LOG/exp8_err_closed.log" 2>&1 &
CLI=$!
sleep 2
kill -TERM $SRV 2>/dev/null
wait $SRV 2>/dev/null; wait $CLI 2>/dev/null
sleep 1

echo "--- Experiment 9 (UDP file server 6001)"
$PY udp_file_server.py > "$LOG/exp9_server.log" 2>&1 &
SRV=$!
sleep 1
run exp9_client.log $PY udp_file_client.py sensor_log.txt
sleep 1
run exp9_err_missing.log $PY udp_file_client.py missing.txt
sleep 1
run exp9_err_invalid.log $PY udp_file_client.py ../secret.txt
sleep 1
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1

$PY udp_file_server.py --dup > "$LOG/exp9_dup_server.log" 2>&1 &
SRV=$!
sleep 1
run exp9_dup_client.log $PY udp_file_client.py sensor_log.txt
sleep 1; kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1

echo "--- Experiment 9 loss: without repair, then with the RESEND repair"
$PY udp_file_server.py --drop 7 > "$LOG/exp9_drop_server.log" 2>&1 &
SRV=$!
sleep 1
run exp9_drop_norepair.log $PY udp_file_client.py sensor_log.txt --no-repair
sleep 1
run exp9_drop_repair.log $PY udp_file_client.py sensor_log.txt
sleep 1; kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1

run exp9_err_noserver.log $PY udp_file_client.py sensor_log.txt
sleep 1

echo "--- Experiment 10 (benchmark, 3 runs each)"
$PY tcp_file_server.py > "$LOG/exp10_tcp_server.log" 2>&1 &
T=$!
$PY udp_file_server.py > "$LOG/exp10_udp_server.log" 2>&1 &
U=$!
sleep 1
run exp10_benchmark.log $PY benchmark.py sensor_log.txt
sleep 1
run exp10_benchmark_small.log $PY benchmark.py notes_log.txt
kill $T $U 2>/dev/null; wait $T $U 2>/dev/null
kill $CAP2 2>/dev/null; wait $CAP2 2>/dev/null

run final_verify.log $PY integrity.py server_files/sensor_log.txt received_tcp_sensor_log.txt received_udp_sensor_log.txt
echo "### done"; ls "$LOG" | wc -l
