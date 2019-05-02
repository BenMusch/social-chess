"""
This class will create a proposed schedule for a tournament.
Note: This is not the same thing as a tournament, as it does
not have a date, a playoff, a winner, or some other details
"""
import chessnouns
from . import game, round, draw
from random import shuffle
import math
from chessutilities import utilities
from chessexceptions import unsolveable_error, scheduling_error


class Schedule(object):
    # This is the number of boards to play, it will determine
    # the number of simultaneous games

    def __repr__(self):

        return_line = "Schedule Object:\n"
        return_line += "There are {} rounds.\n".format(len(self._rounds))
        return return_line

    def __str__(self):
        return_line = "There are {} rounds.\n".format(len(self._rounds))
        return_line += "-----\n"

        count = 0

        print("There are {} rounds in the array.\n".format(len(self._rounds)))
        for two_part_round in self._rounds:
            print("Getting list of matches in round {}\n".format(count))
            return_line += "Round: {}\n".format(count + 1)
            return_line += "******************\n"
            board_counter = 0

            # First set
            for match in two_part_round[0]:
                return_line += "BOARD {} -- White: {} Black: {} \n".format(board_counter + 1, match.get_white_player(),
                                                                           match.get_black_player())
                board_counter += 1
            count += 1
            return_line += "-----\n"

            # Second set
            board_counter = 0
            for match in two_part_round[1]:
                return_line += "BOARD {} -- White: {} Black: {} \n".format(board_counter + 1, match.get_white_player(),
                                                                           match.get_black_player())
                board_counter += 1
            count += 1
            return_line += "-----\n"

        return_line += "-----\n"
        return return_line

    def __init__(self, players, number_of_rounds, lopsided, bye):

        if players is None:
            players = []

        self._players = players
        self._bye_round = bye
        self._lopsided = lopsided
        self._number_of_rounds = number_of_rounds
        # self._number_boards = number_of_boards

        self._advanced_players = []
        self._intermediate_players = []
        self._beginner_players = []
        self._rounds = []

        # We need these for the social split
        self._a_group = []
        self._b_group = []

    def sort_players(self):
        """
        This method breaks the players into their categories

        :return:
        """
        # print("About to sort players")
        for player in self._players:
            if player.get_level() == chessnouns.BEGINNER or player.get_level() == chessnouns.IMPROVING:
                # print("Adding {} to beginner ".format(player.get_name()))
                self._beginner_players.append(player)
            elif player.get_level() == chessnouns.ADEPT:
                # print("Adding {} to intermediate ".format(player.get_name()))
                self._intermediate_players.append(player)
            else:
                # print("Adding {} to advanced ".format(player.get_name()))
                assert player.get_level() == chessnouns.KING or player.get_level() == chessnouns.KNIGHT
                self._advanced_players.append(player)

    def initialize_draws_for_players(self):
        # We need to set draw objects for all players

        for player in self._beginner_players:
            player.set_draw(self._number_of_rounds)

        for player in self._intermediate_players:
            player.set_draw(self._number_of_rounds)

        for player in self._advanced_players:
            player.set_draw(self._number_of_rounds)

    def shuffle_players(self):
        """
        This function randomizes the order of the players to create different pairings
        each run
        :return:
        """
        shuffle(self._beginner_players)
        shuffle(self._intermediate_players)
        shuffle(self._advanced_players)

    def _calculate_a_boards_needed(self):

        # Let's imagine 14, 15, 16, 17
        number = math.trunc(len(self._players) / 4)

        return number

    def _calculate_b_boards_needed(self):
        """
        The a slot is always the even players divided
        by 4. Extras are always added to the b
        set. This was done to make it more likely
        someone unexpectedly late wouldn't miss their game
        """

        # Let's imagine 14, 15, 16, 17
        number = math.trunc(len(self._players) / 4)

        # So we'd have 4, 5, 4, 5

        if len(self._players) % 4 == 3:
            number += 2
        elif len(self._players) % 4 == 1 or len(self._players) % 4 == 2:
            number += 1

        return number

    def divide_players(self):

        half_players = math.trunc(len(self._players) / 2)

        if len(self._advanced_players) > half_players:
            raise scheduling_error.SchedulingError("You must have fewer than half be advanced players to schedule.")

        # So let's add the advanced to group a, unless there's a latecomer
        for candidate_player in self._advanced_players:
            if candidate_player.is_late():
                self._b_group.append(candidate_player)
            else:
                self._a_group.append(candidate_player)

        if len(self._beginner_players) > half_players:
            raise scheduling_error.SchedulingError("You must have fewer than half be advanced players to schedule.")

        # Let's do the beginners
        for candidate_player in self._beginner_players:
            self._b_group.append(candidate_player)

        # Let's get a feel for what we have now.

        # We need twice the slots as boards
        needed_a_slots = self._calculate_a_boards_needed() * 2

        print("Needed a slots was: {} ".format(needed_a_slots))

        needed_b_slots = self._calculate_b_boards_needed() * 2

        actual_a_slots = len(self._a_group)
        actual_b_slots = len(self._b_group)

        # So group B now has 4

        # Now we need to use the intermediates to fill out the groups
        # How many do we need?

        needed = needed_a_slots - actual_a_slots

        for i in range(0, needed):
            self._a_group.append(self._intermediate_players[i])

        for j in range(needed, len(self._intermediate_players)):
            self._b_group.append(self._intermediate_players[j])

        # OK. So the groups should have the right numbers
        return self._a_group, self._b_group

    def schedule_players(self):

        first, second, third, fourth = self._schedule_a_players()
        fifth, sixth, seventh, eighth = self._schedule_b_players()

        self._rounds = [first, fifth, second, sixth, third, seventh, fourth, eighth]

        self._print_all_rounds()

    def assign_scheduled_games_to_draws(self):

        for ind_round in self._rounds:
            for ind_game in ind_round:
                game_players = ind_game.get_players()
                game_players[0].get_draw().add_game_with_game(ind_game)
                if game_players[1].get_id() != chessnouns.BYE_ID:
                    game_players[1].get_draw().add_game_with_game(ind_game)


    """
    This should just be internal functions until get/set
    """

    def _loop_against_list(self, candidate_player, list_of_players):

        is_done = False

        for other_player in list_of_players:
            print("For candidate: {} Looking at possibility: {}".format(candidate_player.get_name(),
                                                                        other_player.get_name()))
            Schedule.try_scheduling_these_guys(candidate_player, other_player)
            finished = candidate_player.get_draw().has_full_draw()
            if finished:
                is_done = True
                break

        return is_done

    def get_total_number_players(self):
        return len(self._advanced_players) + len(self._intermediate_players) + len(self._beginner_players)

    def _schedule_a_players(self):
        # So we've got 20 and 10 slots

        a_boards = self._calculate_a_boards_needed()

        first_half_a = self._a_group[0:a_boards]
        second_half_a = self._a_group[a_boards:a_boards * 2]

        first_names = [a.get_name() for a in first_half_a]
        second_names = [a.get_name() for a in second_half_a]

        print("First half is: {} ".format(first_names))
        print("Second half is: {} ".format(second_names))

        first_set = []

        time = chessnouns.STANDARD_GAME_TIME,

        count = 0
        for i in range(0, a_boards):
            first_set.append(game.Game(first_half_a[count], second_half_a[count], onewhite=True, twowhite=False))
            count += 1

        second_set = []
        count = 0
        for i in range(0, a_boards):
            second_set.append(game.Game(first_half_a[count], second_half_a[count - 1], onewhite=False, twowhite=True))
            count += 1

        third_set = []
        count = 0
        for i in range(0, a_boards):
            third_set.append(game.Game(first_half_a[count], second_half_a[count - 2], onewhite=True, twowhite=False))
            count += 1

        fourth_set = []
        count = 0
        for i in range(0, a_boards):
            fourth_set.append(game.Game(first_half_a[count], second_half_a[count - 3], onewhite=False, twowhite=True))

            count += 1

        return first_set, second_set, third_set, fourth_set

    def _schedule_b_players(self):

        b_boards = self._calculate_a_boards_needed()

        if self._lopsided:
            b_boards_extra = 1
        else:
            b_boards_extra = 0

        print("B Boards was {} and the extra was {} ".format(b_boards, b_boards_extra))

        # So we've got 19 and 10 slots

        # So we need 2 groups of 9

        # Group of 9
        first_half_a = self._b_group[0:b_boards]

        # Group of 10
        second_half_a = self._b_group[b_boards:b_boards * 2 + b_boards_extra]

        first_names = [a.get_name() for a in first_half_a]
        second_names = [a.get_name() for a in second_half_a]

        print("First half is: {} ".format(first_names))
        print("Second half is: {} ".format(second_names))

        first_set = []
        count = 0

        for i in range(0, b_boards):
            if i == 9:
                first_set.append(game.Game.create_bye_game(second_half_a[count], onewhite=True, twowhite=False))
            else:
                first_set.append(game.Game(first_half_a[count], second_half_a[count], onewhite=True, twowhite=False))
            count += 1

        second_set = []
        count = 0

        for i in range(0, b_boards):
            if i == 9:
                second_set.append(game.Game.create_bye_game(second_half_a[count - 1], onewhite=False, twowhite=True))
            else:
                second_set.append(
                    game.Game(first_half_a[count], second_half_a[count - 1], onewhite=False, twowhite=True))
            count += 1

        third_set = []
        count = 0

        for i in range(0, b_boards):
            if i == 9:
                third_set.append(game.Game.create_bye_game(second_half_a[count - 2], onewhite=True, twowhite=False))
            else:
                third_set.append(
                    game.Game(first_half_a[count], second_half_a[count - 2], onewhite=True, twowhite=False))
            count += 1

        fourth_set = []
        count = 0

        for i in range(0, b_boards):
            if i == 9:
                fourth_set.append(game.Game.create_bye_game(second_half_a[count - 3], onewhite=False, twowhite=True))
            else:
                fourth_set.append(
                    game.Game(first_half_a[count], second_half_a[count - 3], onewhite=False, twowhite=True))
            count += 1

        return first_set, second_set, third_set, fourth_set

    @classmethod
    def try_scheduling_these_guys(cls, first, second):
        """
        Factored out this code
        :param first:
        :param second:
        :return: bool - did we succeed?
        """
        # First, it's not him, right?
        if first.get_id() == second.get_id():
            return False
        # Is the other player all scheduled?
        if second.get_draw().has_full_draw():
            return False
        # Have they played
        if second.get_draw().has_played_player_id(first.get_id()):
            return False
        if first.get_draw().has_played_player_id(second.get_id()):
            return False
        # OK. So we can schedule this!
        # print("We got a hit!")
        first.get_draw().add_game_by_player(second)
        second.get_draw().add_game_by_player(first)
        return True

    def _is_a_mirror_game(self, candidate_game, game_list):

        two_players = candidate_game.get_players()
        for possible_game in game_list:
            existing_players = possible_game.get_players()
            test_set = {two_players[0].get_id(), two_players[1].get_id(), existing_players[0].get_id(),
                        existing_players[1].get_id()}

            if len(test_set) == 2:
                # print("Can't do that game")
                return True

        return False

    def _print_player_draws(self):
        """
        This method will print all the players and their draw
        information to the command line
        """
        for p in self._players:
            player_draw = p.get_draw()
            print(player_draw)

    def _print_schedule(self):
        # OK, now let us print and see
        print("***********")
        print("About to print beginner players (LEVEL 1).")
        self._print_player_draws(self._beginner_players)
        # OK, now let us print and see
        print("***********")
        print("About to print intermediate players (LEVEL 2,3).")
        self._print_player_draws(self._intermediate_players)

        # OK, now let us print and see
        print("***********")
        print("About to print advanced players (LEVELS 4-5).")
        self._print_player_draws(self._advanced_players)

    def _print_all_rounds(self):
        """""
        So we are going to print out all the rounds
        """

        # This is just a list of strings for round times
        times = chessnouns.ROUND_TIMES

        print("Schedule of all games")
        count = 1
        for ind_round in self._rounds:
            print("***************")

            print("Round {} ({}):".format(count, times[count - 1]))
            print("***************")
            board = 1
            for ind_game in ind_round:
                print("Board {}: {}".format(board, ind_game))
                board += 1
            count += 1

    def get_a_players(self):
        return self._a_group

    def get_b_players(self):
        return self._b_group

    def print_group_players(self, group):
        self._print_player_draws()

    def _get_beginner_players(self):
        return self._beginner_players

    def _get_intermediate_players(self):
        return self._intermediate_players

    def _get_advanced_players(self):
        return self._advanced_players

    def get_rounds(self):
        return self._rounds
