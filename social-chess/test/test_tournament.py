import chessnouns
from chessnouns import schedule, player, tournament
from chessutilities import utilities
import pytest
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')


def test_init_tournament():
    pass


def test_add_schedule(get_all_players):
    number_to_try = 41

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

    # OK, let's now add this to the tournament

    may_tournament = tournament.Tournament(test_schedule, "Test May")

    may_tournament.create_random_results_all()

    board_slots = may_tournament.get_leaderboard()

    for ind_slot in board_slots:
        print(ind_slot)

    print("\n\nNOW FOR THE SORT\n\n")

    sorted_slots = sorted(board_slots)

    for ind_slot in sorted_slots:
        print(ind_slot)

def test_add_result():
    pass


def test_change_result():
    pass


def test_get_leaderboard():
    pass


def test_get_round():
    pass


def test_playoff():
    pass
