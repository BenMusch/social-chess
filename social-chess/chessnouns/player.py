import chessnouns
from . import draw


class Player(object):
    """
    This class will represent a player
    """

    _id = 0
    _name = chessnouns.NO_NAME
    _level = chessnouns.BEGINNER
    _late = False
    _vip = False

    # This is going to be a temporary variable used in scheduling
    _draw = None

    def __repr__(self):
        return "{} Level: ({}) Late? {} VIP? {}".format(self._name, self._level, self._late, self._vip)

    def __init__(self, identifier, name, level=chessnouns.BEGINNER, late=False, vip=False):

        if not isinstance(name, str):
            print("We got an exception")
            raise TypeError("Names must be strings")

        if level not in range(1, 6):
            print("We got an exception")
            raise ValueError('Level value must be {} to  {}'.format(chessnouns.BEGINNER, chessnouns.KING))

        self._id = identifier
        self._name = name
        self._level = level
        self._late = late
        self._vip = vip

    def set_draw(self, number_rounds):
        self._draw = draw.Draw(self, number_rounds)

    def get_draw(self):
        return self._draw

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_level(self):
        return self._level

    def is_vip(self):
        return self._vip

    def is_late(self):
        return self._late

    def make_late(self):
        self._late = True

    def make_on_time(self):
        self._late = False
