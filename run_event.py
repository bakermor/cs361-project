from operator import itemgetter
from compare_teams import *

def run_event(teams, game_list):
    # teams = [ { Team Name: Name, Players: [ P1, P2, P3, P4 ] } ] ; len=10
    # game_list = [Game1, Game2, ...] ; len=8

    # team_data = [{ Team: Name, Players: [(P1, id), (P2, id),...], Game1: (coins, placement), ... , Game?: (coins, placement) }]
    team_data = compare_teams(teams)
    if team_data[0] == 'invalid':
        return team_data

    result = { 'Games':game_list, 'Teams':{}, 'Coins':{}, 'Overall': {} }  # Coins: {Game:[C1,C2,C3,C4,C5,C6,C7,C8,C9,C10]}

    for t in team_data:
        result['Teams'][t['Team']] = t['Players']

    # avg score per game around 800?
    multiplier = 1
    count = 1
    for g in game_list:
        gCoins = []
        for t in team_data:
            if g in t:
                gCoins.append({ 'Team': t['Team'], 'Coin': t[g][0] * multiplier })
            else:
                gCoins.append({ 'Team': t['Team'], 'Coin': 1000 * multiplier })
        result['Coins'][g] = sorted(gCoins, key=itemgetter('Coin'), reverse=True)
        count += 1
        if count % 2 == 0:
            multiplier += 0.5

    # calculate overall score & placement:
    # result['Coins'][g] = [{Team:Name, Coin:Coin}]
    overall = []
    for team in teams:
        tCoins = 0
        for game in game_list:
            for g in result['Coins'][game]:
                if g['Team'] == team["Team Name"]:
                    tCoins += g['Coin']
        overall.append({'Team': team["Team Name"], 'Coin': tCoins})
    result['Overall'] = sorted(overall, key=itemgetter('Coin'), reverse=True)

    return result

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
    team10 = {'Team Name': 'Pink Parrots', 'Players': ['Ranboo', 'KarlJacobs', 'HBomb94', 'KaraCorvus']}

    teams = [team1, team2, team3, team4, team5, team6, team7, team8, team9, team10]
    games = ["Grid Runners", "Parkour Tag", "Hole in the Wall", "Battle Box", "TGTTOSAWAF", "Ace Race", "Survival Games", "Sands of Time"]

    data = (run_event(teams, games))
    print(data["Overall"])


if __name__ == '__main__':
    main()