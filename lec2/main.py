from flask import Flask

app = Flask(__name__)

app.route("/")
def hello():
    return "Hello World"

app.route("/xyz")
def xyz():
    return "The /xyz Route"

# app.run(debug=True)
app.run()
