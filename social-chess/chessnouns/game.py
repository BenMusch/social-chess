from . import player

class Game(object):
    """
    This will represent a game
    """
    _white_player = player.Player("John Sixpack", 1)
    _black_player = player.Player("Jane Sixpack", 1)
    _game_time = 20

    WHITE_WINS = 0
    BLACK_WINS = 1
    DRAW = 2

    _result = None

    def __str__(self):
        return "White:{} Black:{} ".format(self._white_player, self._black_player)

    def __init__(self, white=player.Player("John Sixpack", 1), black=player.Player("Jane Sixpack", 1), time=20):
        self._white_player = white
        self._black_player = black
        self._game_time = time

        # We need to test for a bye
        if self._white_player.name == "Bye":
            self._result = self.BLACK_WINS
        elif self._black_player.name == "Bye":
            self._result = self.WHITE_WINS


    def is_game_over(self):
        return self._result is not None

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

