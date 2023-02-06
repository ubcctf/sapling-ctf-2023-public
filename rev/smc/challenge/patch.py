start = 0xaba
end = 0xd0e

key = [146, 77, 249, 203, 246, 182, 174, 118, 220, 101, 43, 32, 141, 93, 159, 234, 31, 120, 117, 82, 25, 91, 176, 79, 143, 42, 38, 20, 186, 55, 246, 167]

with open("smc_orig", "rb") as orig:
    elf = bytearray(orig.read())
    data = elf[start:end]
    print(len(data))
    enc = b""
    for i, byte in enumerate(data):
        new_byte = byte ^ (key[i % len(key)])
        enc += (new_byte.to_bytes(1, 'little'))
    with open("smc", "wb") as new_elf:
        for i in range(start,end):
            elf[i] = enc[i-start]
        new_elf.write(elf)