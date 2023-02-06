key = "SAPLINGBCDEFHJKMOQRTUVWXY"
key_map = [None] * 25
for row in range(5):
    for col in range(5):
        idx = ord(key[row * 5 + col]) - 0x41
        loc = row << 4
        loc = loc | col
        print(hex(loc))
        key_map[idx] = loc
print(key_map)

s = "VQVBNCSALQKMYIEMIO"
for c in s:
    print("\'{}\', ".format(c), end="")
    
s = "SAPLINGBCDEFHJKMOQRTUVWXY"
for i, c in enumerate(s):
    if(i % 5 == 0):
        print()
    print("\'{}\', ".format(c), end="")

#flag: WOWGDBISPRETTYNEAT
