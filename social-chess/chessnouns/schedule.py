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

    def initialize_draws_for_players(self):
        # We need to set draw objects for all players

        for player in self._beginner_players:
            player.set_draw(self._number_of_rounds)

        for player in self._intermediate_players:
            player.set_draw(self._number_of_rounds)

        for player in self._advanced_players:
            player.set_draw(self._number_of_rounds)

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

        for i in range(0, needed):
            self._a_group.append(self._intermediate_players[i])

        for j in range(needed, len(self._intermediate_players)):
            self._b_group.append(self._intermediate_players[j])

        # OK. So the groups should have the right numbers
        return self._a_group, self._b_group

    def get_a_players(self):
        return self._a_group

    def get_b_players(self):
        return self._b_group

    def schedule_players(self):

        first, second, third, fourth = self._scheule_a_players()
        fifth, sixth, seventh, eighth = self._schedule_b_players()

        my_rounds = [first, fifth, second, sixth, third, seventh, fourth, eighth]

        self._print_all_rounds(my_rounds)

    def _assign_scheduled_games_to_draws(self):
        pass

    def _scheule_a_players(self):
        # So we've got 20 and 10 slots
        first_half_a = self._a_group[0:10]
        second_half_a = self._a_group[10:20]

        first_names = [a.get_name() for a in first_half_a]
        second_names = [a.get_name() for a in second_half_a]

        # print("First half is: {} ".format(first_names))
        # print("Second half is: {} ".format(second_names))

        first_set = []

        time = chessnouns.STANDARD_GAME_TIME,

        count = 0
        for i in range(0, 10):
            first_set.append(game.Game(first_half_a[count], second_half_a[count], onewhite=True, twowhite=False))
            count += 1

        second_set = []
        count = 0
        for i in range(0, 10):
            second_set.append(game.Game(first_half_a[count], second_half_a[count - 1], onewhite=False, twowhite=True))
            count += 1

        third_set = []
        count = 0
        for i in range(0, 10):
            third_set.append(game.Game(first_half_a[count], second_half_a[count - 2], onewhite=True, twowhite=False))
            count += 1

        fourth_set = []
        count = 0
        for i in range(0, 10):
            fourth_set.append(game.Game(first_half_a[count], second_half_a[count - 3], onewhite=False, twowhite=True))

            count += 1

        return first_set, second_set, third_set, fourth_set

    def _schedule_b_players(self):

        # So we've got 19 and 10 slots

        # So we need 2 groups of 9

        # Group of 9
        first_half_a = self._b_group[0:9]

        # Group of 10
        second_half_a = self._b_group[9:19]

        first_names = [a.get_name() for a in first_half_a]
        second_names = [a.get_name() for a in second_half_a]

        # print("First half is: {} ".format(first_names))
        # print("Second half is: {} ".format(second_names))

        first_set = []
        count = 0

        for i in range(0, 10):
            if i == 9:
                first_set.append(game.Game.create_bye_game(second_half_a[count], onewhite=True, twowhite=False))
            else:
                first_set.append(game.Game(first_half_a[count], second_half_a[count], onewhite=True, twowhite=False))
            count += 1

        second_set = []
        count = 0

        for i in range(0, 10):
            if i == 9:
                second_set.append(game.Game.create_bye_game(second_half_a[count - 1], onewhite=False, twowhite=True))
            else:
                second_set.append(
                    game.Game(first_half_a[count], second_half_a[count - 1], onewhite=False, twowhite=True))
            count += 1

        third_set = []
        count = 0

        for i in range(0, 10):
            if i == 9:
                third_set.append(game.Game.create_bye_game(second_half_a[count - 2], onewhite=True, twowhite=False))
            else:
                third_set.append(
                    game.Game(first_half_a[count], second_half_a[count - 2], onewhite=True, twowhite=False))
            count += 1

        fourth_set = []
        count = 0

        for i in range(0, 10):
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
        first.get_draw().add_game(second)
        second.get_draw().add_game(first)
        return True

    def print_group_players(self, group):
        utilities.print_player_draws(group)

    def is_a_mirror_game(self, candidate_game, game_list):

        two_players = candidate_game.get_players()
        for possible_game in game_list:
            existing_players = possible_game.get_players()
            test_set = {two_players[0].get_id(), two_players[1].get_id(), existing_players[0].get_id(),
                        existing_players[1].get_id()}

            if len(test_set) == 2:
                # print("Can't do that game")
                return True

        return False

    def does_list_contain_players(self, candidate_game, game_list):
        # So we have to figure out if the game is already in there

        two_players = candidate_game.get_players()
        for possible_game in game_list:
            # print("Entering the check")
            # print(game_list)
            # print("Two players")
            # print(candidate_game)
            existing_players = possible_game.get_players()
            test_set = {two_players[0].get_id(), two_players[1].get_id(), existing_players[0].get_id(),
                        existing_players[1].get_id()}
            print("Set length was:{} ".format(len(test_set)))
            print("Set was: {} ".format(test_set))
            if len(test_set) < 4:
                # print("Can't do that game")
                return True

        return False

    def get_all_a_games(self):

        a_games_list = []

        for ind_player in self._a_group:
            draws = ind_player.get_draw()
            games = draws.get_games()
            for matchup in games:
                if not self.is_a_mirror_game(matchup, a_games_list):
                    a_games_list.append(matchup)

        return a_games_list

    def schedule_a_games(self, schedule_list):

        master_list = []

        # Round one
        if schedule_list is None:
            a_games = self.get_all_a_games()
        else:
            a_games = schedule_list

        count = len(a_games)

        print("A games has length: {} ".format(count))

        """ 
        
        Here is the pseudocode
        
        Try the first game, are the players there already?
        No? Then add the game and remove it from the list
        Yes? Go to the next game
        
        while list is not empty:
            
        
        """

        first_round = []
        second_round = []
        third_round = []
        fourth_round = []

        shrinking_list = a_games.copy()

        # Let's do the first round

        print("TOTAL LENGTH AT FIRST ROUND IS: {}".format(len(shrinking_list)))

        count = 0
        while len(first_round) < 8:
            print("Count is {}".format(count))
            ind_game = shrinking_list[count]
            if not self.does_list_contain_players(ind_game, first_round):
                first_round.append(ind_game)
                shrinking_list.remove(ind_game)
                print("First round size now {} ".format(len(first_round)))
            else:
                print("Couldn't schedule it")
            count += 1

        print("First round done. Shrinking list has:{} ".format(len(shrinking_list)))
        print(first_round)

        # Let's do the second round
        count = 0
        while len(second_round) < 10:
            ind_game = shrinking_list[count]
            if not self.does_list_contain_players(ind_game, second_round):
                second_round.append(ind_game)
                shrinking_list.remove(ind_game)
            count += 1

        print("Second round done. Shrinking list has:{} ".format(len(shrinking_list)))

        # Let's do the third round
        count = 0
        while len(third_round) < 10:
            ind_game = shrinking_list[count]
            if not self.does_list_contain_players(ind_game, third_round):
                third_round.append(ind_game)
                shrinking_list.remove(ind_game)
            count += 1

        print("Third round done. Shrinking list has:{} ".format(len(shrinking_list)))

        # Let's do the fourth round
        """
        count = 0
        while len(fourth_round) < 10:
            print("In fourth, at index: {} ".format(count))
            print("Length of list:{} ".format(len(shrinking_list)))
            ind_game = shrinking_list[count+1]
            if not self.does_list_contain_players(ind_game, fourth_round):
                fourth_round.append(ind_game)
                shrinking_list.remove(ind_game)
            count += 1
        """
        # Let's add what's left

        master_list.append(first_round)
        master_list.append(second_round)
        master_list.append(third_round)
        master_list.append(shrinking_list)

        """

        first_list = []
        for a in range(0, 10):
            first_list.append(a_games[a])

        master_list.append(first_list)

        second_list = []
        for a in range(10, 20):
            second_list.append(a_games[a])

        master_list.append(second_list)

        third_list = []
        for a in range(20, 30):
            third_list.append(a_games[a])

        master_list.append(third_list)

        fourth_list = []
        for a in range(30, 40):
            fourth_list.append(a_games[a])

        master_list.append(fourth_list)
        """

        return master_list

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
        times = ["6:00-6:10", "6:15-6:25", "6:30-6:40", "6:45-6:55",
                 "7:00-7:10", "7:15-7:25", "7:30-7:40", "7:45-7:55"]
        print("Schedule of all games")
        count = 1
        for ind_round in rounds:
            print("***************")

            print("Round {} ({}):".format(count, times[count - 1]))
            print("***************")
            board = 1
            for ind_game in ind_round:
                print("Board {}: {}".format(board, ind_game))
                board += 1
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

    def update_draw_dictionary(self, draw_dict, two_players):
        first_player_name = two_players[0].get_name()
        second_player_name = two_players[1].get_name()

        if first_player_name in draw_dict:
            draw_dict[first_player_name] += 1
        else:
            draw_dict[first_player_name] = 1

        if second_player_name in draw_dict:
            draw_dict[second_player_name] += 1
        else:
            draw_dict[second_player_name] = 1

        return

    def print_draw_report(self, rounds_list):
        """"
        So what we need to do here is go through the rounds and
        figure out how many games people played
        """

        print("IN DRAW REPORT")
        result_dictionary = {}
        for games_list in rounds_list:

            for ind_game in games_list:
                print(ind_game)
                two_players = ind_game.get_players()
                self.update_draw_dictionary(result_dictionary, two_players)

        print(result_dictionary)
