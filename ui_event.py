from flask import Blueprint, render_template, redirect, url_for, request
import json
import requests
from run_event import *

event = Blueprint("event", __name__, static_folder="static", template_folder="templates")

TEAMS = ['Red Rabbits', 'Orange Ocelots', 'Yellow Yaks', 'Lime Llamas', 'Green Geckos',
         'Cyan Coyotes', 'Aqua Axolotls', 'Blue Bats', 'Purple Pandas', 'Pink Parrots']


@event.route("/event", methods=["POST","GET"])
def event_sim():
    if request.method == "GET":
        return render_template("EventSim.html", teamIcons=TEAMS)

    # Process Form Data
    if request.method == "POST":
        games = request.form.getlist('game')
        game_lst = get_game_list(games)

        players = [request.form.getlist('p1'), request.form.getlist('p2'), request.form.getlist('p3'),
                   request.form.getlist('p4')]

        team_list = get_team_list(players)

        content = run_event(team_list, game_lst)
        # Handles Invalid Requests
        if 'Error' in content.keys():
            content = content['Error']
            return render_template("EditEventSim.html", p1=players[0], p2=players[1], p3=players[2],
                                   p4=players[3], error=content[1], errorTeam=content[2], games=game_lst,
                                   teamIcons=TEAMS)

        return redirect(url_for("event.display_event", content=json.dumps(content)))

def get_game_list(game_lst):
    for i in range(len(game_lst)):
        # Handles Random Requests
        while game_lst[i] == 'RANDOM':
            response = requests.get("http://127.0.0.1:5001/game")
            if response.json()[0] not in game_lst:
                game_lst[i] = response.json()[0]
    return game_lst

def get_team_list(players):
    team_list = []
    for i in range(10):
        add_players = [players[0][i], players[1][i], players[2][i], players[3][i]]
        # Handles Random Requests
        for j in range(4):
            if add_players[j] == 'RANDOM':
                response = requests.get("http://127.0.0.1:5001/player")
                add_players[j] = response.json()[0]

        team_list.append({'Team Name': TEAMS[i], 'Players': add_players})
    return team_list


@event.route("/display-event/<content>")
def display_event(content):
    content = json.loads(content)

    teams = {}
    for team in content["Teams"]:
        p = content["Teams"][team]
        teams[team] = [p[0][0], p[1][0], p[2][0], p[3][0]]

    return render_template("DisplayEvent.html", games=content["Games"], teams=teams,
                           coins=content["Coins"], overall=content["Overall"], teamIcons=TEAMS)