import sys
from Crypto.Cipher import AES 


enc = bytes.fromhex("b8a363a95d83b3d13886dc97899844463d356fe030f67fa3681537a3d88e8966")
DATA_2 = "a355c8b253a6f0037c9cd331c8b4b5afb7198c944e56db549612942ceec05e8c"

def shuffle_using(xs, y):
    for i in range(0, len(xs), y):
        xs.append(xs.pop(i))
    return xs

def extend_key(key):
    return key * 8

def test_dec(key):
    key_one = key[:2]
    key_two = key[2:]
    
    key_one = extend_key(key_one)
    key_two = extend_key(key_two)
    c_one = AES.new(key_one, AES.MODE_ECB)
    c_two = AES.new(key_two, AES.MODE_ECB)

    res = c_one.decrypt(c_two.decrypt(enc))
    if b"maple" in res:
        print("flag", res)
        sys.exit(0)

secret_len = 8

# bruteforce the secret 
import itertools
idx = 0
total = 7 ** secret_len
for test_secret in itertools.product(range(7), repeat=secret_len):
    idx += 1
    if idx % 100000 == 0:
        print(f"{idx}/{total} ({idx/total})")

    result = list(DATA_2)
    for secret in test_secret:
        result = shuffle_using(result, secret + 1)
    
    key = "".join(result[:8])
    test_dec(bytes.fromhex(key))
