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

    def return_result_numbers(self):
        """
        This method is just a check on the data.
        It will return wins, losses, and draws for
        the tournament.

        If there are no draws, it should return
        40 wins, 40 losses for 40 games, etc.

        """
        wins = 0
        byes = 0
        losses = 0
        draws = 0

        for player_key, draw in self._tournament_draw_dict.items():
            for ind_game in draw.get_games():
                if ind_game.was_drawn():
                    draws += 1
                elif ind_game.was_bye():
                    byes += 1
                elif ind_game.did_player_id_win(player_key):
                    wins += 1
                else:
                    losses += 1

        return wins, byes, losses, draws

    def get_total_number_of_games(self):
        return self._schedule.get_total_number_of_games()

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

    def calculate_playoff_candidates(self):
        """
        Here we are trying to figure out the top two people,
        or, if there are ties, the people tied for the top
        two slots
        :return:
        """

        finalists = []

        # First, let's get the list
        leader_list = sorted(self.get_leaderboard())

        top_person = leader_list[0]

        top_score = top_person.get_weighted_score()
        logger.debug("Top score was: {}".format(top_score))

        finalists.append(top_person)

        next_person = leader_list[1]
        next_score = next_person.get_weighted_score()
        logger.debug("Next score was: {}".format(next_score))

        finalists.append(next_person)

        # Now we have to figure out if the next person

        remaining_list = leader_list[2:]

        for possible_person in remaining_list:
            if possible_person.get_weighted_score() == next_score:
                finalists.append(possible_person)
            else:
                break

        player_break = False

        if len(finalists) > 2:
            return self._try_to_resolve_finalists(finalists)

        return player_break, finalists


    def _try_to_resolve_finalists(self, finalists):

        change = False
        new_finalists = []

        # The logic here isn't easy.
        # Let's first determine if the leader is alone
        top_score = finalists[0].get_weighted_score()
        second_score = finalists[1].get_weighted_score()

        if top_score > second_score:
            # OK, so the top guy is alone
            new_finalists.append(finalists[0])
        else:
            # Ugh, they are tied. Worse, that means
            # all of them are tied. This means we
            # need to see if any played each other
            pass

        return change, new_finalists


