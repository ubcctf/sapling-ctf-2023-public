from Crypto.Cipher import AES 
import os 
from flag import FLAG

DATA = os.urandom(8)
DATA_2 = "a355c8b253a6f0037c9cd331c8b4b5afb7198c944e56db549612942ceec05e8c"

# pads the message to a multiple of 16 bytes
def pad(msg):
    bytes_of_padding = (16 - len(msg)) % 16
    pad_bytes = bytes([bytes_of_padding]) # creates a single byte that has the numerical value of the number of bytes of padding you want
                                          # this padding scheme is called PKCS, don't worry about it, just know it pads the message to 16 bytes
    return msg + pad_bytes * bytes_of_padding

def shuffle_using(xs, y):
    for i in range(0, len(xs), y):
        xs.append(xs.pop(i))
    return xs

def make_key():
    result = list(DATA_2)
    for secret in DATA:
        # I got yelled at by the security team... they said I needed more bits
        result = shuffle_using(result, secret % 16 + 1)
    key = "".join(result[:8])
    return bytes.fromhex(key)

def extend_key(key):
    return key * 8

def encrypt(key, message):
    key_one = key[:2]
    key_two = key[2:]
    
    key_one = extend_key(key_one)
    key_two = extend_key(key_two)

    c_one = AES.new(key_one, AES.MODE_ECB)
    c_two = AES.new(key_two, AES.MODE_ECB)

    return c_two.encrypt(c_one.encrypt(pad(message)))

key = make_key()
print("Decrypt this message to proceed: ", encrypt(key, FLAG).hex())

message = b"is this thing on"
print("Intercepted test message: ", encrypt(key, message).hex())