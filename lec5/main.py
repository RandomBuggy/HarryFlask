from flask import Flask, render_template

app: Flask = Flask(__name__)

@app.route("/")
def index() -> str:
    return render_template("index.html")

app.run(debug=True)
