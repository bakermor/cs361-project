import mysql.connector

def player_data(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="P4ssw0rd",
        database="mccdb"
    )

    mycursor = mydb.cursor()

    get_id = "SELECT player_id FROM players WHERE name=%s"
    mycursor.execute(get_id, (name,))
    player = mycursor.fetchone()
    if player is None:
        return "invalid"
    player_id = player[0]

    get_games = "SELECT game FROM game_data WHERE player_id=%s"
    mycursor.execute(get_games, (player_id,))
    games_played = mycursor.fetchall()
    games = set()  # will contain all games played, without duplicates
    for tup in games_played:
        games.add(tup[0])

    # TODO: order results alphabetically with "Player" at beginning and "Overall" at the end
    results = {'Player':(name,player_id)}
    for game in games_played:
        get_coins = "SELECT coins,placement FROM game_data WHERE player_id=%s AND game=%s"
        mycursor.execute(get_coins, [player_id, game[0]])
        data = mycursor.fetchall()

        coins, placements = [], []
        for tup in data:
            coins.append(tup[0])
            placements.append(tup[1])
        avg_coins = sum(coins) / len(coins)
        avg_place = sum(placements) / len(placements)

        results[game[0]] = (avg_coins, avg_place)

    return results
