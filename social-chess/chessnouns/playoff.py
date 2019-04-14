"""
This class will be for the playoff round
The first player is white in this model
"""
from . import player
from . import game
from chessutilities import utilities
from chessexceptions import game_error
import chessnouns


class Playoff(object):
    _player_one = None
    _player_two = None

    _game = None

    def __init__(self, player_one, player_two):

        if not isinstance(player_one, player.Player) or not isinstance(player_two, player.Player):
            raise TypeError("You must initialize this with player objects, not names")

        self._player_one = player_one
        self._player_two = player_two

    def set_random_colors(self):
        # We will do randomness by getting a random color
        # and setting first player to it
        color = utilities.get_random_color()

        if color == chessnouns.COLOR_WHITE:
            self._game = game.Game(self._player_one, self._player_two, chessnouns.STANDARD_PLAYOFF_LENGTH)
        else:
            self._game = game.Game(self._player_two, self._player_one, chessnouns.STANDARD_PLAYOFF_LENGTH)

    def establish_player_one_as_white(self):
        self._game = game.Game(self._player_one, self._player_two, chessnouns.STANDARD_PLAYOFF_LENGTH)

    def establish_player_one_as_black(self):
        self._game = game.Game(self._player_two, self._player_one, chessnouns.STANDARD_PLAYOFF_LENGTH)

    def get_game(self):
        if self._game is None:
            raise game_error.GameError("You must select colors for the players")
        return self._game

    def get_player_one(self):
        return self._player_one

    def get_player_two(self):
        return self._player_two
