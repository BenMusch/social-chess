from chessnouns import schedule, player
from chessutilities import utilities

"""
These test methods are just to test the Schedule class as a container
for a completed schedule.

The testing of the methods for creating a schedule are going to be in
the test utilities class
"""


def test_initialize_schedule(get_all_players):

    players = get_all_players
    number_of_players = len(players)

    assert number_of_players == 39

    (number_of_boards, lopsided, bye) = utilities.get_number_of_boards_and_tweaks(number_of_players)

    assert number_of_boards == 10
    assert lopsided is True
    assert bye is True

    # FIXME: We should test other things here


def test_setup(get_all_players):
    players = get_all_players

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

    test_schedule.schedule_players()
