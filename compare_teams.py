from player_data import player_data

def compare_teams(teams_list):
    """teams_list = [ { Team Name: Name, Players: [ P1, P2, P3, P4 ] } ]"""
    result = []
    for team in teams_list:
        team_results = {'Team': team['Team Name']}
        team_stats = team_data(team)
        team_games = get_games(team_stats)

        for game in team_games:
            team_results[game] = team_average(game, team_stats)
            team_results['Players'] = get_players(team_stats)

        team_results = sort_results(team_results)
        result.append(team_results)

    # result = [{Team: team, Players: [(Name, id),...], Game 1: (coins, place), ..., Game N: (coins, place)}, ...]
    return result

def team_data(team):
    """team_stats = [{ Player: (P1, id), Game 1: (coins, place), ...}, ..., { Player: (P4, id), ...}]"""
    team_stats = []
    players = team["Players"]
    for player in players:
        data = player_data(player)
        if data == "invalid":
            return 'invalid', player
        team_stats.append(player_data(player))
    return team_stats

def get_games(team_stats):
    team_games = set()
    for player in team_stats:
        team_games.update(player.keys())
    team_games.remove("Player")
    return team_games

def get_players(team_stats):
    player_list = []
    for player in team_stats:
        player_list.append(player["Player"])
    return player_list

def team_average(game, team_stats):
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
    return sum(game_coins), sum(game_placement) / len(game_placement)

def sort_results(team_dict):
    keys = list(team_dict.keys())
    keys.sort()

    keys.remove('Team')
    keys.remove('Players')
    keys.remove('Overall')

    results = {'Team': team_dict['Team'], 'Players': team_dict['Players']}
    results.update({i: team_dict[i] for i in keys})
    results['Overall'] = team_dict['Overall']

    return results


if __name__ == '__main__':
    print(compare_teams([{'Team Name': 'Red Rabbits', 'Players': ["Sapnap", "Dream", "GeorgeNotFound", "BadBoyHalo"]}, {'Team Name': 'Orange Ocelots', 'Players': ["TommyInnit", "Tubbo", "Ranboo", "WilburSoot"]}]))