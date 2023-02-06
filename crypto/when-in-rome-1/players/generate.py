import string
import random

charset = string.ascii_lowercase
flag = "maple{simple_substitute}"

mapping = list(charset)
random.shuffle(mapping)

text = f"""There was only one catch and that was Catch-22, which specified that a concern for one's own safety in the face of dangers that were real and immediate was the process of a rational mind. Orr was crazy and could be grounded. All he had to do was ask; and as soon as he did, he would no longer be crazy and would have to fly more missions. Orr would be crazy to fly more missions and sane if he didn't, but if he was sane, he had to fly them. If he flew them, he was crazy and didn't have to; but if he didn't want to, he was sane and had to. Yossarian was moved very deeply by the absolute simplicity of this clause of {flag} and let out a respectful whistle."""

first = True
out = ""
for char in text:
    if char in string.ascii_uppercase:
        char = char.lower()
    if char in charset:
        out += mapping[charset.index(char)]
    else:
        out += char

print(out)

print("solution")
for a,b in zip(charset, mapping):
    print(f"{a} -> {b}")