#!/usr/bin/env python3

import base64

with open("layer1.txt", "r") as f:
    encoded = f.read()
    binary = base64.a85decode(encoded, adobe=True)

evenbits = int('01010101', 2)

def print_binary(byte):
    print('{:08b}'.format(byte))

s = ""

for byte in binary:
    #print_binary(byte)
    flipped = byte ^ evenbits
    #print_binary(flipped)
    tail = flipped & 1
    shifted = flipped >> 1
    promoted_tail = tail << 7
    result = shifted | promoted_tail
    #print_binary(result)
    s += chr(result)

print(s)