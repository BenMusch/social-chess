import chessnouns
from chessnouns import schedule, player
from chessutilities import utilities
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')


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

    test_schedule = schedule.Schedule(players, chessnouns.DEFAULT_NUMBER_OF_ROUNDS, True, True)


def test_sort_players(get_all_players):
    pass


def test_assign_players_do_draws(get_all_players):
    pass


def test_player_grouping(get_all_players):
    print('\n---------------------------\nTest Schedule Player Grouping\n---------------------------')

    number_to_try = 41
    players = get_all_players[0:number_to_try]

    # Getting the right params
    boards, lopsided, bye = utilities.get_number_of_boards_and_tweaks(number_to_try)

    test_schedule = schedule.Schedule(players, chessnouns.DEFAULT_NUMBER_OF_ROUNDS, lopsided, bye)

    test_schedule.sort_players()

    # These are internal methods
    beginners = test_schedule._get_beginner_players()
    intermediates = test_schedule._get_intermediate_players()
    advanceds = test_schedule._get_advanced_players()

    assert len(advanceds) == 16
    assert len(intermediates) == 13
    assert len(beginners) == 12


def test_create_schedule(get_all_players):
    print('\n---------------------------\nBig Test for Creating Schedule\n---------------------------')

    number_to_try = 33

    players = get_all_players[0:number_to_try]

    # Getting the right params
    boards, lopsided, bye = utilities.get_number_of_boards_and_tweaks(number_to_try)

    logger.debug("Results were: {}, lopsided? {}, bye? {}".format(boards, lopsided, bye))

    test_schedule = schedule.Schedule(players, chessnouns.DEFAULT_NUMBER_OF_ROUNDS, lopsided, bye)

    assert test_schedule is not None

    test_schedule.sort_players()

    test_schedule.initialize_draws_for_players()
    test_schedule.shuffle_players()

    # We need to split players into two groups
    # to allow alternate playing rounds

    a, b = test_schedule.divide_players()

    logger.debug("\nFirst Group has: {} players ".format(len(a)))
    logger.debug("\nSecond Group has: {} players ".format(len(b)))

    test_schedule.schedule_players()

    test_schedule.initialize_draws_for_players()

    test_schedule.assign_scheduled_games_to_draws()

    test_schedule._print_player_draws()


def test_slot_calculations(get_all_players):
    print('\n---------------------------\nTesting Schedule Slot Calculations\n---------------------------')
    players = get_all_players

    # These parameters will be adjusted to correct values for
    # each, but we're using the variables to make the actual
    # calls much easier to read
    lopsided = True
    bye = True

    # 14 players
    #     Round 1A: 6 players, 3 boards
    #     Round 1B: 8 players, 4 boards
    test_schedule = schedule.Schedule(players[0:14], 8, lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 3
    assert test_schedule._calculate_b_boards_needed() == 4

    # 15 players
    #     Round 1A: 6 players, 3 boards
    #     Round 1B: 8 players, 4 boards, 1 bye board = 5
    test_schedule = schedule.Schedule(players[0:15], 8, lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 3
    assert test_schedule._calculate_b_boards_needed() == 5

    # 16 players
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 8 players, 4 boards
    test_schedule = schedule.Schedule(players[0:16], 8, not lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 4
    assert test_schedule._calculate_b_boards_needed() == 4

    # 17 players
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 8 players, 4 boards, one bye board = 5
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
    #     Round 1B: 15 players, 7 boards, one bye = 8
    test_schedule = schedule.Schedule(players[0:27], 8, lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 6
    assert test_schedule._calculate_b_boards_needed() == 8

    # 31 players
    #     Round 1A: 14 players, 7 boards
    #     Round 1B: 16 players, 8 boards, one bye = 9
    test_schedule = schedule.Schedule(players[0:31], 8, lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 7
    assert test_schedule._calculate_b_boards_needed() == 9

    # 36 players
    #     Round 1A: 18 players, 9 boards
    #     Round 1B: 18 players, 9 boards
    test_schedule = schedule.Schedule(players[0:36], 8, not lopsided, not bye)
    assert test_schedule._calculate_a_boards_needed() == 9
    assert test_schedule._calculate_b_boards_needed() == 9

    # 37 players
    #     Round 1A: 18 players, 9 boards
    #     Round 1B: 18 players, 9 boards + one bye = 10
    # assert (9, not lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(36)
    test_schedule = schedule.Schedule(players[0:37], 8, not lopsided, bye)
    assert test_schedule._calculate_a_boards_needed() == 9
    assert test_schedule._calculate_b_boards_needed() == 10
