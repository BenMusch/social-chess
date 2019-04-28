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

    def __init__(self, number_of_games, round_number):
        """
        To set this up, we're going to initialize the arrays
        with  the correct number of games
        :param number_a_games:
        :param number_b_games:
        :param round_number:
        """

        self._number_of_games = number_of_games
        self._round_number = round_number

        # The convention we are using is that the second group has the maximum
        # number of boards

        self._games = []

    def get_games(self):
        return self._games

    def get_round_number(self):
        return self._round_number

    def add_game_to_round(self, game):
        if self.round_is_finished():
            raise scheduling_error.SchedulingError("You cannot add a game to a finished round.")

        # Is there room in a?
        if len(self._games) < self._number_of_games:
            self._games.append((game))
        else:
            # We should not get here
            raise scheduling_error.SchedulingError("You cannot add a game to a finished round.")

    def round_is_finished(self):
        return len(self._games) == self._number_of_games
