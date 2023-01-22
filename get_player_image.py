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