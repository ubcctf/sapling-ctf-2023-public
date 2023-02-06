def deserialize_int(stream):
    size = stream.read(1)[0]
    val = 0
    for i in range(size):
        val |= ((stream.read(1)[0] & 0b01111111) << i * 7)
    return val


ptrs = []
mapping = []

with open('flag.bin', 'rb') as f:
    while b:=f.peek(1)[0]:  #read until the null byte that signifies the start of the mapping
        ptrs.append(deserialize_int(f))

    f.read(1)  #discard the null byte

    while f.peek(1):
        size = deserialize_int(f)
        b = f.read(size)
        mapping.append(b.decode())

#map to decompressed text
out = ''
for ptr in ptrs:
    out += mapping[ptr]

print(out)