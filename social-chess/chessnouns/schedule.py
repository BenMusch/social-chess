"""
This class will create a proposed schedule for a tournament.
Note: This is not the same thing as a tournament, as it does
not have a date, a playoff, a winner, or some other details
"""
import math
import chessnouns
from . import game


class Schedule(object):
    # This is the number of boards to play, it will determine
    # the number of simultaneous games
    _number_boards = 0

    # This is the length of the event
    _number_minutes = 160

    # Space between games
    _rounds_gap = chessnouns.STANDARD_GAME_GAP_TIME

    _game_time = chessnouns.STANDARD_GAME_TIME

    _number_of_rounds = 0

    # This is whether it is team or individual
    _team_play = False

    # This is the data structure that will hold the results
    # It will be an two-dimensional array. An array of rounds

    # We're going to keep track of this at the class level for convenience
    _total_number_of_players = 0

    _advanced_players = []
    _intermediate_players = []
    _beginner_players = []

    # This is a list of the two-part rounds we will have
    _rounds = list()

    def __repr__(self):
        return_line = "Schedule Object:\n"
        return_line += "Number of boards:{} Number of minutes in the tournament:{} Gap in minutes between each set of games:{}" \
                       " Time in minutes for each game:{} " \
                       "Team Play?:{} Have Playoff?:{}\n" \
                       "".format(self._number_boards, self._number_minutes, self._rounds_gap, self._game_time,
                                 self._team_play, self._have_playoff)
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


    def __init__(self, boards, time_per_game=chessnouns.STANDARD_GAME_TIME):

        self._number_boards = boards
        self._game_time = time_per_game

        print("So we have {} boards.".format(boards))
        # First thing we need to do is to create the arrays
        # But we need to figure out how many rounds we can have

        round_time = self._game_time + self._rounds_gap
        self._number_of_rounds = math.trunc(self._number_minutes / round_time)

        print("OK, we have space for {} rounds ".format(self._number_of_rounds))

        # Now we can create the array
        for r in range(0, self._number_of_rounds):
            # create new list
            print(self._rounds)
            print("Creating list # {}\n".format(r))
            self._rounds.append(list())

            current_round_list = self._rounds[r]

            print("We are at round: {}".format(r))

            for m in range(0, boards):
                print("Adding match #{}\n".format(m))
                current_round_list.append(game.Game())

            print("We are done with the round.")

        print(self)
