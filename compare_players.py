from player_data import player_data

def compare_players(player_list):
    result = []
    for player in player_list:
        if player != "":
            p_data = player_data(player)
            if p_data == 'invalid':
                return 'invalid', player
            result.append(p_data)
    return result

print(compare_players(["KaraCorvus", 'Krinios', 'Ranboo', 'Ponk']))