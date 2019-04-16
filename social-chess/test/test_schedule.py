from chessnouns import schedule, player
from chessutilities import utilities
import sqlite3 as sqlite
import pytest

"""
These test methods are just to test the Schedule class as a container
for a completed schedule.

The testing of the methods for creating a schedule are going to be in
the test utilities class
"""


def load_players():
    local_players = []

    con = sqlite.connect('../db/chess.db')  # If this is run from pytest in main dir, this is right

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")

            local_players.append(player.Player(row[1],
                                               level=int(row[3]),
                                               late=False,
                                               vip=(bool(int(row[4])))))
    return local_players


def test_start():
    players = load_players()
    _number_of_players = len(players)
    (_number_of_boards, _lopsided, _bye) = utilities.get_number_of_boards_and_tweaks(_number_of_players)

    assert (10, True, True) == (_number_of_boards, _lopsided, _bye)
    assert (11, True, True) is not (_number_of_boards, _lopsided, _bye)
    assert (10, True, False) is not (_number_of_boards, _lopsided, _bye)
    assert (10, False, True) is not (_number_of_boards, _lopsided, _bye)
