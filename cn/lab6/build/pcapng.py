"""Minimal pcapng reader for the Lab 6 loopback captures.

It exposes the small part of the scapy API that the screenshot renderer needs
(rdpcap, IP/TCP/UDP layer keys, packet.time, bytes(packet)), so the lab does not
depend on scapy being installed.  Only Ethernet + IPv4 + TCP/UDP is decoded,
which is everything that appears in a loopback capture of these experiments.
"""
import struct

IP, TCP, UDP = "IP", "TCP", "UDP"

SHB, IDB, EPB = 0x0A0D0D0A, 0x00000001, 0x00000006
OPT_NAMES = {2: "MSS", 3: "WScale", 4: "SAckOK", 5: "SAck", 8: "Timestamp"}


class Layer:
    def __init__(self, **fields):
        self.__dict__.update(fields)


class Packet:
    def __init__(self, raw, timestamp):
        self.raw = raw
        self.time = timestamp
        self.layers = {}
        self.src = self.dst = "00:00:00:00:00:00"
        self._decode()

    # --- scapy-like access -------------------------------------------------
    def __contains__(self, key):
        return key in self.layers

    def __getitem__(self, key):
        return self.layers[key]

    def __len__(self):
        return len(self.raw)

    def __bytes__(self):
        return self.raw

    # --- decoding ----------------------------------------------------------
    def _decode(self):
        raw = self.raw
        if len(raw) < 14:
            return
        mac = lambda b: ":".join(f"{x:02x}" for x in b)
        self.dst, self.src = mac(raw[0:6]), mac(raw[6:12])
        if struct.unpack_from("!H", raw, 12)[0] != 0x0800:      # IPv4 only
            return
        o = 14
        vihl, tos, total, ident, flags_frag, ttl, proto, chksum = struct.unpack_from("!BBHHHBBH", raw, o)
        ihl = (vihl & 0x0F) * 4
        src = ".".join(str(b) for b in raw[o + 12:o + 16])
        dst = ".".join(str(b) for b in raw[o + 16:o + 20])
        self.layers[IP] = Layer(src=src, dst=dst, ihl=ihl // 4, len=total, id=ident, ttl=ttl,
                                proto=proto, chksum=chksum, flags=flags_frag >> 13,
                                frag=flags_frag & 0x1FFF, tos=tos, offset=o)
        o += ihl
        if proto == 6:
            self._tcp(o)
        elif proto == 17:
            self._udp(o)

    def _tcp(self, o):
        raw = self.raw
        sport, dport, seq, ack, off_res, flags, window, chksum, urg = struct.unpack_from("!HHIIBBHHH", raw, o)
        dataofs = off_res >> 4
        options, i, end = [], o + 20, o + dataofs * 4
        while i < end:
            kind = raw[i]
            if kind == 0:
                break
            if kind == 1:
                options.append(("NOP", None)); i += 1; continue
            if i + 1 >= end:
                break
            length = raw[i + 1]
            body = raw[i + 2:i + length]
            name = OPT_NAMES.get(kind, str(kind))
            if kind == 2 and len(body) == 2:
                value = struct.unpack("!H", body)[0]
            elif kind == 3 and len(body) == 1:
                value = body[0]
            elif kind == 8 and len(body) == 8:
                value = struct.unpack("!II", body)
            elif kind == 4:
                value = ""
            else:
                value = body
            options.append((name, value))
            i += max(length, 2)
        payload = raw[o + dataofs * 4:o + self.layers[IP].len - self.layers[IP].ihl * 4] \
            if IP in self.layers else raw[o + dataofs * 4:]
        self.layers[TCP] = Layer(sport=sport, dport=dport, seq=seq, ack=ack, dataofs=dataofs,
                                 flags=flags, window=window, chksum=chksum, urgptr=urg,
                                 options=options, payload=payload, offset=o)

    def _udp(self, o):
        raw = self.raw
        sport, dport, length, chksum = struct.unpack_from("!HHHH", raw, o)
        self.layers[UDP] = Layer(sport=sport, dport=dport, len=length, chksum=chksum,
                                 payload=raw[o + 8:o + length], offset=o)


def rdpcap(path):
    """Read a pcapng file written by dumpcap and return a list of Packets."""
    data = open(path, "rb").read()
    packets, offset, resolution = [], 0, 1e-6
    while offset + 12 <= len(data):
        btype, blen = struct.unpack_from("<II", data, offset)
        if blen < 12 or offset + blen > len(data):
            break
        body = data[offset + 8:offset + blen - 4]
        if btype == IDB:
            i = 8                                    # linktype (2) + reserved (2) + snaplen (4)
            while i + 4 <= len(body):                # walk the options for if_tsresol
                code, olen = struct.unpack_from("<HH", body, i)
                if code == 0:
                    break
                if code == 9 and olen >= 1:
                    resolution = 10.0 ** -body[i + 4]
                i += 4 + (olen + 3) // 4 * 4
        elif btype == EPB:
            _, tsh, tsl, caplen, _ = struct.unpack_from("<IIIII", body, 0)
            raw = body[20:20 + caplen]
            packets.append(Packet(raw, ((tsh << 32) | tsl) * resolution))
        offset += blen
    return packets


def flag_names(flags):
    return ", ".join(n for b, n in enumerate(("FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR"))
                     if int(flags) >> b & 1)
