from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# home page
@app.route("/<name>")
def home(name):
    l1 = ["tim", "joe", "bill"]
    return render_template("example.html", content=name, r=2, list1=l1)

if __name__ == "__main__":
    app.run()