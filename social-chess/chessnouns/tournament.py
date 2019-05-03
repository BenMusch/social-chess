"""
This class will keep track of an individual tournament
"""
from . import schedule
from . import player
from . import game
from . import round
from datetime import date


class Tournament(object):

    def __init__(self, schedule, tournament_name, tournament_date):

        # The draw dictionary has the player ids
        # as keys, and the draw objects as values

        if not tournament_date:
            self._event_date = date.today()
        else:
            self._event_date = tournament_date

        self._name = tournament_name
        self._schedule = schedule
        self._playoff = None  # This will just be a game
        self._winner = None  # This will be the id of the winner

        # Now we need to build a dictionary for the players,
        # where the the key is the id, value is the draw
        self._tournament_draw_dict = {ind_player.get_id(): ind_player.get_draw() for ind_player in
                                      self._schedule.get_players()}


    def create_random_results_all(self):
        pass

    def create_random_results_for_round(self):
        pass

    def get_leaderboard(self):
        """
        This method will return a list of tuples, sorted
        """
