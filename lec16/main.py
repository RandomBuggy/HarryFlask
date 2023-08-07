# to create database use phpmyadmin-frontend or the mysql-cli
import json
from datetime import datetime
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

with open("./templates/config.json", "r") as f:
    params = json.load(f)["params"]

app:Flask = Flask(__name__)
app.secret_key = "the-super-secret-key"
app.config.update(MAIL_SERVER="smtp.google.com", MAIL_PORT="465", MAIL_USE_SSL=True, MAIL_USERNAME=params["gmail-user"], MAIL_PASSWORD=params["gmail-password"])
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://user@pass:localhost/db_name"
if params["local_server"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]
db: SQLAlchemy = SQLAlchemy(app)
mail: Mail = Mail(app)

class Contacts(db.Model):
    # sno, name, phone_num, msg, date, email
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    # sno, title, slug, content, taglune, date, img_file
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(60), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    img_file = db.Column(db.String(12), nullable=False)

@app.route("/")
def index() -> str:
    posts = Posts.query.filter_by().all()[0:params["num-of-posts"]]
    return render_template("index.html", params=params, posts=posts)

@app.route("/post/<string:post_slug>", methods=["GET"])
def post(post_slug):
    posts = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", params=params, post=posts)

@app.route("/about")
def about() -> str:
    return render_template("about.html", params=params)

@app.route("/dashboard", methods["GET", "POST"])
def dashboard():
    if "user" in session and session["user"] == params["user-name"]:
        posts = Posts.query.all()
        return render_template("dashboard.html", params=params, posts=posts)
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("passwd")
        if username == params["user-name"] and password == params["user-password"]:
            session["user"] = username
            posts = Posts.query.all()
            return render_template("dashboard.html", params=params, posts=posts)
    else:
        return render_template("admin.html", params=params)

@app.route("/edit/<string:sno>", methods["GET", "POST"])
def edit(sno):
    if "user" in session and session["user"] == params["user-name"]:
        if request.method == "POST":
            box_title = request.form.get("title")
            tagline = request.form.get("tagline")
            slug = request.form.get("slug")
            content = request.form.get("content")
            img_file = request.form.get("img_file")

            if sno == "0":
                post = Posts(title=box_title, slug=slug, content=content, tagline=tagline, img_file=img_file, date=datetime.now())
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()

                post.title = box_title
                post.slug = slug
                post.content = content
                post.tagline = tagline
                post.img_file = img_file
                post.date = datetime.now()

                db.session.commit()
                return redirect("/edit/"+sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template("edit.html", params=params, post=post)

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

        mail.send_message(f"New message from {name}", sender=email, recipients=[params["gmail-user"]], body=f"{message}\n{phone}")

    return render_template("contact.html", posts=posts)

app.run(debug=True)
