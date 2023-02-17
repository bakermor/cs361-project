from flask import Blueprint, render_template, redirect, url_for, request
import json
import requests
from player_data import *

single_player = Blueprint("single_player", __name__, static_folder="static", template_folder="templates")

TEAMS = ['Red Rabbits', 'Orange Ocelots', 'Yellow Yaks', 'Lime Llamas', 'Green Geckos', 'Cyan Coyotes', 'Aqua Axolotls',
         'Blue Bats', 'Purple Pandas', 'Pink Parrots']


@single_player.route("/player-data", methods=["POST","GET"])
def player():
    if request.method == "GET":
        return render_template("PlayerData.html", teamIcons=TEAMS)

    # Process Submitted Form
    if request.method == "POST":
        req_player = request.form["pname"]
        # Handles Random Inputs
        if req_player == 'RANDOM':
            response = requests.get("http://127.0.0.1:5001/player")
            req_player = response.json()[0]

        content = player_data(req_player)
        # Handles Invalid Requests
        if content == 'invalid':
            return render_template("PlayerData.html", error=req_player, teamIcons=TEAMS)

        return redirect(url_for("single_player.display_player", content=json.dumps(content)))


@single_player.route("/display/<content>")
def display_player(content):
    content = json.loads(content)
    data = []

    # Adds each game to data
    for key in content:
        if key != "Player" and key != "Overall":
            game = [key, int(content[key][1]), int(content[key][0])]
            data.append(game)

    overall = ["Overall", int(content["Overall"][1]), int(content["Overall"][0])]

    return render_template("DisplayPlayerData.html", player=content["Player"][0], games=data,
                           p_id="/images/"+str(content["Player"][1])+".png", overall=overall, teamIcons=TEAMS)