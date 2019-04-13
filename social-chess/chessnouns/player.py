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


    def __init__(self, name, level=1, late=False, vip=False):
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