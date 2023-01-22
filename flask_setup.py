from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

# home page
@app.route("/")
def home(name):
    l1 = ["tim", "joe", "bill"]
    return render_template("example.html", content=name, r=2, list1=l1)

@app.route("/login", methods=["POST","GET"])
def form_example():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("example2.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run()