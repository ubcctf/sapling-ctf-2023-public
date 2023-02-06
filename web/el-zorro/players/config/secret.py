import base64
import random
import string

def gen_admin():
    chars = string.ascii_lowercase
    res ="admin" + ''.join(random.choice(chars) for i in range(10))
    return res


def gen_secret(file):
    with open(file, "r") as f:
        # strip any newlines at end of file and b64 encode
        secret = base64.b64encode(f.read().encode().strip())
        # remove the 2 equal signs
        return secret.decode()[:-2]
