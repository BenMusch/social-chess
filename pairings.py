"""
This module contains all of the objects we need
"""
class Pairings(object):

    # This is the data structure that will hold the results
    # It will be an two-dimensional array. An array of rounds

    rounds = []

    def __init__(self):
        pass

"""
This will represent a game
"""
class Match(object):

    _white_player = None
    _black_player = None
    _game_time = 20

    WHITE_WINS = 0
    BLACK_WINS = 1
    DRAW = 2

    _result = DRAW

    def __init__(self, white=player_one, black=player_two, time=20):
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

