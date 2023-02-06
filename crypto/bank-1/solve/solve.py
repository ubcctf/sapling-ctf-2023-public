from pwn import *

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

def purchase_flag():
    r.sendline("3")
    r.interactive()

pin = ""
length = 12
for i in range(6):
    # request money like: '1|111111111111|????|50'
    # the transaction will split into the blocks:
    # '1|111111111111|?' and '???|50....'
    expected_block = request_money(int('1' * (length - i)))[:16]

    # now, we can brute force that last digit in the first block ('1|111111111111|?')
    for guess in range(10):
        pin_guess = (pin + str(guess)).ljust(4, '0')
        block = send_money(0, int('1' * (length - i)), pin_guess, 1)[:16]
        
        # if we have the same first block, then we've found the pin
        if block == expected_block:
            pin += str(guess)
            break

        print(block, expected_block)

pin = int(pin)
# assert pin == challenge.ADMIN_PIN

send_money(0, 1, pin, 100_000)
purchase_flag()
