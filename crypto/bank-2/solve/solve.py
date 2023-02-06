from pwn import *
import codecs
import sys

# context.log_level = "debug"
r = remote("bank-2.ctf.maplebacon.org", 1337)

r.recvuntil(b"Ciphertext: ")
cipher_text = bytes.fromhex(r.recvline().strip().decode())
r.recvuntil(b"IV: ")
IV = bytes.fromhex(r.recvline().strip().decode())
r.recvuntil(b":")

print("goal:", cipher_text, IV)

def check_secret(payload, iv):
    # print("sending", payload, iv)
    r.sendline(payload.hex().encode())
    r.recvuntil(b":")
    r.sendline(iv.hex().encode())
    resp = r.recvuntil(b":")
    if b"Oh no" in resp:
        print("failed")
        sys.exit(1)
    print(resp)
    return b"received" in resp
    # try:
    #     challenge.decrypt(payload, iv)
    #     return True
    # except:
    #     return False

def blockify(msg):
    blocks = []
    for i in range(0,len(msg),16):
        blocks.append(msg[i:i+16])
    return blocks

def xor(a,b):
    assert len(a) == len(b)
    return bytes([x ^ y for x,y in zip(a,b)])

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

def generate(inter_block, m):
    ret = b''
    for i in range(m):
        ret += bytes([inter_block[i] ^ (m+1)])
    return ret
    
def attack_block(target, IV):
    latest_inter_block = []
    for n in range(16):
        extra = generate(latest_inter_block,n)
        answer = None
        for i in range(256):
            test = bytes([i])
            payload = extra + test + b'A' * (15-n)
            res = check_secret(target, payload)
            if res:
                if n == 0:
                    # print("continuity check")
                    payload = bytes([(i ^ 1) ^ 2]) + b"A" * 15 
                    if check_secret(target, payload):
                        # print("continuity failed, first byte probably not a valid padding byte")
                        continue
                    for possible_second in range(256):
                        payload = bytes([(i ^ 1) ^ 2]) + bytes([possible_second]) + b"A" * 14
                        if check_secret(target, payload):
                            break
                    else:
                        # print("continuity failed, first byte probably a valid padding byte that wasnt 0x1")
                        continue
                print("found it:",i, "n=",n)
                answer = i
                break
        if answer == None:
            raise Exception("No answer found")
        latest_inter_block += [(answer ^ (n+1))]
    return latest_inter_block

def padding_oracle_attack():
    # cipher_text, IV = challenge.intercepted_ctxt, challenge.intercepted_iv
    blocks = blockify(cipher_text)
    inter = []
    for i in range(len(blocks)):
        inter += attack_block(blocks[i], IV)


    inter_bytes = bytes(inter)
    # print("obtained inter")
    # for x in challenge.blockify(inter_bytes):
    #     print(x.hex())
    
    # print("real inter")
    # real_inter = b""
    # for block in blocks:
    #     aaa = challenge.cipher.decrypt(block)
    #     real_inter += aaa
    #     print(aaa.hex())

    final = strip_padding(xor(inter_bytes, IV+cipher_text[:-16]))
    secret = codecs.decode(final,'ascii')
    print(secret)

padding_oracle_attack()