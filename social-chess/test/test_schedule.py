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


@pytest.fixture(scope="module")
def load_players():
    local_players = []

    con = sqlite.connect('../db/chess.db')  # If this is run from pytest in main dir, this is right

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            # print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")

            local_players.append(player.Player(row[0], row[1],
                                               level=int(row[3]),
                                               late=False,
                                               vip=(bool(int(row[4])))))

    return local_players


def test_initialize_schedule(load_players):
    """
        This setup will test the initializing of the schedule object
        then setting up of rounds, and the sorting of players,
        but not the actual scheduling, which will come later
        :return:
        """
    players = load_players
    number_of_players = len(players)

    assert number_of_players == 39

    (number_of_boards, lopsided, bye) = utilities.get_number_of_boards_and_tweaks(number_of_players)

    assert number_of_boards == 10
    assert lopsided is True
    assert bye is True

    # FIXME: We should test other things here


def test_setup(load_players):
    players = load_players

    test_schedule = schedule.Schedule(players, 8, True, True, 10)

    assert test_schedule is not None

    test_schedule.sort_players()

    beginners = test_schedule.get_beginner_players()
    intermediates = test_schedule.get_intermediate_players()
    advanceds = test_schedule.get_advanced_players()

    assert len(advanceds) == 14
    assert len(intermediates) == 13
    assert len(beginners) == 12

    test_schedule.initialize_draws_for_players()
    test_schedule.shuffle_players()

    # We need to split players into two groups
    # to allow alternate playing rounds

    a, b = test_schedule.divide_players()

    print("\nFirst Group has: {} players ".format(len(a)))

    for thing in a:
        print("{} ({})".format(thing.get_name(), thing.get_level()))

    print("\nSecond Group has: {} players ".format(len(b)))
    for other in b:
        print("{} ({})".format(other.get_name(), other.get_level()))

    test_schedule.start_over_players()
