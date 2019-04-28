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
            # print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")

            local_players.append(player.Player(row[0], row[1],
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


def get_schedule():
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

    return number_of_boards, test_schedule


def test_setup():
    number_of_boards, test_schedule = get_schedule()

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

    # FIXME: What goes here?

    # Now to test out the sorting

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


    """
    test_schedule.schedule_a_players()

    test_schedule.schedule_b_players()

    test_schedule.set_schedule_colors()

    test_schedule.print_group_players(test_schedule.get_a_players())
    print("---------------")
    test_schedule.print_group_players(test_schedule.get_b_players())

    print("GETTING GAMES")

    list_of_a_games = test_schedule.get_all_a_games()
    print("There are {} A Games.".format(len(list_of_a_games)))

    print(list_of_a_games)

    print("\n\nSORTING GAMES")

    sorted_list = sorted(list_of_a_games, key=get_points)

    print(sorted_list)

    print("\n\nSCHEDULING A GAMES: RANDOM")

    rounds_list = test_schedule.schedule_a_games(None)

    count = 1
    for round in rounds_list:
        print("ROUND: {} ".format(count))
        print(round)
        count += 1
    
    print("\n\nSCHEDULING A GAMES: SORTED")

    rounds_list = test_schedule.schedule_a_games(sorted_list)

    count = 1
    for round in rounds_list:
        print("ROUND: {} ".format(count))
        print(round)
        count += 1

    test_schedule.print_draw_report(rounds_list)
    
    """

    # test_schedule.schedule_advanced_players()
    # test_schedule.schedule_intermediate_players()
    # test_schedule.schedule_beginner_players()

    #

    # test_schedule.print_schedule()

    # test_schedule.fill_in_rounds()


def get_points(game):
    return game.get_game_points()


def xx_placement():
    """
    OK, here's the hard part. We are going to test everyone getting
    placed where they are supposed to.
    :return:
    """
    number_of_boards, test_schedule = get_schedule()

    test_schedule.set_up_rounds()
    test_schedule.sort_players()
