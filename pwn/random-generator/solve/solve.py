from pwn import *

exe = ELF("rand_gen")

context.binary = exe
context.log_level = 'DEBUG'

def start():
    if args.LOCAL:
        r = process([exe.path])
        if args.R2:
            util.proc.wait_for_debugger(util.proc.pidof(r)[0])
    else:
        r = remote("rua_host_goes_here", 1337)
    return r


io = start()
io.sendlineafter(b"How many random number you want: \n",b"32")
io.recvuntil(b"here is your random values\n")
values = [int(x) for x in io.recvuntil("\n",drop=True).decode().split(" ") if x !=""]
for i in range(256):
    print(i,":","".join(map(lambda x:chr(x^i),values)))
