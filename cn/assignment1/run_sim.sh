ip link set lo up
for a in 10.7.91.204 10.7.88.166 10.7.72.69 10.7.183.22; do ip addr add $a/16 dev lo; done
python3 -u server.py > server.log 2>&1 & SP=$!; sleep 1
run() { printf '%s\n%s\n' "$3" "$4" | python3 friend.py "$1" "$2" 10.7.91.204 > "$5"; sleep "$6"; }
run 10.7.88.166 $(shuf -i 49152-65535 -n1) "Syed Abdul Hasib" "546619" friend_1.log 52
run 10.7.72.69 $(shuf -i 49152-65535 -n1) "Zohaib Anwar" "555013" friend_2.log 74
run 10.7.183.22 0 "Abdullah" "549117" friend_3.log 1
kill $SP
