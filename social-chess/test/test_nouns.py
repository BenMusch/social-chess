from chessnouns import player, round, game, draw
import chessnouns
import pytest
from chessutilities import utilities
from chessexceptions import game_error


class TestNouns(object):

    def test_create_player_exceptions(self):
        # Test for fail on player name is not a string
        with pytest.raises(TypeError):
            assert player.Player(1, 999)

        # Test for fail with invalid level
        with pytest.raises(ValueError):
            assert player.Player(1, "Ed Lyons", 0, False, False)

    def test_player_attributes(self):
        p = player.Player(1, "Ed Lyons", chessnouns.KING, False, False)

        assert p.get_name() == "Ed Lyons"
        assert not p.is_late()
        assert not p.is_vip()

        # Make flag changes
        p.make_late()
        assert p.is_late()

        p.make_on_time()
        assert not p.is_late()

    def test_round_object(self):
        test_round = round.Round(2, 2, 1)

        a_list = test_round.get_a_games()
        b_list = test_round.get_b_games()
        round_number = test_round.get_round_number()

        assert isinstance(a_list, list)
        assert isinstance(b_list, list)
        assert round_number == 1

        assert len(a_list) == 0
        assert len(b_list) == 0

        # OK, so let us add some games
        # We need four total games with 8 players

        player_one = player.Player(1, "John", chessnouns.IMPROVING, False, False)
        player_two = player.Player(2, "Sally", chessnouns.IMPROVING, False, False)
        player_three = player.Player(3, "Sue", chessnouns.IMPROVING, False, False)
        player_four = player.Player(4, "Mark", chessnouns.IMPROVING, False, False)
        player_five = player.Player(5, "George", chessnouns.IMPROVING, False, False)
        player_six = player.Player(6, "Larry", chessnouns.IMPROVING, False, False)
        player_seven = player.Player(7, "Marcus", chessnouns.IMPROVING, False, False)
        player_eight = player.Player(8, "Janus", chessnouns.IMPROVING, False, False)

        # We now need some games
        game_one = game.Game(player_one, player_two)
        game_two = game.Game(player_one, player_three)
        game_three = game.Game(player_two, player_three)
        game_four = game.Game(player_five, player_seven)

        # Now let's add some to the round

        test_round.add_to_round(game_one)

        # What is the state of the round?

        # First, let's see if the round is done
        assert test_round.round_is_finished() is False
        assert len(test_round.get_a_games()) == 1

        # And let's be sure that the b games are intact
        assert len(test_round.get_b_games()) == 0





