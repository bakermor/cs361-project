from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# home page
@app.route("/")
def home():
    return render_template("HomePage.html")

@app.route("/player-data")
def player():
    return render_template("PlayerData.html")

if __name__ == "__main__":
    app.run(debug=True)
