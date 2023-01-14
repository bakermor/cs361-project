import mysql.connector


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="P4ssw0rd",
        database="mccdb"
    )

    mycursor = mydb.cursor()

    mydb.commit()


main()

