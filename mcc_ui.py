from flask import Flask, redirect, url_for, render_template, request
import json
from compare_players import *
from compare_teams import *

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("HomePage.html")

# Player Data
@app.route("/player-data", methods=["POST","GET"])
def player():
    # Process form data
    if request.method == "POST":
        req_player = request.form["pname"]
        content = player_data(req_player)
        # TODO: redirect to page of valid player names if invalid
        if content == 'invalid':
            pass
        content['Type'] = 'player'
        return redirect(url_for("display", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("PlayerData.html")

# Compare Players
@app.route("/compare-players", methods=["POST","GET"])
def compare_p():
    # Process form data
    if request.method == "POST":
        req_players = request.form.getlist('pname')
        content = compare_players(req_players)
        # TODO: redirect to page of valid player names if invalid
        if content[0] == 'invalid':
            pass
        content['Type'] = 'players'
        return redirect(url_for("display", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("ComparePlayers.html", count=2)

# Compare Teams
@app.route("/compare-teams", methods=["POST","GET"])
def compare_t():
    # Process form data
    if request.method == "POST":
        pass

    # Load initial webpage
    else:
        return render_template("CompareTeams.html")

# Simulate Event
@app.route("/event", methods=["POST","GET"])
def event_sim():
    # Process form data
    if request.method == "POST":
        pass

    # Load initial webpage
    else:
        return render_template("EventSim.html")

# Display Valid Players
@app.route("/valid")
def valid_players():
    return render_template("ValidPlayers.html")

# Display Data
@app.route("/display/<content>")
def display(content):
    content = json.loads(content)

    # Display Player Data results
    if content["Type"] == "player":
        data = []
        for key in content:
            if key != "Type" and key != "Player":
                game = [key, int(content[key][1]), int(content[key][0])]
                data.append(game)
        print(data)
        return render_template("DisplayPlayerData.html", player=content["Player"][0], games=data, p_id="/images/"+str(content["Player"][1])+".png")

    # TODO: Display Compare Player results
    if content["Type"] == "players":
        pass

if __name__ == "__main__":
    app.run(debug=True)
