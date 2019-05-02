"""
This class will keep track of an individual tournament
"""
from . import schedule
from . import player
from . import game
from . import round


class Tournament(object):
    def __init__(self):

        # The draw dictionary has the player ids
        # as keys, and the draw objects as values

        self._event_date  = ""
        self._draw_dict = {}
        self._playoff = None # This will just be a game
        self._winner = None # This will be the id of the winner



