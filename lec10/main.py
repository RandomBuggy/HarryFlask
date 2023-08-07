# to create database use phpmyadmin-frontend or the mysql-cli
import json
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

with open("./templates/config.json", "r") as f:
    params = json.load(f)["params"]

app:Flask = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://user@pass:localhost/db_name"
if params["local_server"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]
db: SQLAlchemy = SQLAlchemy(app)

class Contacts(db.Model):
    # sno, name, phone_num, msg, date, email
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))
    email = db.Column(db.String(20), nullable=False)

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/about")
def about() -> str:
    return render_template("about.html")

@app.route("/contact", methods = ["GET", "POST"])
def contact() -> str:
    if request.method == "POST":
        name: str | None = request.form.get("name")
        email: str | None = request.form.get("email")
        phone: str | None = request.form.get("phone")
        message: str | None = request.form.get("message")

        entry: Contacts = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)

        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html")

app.run(debug=True)
