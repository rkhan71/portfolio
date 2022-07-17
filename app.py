from flask import Flask, render_template, redirect, request
from mailjet_rest import Client

app = Flask(__name__)

# configure app, mostly stuff for mail
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not request.form.get("name"):
            return redirect("/")
        if not request.form.get("email"):
            return redirect("/")
        if not request.form.get("message"):
            return redirect("/")
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        api_key = '3c7cbcf70fe0f8cc6f9b43fedb4c9502'
        api_secret = 'f5da1f9005ddd5165317ef7a6f3d6478'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "portfoliobot1@gmail.com",
                "Name": "Portfolio"
            },
            "To": [
                {
                "Email": "portfoliobot1@gmail.com",
                "Name": "Portfolio"
                },
                {
                    "Email": "rayan.ahkhan@gmail.com",
                    "Name": "Rayan"
                },
                {
                    "Email": email,
                    "Name": name
                }
            ],
            "Subject": "Subject",
            "TextPart": message
            }
        ]
        }
        mailjet.send.create(data=data)
        sent = True
    else:
        sent = False
    return render_template("contact.html", sent=sent)