#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES
import struct
QUAD = struct.Struct('>Q')

with open("layer5.txt", "r") as f:
    encoded = f.read()
    decoded = base64.a85decode(encoded, adobe=True)

KEK = decoded[:32]
IV = QUAD.unpack(decoded[32:40])[0]
WRAPPED_KEY = decoded[40:80]
ENCIV = decoded[80:96]
ENCRYPTED_PAYLOAD = decoded[96:]

def aes_unwrap_key_and_iv(kek, wrapped):
    n = len(wrapped)//8 - 1
    #NOTE: R[0] is never accessed, left in for consistency with RFC indices
    R = [None]+[wrapped[i*8:i*8+8] for i in range(1, n+1)]
    A = QUAD.unpack(wrapped[:8])[0]
    decrypt = AES.new(kek, AES.MODE_ECB).decrypt
    for j in range(5,-1,-1): #counting down
        for i in range(n, 0, -1): #(n, n-1, ..., 1)
            ciphertext = QUAD.pack(A^(n*j+i)) + R[i]
            B = decrypt(ciphertext)
            A = QUAD.unpack(B[:8])[0]
            R[i] = B[8:]
    return b"".join(R[1:]), A

KEY, new_IV = aes_unwrap_key_and_iv(KEK, WRAPPED_KEY)
assert new_IV == IV
#print(KEY)

cipher = AES.new(KEY, AES.MODE_CBC, ENCIV)
print(cipher.decrypt(ENCRYPTED_PAYLOAD).decode())