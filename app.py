from flask import Flask, render_template, redirect, request
from mailjet_rest import Client
import os

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
        # Make sure all required data is submitted in form
        if not request.form.get("name"):
            return redirect("/")
        if not request.form.get("email"):
            return redirect("/")
        if not request.form.get("message"):
            return redirect("/")
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Store sensitive keys in environment and get them from there. Use this to set up sending the email with mailjet API.
        api_key = os.environ["MJ_API_KEY"]
        api_secret = os.environ["MJ_API_SEC"]
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # This is a dictionary of all the information that mailjet needs to send the email
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
                # Send email to user as well
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
        
        # Send email
        mailjet.send.create(data=data)

        # Variable to check when email is sent so message can be shown on users screen
        sent = True
    else:
        sent = False
    return render_template("contact.html", sent=sent)