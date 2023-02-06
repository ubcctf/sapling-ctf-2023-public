#!/usr/bin/env python3
from Crypto.Util.number import getPrime, bytes_to_long, inverse, long_to_bytes
from secrets import flag


def verify(sig, msg):
    return msg == long_to_bytes(pow(bytes_to_long(sig), e, N))


def sign(msg):
    return long_to_bytes(pow(bytes_to_long(msg), d, N))


p = getPrime(512)
q = getPrime(512)
N = p * q
e = 65537

print("N:", hex(N))

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

msg1 = b"Baba is you."
sig1 = sign(msg1)
assert verify(sig1, msg1)
print("Baba is you:", sig1.hex())

msg2 = bytes.fromhex(input(">>> "))
if msg2 == b"Baba is flag.":
    print("Baba is lose.")
    exit()
sig2 = sign(msg2)
assert verify(sig2, msg2)
print("Baba is", sig2.hex())

msg3 = b"Baba is flag."
sig3 = bytes.fromhex(input(">>> "))

if verify(sig3, msg3):
    print("Baba is win.", flag)
else:
    print("Baba is lose.")
