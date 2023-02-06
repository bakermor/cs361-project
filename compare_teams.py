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
            data = player_data(player)
            if data == "invalid":
                return 'invalid', player
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
                    if game != 'Overall':
                        game_coins.append(200)
                    else:
                        game_coins.append(1500)
                    game_placement.append(20)
            avg_coins = sum(game_coins)
            avg_place = sum(game_placement) / len(game_placement)

            team_results[game] = (avg_coins, avg_place)
            team_results['Players'] = player_list

        result.append(team_results)
    return result

if __name__ == '__main__':
    print(compare_teams([{'Team Name': 'Red Rabbits', 'Players': ["Sapnap", "Dream", "GeorgeNotFound", "BadBoyHalo"]}, {'Team Name': 'Orange Ocelots', 'Players': ["TommyInnit", "Tubbo", "Ranboo", "WilburSoot"]}]))