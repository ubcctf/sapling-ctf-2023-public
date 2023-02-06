import json
import asyncio
import websockets

charset = "abcdefghijklmnopqrstuvwxyz0123456789._:) "

# scuffy script lol
# dist gives you info on whether you're one char closer to the flag or not
# use this to incrementally construct flag (i did it starting from the end of the flag)

async def main():
    # target_url = "ws://localhost:1337"
    target_url = "ws://hintbot.ctf.maplebacon.org"
    async with websockets.connect(target_url) as client:
        for length in range(60, 20, -1):
            supposed_answer = "maple " + "X" * length
            idx = len(supposed_answer) - 1
            res = await test_answer(client, supposed_answer, idx)

async def test_answer(client, ans, idx):
    new_ans = await brute_char(client, ans, idx)
    if new_ans is None:
        print(ans) # fleg
        return None
    res = []
    for a in new_ans:
        r_res = await test_answer(client, a, idx - 1)
        if r_res is not None:
            res.extend(r_res)
    return res
        
async def brute_char(client, ans, idx):
    seen = {}
    for c in charset:
        msg = ans[:idx] + c + ans[idx + 1:]
        await client.send(json.dumps({"msg": msg, "debug": True}))
        resp = await client.recv()
        resp = json.loads(resp)
        if "dist" not in resp:
            return None # too close to the answer
        key = resp["dist"]
        if key not in seen:
            seen[key] = []
        seen[key].append(c)
    minkey = min(seen.keys())
    if len(seen.keys()) == 1:
        return None
    correct_chars = seen[minkey]
    correct_answers = [ans[:idx] + c + ans[idx + 1:] for c in correct_chars]
    return correct_answers


if __name__ == '__main__':
    asyncio.run(main())
