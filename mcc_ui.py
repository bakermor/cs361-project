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
        return redirect(url_for("display_player", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("PlayerData.html")

# Compare Players
@app.route("/compare-players", methods=["POST","GET"])
def compare_p():
    # Process form data
    if request.method == "POST":
        req_players = request.form.getlist('pname')
        print(req_players)
        content = compare_players(req_players)
        # TODO: redirect to page of valid player names if invalid
        print(content)
        if content[0] == 'invalid':
            pass
        # if "coins" in request.form.keys():
        #     content.append({"coins": request.form["coins"]})
        # else:
        #     content.append({"coins": 0})

        return redirect(url_for("display_players", content=json.dumps(content)))

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
def display_player(content):
    content = json.loads(content)

    # Display Player Data results
    data = []
    for key in content:
        if key != "Player":
            game = [key, int(content[key][1]), int(content[key][0])]
            data.append(game)
    print(data)
    return render_template("DisplayPlayerData.html", player=content["Player"][0], games=data, p_id="/images/"+str(content["Player"][1])+".png")

@app.route("/display-p/<content>", methods=["POST", "GET"])
def display_players(content):
    # TODO: Display Compare Player results
    if request.method == "POST":
    #     print(request.form)
    #     p_names = json.loads(request.form["p_names"])
    #     img_paths = json.loads(request.form["imgs"])
    #     game_lst = json.loads(request.form["games"])
    #     data = json.loads(request.form["data"])
    #     coins = request.form["coins"]
    #     print(data)
    #     print(p_names)
    #     print(game_lst)
    #
    #     return render_template("DisplayCompareP.html", p_names=p_names, imgs=img_paths, games=game_lst, num_p=len(p_names),
    #                            data=data, coins=coins)
        pass

    else:
        content = json.loads(content)

        p_names = []
        img_paths = []
        game_lst = set()
        data = {}

        for p in content:
            p_names.append(p["Player"][0])
            img_paths.append("/images/"+str(p["Player"][1])+".png")
            game_lst.update(p.keys())

            p_game = {}
            for key in p:
                if key != "Player":
                    p_game[key] = (int(p[key][0]), int(p[key][1]))
            data[p["Player"][0]] = p_game
        game_lst.remove("Player")

        return render_template("DisplayCompareP.html", p_names=p_names, imgs=img_paths, games=game_lst, num_p=len(p_names), data=data, coins=0)


if __name__ == "__main__":
    app.run(debug=True)
