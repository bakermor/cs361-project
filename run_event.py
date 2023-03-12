from operator import itemgetter
from compare_teams import *

def run_event(teams, game_list):
    """
    teams = [ { Team Name: Name, Players: [ P1, P2, P3, P4 ] } ]
    game_list = [Game1, Game2, ...] ; len=8
    """

    team_stats = compare_teams(teams)
    if team_stats[0] == 'invalid':
        return {'Error' : team_stats}

    result = { 'Games':game_list, 'Teams':{}, 'Coins':{}, 'Overall': {} }
    for t in team_stats:
        result['Teams'][t['Team']] = t['Players']

    calculate_game_averages(game_list, team_stats, result)
    result['Overall'] = calculate_results(teams, game_list, result)
    return result

def calculate_game_averages(game_list, team_stats, result):
    multiplier, count = 1,1
    for g in game_list:
        gCoins = []
        for t in team_stats:
            if g in t:
                gCoins.append({ 'Team': t['Team'], 'Coin': t[g][0] * multiplier })
            else:
                gCoins.append({ 'Team': t['Team'], 'Coin': 1000 * multiplier })
        result['Coins'][g] = sorted(gCoins, key=itemgetter('Coin'), reverse=True)
        count += 1
        if count % 2 == 0:
            multiplier += 0.5

def calculate_results(teams, game_list, result):
    overall = []
    for team in teams:
        tCoins = 0
        for game in game_list:
            for g in result['Coins'][game]:
                if g['Team'] == team["Team Name"]:
                    tCoins += g['Coin']
        overall.append({'Team': team["Team Name"], 'Coin': tCoins})
    return sorted(overall, key=itemgetter('Coin'), reverse=True)


def main():
    team1 = {'Team Name': 'Red Rabbits', 'Players': ['Illumina', 'Ph1LzA', 'ElainaExe', 'Shubble']}
    team2 = {'Team Name': 'Orange Ocelots', 'Players': ['Antfrost', 'Fundy', 'Tubbo', '5up']}
    team3 = {'Team Name': 'Yellow Yaks', 'Players': ['CaptainSparklez', 'Dream', 'GeorgeNotFound', 'Quackity']}
    team4 = {'Team Name': 'Lime Llamas', 'Players': ['Krinios', 'Krtzy', 'sylvee', 'Nihachu']}
    team5 = {'Team Name': 'Green Geckos', 'Players': ['KarlJacobs', 'awesamdude', 'TommyInnit', 'Ponk']}
    team6 = {'Team Name': 'Cyan Coyotes', 'Players': ['OrionSound', 'Seapeekay', 'Solidarity', 'Smallishbeans']}
    team7 = {'Team Name': 'Aqua Axolotls', 'Players': ['cubfan135', 'PeteZahHutt', 'Ryguy', 'Grian']}
    team8 = {'Team Name': 'Blue Bats', 'Players': ['Punz', 'Smajor', 'vGumiho', 'Eret']}
    team9 = {'Team Name': 'Purple Pandas', 'Players': ['falsesymmetry', 'fruitberries', 'fWhip', 'Renthedog']}
    team10 = {'Team Name': 'Pink Parrots', 'Players': ['Ranboo', 'CaptainPuffy', 'HBomb94', 'KaraCorvus']}

    teams = [team1, team2, team3, team4, team5, team6, team7, team8, team9, team10]
    games = ["Grid Runners", "Parkour Tag", "Hole in the Wall", "Battle Box", "TGTTOSAWAF", "Ace Race",
             "Survival Games", "Sands of Time"]

    data = (run_event(teams, games))
    print(data)
    print(data["Overall"])


if __name__ == '__main__':
    main()