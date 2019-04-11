import math

"""
This module contains all of the objects we need
"""


class Player(object):
    """
    This class will represent a player
    """
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3

    _name = "Blank"
    _level = BEGINNER
    _late = False
    _vip = False


    def __repr__(self):
        return "{}({})".format(self._name, self._level)


    def __init__(self, name, level, late=False, vip=False):
        self._name = name
        self._level = level
        self._late = late
        self._vip = vip


    def name(self):
        return self._name


    def level(self):
        return self._level


    def is_vip(self):
        return self._vip


    def is_late(self):
        return self._vip


class Match(object):
    """
    This will represent a game
    """
    _white_player = Player("John Sixpack", 1)
    _black_player = Player("Jane Sixpack", 1)
    _game_time = 20

    WHITE_WINS = 0
    BLACK_WINS = 1
    DRAW = 2

    _result = DRAW

    def __repr__(self):
        return "White:{} Black:{} ".format(self._white_player, self._black_player)

    def __init__(self, white=Player("John Sixpack", 1), black=Player("Jane Sixpack", 1), time=20):
        self._white_player = white
        self._black_player = black
        self._game_time = time

    def get_white_player(self):
        return self._white_player


    def get_black_player(self):
        return self._black_player



    def set_time(self, time):
        self._game_time = time

    def get_time(self):
        return self._game_time

    def set_result(self, result):
        self._result = result

    def get_result(self):
        return self._result


class Schedule(object):

    # This is the number of boards to play, it will determine
    # the number of simultaneous games
    _number_boards = 0

    # This is the length of the event
    _number_minutes = 160

    # Space between games
    _rounds_gap = 10

    _game_time = 20

    _number_of_rounds = 0

    # This is whether it is team or individual
    _team_play = False

    # This will indicate whether we will have a playoff of
    # the top two scorers

    _have_playoff = False

    # This is the data structure that will hold the results
    # It will be an two-dimensional array. An array of rounds

    """
     rounds = 
     [ Match, Match, Match, Match, Match, Match ]
     ...
     [ Match, Match, Match, Match, Match, Match ]
    """

    # We're going to keep track of this at the class level for convenience
    _total_number_of_players = 0

    _advanced_players = []
    _intermediate_players = []
    _beginner_players = []


    _rounds = list()

    def __repr__(self):
        return_line = "Schedule Object:\n"
        return_line += "Number of boards:{} Number of minutes in the tournament:{} Gap in minutes between rounds:{}" \
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
        for individual_round in self._rounds:
            print("Getting list of matches in round {}\n".format(count))
            return_line += "Round: {}\n".format(count + 1)
            return_line += "******************\n"
            board_counter = 0
            for match in individual_round:
                return_line += "BOARD {} -- White: {} Black: {} \n".format(board_counter + 1, match.get_white_player(),
                                                                           match.get_black_player())
                board_counter += 1
            count += 1
            return_line += "-----\n"
        return_line += "-----\n"
        return return_line

    # The hard question is, what do we initialize with?
    # So the number of players will be static. But what do we do with the number of boards?
    # I guess we can try a maximum number of boards, then let
    def __init__(self, boards, time_per_game=20):

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
                print ("Adding match #{}\n".format(m))
                current_round_list.append(Match())

            print("We are done with the round.")

        print(self)
