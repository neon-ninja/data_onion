#!/usr/bin/env python3

import base64

with open("layer3.txt", "r") as f:
    encoded = f.read()
    decoded = base64.a85decode(encoded, adobe=True)

# We know some of the input text, so we can scan the encoded data, and when
# we find the right place, xoring with our known bytes will give us the
# key.
known_text = b'==[ Payload ]==================='

for offset in range(len(decoded)):
    unrotated_key = [databyte ^ knownbyte for (databyte, knownbyte) in zip(decoded[offset:offset + 32], known_text)]
    rotation_offset = offset % 32
    key = unrotated_key[-rotation_offset:] + unrotated_key[:-rotation_offset]
    cycles = len(decoded) // 32 + 1
    cycled_key = (key * cycles)[:len(decoded)]

    b = []
    for (databyte, keybyte) in zip(decoded, cycled_key):
        b.append(databyte ^ keybyte)

    # Simply try until we get decodable utf-8 data that has what we want
    try:
        output = bytes(b).decode('utf-8')
        if output.startswith('==[ Layer 4/5: ') and '==[ Payload ]============================================' in output:
            print(output)
    except:
        pass
