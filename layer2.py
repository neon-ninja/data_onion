#!/usr/bin/env python3

import base64

with open("layer2.txt", "r") as f:
    encoded = f.read()
    binary = base64.a85decode(encoded, adobe=True)

def binary_str(byte):
    return '{:08b}'.format(byte)

result = ""

for byte in binary:
    s = binary_str(byte)[:7]
    ones = sum(c == "1" for c in s)
    parity = byte & 1
    if ones % 2 == parity:
        result += s

final = ""

for i in range(0, len(result), 8):
    final += chr(int(result[i:i+8], 2))

print(final)