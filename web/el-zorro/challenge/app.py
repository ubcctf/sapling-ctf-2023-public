from flask import Flask, request, session, render_template, redirect
import os
from config.secret import gen_secret, gen_admin

app = Flask(__name__)
app.config['SECRET_KEY'] = gen_secret(os.environ.get("SECRET_KEY_FILE"))
app.config['DEBUG'] = False
os.environ["ADMIN"] = gen_admin()

@app.route('/')
def index():
    if not session.get("name"):
        return redirect("/signin")
    return render_template("index.html")

@app.route('/signin', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if len(request.form.get("fox")) > 35 or len(request.form.get("name")) > 15:
            return render_template("error.html", error="Name or fox name too long.")
        if request.form.get("name") in os.environ.get("ADMIN"):
            return render_template("error.html", error="Invalid name!")
        if "." in request.form.get("fox"):
            return render_template("error.html", error="Invalid fox!")
        session["name"] = request.form.get("name")
        session["fox"] = request.form.get("fox")
        return redirect("/")
    return render_template("login.html")


@app.route('/fox')
def governmentAssignedFox():
    if not session.get("name"):
        return redirect("/signin")
    user = session["name"]
    fox = session['fox']
    fox_img = os.path.join("static", "images", fox + ".gif")
    try:
        with open(os.path.join("assets", "fox_descs", fox), "r") as f:
            fox_desc = f.read(100)
            if fox_desc.startswith("FLAG"):
                if session["name"] == os.environ.get("ADMIN"):
                    flag = open("/flag_la_volpe", "r")
                    return flag
                else:
                    return render_template("error.html", error="You can't read that :>")
            return render_template("fox.html", image=fox_img, description=fox_desc, name=user)
    except FileNotFoundError:
        return render_template("error.html", error="Unable to find fox description file.")
    except PermissionError:
        return render_template("error.html", error="You dont have access.")


@app.route('/changefox', methods = ["POST", "GET"])
def changeFox():
    if not session.get("name"):
        return redirect("/signin")
    if request.method == "POST":
        session["fox"] = request.form.get("fox")
        return redirect("/fox")
    else:
        return render_template("change.html")

@app.route('/signout')
def logout():
    session["name"] = None
    session["fox"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8080)