from chessutilities import utilities
import chessnouns
from chessnouns import schedule, tournament, slot

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('chess')


def test_slots(get_all_players):
    print('\n---------------------------\nTesting Leaderboard Slots\n---------------------------')

    did_break = False
    number_to_try = 41

    players = get_all_players[0:number_to_try]

    # Getting the right params
    boards, lopsided, bye = utilities.get_number_of_boards_and_tweaks(number_to_try)

    test_schedule = schedule.Schedule(players, chessnouns.DEFAULT_NUMBER_OF_ROUNDS, lopsided, bye)

    assert test_schedule is not None

    test_schedule.sort_players()
    test_schedule.initialize_draws_for_players()

    # We need to split players into two groups
    # to allow alternate playing rounds

    a, b = test_schedule.divide_players()
    test_schedule.schedule_players()

    test_schedule.assign_scheduled_games_to_draws()

    test_schedule._print_player_draws()

    # OK, let's now add this to the tournament

    may_tournament = tournament.Tournament(test_schedule, "Test May")

    may_tournament.create_random_results_all()

    board_slots = may_tournament.get_leaderboard()

    print("LEADERBOARD SLOTS")

    for ind_slot in board_slots:
        print(ind_slot)

    print("TOP TEN ONLY")
    top_ten_slots = may_tournament.get_leaderboard(10)

    assert 10 == len(top_ten_slots)

    for top_ten in top_ten_slots:
        print(top_ten)