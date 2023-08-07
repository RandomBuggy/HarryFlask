# to create database use phpmyadmin-frontend or the mysql-cli
from flask import Flask, render_template

app:Flask = Flask(__name__)

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/about")
def about() -> str:
    return render_template("about.html")

@app.route("/contact")
def contact() -> str:
    return render_template("contact.html")

app.run(debug=True)
