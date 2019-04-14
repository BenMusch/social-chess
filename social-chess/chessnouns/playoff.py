"""
This class will be for the playoff round
"""
from . import player
from . import game
from chessutilities import utilities
import chessnouns


class Playoff(object):

    _player_one = None
    _player_two = None

    _game = None

    def __init__(self, player_one, player_two):

        if not isinstance(player_one,chessnouns.player) or not isinstance(player_two,chessnouns.player):
            raise TypeError("You must initialize this with player objects, not names")

        self._player_one = player_one
        self._player_two = player_two

    def set_random_colors(self):
        # We will do randomness by getting a random color
        # and setting first player to it
        color = utilities.get_random_color()

        if color == chessnouns.COLOR_WHITE:
            self._game = chessnouns.game(self._player_one, self._player_two, chessnouns.STANDARD_PLAYOFF_LENGTH)
        else:
            self._game = chessnouns.game(self._player_two, self._player_one, chessnouns.STANDARD_PLAYOFF_LENGTH)

    def choose_white_player_one(self):
        self._game = chessnouns.game(self._player_one, self._player_two, chessnouns.STANDARD_PLAYOFF_LENGTH)

    def choose_black_player_one(self):
        self._game = chessnouns.game(self._player_two, self._player_one, chessnouns.STANDARD_PLAYOFF_LENGTH)

    def get_game(self):
        return self._game

