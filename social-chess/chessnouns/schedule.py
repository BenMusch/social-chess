"""
This class will create a proposed schedule for a tournament.
Note: This is not the same thing as a tournament, as it does
not have a date, a playoff, a winner, or some other details
"""
import chessnouns
from . import game, round, draw
from random import shuffle
from chessutilities import utilities
from chessexceptions import unsolveable_error


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

    def __init__(self, players, number_of_rounds, lopsided, bye, number_of_boards):

        if players is None:
            players = []

        self._players = players
        self._bye_round = bye
        self._lopsided = lopsided
        self._number_of_rounds = number_of_rounds
        self._number_boards = number_of_boards

        self._advanced_players = []
        self._intermediate_players = []
        self._beginner_players = []
        self._rounds = []

        # We need these for the social split
        self._advanced_a = []
        self._advanced_b = []
        self._intermediate_a = []
        self._intermediate_b = []
        self._beginner_a = []
        self._beginner_b = []

        self._a_group = []
        self._b_group = []

    def set_up_rounds(self):
        """
        This creates the round data structure, which will begin by being populated with
        empty game objects

        :return:
        """

        # In our model, the b part of the round is always equal to
        # the number of boards
        number_b = self._number_boards

        # The a part of the round is either equal to the number of
        # boards, or it is one less, if the tournament is lopsided

        number_a = self._number_boards

        if self._lopsided:
            number_a -= 1

        for count in range(0, self._number_of_rounds):
            # So we need two lists
            self._rounds.append(round.Round(number_a, number_b, count + 1))

    def get_rounds(self):
        return self._rounds

    def get_beginner_players(self):
        return self._beginner_players

    def get_intermediate_players(self):
        return self._intermediate_players

    def get_advanced_players(self):
        return self._advanced_players

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

    def shuffle_players(self):
        """
        This function randomizes the order of the players to create different pairings
        each run
        :return:
        """
        shuffle(self._beginner_players)
        shuffle(self._intermediate_players)
        shuffle(self._advanced_players)

    def set_up_draws(self, number_of_rounds):

        for player in self._beginner_players:
            player.set_draw(number_of_rounds)

        for player in self._intermediate_players:
            player.set_draw(number_of_rounds)

        for player in self._advanced_players:
            player.set_draw(number_of_rounds)

    def _loop_against_list(self, candidate_player, list_of_players):

        is_done = False

        for other_player in list_of_players:
            # print("Looking at candidate: {}".format(other_player.get_name()))
            Schedule.try_scheduling_these_guys(candidate_player, other_player)
            finished = candidate_player.get_draw().has_full_draw()
            if finished:
                is_done = True
                break

        return is_done

    def initialize_draws_for_players(self):
        # We need to set draw objects for all players

        # print("Setting up draws")
        self.set_up_draws(chessnouns.DEFAULT_NUMBER_OF_GAMES)

    def get_total_number_players(self):
        return len(self._advanced_players) + len(self._intermediate_players) + len(self._beginner_players)

    def divide_players(self):
        # FIXME: It's probably better to test to see if the number of advanced
        # players is less than half

        # So let's add the advanced to group a, unless there's a latecomer
        for candidate_player in self._advanced_players:
            if candidate_player.is_late():
                self._b_group.append(candidate_player)
            else:
                self._a_group.append(candidate_player)

        # So we should have 14 out of the needed 20

        # Let's do the beginners
        for candidate_player in self._beginner_players:
            self._b_group.append(candidate_player)

        # So group B now has 4

        # Now we need to use the intermediates to fill out the groups
        # How many do we need?

        needed = 20 - len(self._a_group)

        for i in range(0,needed):
            self._a_group.append(self._intermediate_players[i])

        for j in range(needed, len(self._intermediate_players)):
            self._b_group.append(self._intermediate_players[j])

        # OK. So the groups should have the right numbers
        return self._a_group, self._b_group

    def schedule_advanced_players(self):

        for candidate_player in self._advanced_players:
            # print("Scheduling for: {}".format(candidate_player.get_name()))

            # print("Matchups for player are: {} ".format(candidate_player.get_draw()))

            while candidate_player.get_draw().has_full_draw() is False:

                finished = self._loop_against_list(candidate_player, self._advanced_players)

                if finished:
                    continue

                finished = self._loop_against_list(candidate_player, self._intermediate_players)

                if finished:
                    continue

                finished = self._loop_against_list(candidate_player, self._beginner_players)

                if finished:
                    continue

                # FIXME: Let's try adding a bye - is this the answer?
                candidate_player.get_draw().add_bye()

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
        first.get_draw().add_game(second)
        second.get_draw().add_game(first)
        return True

    def schedule_beginner_players(self):
        for candidate_player in self._beginner_players:
            finished = self._loop_against_list(candidate_player, self._beginner_players)

            if finished:
                continue

            # FIXME: Let's try adding a bye - is this the answer?
            candidate_player.get_draw().add_bye()

    def schedule_intermediate_players(self):

        for candidate_player in self._intermediate_players:
            finished = self._loop_against_list(candidate_player, self._intermediate_players)

            if finished:
                continue

            finished = self._loop_against_list(candidate_player, self._beginner_players)

            if finished:
                continue

            # FIXME: Let's try adding a bye - is this

    def set_schedule_colors(self):
        """
        Right now this is just going to do it randomly

        :return:
        """
        master_list = self._advanced_players + self._intermediate_players + self._beginner_players

        for each_player in master_list:
            games = each_player.get_draw().get_games()
            for ind_game in games:
                if not ind_game.are_colors_set():
                    ind_game.set_random_colors()

        # Now we are going to make sure nobody got all one color
        # We will run through the loop twice, as the first
        # pass might have created a one-color draw for another

        for each_player in master_list:
            each_draw = each_player.get_draw()
            if each_draw.is_all_one_color():
                # Do something!
                each_draw.flip_color_two_games()

        for each_player in master_list:
            each_draw = each_player.get_draw()
            if each_draw.is_all_one_color():
                # Do something!

                each_draw.flip_color_two_games()

    def schedule_next_game(self, round_number):
        pass

    def print_schedule(self):
        # OK, now let us print and see
        print("***********")
        print("About to print beginner players (LEVEL 1).")
        utilities.print_player_draws(self._beginner_players)

        # OK, now let us print and see
        print("***********")
        print("About to print intermediate players (LEVEL 2,3).")
        utilities.print_player_draws(self._intermediate_players)

        # OK, now let us print and see
        print("***********")
        print("About to print advanced players (LEVELS 4-5).")
        utilities.print_player_draws(self._advanced_players)

    def _print_all_rounds(self, rounds):
        """""
        So we are going to print out all the rounds
        """
        print("Schedule of all games")
        count = 1
        for ind_round in rounds:
            print("Round {}:".format(count))
            for ind_game in ind_round:
                print(ind_game)
            count += 1

    def fill_in_rounds(self):
        """
        So what we are going to do is take everyone's draws
        and figure out when the games are all going to take place

        So we're looking at a set of rounds like:

        9 games - 1 bye
        10 games
        9 games - 1 bye
        10 games
        9 games - 1 bye
        10 games
        9 games - 1 bye
        10 games
        :return:
        """
        players = utilities.get_set_of_players()

        clem = players[0]
        sarah = players[1]
        will = players[2]
        evan = players[3]
        jay = players[4]

        real_game = game.Game(clem, sarah)
        real_game.set_random_colors()
        bye_game = game.Game.create_bye_game(will)
        bye_game.set_random_colors()

        first_set = [real_game] * 9
        first_set.append(bye_game)
        second_set = [real_game] * 10

        third_set = [real_game] * 9
        third_set.append(bye_game)
        fourth_set = [real_game] * 10

        fifth_set = [real_game] * 9
        fifth_set.append(bye_game)
        sixth_set = [real_game] * 10

        seventh_set = [real_game] * 9
        seventh_set.append(bye_game)
        eighth_set = [real_game] * 10

        rounds = [first_set, second_set, third_set, fourth_set, fifth_set,
                  sixth_set, seventh_set, eighth_set]

        # So let's try to add the real games
        player_one = self._advanced_players[0]
        one_draw = player_one.get_draw()
        one_draw_games = one_draw.get_games()
        first_set[0] = one_draw_games[0]
        third_set[0] = one_draw_games[1]
        fifth_set[0] = one_draw_games[2]

        seventh_set[0] = one_draw_games[3]

        # Now let's get preston

        self._print_all_rounds(rounds)
