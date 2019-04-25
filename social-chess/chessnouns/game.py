from . import player
import chessnouns
import random


class Game(object):
    """
    This will represent a game
    """
    def __str__(self):
        return "White:{} Black:{} ".format(self._white_player.get_name(), self._black_player.get_name())

    def __init__(self, player_one, player_two, time=chessnouns.STANDARD_GAME_TIME, onewhite=False, twowhite=False):

        # We need to test for a bye
        if player_one.get_id() == chessnouns.BYE_ID:
            self._white_player = player_one
            self._black_player = player_two
            self._result = chessnouns.BLACK_WINS
        elif player_two.get_id() == chessnouns.BYE_ID:
            self._white_player = player_two
            self._black_player = player_one
            self._result = chessnouns.WHITE_WINS
        else:
            if onewhite:
                self._white_player = player_one
                self._black_player = player_two
            elif twowhite:
                self._white_player = player_two
                self._black_player = player_one
            else:

                r1 = random.randint(0, 2)

                if r1 == 1:
                    self._white_player = player_one
                    self._black_player = player_two
                else:
                    self._white_player = player_two
                    self._black_player = player_one

        self._game_time = time

    def is_game_over(self):
        return self._result is not None

    def flip_colors(self):
        self._white_player, self._black_player = self._black_player, self._white_player

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
