"""
This is the command-line tool that drives the creation of tournament pairings. 
"""
import sqlite3 as sqlite
from chessnouns import player
from chessutilities import utilities

players = []


def load_players():

    con = sqlite.connect("../db/chess.db")

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")

            players.append(player.Player(row[1],level=int(row[3]), late=False, vip=(1 == int(row[4]))))


    print(players)


def get_round_options(number_players, minutes_total, minutes_round):
    """
    :param number_players:
    :param minutes_total:
    :param minutes_round:
    :return: an array of tuples

    So this is going to be hard. First, let's start with the idea that there are 14 players, 30 minutes per round,
    150 minutes for the whole thing

    We also want the rule that people can only play half the time

    This means that if you want 30 minute games, you need one full hour to do a round.
    If you want 20 minute games, you need 40 minutes for a full round


    If you want 14 players and 30 minute games, you get only 2 full rounds (everyone gets 2 games).

    3 boards

    0-30

    Round 1A: Only six can play
    1-6 play, 7th gets a bye

    30-60

    Round 1B:
    8-14 play

    60-90

    Round 2A:
    2-7 play, 1 gets a bye

    90-120

    Round 2B:
    8-14 play

    20 minutes Playoff


    If you want 14 players and 25 minute games....

    0-25 Round 1A
    25-50 Round 1B

    50-75 Round 2A
    75-100 Round 2B

    100-125 Round 3A
    125-150 Round 3B

    150-170 Playoff


    If you want 14 players and 20 minute games....

    0-20 Round 1A
    20-40 Round 1B

    40-60 Round 2A
    60-80 Round 2B

    80-100 Round 3A
    100-120 Round 3B

    130-150 Playoff

    What about 14 players and 15 minute games

    0-15 Round 1A
    15-30 Round 1B

    30-45 Round 2A
    45-60 Round 2B

    60-75 Round 3A
    75-90 Round 3B

    90-105 Round 4A
    105-120 Round 4B

    130-150 Playoff




    """




    answer_array = []



def main():
    load_players()



if __name__ == '__main__':
    main()


load_players()

for i in range(7,51):
    needed_boards, lopsided, bye = utilities.get_number_of_boards_and_tweaks(i)
    print("For Players {}, Boards {} Lopsided? {}, Bye? {}".format(i, needed_boards, lopsided, bye))



