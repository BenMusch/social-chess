from . import player
from chessutilities import utilities


class Draw(object):
    """
    The draw will be the lineup that a player has in a
    tournament. It will be used in creating the schedule,
    in order to help figure out who needs to be paired,
    and it will also be used during a tournament to the
    matches for a player
    """

    _matchups = []
    _draw_player = None

    # The number of rounds is the maxumum number
    # of games
    _number_of_rounds = 0

    def __init__(self, player_for_draw, number_rounds):
        assert isinstance(player_for_draw, player.Player)
        self._draw_player = player_for_draw
        self._number_of_rounds = number_rounds

    def __repr__(self):
        return_line = ""
        for person_id in self._matchups:
            selected_player = utilities.get_player_for_id(person_id)
            return_line += self._draw_player.get_name() + " vs. " + selected_player.get_name()
        return return_line

    def get_number_of_rounds(self):
        return self._number_of_rounds

    def get_rounds_left(self):
        return self._number_of_rounds - len(self._matchups)

    def get_matchups(self):
        return self._matchups

    def number_matchups_scheduled(self):
        return len(self._matchups)

    def add_matchup(self, opposing_player):
        assert isinstance(opposing_player, player.Player)
        self._matchups.append(opposing_player.get_id())

    def clear_matchups(self):
        self._matchups = []

    def has_full_draw(self):
        return len(self._matchups) == self._number_of_rounds

    def get_player(self):
        return self._draw_player
