from player_data import player_data

def compare_teams(teams_list):
    """teams_list = [ { Team Name: Name, Players: [ P1, P2, P3, P4 ] } ]"""
    # TODO: add Players key w/ list of tuples containing player name and id
    result = []
    for team in teams_list:
        team_results = {'Team': team['Team Name']}

        team_stats = []
        players = team["Players"]
        for player in players:
            team_stats.append(player_data(player))

        team_games = set()
        player_list = []
        for player in team_stats:
            team_games.update(player.keys())
            player_list.append(player["Player"])
        team_games.remove("Player")

        for game in team_games:
            game_coins = []
            game_placement = []
            for player in team_stats:
                if game in player.keys():
                    game_coins.append(player[game][0])
                    game_placement.append(player[game][1])
                else:
                    game_placement.append(20)
            avg_coins = sum(game_coins)
            avg_place = sum(game_placement) / len(game_placement)

            team_results[game] = (avg_coins, avg_place)
            team_results['Players'] = player_list

        result.append(team_results)
    return result

#print(compare_teams([{'Team Name': 'Red Rabbits', 'Players': ['Sapnap', 'sylvee', 'Tubbo', 'Smajor']}, {'Team Name': 'Orange Ocelots', 'Players': ['Dream', 'GeorgeNotFound', 'Quackity', 'KarlJacobs']}]))