from . import game
from chessexceptions import scheduling_error


class Round(object):
    """
    A round is actually two sets of games, where everyone plays
    or gets a bye. Normally, a round would be a set of games,
    but a key requirement for such a social event is that people
    need a break between games to eat, drink, and socialize.

    This means that only half play at once. So a round is two
    sets of games exercising all the players. We will refer
    to the two sets of games as A and B.

    """

    # There will be a list of Games for the first set
    # and one for the second. It is important to know
    # that these lists may not be the same size, to
    # accommodate unusual numbers of players

    _round_number = 1
    _number_of_boards = 0
    _number_a_games = 0
    _number_b_games = 0

    _a_games = []
    _b_games = []

    def __init__(self, number_a_games, number_b_games, round_number):
        """
        To set this up, we're going to initialize the arrays
        with  the correct number of games

        :param number_a_games:
        :param number_b_games:
        :param round_number:
        """

        if not isinstance(number_a_games, int) or isinstance(number_b_games, int) or \
                isinstance(round_number, int):
            raise TypeError("You must initialize this class with three numbers")

        self._round_number = round_number

        # The convention we are using is that the second group has the maximum
        # number of boards
        self._number_of_boards = number_b_games
        self._number_a_games = number_a_games
        self._number_b_games = number_b_games

    def get_a_games(self):
        return self._a_games

    def get_b_games(self):
        return self._b_games

    def get_round_number(self):
        return self._round_number

    def add_to_round(self, game):
        if self.round_is_finished():
            raise scheduling_error.SchedulingError("You cannot add a game to a finished round.")

        # Is there room in a?
        if len(self._a_games) < self._number_a_games:
            self._a_games.append((game))
        elif len(self._b_games) < self._number_b_games:
            self._b_games.append((game))
        else:
            # We should not get here
            raise scheduling_error.SchedulingError("You cannot add a game to a finished round.")

    def round_is_finished(self):
        return len(self._a_games) < self._number_a_games and len(self._b_games) < self._number_b_games
