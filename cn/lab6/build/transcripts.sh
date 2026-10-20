#!/bin/bash
# Re-runs only the (deterministic, server-free) verification commands and records
# both the command line and its output, so a screenshot shows a real transcript.
set -u
V=$1                       # A or B
WORK=/home/arqamwd/nust/cn/lab6/run$V
LOG=/home/arqamwd/nust/cn/lab6/build/logs$V
CODE=/home/arqamwd/nust/cn/lab6/code$V
cd "$WORK" || exit 1

t() {
  local f="$LOG/$1"; shift
  local disp=""
  for a in "$@"; do case "$a" in *" "*) disp="$disp '$a'";; *) disp="$disp $a";; esac; done
  echo "\$$disp" >> "$f"
  "$@" >> "$f" 2>&1
}

rm -f "$LOG"/ts_*.log

# Experiment 5 verification
t ts_exp5_verify.log stat -c "%10s bytes  %n" share_me.txt received_share_me.txt
t ts_exp5_verify.log cmp share_me.txt received_share_me.txt
echo "(no output from cmp = the two files are identical)" >> "$LOG/ts_exp5_verify.log"
t ts_exp5_verify.log sha256sum share_me.txt received_share_me.txt

# Experiment 7 file generation and integrity
if [ "$V" = "A" ]; then
  t ts_exp7.log python3 generate_log.py 300 sensor_log.txt
  t ts_exp7.log python3 file_tools.py sensor_log.txt
  t ts_exp7.log python3 generate_log.py 100 notes_log.txt
  t ts_exp7.log python3 file_tools.py notes_log.txt
  t ts_exp7.log head -3 sensor_log.txt
else
  t ts_exp7.log python3 make_log.py 300 sensor_log.txt
  t ts_exp7.log python3 make_log.py 100 notes_log.txt
  t ts_exp7.log python3 integrity.py sensor_log.txt notes_log.txt
  t ts_exp7.log head -3 sensor_log.txt
fi

# Experiment 6 setup
IP=$(ip -4 -o addr show wlp0s20f3 | awk '{print $4}' | cut -d/ -f1)
t ts_exp6.log ip -4 -o addr show wlp0s20f3
t ts_exp6.log ping -c 3 "$IP"
echo "$IP" > "$LOG/ts_ip.txt"

# final integrity of both received copies
t ts_final.log sha256sum server_files/sensor_log.txt received_tcp_sensor_log.txt received_udp_sensor_log.txt
t ts_final.log stat -c "%10s bytes  %n" server_files/sensor_log.txt received_tcp_sensor_log.txt received_udp_sensor_log.txt
echo "### transcripts for version $V done"
