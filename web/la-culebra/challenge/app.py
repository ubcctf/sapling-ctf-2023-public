from flask import Flask, request, render_template_string, render_template, redirect
import redis
import base64
import os
app = Flask(__name__)

red = redis.Redis(host="localhost", port=6379)
with open("flag.txt", "r") as f:
    red.set("flag", f.readline())
os.remove("flag.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getsnakefact/<snake>')
def getsnake(snake):
    if snake == "flag":
        return redirect('/')
    red = redis.Redis(host="localhost", port=6379)
    try:
        desc = base64.b64decode(red.get(snake)).decode()
    except Exception:
        print(Exception)
        desc = "Error retrieving snake fact"
    if desc.startswith('maple{'):
        return redirect('/')
    return render_template_string(desc)

@app.route('/newsnakefact', methods = ["POST"])
def setsnake():
    if request.method == "POST":
        if request.json["snake"] == "flag":
            return redirect('/')
        red = redis.Redis(host="localhost", port=6379)
        desc = base64.b64encode(request.json["description"].encode())
        red.set(request.json["snake"], desc)
        return redirect('/')