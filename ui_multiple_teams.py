from flask import Blueprint, render_template, redirect, url_for, request
import json
import requests
from compare_teams import *

multiple_teams = Blueprint("multiple_teams", __name__, static_folder="static", template_folder="templates")

TEAMS = ['Red Rabbits', 'Orange Ocelots', 'Yellow Yaks', 'Lime Llamas', 'Green Geckos', 'Cyan Coyotes', 'Aqua Axolotls',
         'Blue Bats', 'Purple Pandas', 'Pink Parrots']


@multiple_teams.route("/compare-teams", methods=["POST","GET"])
def compare_t():
    if request.method == "GET":
        return render_template("CompareTeams.html", count=2, teamIcons=TEAMS)

    # Process Form Data
    if request.method == "POST":
        teams = request.form.getlist('teamName')
        players = [request.form.getlist('p1'), request.form.getlist('p2'), request.form.getlist('p3'),
                       request.form.getlist('p4')]

        req_teams = get_content(teams, players)
        content = compare_teams(req_teams)

        # Handles Invalid Requests
        if content[0] == 'invalid':
             return render_template("CompareTeams.html", count=len(req_teams), teamName=teams, p1=players[0],
                                    p2=players[1], p3=players[2], p4=players[3], error=content[1],
                                    errorTeam=content[2], teamIcons=TEAMS)

        return redirect(url_for("multiple_teams.display_teams", content=json.dumps(content)))

def get_content(teams, p):
    req_teams = []
    for i in range(len(teams)):
        team_players = [p[0][i], p[1][i], p[2][i], p[3][i]]

        # Handles Random Requests
        for j in range(4):
            if team_players[j] == "RANDOM":
                response = requests.get("http://127.0.0.1:5001/player")
                team_players[j] = response.json()[0]

        # Handles Incomplete Requests
        if "" not in team_players:
            teamDic = {'Team Name': teams[i], 'Players': team_players}
            req_teams.append(teamDic)
    return req_teams


@multiple_teams.route("/edit-compare", methods=["POST", "GET"])
def edit_p():
    if request.method == "POST":
        teamName = request.form.getlist('teamName')
        players = [request.form.getlist('p1'), request.form.getlist('p2'), request.form.getlist('p3'),
                   request.form.getlist('p4')]
        return render_template("CompareTeams.html", count=len(teamName), teamName=teamName, p1=players[0],
                                    p2=players[1], p3=players[2], p4=players[3], teamIcons=TEAMS)


@multiple_teams.route("/display-t/<content>")
def display_teams(content):
    t_names, p_names, img_paths = [], [], []
    game_lst = set()
    data = {}

    content = json.loads(content)

    for team in content:
        t_names.append(team["Team"])

        p_paths = ["/images/" + str(team["Team"]) + ".png"]
        for player in team["Players"]:
            p_names.append(player[0])
            p_paths.append("/images/"+str(player[1])+".png")
        img_paths.append(p_paths)

        game_lst.update(team.keys())
        data[team["Team"]] = team_games(team)

    game_lst.remove("Team")
    game_lst.remove("Players")
    game_lst.remove("Overall")

    return render_template("DisplayCompareT.html", t_names=t_names, p_names=p_names, imgs=img_paths, games=game_lst,
                            num_t=len(t_names), data=data, teamIcons=TEAMS)

def team_games(team):
    t_game = {}
    for key in team:
        if key != "Team" and key != "Players":
            t_game[key] = (int(team[key][0]), int(team[key][1]))
    return t_game