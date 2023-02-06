from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime, inverse, isPrime

p = getPrime(1024)
q = p + 2
while not isPrime(q):
    q += 2

N = p * q
e = 65537
phi = (p-1) * (q-1)
d = inverse(e, phi)

key = RSA.construct((N, e, d, p, q))

with open("private.key", 'wb') as content_file:
    content_file.write(key.exportKey('PEM'))

pubkey = key.publickey()
with open("public.key", 'wb') as content_file:
    content_file.write(pubkey.exportKey('PEM'))