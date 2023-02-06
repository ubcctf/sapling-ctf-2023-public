from pwn import * # requires pwntools

# context.log_level = "debug"
r = remote("bank-1.ctf.maplebacon.org", 1337)
r.recvuntil(">")

def request_money(amt):
    r.sendline(b"2")
    r.recvuntil(b":")
    r.sendline(str(amt).encode())
    r.recvuntil(b"Your receipt: ")
    ctxt = r.recvline()
    r.recvuntil(b">")
    return ctxt

def send_money(sender_id, recipient_id, sender_pin, amount):
    r.sendline(b"1")
    r.recvuntil(b":")
    r.sendline(str(sender_id).encode())
    r.recvuntil(b":")
    r.sendline(str(recipient_id).encode())
    r.recvuntil(b":")
    r.sendline(str(sender_pin).encode())
    r.recvuntil(b":")
    r.sendline(str(amount).encode())
    r.recvuntil(b"Your receipt: ")
    ctxt = r.recvline()
    r.recvuntil(b">")
    return ctxt