"""
This class will keep track of an individual tournament
"""
import chessnouns
from . import slot
from . import player
from . import game
from datetime import date
from chessutilities import utilities
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('chess')


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
                # logger.debug("Setting result for game: {} ".format(ind_game))
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

    def get_leaderboard(self, maximum_number=0):
        """
        This method will return a list of tuples, sorted

        We will go through the draw dictionary, tally up the score, and then
        add the entries to a list of slot objects, and then sort them

        """

        # FIXME: We need to check to see that results got created before
        # doing this

        slot_list = []
        for player_key, draw in self._tournament_draw_dict.items():
            # tourney_player = utilities.get_player_for_id(player_key)
            tourney_player = self._schedule.get_scheduled_player_for_id(player_key)
            raw_points = draw.get_total_raw_points()
            weighted_points = draw.get_total_weighted_score()
            rounds_completed = draw.get_number_of_rounds_completed()
            slot_list.append(slot.Slot(tourney_player, rounds_completed, raw_points,
                                       str(round(weighted_points, chessnouns.WEIGHTED_SCORE_DECIMAL_PRECISION))))

        if maximum_number == 0:
            return sorted(slot_list)
        else:
            # So we only want the top X players
            return sorted(slot_list)[:maximum_number]

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
            logger.debug("We have more than two finalists with scores: ")
            for final_person in finalists:
                logger.debug(str(final_person.get_weighted_score()))
            return self._try_to_resolve_finalists(finalists)

        return player_break, finalists

    def _try_to_resolve_finalists(self, finalists_slots):

        # FIXME: We need to be careful about how draws are scored

        logger.debug("PLAYERS WE ARE RESOLVING:")
        for final_slot in finalists_slots:
            logger.debug(final_slot.get_player().get_name() + " | " + str(final_slot.get_player().get_level()))

        change = False
        new_finalists = []

        # The logic here isn't easy.
        # Let's first determine if the leader is alone
        top_score = finalists_slots[0].get_weighted_score()
        second_score = finalists_slots[1].get_weighted_score()

        if top_score > second_score:
            # OK, so the top guy is alone
            new_finalists.append(finalists_slots[0])
            logger.info("So our clear winner was: {}".format(finalists_slots[0].get_player().get_name()))
            # We also need to remove him
            finalists_slots.remove(finalists_slots[0])

            # OK, let's see how many others
            if len(finalists_slots) == 2:
                # So we only have two left
                # Let's see if they played
                second_player = finalists_slots[0].get_player()
                logger.debug("Second player was: {}".format(second_player.get_name()))
                third_player = finalists_slots[1].get_player()
                logger.debug("Third player was: {}".format(third_player.get_name()))
                played_game = self._schedule.get_common_game(second_player, third_player)

                if played_game:

                    if played_game.was_drawn():
                        # Ugh.
                        # OK, let's see if they were the same level
                        if second_player.get_level() < third_player.get_level():
                            # OK, that means we give the second player a performance bonus
                            # as the underdog with same points, and he gets the slot
                            logger.info("We used a performance bonus: second greater than third in a draw")
                            new_finalists.append(second_player)
                            change = True
                            return change, new_finalists
                        elif third_player.get_level() < second_player.get_level():
                            # So the other guy gets the performance bonus
                            logger.info("We used a performance bonus: third greater than second in a draw")
                            new_finalists.append(third_player)
                            change = True
                            return change, new_finalists
                        else:
                            # They are the same level also. So we fail
                            logger.info("They were equal in the draw, no performance bonus")
                            new_finalists += [second_player, third_player]
                            return change, finalists_slots
                    elif played_game.did_player_id_win(second_player.get_id()):
                        logger.info("Second beat third. We broke a tie with the played function")
                        new_finalists.append(finalists_slots[1])
                        change = True
                        return change, new_finalists
                    else:
                        logger.info("Third beat second. We broke a tie with the played function")
                        new_finalists.append(finalists_slots[2])
                        change = True
                        return change, new_finalists

                else:
                    # So they didn't play
                    # Let's see if we can do a performance bonus
                    if second_player.get_level() < third_player.get_level():
                        # OK, that means we give the second player a performance bonus
                        # as the underdog with same points, and he gets the slot
                        logger.info("We used a performance bonus - second was lower than third")
                        new_finalists.append(second_player)
                        change = True
                        return change, new_finalists
                    elif third_player.get_level() < second_player.get_level():
                        # So the other guy gets the performance bonus
                        logger.info("We used a performance bonus = third was lower than second")
                        new_finalists.append(third_player)
                        change = True
                        return change, new_finalists
                    else:
                        # They are the same level also. So we fail
                        logger.info("Didn't play a game. They were equal, no performance bonus")
                        new_finalists += [second_player, third_player]
                        return change, new_finalists

            if len(finalists_slots) > 2:
                # So we have a top person, and more than 2 runners-up
                # Egad.
                # OK, let's see if we can grab one by being an upset
                # candidate

                # Let's see if we can sort the three other players
                # by who they lost against

                # First, let's see if there are differences:
                logger.info("We have more than 2 after the top person")

                for item in finalists_slots:
                    logger.info(str(item))
                losses_total = 0
                for finalist_slot in finalists_slots:
                    candidate_player = finalist_slot.get_player()
                    logger.info("Player is {}".format(candidate_player))
                    candidate_draw = candidate_player.get_draw()
                    logger.info("Draw was {}".format(candidate_draw))
                    losses_total += candidate_draw.get_total_loss_points()

                if losses_total % len(finalists_slots) == 0:
                    # OK, so no differences in losses, we fail
                    logger.info("There were no differences after accounting for losses")
                    return change, finalists_slots
                else:
                    # OK, so we have some differences
                    logger.info("Let's get the list sorted by the losses.")
                    new_list = sorted(finalists_slots, key=self._get_points_for_player, reverse=False)
                    for lost_slot in new_list:
                        lost_player = lost_slot.get_player()
                        logger.info("Player: {}, Loss points: {}".format(lost_player.get_name(),
                                                                         lost_player.get_draw().get_total_loss_points()))
                        logger.info(lost_player.get_draw().output_win_loss_record())


                return change, finalists_slots

        else:
            # Ugh, they are tied. Worse, that means
            # all of them are tied. This means we
            # need to see if any played each other

            # For now, let's try upset candidates
            return change, finalists_slots

        return change, new_finalists

    def _get_points_for_player(self, item):
        return item.get_player().get_draw().get_total_loss_points()

    def _look_for_upset_candidate(self, candidate_list):

        found = False

        number_found = 0

        # First, we need to find out if there are any difference
        # among the levels, for any number of candidates
        total = 0

        for candidate in candidate_list:
            total += candidate.get_level()

        # OK, now we should be able to see
        if total % len(candidate_list) == 0:
            # We're dead. They're all the same
            return False, None

        else:
            # Good, we have at least some difference
            pass

        return found, player
