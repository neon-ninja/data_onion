#!/usr/bin/env python3

import base64

with open("layer0.txt", "r") as f:
    encoded = f.read()
    binary = base64.a85decode(encoded, adobe=True)
    print(binary.decode())