from Crypto.Cipher import AES 

messages = [
    "hey did you get the message, the funds have been transferred to the bank",
    "okey got it boss",
    "ok ill meet you there then",
    "wait boss?",
    "don't ask questions here, even if we're encrypting our messages, we should only talk about details when in person",
    "oh ok boss ill ask you when we get there then",
    "good",
    "we're meeting at the maple{5upeR_5ECReT_ExCh4nGE} right?",
    "oh my god what part of 'only talk about details in person' do you not understand??"]

key = "1666b7e028d54f193895dbc3bddba88a"
c = AES.new(bytes.fromhex(key), AES.MODE_ECB)

def pad(msg):
    bytes_of_padding = (16 - len(msg)) % 16
    pad_bytes = bytes([bytes_of_padding]) 
    return msg + pad_bytes * bytes_of_padding

def blockify(msg):
    blocks = []
    for i in range(0,len(msg),16):
        blocks.append(msg[i:i+16])
    return blocks

for m in messages:
    ms = blockify(m)
    res = ""
    for b in ms:
        res += c.encrypt(pad(b.encode())).hex()
    print("> ", res)


# setting up AES
# include an image of a hex encoded aes key with the last byte smudged out
# instruct people to decrypt the messages

# - they have to split the messages into 16 byte chunks
# - they have to guess the last byte to make a 16 byte key
