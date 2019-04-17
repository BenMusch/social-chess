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
    number_of_players = len(players)
    (number_of_boards, lopsided, bye) = utilities.get_number_of_boards_and_tweaks(number_of_players)

    assert (10, True, True) == (number_of_boards, lopsided, bye)
    assert (11, True, True) is not (number_of_boards, lopsided, bye)
    assert (10, True, False) is not (number_of_boards, lopsided, bye)
    assert (10, False, True) is not (number_of_boards, lopsided, bye)


def test_setup():
    """
    This setup will test the initializing of the schedule object
    then setting up of rounds, and the sorting of players,
    but not the actual scheduling, which will come later
    :return:
    """
    players = load_players()
    number_of_players = len(players)

    assert number_of_players == 39

    (number_of_boards, lopsided, bye) = utilities.get_number_of_boards_and_tweaks(number_of_players)

    assert number_of_boards == 10
    assert lopsided is True
    assert bye is True

    test_schedule = schedule.Schedule(players, 4, lopsided, bye, number_of_boards)

    assert test_schedule is not None

    test_schedule.set_up_rounds()

    # OK, so we need to get the rounds and see what happened.
    # What we should have is a list of rounds with None
    # references as the correct number of placeholders

    rounds = test_schedule.get_rounds()

    # Test it is not null

    assert rounds is not None

    # Test that the number of rounds is correct

    assert 4 == len(rounds)

    # Get each list, test for correct length and contents

    one_a_games = rounds[0].get_a_games()
    one_b_games = rounds[0].get_b_games()
    two_a_games = rounds[1].get_a_games()
    two_b_games = rounds[1].get_b_games()
    three_a_games = rounds[2].get_a_games()
    three_b_games = rounds[2].get_b_games()
    four_a_games = rounds[3].get_a_games()
    four_b_games = rounds[3].get_b_games()

    assert len(one_a_games) == number_of_boards - 1
    assert len(one_b_games) == number_of_boards
    assert len(two_a_games) == number_of_boards - 1
    assert len(two_b_games) == number_of_boards
    assert len(three_a_games) == number_of_boards - 1
    assert len(three_b_games) == number_of_boards
    assert len(four_a_games) == number_of_boards - 1
    assert len(four_b_games) == number_of_boards

    assert one_a_games[0] is None
    assert one_a_games[5] is None
    assert four_a_games[0] is None
    assert four_a_games[5] is None

