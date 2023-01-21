from flask import Flask, redirect, url_for

app = Flask(__name__)

# home page
@app.route("/")
def home():
    return "Hello! main page <h1>HELLO<h1>"

# user page
@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

# redirect user url_for("name of function")
@app.route("/admin")
def admin():
    return redirect(url_for("home"))

# redirect to specific url
@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
    app.run()