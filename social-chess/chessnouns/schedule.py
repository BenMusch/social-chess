"""
This class will create a proposed schedule for a tournament.
Note: This is not the same thing as a tournament, as it does
not have a date, a playoff, a winner, or some other details
"""
import chessnouns
from . import game, round, draw
from random import shuffle
from chessutilities import utilities
from chessexceptions import unsolveable_error


class Schedule(object):
    # This is the number of boards to play, it will determine
    # the number of simultaneous games
    _number_boards = 0

    _number_of_rounds = 0

    # The lopsided variable is about game sets that differ by one
    # each time
    _lopsided = False

    # This variable determines whether or not we need to have one
    # person sit out one game each round
    _bye_round = False

    # This is whether it is team or individual
    _team_play = False

    _players = list()

    # We're going to keep track of this at the class level for convenience
    _total_number_of_players = 0

    _advanced_players = []
    _intermediate_players = []
    _beginner_players = []

    # This is a list of the two-part rounds we will have
    _rounds = list()

    def __repr__(self):

        return_line = "Schedule Object:\n"
        return_line += "There are {} rounds.\n".format(len(self._rounds))
        return return_line

    def __str__(self):
        return_line = "There are {} rounds.\n".format(len(self._rounds))
        return_line += "-----\n"

        count = 0

        print("There are {} rounds in the array.\n".format(len(self._rounds)))
        for two_part_round in self._rounds:
            print("Getting list of matches in round {}\n".format(count))
            return_line += "Round: {}\n".format(count + 1)
            return_line += "******************\n"
            board_counter = 0

            # First set
            for match in two_part_round[0]:
                return_line += "BOARD {} -- White: {} Black: {} \n".format(board_counter + 1, match.get_white_player(),
                                                                           match.get_black_player())
                board_counter += 1
            count += 1
            return_line += "-----\n"

            # Second set
            board_counter = 0
            for match in two_part_round[1]:
                return_line += "BOARD {} -- White: {} Black: {} \n".format(board_counter + 1, match.get_white_player(),
                                                                           match.get_black_player())
                board_counter += 1
            count += 1
            return_line += "-----\n"

        return_line += "-----\n"
        return return_line

    def __init__(self, players, number_of_rounds, lopsided, bye, number_of_boards):

        self._players = players
        self._bye_round = bye
        self._lopsided = lopsided
        self._number_of_rounds = number_of_rounds
        self._number_boards = number_of_boards

    def set_up_rounds(self):
        """
        This creates the round data structure, which will begin by being populated with
        empty game objects

        :return:
        """

        # In our model, the b part of the round is always equal to
        # the number of boards
        number_b = self._number_boards

        # The a part of the round is either equal to the number of
        # boards, or it is one less, if the tournament is lopsided

        number_a = self._number_boards

        if self._lopsided:
            number_a -= 1

        for count in range(0, self._number_of_rounds):
            # So we need two lists
            self._rounds.append(round.Round(number_a, number_b, count + 1))

    def get_rounds(self):
        return self._rounds

    def get_beginner_players(self):
        return self._beginner_players

    def get_intermediate_players(self):
        return self._intermediate_players

    def get_advanced_players(self):
        return self._advanced_players

    def sort_players(self):
        """
        This method breaks the players into their categories

        :return:
        """
        for player in self._players:
            if player.get_level() == chessnouns.BEGINNER:
                self._beginner_players.append(player)
            elif player.get_level() == chessnouns.IMPROVING or player.get_level() == chessnouns.ADEPT:
                self._intermediate_players.append(player)
            else:
                assert player.get_level() == chessnouns.KING or player.get_level() == chessnouns.KNIGHT
                self._advanced_players.append(player)

    def shuffle_players(self):
        """
        This function randomizes the order of the players to create different pairings
        each run
        :return:
        """
        shuffle(self._beginner_players)
        shuffle(self._intermediate_players)
        shuffle(self._advanced_players)

    def set_up_draws(self, number_of_rounds):

        for player in self._beginner_players:
            player.set_draw(number_of_rounds)

        for player in self._intermediate_players:
            player.set_draw(number_of_rounds)

        for player in self._advanced_players:
            player.set_draw(number_of_rounds)

    def schedule_advanced_players(self):
        """
        We are going to get the advanced players set up first.

        :return:
        """

        # We need to set draw objects for all players
        # FIXME : We need this to be pulled out for somewhere else
        self.set_up_draws(chessnouns.DEFAULT_NUMBER_OF_GAMES)

        # Let's do round 1
        # It's best to think of a round as a single list,
        # rather than two lists together, as we see in the
        # round class.

        for candidate_player in self._advanced_players:
            if candidate_player.draw.has_full_draw():
                continue
            # So he needs a game from another player
            # Let's try advance first
            scheduled = False
            for other_player in self._advanced_players:
                scheduled = Schedule.try_scheduling_these_guys(candidate_player, other_player)

            # Did we schedule the game?
            if not scheduled:
                # So this means all the other advanced players
                # are scheduled, so we need to try intermediates
                for medium_player in self._intermediate_players:
                    scheduled = Schedule.try_scheduling_these_guys(candidate_player, medium_player)

            if not scheduled:
                # So this means all the other intermediate players
                # are scheduled, so we need to try beginners
                for beginner_player in self._beginner_players:
                    scheduled = Schedule.try_scheduling_these_guys(candidate_player, beginner_player)

            if not scheduled:
                # FIXME: Let's try adding a bye - is this the answer?
                candidate_player.draw.add_bye()

        # OK, now let us print and see
        utilities.print_player_draws(self._advanced_players)

    @classmethod
    def try_scheduling_these_guys(cls, first, second):
        """
        Factored out this code
        :param first:
        :param second:
        :return: bool - did we succeed?
        """
        # First, it's not him, right?
        if first is second:
            return False
        # Is the other player all scheduled?
        if second.draw.has_full_draw():
            return False
        # Has the other player already played this guy?
        if second.draw.has_played_player_id(first.get_id):
            return False
        # OK. So we can schedule this!
        first.draw.add_matchup(second.get_id())
        second.draw.add_matchup(first.get_id())
        return True

    def schedule_beginner_players(self):
        for candidate_player in self._beginner_players:
            if candidate_player.draw.has_full_draw():
                continue
            # So he needs a game from another player
            scheduled = False
            for other_player in self._beginner_players:
                scheduled = Schedule.try_scheduling_these_guys(candidate_player, other_player)

            if not scheduled:
                # FIXME: Let's try adding a bye - is this the answer?
                candidate_player.draw.add_bye()

        # OK, now let us print and see
        utilities.print_player_draws(self._beginner_players)

    def schedule_intermediate_players(self):

        for candidate_player in self._intermediate_players:
            if candidate_player.draw.has_full_draw():
                continue
            # So he needs a game from another player
            # Let's try advance first
            scheduled = False
            for other_player in self._intermediate_players:
                scheduled = Schedule.try_scheduling_these_guys(candidate_player, other_player)

            # Did we schedule the game?
            if not scheduled:
                # So this means all the other intermediate players
                # are scheduled, so we need to try beginners
                for beginner_player in self._beginner_players:
                    scheduled = Schedule.try_scheduling_these_guys(candidate_player, beginner_player)

            if not scheduled:
                # FIXME: Let's try adding a bye - is this the answer?
                candidate_player.draw.add_bye()

        # OK, now let us print and see
        utilities.print_player_draws(self._intermediate_players)

    def schedule_next_game(self, round_number):
        pass

    def fill_in_rounds(self):
        """
        So what we are going to do is take everyone's draws
        and figure out when the games are all going to take place
        :return:
        """
