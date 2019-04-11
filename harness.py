"""
This is the command-line tool that drives the creation of tournament pairings. 
"""
import sqlite3 as sqlite
from chess_entities import Player

players = []


def load_players():

    con = sqlite.connect('chess.db')

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")

            players.append(Player(row[1],level=int(row[3]), late=False, vip=(1 == int(row[4]))))

