#!/usr/bin/env python3

import base64
import numpy as np
import struct
imm32 = struct.Struct('<I')

a, b, c, d, e, f = np.zeros(6, np.uint8)
la, lb, lc, ld, ptr, pc = np.zeros(6, np.uint32)

mem = b""

with open("layer6_test.txt") as f: # test program, prints "Hello, world!"
    for l in f.readlines():
        l = l[:l.index("#")].strip().replace(" ", "")
        mem += bytes.fromhex(l)

with open("layer6.txt", "r") as f:
    encoded = f.read()
    mem = bytearray(base64.a85decode(encoded, adobe=True))

#print(mem)
ln = 0

while True:
    i = mem[pc]
    ln += 1
    #print(ln, hex(i))
    if i == 0xC2: # ADD a <- b
        a = (a + b) % 256
        pc += 1
    elif i == 0xE1: # APTR imm8
        ptr += mem[pc + 1]
        pc += 2
    elif i == 0xC1: # CMP
        f = 0 if a == b else 1
        pc += 1
    elif i == 0x01: # HALT
        break
    elif i == 0x21: # JEZ imm32
        if f == 0:
            pc = imm32.unpack(mem[pc + 1: pc + 5])[0]
        else:
            pc += 5
    elif i == 0x22: # JNZ imm32
        if f != 0:
            pc = imm32.unpack(mem[pc + 1: pc + 5])[0]
        else:
            pc += 5
    elif i == 0xC4: # XOR
        a ^= b
        pc += 1
    elif i == 0x02: # OUT
        print(chr(a), end="")
        pc += 1
    elif i == 0xC3: # SUB
        a -= b
        if a < 0:
            a += 256
        pc += 1
    elif i & 0b01000000: # MV
        dest = (i & 0b00111000) >> 3
        src = i & 0b00000111
        if src == 0: # MVI
            src = mem[pc + 1]
            pc += 2
        else:
            try:
                src = [0,a,b,c,d,e,f,mem[ptr+c]][src]
            except IndexError:
                src = [0,a,b,c,d,e,f,0][src]
            pc += 1
        if dest == 1:
            a = src
        elif dest == 2:
            b = src
        elif dest == 3:
            c = src
        elif dest == 4:
            d = src
        elif dest == 5:
            e = src
        elif dest == 6:
            f = src
        elif dest == 7:
            mem[ptr+c] = src
    elif i & 0b10000000: # MV32
        dest = (i & 0b00111000) >> 3
        src = i & 0b00000111
        if src == 0: # MVI32
            src = imm32.unpack(mem[pc + 1: pc + 5])[0]
            pc += 5
        else:
            src = [0, la, lb, lc, ld, ptr, pc][src]
            pc += 1
        if dest == 1:
            la = src
        elif dest == 2:
            lb = src
        elif dest == 3:
            lc = src
        elif dest == 4:
            ld = src
        elif dest == 5:
            ptr = src
        elif dest == 6:
            pc = src
    else:
        print("\nERROR")
        break
print()