#!/bin/bash
# Runs every Experiment / Lab Task of version A for real and stores the terminal
# transcripts in logsA/ and the loopback captures in ../captures/.
set -u
CODE=/home/arqamwd/nust/cn/lab6/codeA
WORK=/home/arqamwd/nust/cn/lab6/runA
LOG=/home/arqamwd/nust/cn/lab6/build/logsA
CAPDIR=/home/arqamwd/nust/cn/lab6/captures
PY=python3

rm -rf "$WORK" "$LOG"; mkdir -p "$WORK" "$LOG" "$CAPDIR"
cp "$CODE"/*.py "$WORK"/            # the manual asks for every lab file in one folder
cd "$WORK" || exit 1
run() { local out=$1; shift; "$@" > "$LOG/$out" 2>&1; }

echo "### prep: data files"
$PY -c "open('share_me.txt','w').write('Hello from the server\n' * 500)"
run exp7_generate.log $PY generate_log.py 300 sensor_log.txt
mkdir -p server_files && cp sensor_log.txt server_files/
run exp7_generate_small.log $PY generate_log.py 100 notes_log.txt
cp notes_log.txt server_files/
run exp7_tools.log $PY file_tools.py sensor_log.txt
run exp7_tools_small.log $PY file_tools.py notes_log.txt
echo "secret admin password" > secret.txt

echo "### capture 1: messaging (ports 5000 / 5001)"
dumpcap -i lo -q -w "$CAPDIR/lab6_msg.pcapng" -a duration:60 > /dev/null 2>&1 &
CAP=$!
sleep 2

echo "--- Experiment 1 + Group A tasks 1-3 (TCP 5000)"
$PY -u tcp_server.py > "$LOG/exp1_server.log" 2>&1 &
S1=$!
sleep 1
printf 'Hello Server\nComputer Networks\nLab 6 socket programming\nArqam Waheed 553514\nTCP is reliable\nexit\n' \
  | run exp1_client.log $PY -u tcp_client.py
wait $S1 2>/dev/null
sleep 1

echo "--- Experiment 2 + Group A task 4 (UDP 5001)"
$PY -u udp_server.py > "$LOG/exp2_server.log" 2>&1 &
S2=$!
sleep 1
printf 'Hello Server\nUDP has no handshake\nDatagrams are independent\nArqam Waheed 553514\nFaster but not reliable\nexit\n' \
  | run exp2_client.log $PY -u udp_client.py
sleep 1
wait $S2 2>/dev/null
sleep 1
kill $CAP 2>/dev/null; wait $CAP 2>/dev/null
sleep 1

echo "--- Group A task 5 (TCP calculator 5005)"
$PY -u calc_server.py > "$LOG/taskA5_server.log" 2>&1 &
S3=$!
sleep 1
printf '12 + 8\n7 * 6\n45 / 4\n10 / 0\n5 ^ 2\nexit\n' | run taskA5_client.log $PY -u calc_client.py
sleep 1; wait $S3 2>/dev/null; sleep 1

echo "--- Group A task 6 (UDP echo 5006)"
$PY -u echo_server.py > "$LOG/taskA6_server.log" 2>&1 &
S4=$!
sleep 1
printf 'Echo this back\nMiXeD CaSe 123\nexit\n' | run taskA6_client.log $PY -u echo_client.py
sleep 1; wait $S4 2>/dev/null; sleep 1

echo "--- Experiment 4 (byte stream, 5004)"
$PY -u boundary_server.py > "$LOG/exp4_server.log" 2>&1 &
sleep 1
run exp4_client.log $PY boundary_client.py
sleep 2
$PY -u boundary_server.py > "$LOG/exp4_server_split.log" 2>&1 &
sleep 1
run exp4_client_split.log $PY boundary_client.py --split
sleep 2

echo "--- Experiment 5 (file sharing, 5002)"
$PY -u share_server.py > "$LOG/exp5_server.log" 2>&1 &
sleep 1
run exp5_client.log $PY share_client.py
sleep 1
{ ls -l share_me.txt received_share_me.txt
  cmp share_me.txt received_share_me.txt && echo "cmp: files are identical"
  sha256sum share_me.txt received_share_me.txt; } > "$LOG/exp5_verify.log" 2>&1

echo "--- Experiment 6 (same machine over the real interface IP)"
IP=$(ip -4 -o addr show wlp0s20f3 | awk '{print $4}' | cut -d/ -f1)
echo "interface IP: $IP" > "$LOG/exp6_setup.log"
ip -4 -o addr show wlp0s20f3 >> "$LOG/exp6_setup.log" 2>&1
ping -c 3 "$IP" >> "$LOG/exp6_setup.log" 2>&1
$PY -u share_server.py --lan > "$LOG/exp6_server.log" 2>&1 &
sleep 1
run exp6_client.log $PY share_client.py "$IP"
sleep 1
$PY -c "import hashlib;print('share_me.txt        ',hashlib.sha256(open('share_me.txt','rb').read()).hexdigest())" > "$LOG/exp6_verify.log"
$PY -c "import hashlib;print('received_share_me.txt',hashlib.sha256(open('received_share_me.txt','rb').read()).hexdigest())" >> "$LOG/exp6_verify.log"

echo "### capture 2: file transfer (ports 6000 / 6001)"
dumpcap -i lo -q -w "$CAPDIR/lab6_files.pcapng" -a duration:90 > /dev/null 2>&1 &
CAP2=$!
sleep 2

echo "--- Experiment 8 (TCP file server 6000)"
$PY -u tcp_file_server.py > "$LOG/exp8_server.log" 2>&1 &
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

echo "--- Experiment 8 premature closure (--slow + Ctrl+C)"
$PY -u tcp_file_server.py --slow > "$LOG/exp8_slow_server.log" 2>&1 &
SRV=$!
sleep 1
$PY tcp_file_client.py sensor_log.txt > "$LOG/exp8_err_closed.log" 2>&1 &
CLI=$!
sleep 2
kill -TERM $SRV 2>/dev/null          # same effect as Ctrl+C: the server dies mid-transfer
wait $SRV 2>/dev/null
wait $CLI 2>/dev/null
sleep 1

echo "--- Experiment 9 (UDP file server 6001)"
$PY -u udp_file_server.py > "$LOG/exp9_server.log" 2>&1 &
SRV=$!
sleep 1
run exp9_client.log $PY udp_file_client.py sensor_log.txt
sleep 1
run exp9_err_missing.log $PY udp_file_client.py missing.txt
sleep 1
run exp9_err_invalid.log $PY udp_file_client.py ../secret.txt
sleep 1
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1

$PY -u udp_file_server.py --dup > "$LOG/exp9_dup_server.log" 2>&1 &
SRV=$!
sleep 1
run exp9_dup_client.log $PY udp_file_client.py sensor_log.txt
sleep 1; kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1

$PY -u udp_file_server.py --drop > "$LOG/exp9_drop_server.log" 2>&1 &
SRV=$!
sleep 1
run exp9_drop_client.log $PY udp_file_client.py sensor_log.txt
sleep 1; kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; sleep 1

run exp9_err_noserver.log $PY udp_file_client.py sensor_log.txt
sleep 1

echo "--- Experiment 10 (three runs each)"
$PY -u tcp_file_server.py > "$LOG/exp10_tcp_server.log" 2>&1 &
T=$!
$PY -u udp_file_server.py > "$LOG/exp10_udp_server.log" 2>&1 &
U=$!
sleep 1
for i in 1 2 3; do run exp10_tcp_$i.log $PY tcp_file_client.py sensor_log.txt; sleep 1; done
for i in 1 2 3; do run exp10_udp_$i.log $PY udp_file_client.py sensor_log.txt; sleep 1; done
kill $T $U 2>/dev/null; wait $T $U 2>/dev/null
kill $CAP2 2>/dev/null; wait $CAP2 2>/dev/null

echo "### integrity of the received copies"
{ sha256sum server_files/sensor_log.txt received_tcp_sensor_log.txt received_udp_sensor_log.txt
  ls -l server_files/sensor_log.txt received_tcp_sensor_log.txt received_udp_sensor_log.txt; } > "$LOG/final_verify.log" 2>&1

echo "### done"; ls "$LOG" | wc -l
