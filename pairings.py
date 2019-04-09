import math
"""
This module contains all of the objects we need
"""

"""
This class will represent a player
"""
class Player(object):

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

"""
This will represent a game
"""
class Match(object):

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

    def set_time(self,time):
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

    _rounds = []

    def __repr__(self):
        return "There are {} rounds. ".format(self._number_of_rounds)


    def __init__(self, boards, time_per_game=20):

        self._number_boards = boards
        self._game_time = time_per_game

        print ("So we have {} boards.".format(boards))
        # First thing we need to do is to create the arrays
        # But we need to figure out how many rounds we can have

        round_time = self._game_time + self._rounds_gap
        self._number_of_rounds = math.trunc(self._number_minutes / round_time)

        print ("OK, we have space for {} rounds ".format(self._number_of_rounds))

        # Now we can create the array
        for r in range(0,self._number_of_rounds):
            print("We are at: {}".format(r))
            self._rounds.append(list())
            for m in range(0,boards):
                self._rounds[r].append(Match())

        print(self)

