import random

# Flag has to be multiple of 4 characters
flag = b"maple{1s_Th1s_53lf_Modify1ng_C0d3??}"
len = len(flag) // 4
print(len)

k = [random.randint(0, 2 ** 31) for _ in range(len)]
flag_arr = []

for i in range(0,len-1):
    a = int.from_bytes(flag[i*4:i*4+4], byteorder='little', signed=True)
    b = int.from_bytes(flag[i*4+4:i*4+8], byteorder='little', signed=True)
    print(flag[i*4:i*4+4], flag[i*4+4:i*4+8])
    c = (a ^ b) + k[i]
    flag_arr.append(c)
flag_arr.append(int.from_bytes(flag[-4:], byteorder='little', signed=True) + k[len-1])
print(flag_arr)
print(k)