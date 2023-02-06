from flask import Flask, request, render_template_string, make_response
import os
app = Flask(__name__)




@app.route('/')
def index():
    if str(request.user_agent).startswith('curl'):
        message = "Hello! You're using curl! Awesome. Let's navigate curl's cool features together, okay?\n\n visit my endpoint at /one!"
        return render_template_string(message)
    else:
        return render_template_string("you need to curl! >:(")


@app.route('/one')
def one():
    if str(request.user_agent).startswith('curl'):
        if request.args.get("anime") == None:
            message="""Hello and welcome to /one :) I'm looking for a query parameter called 'name' - if you don't know what query params are, I reccommend checking out https://branch.io/glossary/query-parameters/\n\nGive me an 'anime' query parameter on this endpoint here, with the name of Tatsuki Fujimoto's magnum opus anime (2 words).\n"""
            return render_template_string(message)
        elif request.args.get('anime').lower() == "chainsaw man":
            message="""I AGREE! Chainsaw Man is a fantastic anime. Great! You're ready to go the second endpoint. See you over at /sad92jd8s98eud3o0sd0 !\n"""
            return render_template_string(message)
        else:
            message="""Hmm... try again!\n"""
            return render_template_string(message)
    else:
        return render_template_string("you need to curl! >:(")

@app.route('/sad92jd8s98eud3o0sd0', methods = ["POST", "GET"])
def two():
    if str(request.user_agent).startswith('curl'):
        if request.method == 'GET':
            message = """Hello and welcome to /sad92jd8s98eud3o0sd0!\nNow we're going to deal with POST requests done in curl. These are just regular HTTP requests carrying some data. You may need to check out the 'man' page for curl - if you have a linux OS (MAC OS, linux, or Windows WSL) you may be able to get the manual for curl by typing 'man curl' to grab it from the command line.\n\nIf not, that's fine - google is always there for you :) Check out https://curl.se/docs/manpage.html#-d as a start!\nWhen you're ready, make another curl request to this endpoint again, but I want a request body with the name "anime" and the value of it being Gege Akutami's magnum opus anime (2 words).\n"""
            return render_template_string(message)
        if request.method == "POST":
            if str(request.form.get("anime")).lower() == "jujutsu kaisen" and request.args.get("anime") == None:
                message = """THAT'S CORRECT! Jujutsu Kaisen is a very good anime. \n\nYou're starting to get the basics of curl down! We're almost done, you'll get your flag soon. See you at /xci893hr8fseifhu93nf83 !\n"""
                return render_template_string(message)
            else:
                message = "Hmm... Not quite right! Try again :)"
                return render_template_string(message)
    else:
        return render_template_string("you need to curl! >:(")


@app.route('/xci893hr8fseifhu93nf83', methods = ["POST", "GET"])
def three():
    if str(request.user_agent).startswith('curl'):
        if request.headers.get('X-Curl-Creator') == None:
            message = """Hello and welcome to /xci893hr8fseifhu93nf83! You're almost done. Now, we're going to do a quick dive into headers in curl. You can specify standard headers (content-type, content-length, etc) and custom headers with a very simple option in curl. Try and get it yourself ;) as always, a great resource is https://curl.se/docs/manpage.html \n\n I'm looking for a header called "X-Curl-Creator" with the value being the original author of curl (firstname lastname).\n\n"""
            return render_template_string(message)
        if request.headers.get('X-Curl-Creator').lower() == "daniel stenberg":
            message = "YOU GOT IT! Did you know that he was a recipient of the Polhem Prize in 2017 for his work on curl? Also, the correct nomenclature of curl is actually cURL which stands for 'Client URL'.\n\n The flag is in a custom header sent in this response. Can you get it? :)!"
            resp = make_response(render_template_string(message))
            resp.headers["X-Flag"] = os.environ.get("FLAG")
            return resp
        else:
            message = """Hmm, that's not quite correct!\n\n"""
            return render_template_string(message)
    else: 
        return render_template_string("you need to curl! >:(")