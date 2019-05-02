from chessnouns import schedule, player
from chessutilities import utilities

"""
These test methods are just to test the Schedule class as a container
for a completed schedule.

The testing of the methods for creating a schedule are going to be in
the test utilities class
"""


def test_initialize_schedule(get_all_players):
    players = get_all_players[0:39]
    number_of_players = len(players)

    assert number_of_players == 39

    (number_of_boards, lopsided, bye) = utilities.get_number_of_boards_and_tweaks(number_of_players)

    assert number_of_boards == 10
    assert lopsided is True
    assert bye is True

    # FIXME: We should test other things here


def test_divide_players(get_all_players):
    # FIXME: need more here
    players = get_all_players

    test_schedule = schedule.Schedule(players, 8, True, True)


def test_sort_players(get_all_players):
    pass


def test_assign_players_do_draws(get_all_players):
    pass


def test_setup(get_all_players):
    players = get_all_players

    print("\nScheduling players. Number for this run is: {}".format(len(players)))

    test_schedule = schedule.Schedule(players, 8, True, True)

    assert test_schedule is not None

    test_schedule.sort_players()

    # These are internal methods
    beginners = test_schedule._get_beginner_players()
    intermediates = test_schedule._get_intermediate_players()
    advanceds = test_schedule._get_advanced_players()

    assert len(advanceds) == 16
    assert len(intermediates) == 13
    assert len(beginners) == 12

    test_schedule.initialize_draws_for_players()
    test_schedule.shuffle_players()

    # We need to split players into two groups
    # to allow alternate playing rounds

    a, b = test_schedule.divide_players()

    print("\nFirst Group has: {} players ".format(len(a)))
    print("\nSecond Group has: {} players ".format(len(b)))

    for thing in a:
        print("{} ({})".format(thing.get_name(), thing.get_level()))

    print("\nSecond Group has: {} players ".format(len(b)))
    for other in b:
        print("{} ({})".format(other.get_name(), other.get_level()))

    test_schedule.schedule_players()

    test_schedule.assign_scheduled_games_to_draws()

    test_schedule._print_player_draws()


def test_slot_calculations(get_all_players):
    print('\n---------------------------\nTesting Schedule Slot Calculations\n---------------------------')
    players = get_all_players

    # Let's test out these numbers
    # 14, 15, 16, 17, 18, 27, 31, 36, 75
    lopsided = True
    bye = True

    # 14 players
    #     Round 1A: 6 players, 3 boards
    #     Round 1B: 8 players, 4 boards
    # assert (4, lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(14)
    test_schedule = schedule.Schedule(players[0:14], 8, lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 3
    assert test_schedule._calculate_b_boards_needed() == 4

    # 15 players
    #     Round 1A: 6 players, 3 boards
    #     Round 1B: 8 players, 4 boards, 1 bye board
    # assert (4, lopsided, bye) == utilities.get_number_of_boards_and_tweaks(15)
    test_schedule = schedule.Schedule(players[0:15], 8, lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 3
    assert test_schedule._calculate_b_boards_needed() == 5

    # 16 players
    #
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 8 players, 4 boards
    # assert (4, not lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(16)
    test_schedule = schedule.Schedule(players[0:16], 8, not lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 4
    assert test_schedule._calculate_b_boards_needed() == 4

    # 17 players
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 8 players, 4 boards, one bye
    # assert (4, not lopsided, bye) == utilities.get_number_of_boards_and_tweaks(17)
    test_schedule = schedule.Schedule(players[0:17], 8, not lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 4
    assert test_schedule._calculate_b_boards_needed() == 5

    # 18 players
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 10 players, 5 boards
    test_schedule = schedule.Schedule(players[0:18], 8, lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 4
    assert test_schedule._calculate_b_boards_needed() == 5

    # 27 players
    #     Round 1A: 12 players, 6 boards,
    #     Round 1B: 15 players, 7 boards, one bye
    # assert (7, lopsided, bye) == utilities.get_number_of_boards_and_tweaks(27)
    test_schedule = schedule.Schedule(players[0:27], 8, lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 6
    assert test_schedule._calculate_b_boards_needed() == 8

    # 31 players
    #     Round 1A: 14 players, 7 boards
    #     Round 1B: 16 players, 8 boards, one bye
    test_schedule = schedule.Schedule(players[0:31], 8, lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 7
    assert test_schedule._calculate_b_boards_needed() == 9

    # 36 players
    #     Round 1A: 18 players, 9 boards
    #     Round 1B: 18 players, 9 boards
    # assert (9, not lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(36)
    test_schedule = schedule.Schedule(players[0:36], 8, not lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 9
    assert test_schedule._calculate_b_boards_needed() == 9
