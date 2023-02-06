import ctypes

# The main trick of this challenge is to realize that the binary is self-modifying.
# From there, you can proceed in two ways: break in the init() function and dump the
# loaded main() function from memory there, or manually decrypt the program.

s2 = [ctypes.c_int(int.from_bytes(bytes.fromhex(i), byteorder='little')).value for i in """
F7AC6980 07B75773 6EE61518 9C49F0C4
96189D91 A60A4E61 5854673D 1CC8C071
6C6E7293
""".replace('\n', ' ').strip().split(' ')][::-1]

v7 = [ctypes.c_int(int.from_bytes(bytes.fromhex(i), byteorder='little')).value for i in """
EF922861 CD87FE30 42DBB815 7D108646
93166766 90B54660 32E2083A B04BB158
392F3316
""".replace('\n', ' ').strip().split(' ')][::-1]

print(s2)

s2[0] = s2[0] - v7[0]
for i, f in enumerate(s2[1:]):
    s2[i+1] = (f - v7[i+1]) ^ s2[i]

print(b''.join([ctypes.c_uint(f).value.to_bytes(4, byteorder='little') for f in s2][::-1]))
