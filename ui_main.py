from flask import Flask, redirect, url_for, render_template, request
import requests
import json
from run_event import *
from ui_single_player import single_player
from ui_multiple_players import multiple_players
from ui_multiple_teams import multiple_teams

app = Flask(__name__)
app.register_blueprint(single_player, url_prefix="")
app.register_blueprint(multiple_players, url_prefix="")
app.register_blueprint(multiple_teams, url_prefix="")

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

# Simulate Event
@app.route("/event", methods=["POST","GET"])
def event_sim():
    # Process form data
    if request.method == "POST":
        game_lst = request.form.getlist('game')

        for i in range(len(game_lst)):
            while game_lst[i] == 'RANDOM':
                response = requests.get("http://127.0.0.1:5001/game")
                if response.json()[0] not in game_lst:
                    game_lst[i] = response.json()[0]

        teams = ["Red Rabbits", "Orange Ocelots", "Yellow Yaks", "Lime Llamas", "Green Geckos", "Cyan Coyotes", "Aqua Axolotls", "Blue Bats", "Purple Pandas", "Pink Parrots"]
        p1 = request.form.getlist('p1')
        p2 = request.form.getlist('p2')
        p3 = request.form.getlist('p3')
        p4 = request.form.getlist('p4')
        # teams = [ { Team Name: Name, Players: [ P1, P2, P3, P4 ] } ]
        team_list = []
        for i in range(len(teams)):
            add_players = [p1[i], p2[i], p3[i], p4[i]]

            for j in range(4):
                if add_players[j] == 'RANDOM':
                    response = requests.get("http://127.0.0.1:5001/player")
                    add_players[j] = response.json()[0]

            team_list.append({ 'Team Name': teams[i], 'Players': add_players})

        content = run_event(team_list, game_lst)
        if 'Error' in content.keys():
            content = content['Error']
            return render_template("EditEventSim.html", p1=p1, p2=p2, p3=p3, p4=p4, error=content[1],
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
