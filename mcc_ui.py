from flask import Flask, redirect, url_for, render_template, request
import json
from compare_players import *
from run_event import *

app = Flask(__name__)

TEAMS = ['Red Rabbits', 'Orange Ocelots', 'Yellow Yaks', 'Lime Llamas', 'Green Geckos', 'Cyan Coyotes', 'Aqua Axolotls',
         'Blue Bats', 'Purple Pandas', 'Pink Parrots']

# Home Page
@app.route("/")
def home():
    return render_template("HomePage.html", teamIcons=TEAMS)

# Display Valid Players
@app.route("/valid")
def valid_players():
    return render_template("ValidPlayers.html", teamIcons=TEAMS)


# Player Data
@app.route("/player-data", methods=["POST","GET"])
def player():
    # Process form data
    if request.method == "POST":
        req_player = request.form["pname"]
        content = player_data(req_player)
        if content == 'invalid':
            return render_template("PlayerData.html", error=req_player, teamIcons=TEAMS)
        return redirect(url_for("display_player", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("PlayerData.html", teamIcons=TEAMS)

# Display Player Data
@app.route("/display/<content>")
def display_player(content):
    content = json.loads(content)

    data = []
    for key in content:
        if key != "Player" and key != "Overall":
            game = [key, int(content[key][1]), int(content[key][0])]
            data.append(game)
    overall = ["Overall", int(content["Overall"][1]), int(content["Overall"][0])]
    return render_template("DisplayPlayerData.html", player=content["Player"][0], games=data,
                           p_id="/images/"+str(content["Player"][1])+".png", overall=overall, teamIcons=TEAMS)


# Compare Players
@app.route("/compare-players", methods=["POST","GET"])
def compare_p():
    # Process form data
    if request.method == "POST":
        req_players = request.form.getlist('pname')
        content = compare_players(req_players)

        if content[0] == 'invalid':
            return render_template("DisplayCompareP.html", p_names=req_players, error=content[1], teamIcons=TEAMS)

        return redirect(url_for("display_players", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("ComparePlayers.html", count=2, teamIcons=TEAMS)

# Display Compare Players
@app.route("/display-p/<content>", methods=["POST", "GET"])
def display_players(content):
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
        game_lst.remove("Overall")

        return render_template("DisplayCompareP.html", p_names=p_names, imgs=img_paths, games=game_lst,
                               num_p=len(p_names), data=data, coins=0, teamIcons=TEAMS)


# Compare Teams
@app.route("/compare-teams", methods=["POST","GET"])
def compare_t():
    # Process form data
    if request.method == "POST":
        teams = request.form.getlist('teamName')
        p1 = request.form.getlist('p1')
        p2 = request.form.getlist('p2')
        p3 = request.form.getlist('p3')
        p4 = request.form.getlist('p4')

        req_teams = []
        for i in range(len(teams)):
            players = [p1[i], p2[i], p3[i], p4[i]]
            if "" not in players:
                teamDic = {'Team Name': teams[i], 'Players': players}
                req_teams.append(teamDic)
        content = compare_teams(req_teams)

        if content[0] == 'invalid':
             return render_template("CompareTeams.html", count=len(req_teams), teamName=teams, p1=p1, p2=p2, p3=p3,
                                    p4=p4, error=content[1], errorTeam=content[2], teamIcons=TEAMS)

        content.append({'Team':'edit', 'data': request.form})
        return redirect(url_for("display_teams", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("CompareTeams.html", count=2, teamIcons=TEAMS)

# Edit Compare Teams
@app.route("/edit-compare", methods=["POST", "GET"])
def edit_p():
    if request.method == "POST":
        teamName = request.form.getlist('teamName')
        p1 = request.form.getlist('p1')
        p2 = request.form.getlist('p2')
        p3 = request.form.getlist('p3')
        p4 = request.form.getlist('p4')
        return render_template("CompareTeams.html", count=len(teamName), teamName=teamName, p1=p1, p2=p2, p3=p3, p4=p4,
                               teamIcons=TEAMS)

# Display Compare Teams
@app.route("/display-t/<content>", methods=["POST", "GET"])
def display_teams(content):
    if request.method == "GET":
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
        game_lst.remove("Overall")

        return render_template("DisplayCompareT.html", t_names=t_names, p_names=p_names, imgs=img_paths, games=game_lst,
                               num_t=len(t_names), data=data, edit=edit, teamIcons=TEAMS)


# Simulate Event
@app.route("/event", methods=["POST","GET"])
def event_sim():
    # Process form data
    if request.method == "POST":
        game_lst = request.form.getlist('game')

        teams = ["Red Rabbits", "Orange Ocelots", "Yellow Yaks", "Lime Llamas", "Green Geckos", "Cyan Coyotes", "Aqua Axolotls", "Blue Bats", "Purple Pandas", "Pink Parrots"]
        p1 = request.form.getlist('p1')
        p2 = request.form.getlist('p2')
        p3 = request.form.getlist('p3')
        p4 = request.form.getlist('p4')
        # teams = [ { Team Name: Name, Players: [ P1, P2, P3, P4 ] } ]
        team_list = []
        for i in range(len(teams)):
            team_list.append({ 'Team Name': teams[i], 'Players': [p1[i], p2[i], p3[i], p4[i]]})

        content = run_event(team_list, game_lst)
        if 'Error' in content.keys():
            content = content['Error']
            return render_template("EditEventSim.html", teamNames=TEAMS, p1=p1, p2=p2, p3=p3, p4=p4, error=content[1],
                                   errorTeam=content[2], games=game_lst, teamIcons=TEAMS)
        return redirect(url_for("display_event", content=json.dumps(content)))

    # Load initial webpage
    else:
        return render_template("EventSim.html", teamIcons=TEAMS)

# Display Simulate Event
@app.route("/display-event/<content>")
def display_event(content):
    content = json.loads(content)
    games = content["Games"]
    teams = {}
    coins = content["Coins"]
    overall = content["Overall"]
    for team in content["Teams"]:
        p = content["Teams"][team]
        teams[team] = [p[0][0], p[1][0], p[2][0], p[3][0]]

    return render_template("DisplayEvent.html", games=games, teams=teams, coins=coins, overall=overall, teamIcons=TEAMS)

if __name__ == "__main__":
    app.run(debug=True)
