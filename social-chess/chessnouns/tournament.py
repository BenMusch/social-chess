"""
This class will keep track of an individual tournament
"""
from . import slot
from . import player
from . import game
from datetime import date
from chessutilities import utilities
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')


class Tournament(object):

    def __init__(self, schedule, tournament_name, tournament_date=None):

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

        rounds = self._schedule.get_rounds()
        count = 1
        logger.debug("Creating random results in round {}".format(count))
        for ind_round in rounds:
            for ind_game in ind_round:
                logger.debug("Setting result for game: {} ".format(ind_game))
                ind_game.set_likely_random_result()


    def create_random_results_for_round(self):
        pass

    def get_leaderboard(self):
        """
        This method will return a list of tuples, sorted

        We will go through the draw dictionary, tally up the score, and then
        add the entries to a list of slot objects, and then sort them

        """

        # FIXME: We need to check to see that results got created before
        # doing this

        leaderboard = []
        for player_key, draw in self._tournament_draw_dict.items():
            name = utilities.get_player_for_id(player_key).get_name()
            raw_points = draw.get_total_raw_points()
            weighted_points = draw.get_total_weighted_score()
            leaderboard.append(slot.Slot(name, raw_points, str(round(weighted_points, 2))))

        return leaderboard

