import string
import random

charset = string.ascii_lowercase
flag = "maple{trigrams_and_patterns_galore!}"

N = 3
mappings = [list(charset) for _ in range(N)]

for i in range(N):
    random.shuffle(mappings[i])

text = open("text.txt").read()

parts = text.split(" ")
inserted = parts[:300] + [flag] + parts[300:]
text = " ".join(inserted)

first = True
out = ""
for i,char in enumerate(text):
    mapping = mappings[i % N]
    if char in string.ascii_uppercase:
        char = char.lower()
    
    if char == "\"":
        char = "'"
    if char == "\n":
        char = " "

    if char in charset:
        out += mapping[charset.index(char)]
    else:
        out += char

# print(out)
with open("enc.txt", "w") as f:
    f.write(out)

print("solution")
for i in range(N):
    print(f"mapping {i}")
    for a,b in zip(charset, mappings[i]):
        print(f"{a} -> {b}")