from . import player
from chessutilities import utilities
import chessnouns


class Draw(object):
    """
    The draw will be the lineup that a player has in a
    tournament. It will be used in creating the schedule,
    in order to help figure out who needs to be paired,
    and it will also be used during a tournament to the
    matches for a player
    """

    def __init__(self, player_for_draw, number_rounds):
        print("Draw initialized for {}({}) ".format(player_for_draw.get_name(), player_for_draw.get_level()))
        self._matchups = list()
        print("Number of matchups at init is {} ".format(len(self._matchups)))
        assert isinstance(player_for_draw, player.Player)
        self._draw_player = player_for_draw
        self._number_of_rounds = number_rounds

    def __str__(self):
        return_line = "{}'s ({}) Draw--- ".format(self._draw_player.get_name(), self._draw_player.get_level(), end= "++")
        for person_id in self._matchups:
            selected_player = utilities.get_player_for_id(person_id)
            return_line += selected_player.get_name() + "({}) | ".format(selected_player.get_level())
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
        #print("Adding matchup for: {} opponent: {} ".format(self._draw_player.get_name(), opposing_player.get_name()))
        self._matchups.append(opposing_player.get_id())

    def add_bye(self):
        self._matchups.append(chessnouns.BYE_ID)

    def clear_matchups(self):
        self._matchups = []

    def has_full_draw(self):
        #print("He has {} matchups in rounds {} ".format(len(self._matchups), self._number_of_rounds))
        return len(self._matchups) >= self._number_of_rounds

    def get_player(self):
        return self._draw_player

    def has_played_player_id(self, id):
        """
        This is a convenience method for
        checking to see if someone has already been scheduled
        :param id: id
        :return: bool
        """
        return id in self._matchups
