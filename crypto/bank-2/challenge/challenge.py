#!/usr/bin/env python3
from Crypto.Cipher import AES 
import os 
import traceback 
from secret import FLAG

# ======= AES and CBC stuff =======
key = os.urandom(16) # This is 16 bytes of cryptographically random data, there's no way you can bruteforce or guess this
cipher = AES.new(key, AES.MODE_ECB) # This says ECB mode, but we'll never encrypt more than 16 bytes at a time, so this is just AES with no mode

# hmmm... this looks different
def pad(msg):
    bytes_of_padding = (16 - len(msg)) % 16
    pad_bytes = bytes([bytes_of_padding])
    return pad_bytes * bytes_of_padding + msg

# hmmm... wonder why this is here
class InvalidPadding(Exception):
    pass

def strip_padding(block, quiet=False):
    first = block[0]
    if first > 16:
        if not quiet: 
            print(f"[+] The first byte is {hex(first)}. No padding, returning")
        return block

    if not quiet: 
        print(f"[+] The first byte is {hex(first)}, checking the first {first} bytes for padding validity")

    if all([first == b for b in block[:first]]):
        if not quiet: 
            print(f"[+] Padding is valid")
        return block[first:]
    else:
        if not quiet: 
            print(f"[+] Padding is invalid!")
        raise InvalidPadding()

# splits the message into 16 byte chunks
# msg must be a multiple of 16 bytes long
def blockify(msg):
    blocks = []
    for i in range(0,len(msg),16):
        blocks.append(msg[i:i+16])
    return blocks

def xor(a,b):
    assert len(a) == len(b)
    return bytes([x ^ y for x,y in zip(a,b)])

def encrypt(ptxt):
    iv = os.urandom(16)
    msg = pad(ptxt)
    blocks = blockify(msg)
    result = b""
    last = iv 
    for block in blocks:
        next = cipher.encrypt(xor(last, block))
        result = result + next
        last = next
    return result, iv

def decrypt(ctxt, iv):
    ctxt_blocks = blockify(ctxt)
    ptxt_blocks = []
    last = iv
    for block in ctxt_blocks:
        intermediate = cipher.decrypt(block)
        ptxt_blocks.append(xor(last, intermediate))
        last = block
    ptxt_blocks[-1] = strip_padding(ptxt_blocks[-1])
    result = b"".join(ptxt_blocks)
    return result
            

intercepted_ctxt, intercepted_iv = encrypt(FLAG)
inbox = []

def send_email():
    try:
        email_hex = input("Input your email: ")
        iv_hex = input("Input your IV: ")
        email = bytes.fromhex(email_hex)
        iv = bytes.fromhex(iv_hex)
        contents = decrypt(email, iv)
        inbox.append(contents)
        print("Email received.")
    except InvalidPadding as e:
        print("Email is corrupted, try again")
    except Exception as e:
        print(f"Oh no something has gone wrong")
        traceback.print_exc()

def main():
    print("Your task is to decrypt this intercepted email")
    print(f"Ciphertext: {intercepted_ctxt.hex()}")
    print(f"IV: {intercepted_iv.hex()}")

    while True:
        print("===")
        send_email()

if __name__ == "__main__":
    main()