from flask import Flask, render_template

from ui_single_player import single_player
from ui_multiple_players import multiple_players
from ui_multiple_teams import multiple_teams
from ui_event import event

app = Flask(__name__)
app.register_blueprint(single_player, url_prefix="")
app.register_blueprint(multiple_players, url_prefix="")
app.register_blueprint(multiple_teams, url_prefix="")
app.register_blueprint(event, url_prefix="")

TEAMS = ['Red Rabbits', 'Orange Ocelots', 'Yellow Yaks', 'Lime Llamas', 'Green Geckos', 'Cyan Coyotes', 'Aqua Axolotls',
         'Blue Bats', 'Purple Pandas', 'Pink Parrots']

# Home Page
@app.route("/")
def home():
    return render_template("HomePage.html", teamIcons=TEAMS)

# Valid Players
@app.route("/valid")
def valid_players():
    return render_template("ValidPlayers.html", teamIcons=TEAMS)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
