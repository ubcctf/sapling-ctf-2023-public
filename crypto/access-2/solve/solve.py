from Crypto.Util import number
from Crypto.Cipher import AES 
import hashlib

want = "20a667175dfa51fc1ef0b4c73fc6c96ba29fbd7612015d389a3c35b753124822"

known_ptxt = b"is this thing on"
known_ctxt_hex = "3d23351bb8a61128ff846e5ea736cab2"
known_ctxt = bytes.fromhex(known_ctxt_hex)
empty = bytes([0]*12)

debug = [3829705, 13449307]

forwards = {}
backwards =  {}
N = 2**16
for guess in range(N):
    if guess % 100000 == 0:
        print(f"{guess}/{N} ({guess/N})")

    key_part = guess.to_bytes(2,byteorder="big")
    key = key_part * 8
    c = AES.new(key, AES.MODE_ECB)
    f = c.encrypt(known_ptxt)
    b = c.decrypt(known_ctxt)

    forwards[f] = key_part
    backwards[b] = key_part

print("done")

for a in forwards.keys():
    if a in backwards:
        print("found it")
        key_one = forwards[a] * 8
        key_two = backwards[a] * 8
        c_one = AES.new(key_one, AES.MODE_ECB)
        c_two = AES.new(key_two, AES.MODE_ECB)
        print("flag",c_one.decrypt(c_two.decrypt(bytes.fromhex(want))))
        break