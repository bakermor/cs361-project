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
        content = compare_players(req_players)

        # TODO: redirect to page of valid player names if invalid
        if content[0] == 'invalid':
            pass

        return redirect(url_for("display_players", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("ComparePlayers.html", count=2)

# Compare Teams
@app.route("/compare-teams", methods=["POST","GET"])
def compare_t():
    # Process form data
    if request.method == "POST":
        teams = request.form.getlist('teamName')
        print(teams)
        p1 = request.form.getlist('p1')
        p2 = request.form.getlist('p2')
        p3 = request.form.getlist('p3')
        p4 = request.form.getlist('p4')

        req_teams = []
        if len(teams) == len(p1) and len(p1) == len(p2) and len(p1) == len(p3) and len(p1) == len(p4):
            for i in range(len(teams)):
                players = [p1[i], p2[i], p3[i], p4[i]]
                teamDic = {'Team Name': teams[i], 'Players': players}
                req_teams.append(teamDic)
        # TODO: handle incomplete requests
        else:
            pass

        content = compare_teams(req_teams)

        # TODO: redirect to page of valid player names if invalid
        if content[0] == 'invalid':
             pass
        print(request.form)
        content.append({'Team':'edit', 'data': request.form})
        return redirect(url_for("display_teams", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("CompareTeams.html", count=2)

@app.route("/edit-compare", methods=["POST", "GET"])
def edit_p():
    if request.method == "POST":
        print(request.form)
        teamName = request.form.getlist('teamName')
        p1 = request.form.getlist('p1')
        p2 = request.form.getlist('p2')
        p3 = request.form.getlist('p3')
        p4 = request.form.getlist('p4')
        return render_template("CompareTeams.html", count=len(teamName), teamName=teamName, p1=p1, p2=p2, p3=p3, p4=p4)

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
    return render_template("DisplayPlayerData.html", player=content["Player"][0], games=data, p_id="/images/"+str(content["Player"][1])+".png")

@app.route("/display-p/<content>", methods=["POST", "GET"])
def display_players(content):
    # TODO: Display Compare Player results
    if request.method == "POST":
        pass

    else:
        content = json.loads(content)

        p_names = []
        img_paths = []
        game_lst = set()
        data = {}

        for p in content:
            p_names.append(p["Player"][0])
            img_paths.append("/images/" + str(p["Player"][1]) + ".png")
            game_lst.update(p.keys())

            p_game = {}
            for key in p:
                if key != "Player":
                    p_game[key] = (int(p[key][0]), int(p[key][1]))
            data[p["Player"][0]] = p_game
        game_lst.remove("Player")

        return render_template("DisplayCompareP.html", p_names=p_names, imgs=img_paths, games=game_lst,
                               num_p=len(p_names), data=data, coins=0)

@app.route("/display-t/<content>", methods=["POST", "GET"])
def display_teams(content):
    # TODO: Display Compare Player results
    if request.method == "POST":
        pass

    else:
        content = json.loads(content)
        edit = ""
        for team in content:
            if team["Team"] == 'edit':
                edit = team["data"]
                content.remove(team)

        t_names = []
        p_names = []
        img_paths = []
        game_lst = set()
        data = {}

        for t in content:
            t_names.append(t["Team"])

            p_paths = ["/images/" + str(t["Team"]) + ".png"]
            for player in t["Players"]:
                p_names.append(player[0])
                p_paths.append("/images/"+str(player[1])+".png")

            img_paths.append(p_paths)
            game_lst.update(t.keys())

            t_game = {}
            for key in t:
                if key != "Team" and key != "Players":
                    t_game[key] = (int(t[key][0]), int(t[key][1]))
            data[t["Team"]] = t_game
        game_lst.remove("Team")
        game_lst.remove("Players")

        return render_template("DisplayCompareT.html", t_names=t_names, p_names=p_names, imgs=img_paths, games=game_lst,
                               num_t=len(t_names), data=data, edit=edit)

if __name__ == "__main__":
    app.run(debug=True)
