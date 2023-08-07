from flask import Flask, render_template

app = Flask(__name__)

app.route("/")
def index():
    return render_template("templates/index.html")

app.route("/xyz")
def harry():
    return "Hello World"

app.route("/about")
def about():
    name = "ME"
    return render_template("templates/about.html", name=name)
app.run(debug=True)
