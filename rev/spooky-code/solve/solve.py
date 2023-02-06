with open('./spooky', 'rb') as f:
    b = f.read()
    flag = [b[0x1062]]    #first chunk stores the flag char in a different location
    flag += list(b[0x1080:0x17AC:0x20])  #data array from ELF, only extracting every 0x20 byte starting from the next chunk (all other characters are useless)

    for i, c in enumerate(flag[1:]):
        flag[i+1] = c ^ flag[i]

    print(bytes(flag).decode())