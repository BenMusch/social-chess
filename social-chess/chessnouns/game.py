from . import player
import chessnouns
import random
from chessexceptions import game_error


class Game(object):
    """
    This will represent a game. It is one of the most
    important core components of the system.

    Some things:

    1. You initialize a game with the two players
    2. You do not choose the colors at that time.
    3. You can initialize a game as a bye

    """

    @classmethod
    def create_bye_game(cls, player_getting_bye):
        return Game(player_getting_bye, player.Player.make_bye_player(), onewhite=False, twowhite=False, bye=True)

    def __str__(self):

        if self._color_code == chessnouns.NO_COLOR_SELECTED:
            color_string = "No colors selected"
        elif self._color_code == chessnouns.PLAYER_ONE_IS_WHITE:
            color_string = "White [1], Black [2]"
        else:
            color_string = "Black [1], White[2]"

        return_line = "{}({}) vs. {}({}) ".format(self._player_one.get_name(),
                                              self._player_one.get_level(),
                                              self._player_two.get_name(),
                                              self._player_two.get_level(),
                                              end=" ")
        return_line += color_string

        return return_line

    def make_player_one_white(self):
        self._color_code = chessnouns.PLAYER_ONE_IS_WHITE

    def make_player_two_white(self):
        self._color_code = chessnouns.PLAYER_ONE_IS_BLACK

    def __init__(self, player_one, player_two, time=chessnouns.STANDARD_GAME_TIME,
                 onewhite=False, twowhite=False, bye=False):

        self._bye = bye
        self._player_one = player_one
        self._player_two = player_two
        self._result = chessnouns.NO_RESULT
        self._game_time = time

        if onewhite:
            self._color_code = chessnouns.PLAYER_ONE_IS_WHITE
        elif twowhite:
            self._color_code = chessnouns.PLAYER_ONE_IS_BLACK
        else:
            self._color_code = chessnouns.NO_COLOR_SELECTED

    def are_colors_set(self):
        return self._color_code != chessnouns.NO_COLOR_SELECTED

    def set_random_colors(self):

        r1 = random.randint(0, 2)

        if r1 == 1:
            self._color_code = chessnouns.PLAYER_ONE_IS_WHITE
        else:
            self._color_code = chessnouns.PLAYER_ONE_IS_BLACK

    def contains_player(self, player):
        return self._player_one == player or self._player_two == player

    def is_bye(self):
        return self._bye

    def get_players(self):
        return [self._player_one, self._player_two]

    def is_game_over(self):
        return self._result != chessnouns.NO_RESULT

    def flip_colors(self):

        if self._color_code == chessnouns.NO_COLOR_SELECTED:
            raise game_error.GameError("You cannot flip colors before selecting them")
        elif self._color_code == chessnouns.PLAYER_ONE_IS_WHITE:
            self._color_code = chessnouns.PLAYER_ONE_IS_BLACK
        else:
            self._color_code = chessnouns.PLAYER_ONE_IS_WHITE

    def get_white_player(self):
        if self._color_code == chessnouns.NO_COLOR_SELECTED:
            raise game_error.GameError("You cannot get the white player without selecting colors")
        if self._color_code == chessnouns.PLAYER_ONE_IS_WHITE:
            return self._player_one
        else:
            return self._player_two

    def get_black_player(self):
        if self._color_code == chessnouns.NO_COLOR_SELECTED:
            raise game_error.GameError("You cannot get the black player without selecting colors")
        if self._color_code == chessnouns.PLAYER_ONE_IS_BLACK:
            return self._player_one
        else:
            return self._player_two

    def set_time(self, time):
        self._game_time = time

    def get_time(self):
        return self._game_time

    def set_result(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def get_winning_player(self):

        if self._bye is True:
            return self._player_one

        if self._color_code == chessnouns.NO_COLOR_SELECTED:
            raise game_error.GameError("You cannot get the winning player without selecting colors")
        if self._result == chessnouns.NO_RESULT:
            raise game_error.GameError("You cannot get the winning player without a result")
        if self._color_code == chessnouns.PLAYER_ONE_IS_WHITE and self._result == chessnouns.WHITE_WINS:
            return self._player_one
        else:
            return self._player_two
