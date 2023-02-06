from pwn import *
from sympy.ntheory import discrete_log

def nn_ints(data):
    results = re.findall(r'\d+', data.decode())
    return list(map(int, results))

r = remote('localhost', 1337, level="DEBUG")

r.recvuntil("1. ")
x, modulo = nn_ints(r.recvuntil(">>> "))
r.sendline(str(x % modulo))

r.recvuntil("2. ")
x, modulo = nn_ints(r.recvuntil(">>> "))
r.sendline(str(x % modulo))

r.recvuntil("3. ")
x, y = nn_ints(r.recvuntil(">>> "))
r.sendline(str(x ** y))

r.recvuntil("4. ")
x, y, modulo = nn_ints(r.recvuntil(">>> "))
r.sendline(str(pow(x, y, modulo)))

r.recvuntil("5. ")
x, y, modulo = nn_ints(r.recvuntil(">>> "))
r.sendline(str(pow(x, y, modulo)))

r.recvuntil("6. ")
x, result, modulo = nn_ints(r.recvuntil(">>> "))
r.sendline(str(discrete_log(modulo, result, x)))

r.recvuntil("7. ")
x, result, modulo = nn_ints(r.recvuntil(">>> "))
r.sendline(str(discrete_log(modulo, result, x)))

print(r.recv())