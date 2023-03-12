from flask import Blueprint, render_template, redirect, url_for, request
import json
import requests
from compare_players import *

multiple_players = Blueprint("multiple_players", __name__, static_folder="static", template_folder="templates")

TEAMS = ['Red Rabbits', 'Orange Ocelots', 'Yellow Yaks', 'Lime Llamas', 'Green Geckos',
         'Cyan Coyotes', 'Aqua Axolotls', 'Blue Bats', 'Purple Pandas', 'Pink Parrots']


@multiple_players.route("/compare-players", methods=["POST","GET"])
def compare_p():
    if request.method == "GET":
        return render_template("ComparePlayers.html", count=2, teamIcons=TEAMS)

    # Process Form Data
    if request.method == "POST":
        req_players = request.form.getlist('pname')
        # Handles Random Requests
        for i in range(len(req_players)):
            if req_players[i] == "RANDOM":
                response = requests.get("http://127.0.0.1:5001/player")
                req_players[i] = response.json()[0]

        content = compare_players(req_players)
        # Handles Invalid Requests
        if content[0] == 'invalid':
            return render_template("DisplayCompareP.html", p_names=req_players, error=content[1],
                                   teamIcons=TEAMS, num_p = len(req_players))

        return redirect(url_for("multiple_players.display_players", content=json.dumps(content)))


# Display Compare Players
@multiple_players.route("/display-p/<content>", methods=["POST", "GET"])
def display_players(content):
    if request.method == "POST":
        pass

    else:
        p_names, img_paths = [], []
        game_lst = set()
        data = {}

        content = json.loads(content)
        for p in content:
            p_names.append(p["Player"][0])
            img_paths.append("/images/" + str(p["Player"][1]) + ".png")
            game_lst.update(p.keys())

            # data[Player Name] = {Game : Coins,Placement, ...} for each game played
            p_game = {}
            for key in p:
                if key != "Player":
                    p_game[key] = (int(p[key][0]), int(p[key][1]))
            data[p["Player"][0]] = p_game

        game_lst.remove("Player")
        game_lst.remove("Overall")

        return render_template("DisplayCompareP.html", p_names=p_names, imgs=img_paths, games=game_lst,
                               num_p=len(p_names), data=data, coins=0, teamIcons=TEAMS)
