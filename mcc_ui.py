from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# home page
@app.route("/")
def home():
    return render_template("HomePage.html")

@app.route("/player-data")
def player():
    return render_template("PlayerData.html")

@app.route("/compare-players")
def compare_p():
    return render_template("ComparePlayers.html")

@app.route("/compare-teams")
def compare_t():
    return render_template("CompareTeams.html")

@app.route("/event")
def event_sim():
    return render_template("EventSim.html")

if __name__ == "__main__":
    app.run(debug=True)
