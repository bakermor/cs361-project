from player_data import player_data

def compare_players(player_list):
    result = []
    for player in player_list:
        result.append(player_data(player))
    return result