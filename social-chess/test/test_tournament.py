import chessnouns
from chessnouns import schedule, player, tournament
from chessutilities import utilities
import pytest
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('chess')


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

    test_schedule.assign_scheduled_games_to_draws()

    test_schedule._print_player_draws()

    # OK, let's now add this to the tournament

    may_tournament = tournament.Tournament(test_schedule, "Test May")

    may_tournament.create_random_results_all()

    board_slots = may_tournament.get_leaderboard()

    for ind_slot in board_slots:
        print(ind_slot)

    print("Let's get the stats for the tournament")

    print("Number of games: {}".format(may_tournament.get_total_number_of_games()))

    wins, byes, losses, draws = may_tournament.return_result_numbers()

    print("Number of wins: {}".format(wins))
    print("Number of byes: {}".format(byes))
    print("Number of losses: {}".format(losses))
    print("Number of draws: {}".format(draws))

    tie_breakers_used, candidates = may_tournament.calculate_playoff_candidates()

    print("Playoff Players:")
    print(candidates)


def test_tiebreakers(get_all_players):
    breaks = 0
    schedules_with_two_in_playoffs = 0
    schedules_with_three_in_playoffs = 0
    schedules_with_four_in_playoffs = 0
    schedules_with_more_in_playoffs = 0

    number_of_tournaments = 1

    for count in range(0, number_of_tournaments):
        did_break = False
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
        test_schedule.schedule_players()

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

        print("Let's get the stats for the tournament")

        print("Number of games: {}".format(may_tournament.get_total_number_of_games()))

        wins, byes, losses, draws = may_tournament.return_result_numbers()

        print("Number of wins: {}".format(wins))
        print("Number of byes: {}".format(byes))
        print("Number of losses: {}".format(losses))
        print("Number of draws: {}".format(draws))

        did_break, candidates = may_tournament.calculate_playoff_candidates()

        print(candidates)

        if len(candidates) == 2:
            schedules_with_two_in_playoffs += 1
        elif len(candidates) == 3:
            schedules_with_three_in_playoffs += 1
        elif len(candidates) == 4:
            schedules_with_four_in_playoffs += 1
        else:
            schedules_with_more_in_playoffs += 1

        if did_break:
            breaks += 1

    print("Final report for Playoff Generation in {} Tournaments:".format(number_of_tournaments))
    print("2 Finalists: {}/{}\n3 Finalists: {}/{}\n4 finalists: {}/{}\n5 or more : {}/{}".format(
        schedules_with_two_in_playoffs, number_of_tournaments, schedules_with_three_in_playoffs, number_of_tournaments,
        schedules_with_four_in_playoffs,
        number_of_tournaments, schedules_with_more_in_playoffs, number_of_tournaments, ))
    print("Playoffs determined by tie breakers: {}".format(breaks))


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
