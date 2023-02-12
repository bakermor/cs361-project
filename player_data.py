import mysql.connector

def player_data(name):
    """
    Returns dict containing average coins and placements for each game
    """

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="P4ssw0rd",
        database="mccdb"
    )
    mycursor = mydb.cursor()

    player_id = get_player_id(name, mycursor)
    if player_id == 'invalid':
        return 'invalid'
    games = get_games(player_id, mycursor)

    results = {'Player':(name,player_id)}
    for game in games:
        results[game] = get_game_averages(player_id, game, mycursor)

    results = sort_dict(results)
    # results = {'Player': (name, id), 'Game 1': (coins, place), ..., 'Game N': (coins, place), 'Overall': (coins, place)}
    return results

def get_player_id(name, mycursor):
    command = "SELECT player_id FROM players WHERE name=%s"
    mycursor.execute(command, (name,))
    player = mycursor.fetchone()
    if player is None:
        return "invalid"
    return player[0]

def get_games(player_id, mycursor):
    command = "SELECT game FROM game_data WHERE player_id=%s"
    mycursor.execute(command, (player_id,))
    games_played = mycursor.fetchall()
    games = set()  # will contain all games played, without duplicates
    for tup in games_played:
        games.add(tup[0])
    return games

def get_game_averages(player_id, game, mycursor):
    command = "SELECT coins,placement FROM game_data WHERE player_id=%s AND game=%s"
    mycursor.execute(command, [player_id, game])
    data = mycursor.fetchall()

    coins, placements = [], []
    for tup in data:
        coins.append(tup[0])
        placements.append(tup[1])
    avg_coins = sum(coins) / len(coins)
    avg_place = sum(placements) / len(placements)
    return avg_coins, avg_place

def sort_dict(game_dict):
    keys = list(game_dict.keys())
    keys.sort()

    keys.remove('Player')
    keys.remove('Overall')

    results = {'Player': game_dict['Player']}
    results.update({i: game_dict[i] for i in keys})
    results['Overall'] = game_dict['Overall']

    return results
