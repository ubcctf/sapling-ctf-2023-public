# El Zorro

Use `os.path.join` quirk to LFI any file you want, but the read function in `app.py` restricts the content you see to only 100 bytes - which isn't much.

```py
with open(os.path.join("assets", "fox_descs", fox), "r") as f:
    fox_desc = f.read(100)
```

You also can't add a period in your fox value so you can't open alot of files. However, you can look at how Flask sessions are signed in `config/secret.py`:

```py
import base64

def gen_secret(file):
    with open(file, "r") as f:
        secret = base64.b64encode(f.read().encode())
        #Remove the 2 equal signs
        return secret.decode()[:-2]

```

The program opens a file, base64-encodes the result, and it becomes the app's secret key used to sign cookies:

```py
# The secret key used for my signed cookies!
app.secret_key = gen_secret("/proc/sys/kernel/random/boot_id")
Session(app)
```
If we open that file then we can get the value of the secret key ourselves, b64 encode it ourselves, and sign our own sessional cookies. This is important as Flask uses python's pickle module to serialize the cookie, which is vulnerable to RCE. Grab the secret key, forge your own RCE cookie, and open the flag yourself.
