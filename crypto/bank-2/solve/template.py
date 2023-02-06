from pwn import * # requires pwntools

# context.log_level = "debug"
r = remote("bank-2.ctf.maplebacon.org", 1337)

r.recvuntil(b"Ciphertext: ")
cipher_text = bytes.fromhex(r.recvline().strip().decode())
r.recvuntil(b"IV: ")
IV = bytes.fromhex(r.recvline().strip().decode())
r.recvuntil(b":")

def check_secret(payload, iv):
    # print("sending", payload, iv)
    r.sendline(payload.hex().encode())
    r.recvuntil(b":")
    r.sendline(iv.hex().encode())
    resp = r.recvuntil(b":")
    return resp
