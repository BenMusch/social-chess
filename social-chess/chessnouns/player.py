import chessnouns


class Player(object):
    """
    This class will represent a player
    """

    _name = chessnouns.NO_NAME
    _level = chessnouns.BEGINNER
    _late = False
    _vip = False

    def __repr__(self):
        return "{} Level: ({}) Late? {} VIP? {}".format(self._name, self._level, self._late, self._vip)

    def __init__(self, name, level=chessnouns.BEGINNER, late=False, vip=False):

        if not isinstance(name, str):
            print("We got an exception")
            raise Exception("Names must be strings")

        if level not in range(1, 4):
            print("We got an exception")
            raise Exception('Level value must be {}, {}, or {}'.format(chessnouns.BEGINNER, chessnouns.INTERMEDIATE,
                                                                       chessnouns.ADVANCED))

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
        return self._late

    def make_late(self):
        self._late = True

    def make_on_time(self):
        self._late = False
