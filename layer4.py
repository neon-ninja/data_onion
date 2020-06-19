#!/usr/bin/env python3

import base64
from struct import unpack

with open("layer4.txt", "r") as f:
    encoded = f.read()
    decoded = base64.a85decode(encoded, adobe=True)

def str_ip(bytes):
    return ".".join(str(int(b)) for b in bytes)

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def calc_checksum(msg):
    s = 0
    w = 0
    for i in range(0, len(msg), 2):
        w = msg[i] + (msg[i+1] << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

offset = 0
while offset < len(decoded):
    ipv4 = decoded[offset:offset+20]

    protocol = ipv4[9]
    length = unpack(">H", ipv4[2:4])[0]
    sourceIP = str_ip(ipv4[12:16])
    destIP = str_ip(ipv4[16:20])
    checksum = calc_checksum(ipv4)

    if sourceIP == "10.1.1.10" and destIP == "10.1.1.200" and checksum == 0:
        udp = decoded[offset+20:offset+28]
        srcPort, destPort, udpLength, udpChecksum = unpack(">HHHH", udp)
        if destPort == 42069:
            #print(sourceIP, destIP, checksum, length, protocol)
            data = decoded[offset+28:offset+length]
            pseudoheader = ipv4[12:20] + bytes([0, protocol]) + udp[4:6] + udp[0:4] + udp[4:6] + udp[6:8] + data
            if len(pseudoheader) % 2 != 0:
                pseudoheader += bytes([0])
            #print(srcPort, destPort, udpLength, udpChecksum)
            udpChecksum = calc_checksum(pseudoheader)
            if udpChecksum == 0:
                print(data.decode().strip())
    offset += length