from chessnouns import player, round
import chessnouns
import pytest


class TestNouns(object):

    def test_create_player_exceptions(self):
        # Test for fail on player name is not a string
        with pytest.raises(TypeError):
            assert player.Player(999)

        # Test for fail with invalid level
        with pytest.raises(ValueError):
            assert player.Player("Ed Lyons", 0, False, False)

    def test_player_attributes(self):
        p = player.Player("Ed Lyons", chessnouns.ADVANCED, False, False)

        assert p.name() == "Ed Lyons"
        assert not p.is_late()
        assert not p.is_vip()

        # Make flag changes
        p.make_late()
        assert p.is_late()

        p.make_on_time()
        assert not p.is_late()

    def test_round_object(self):
        test_round = round.Round(3, 4, 1)

        a_list = test_round.get_a_games()
        b_list = test_round.get_b_games()
        round_number = test_round.get_round_number()

        assert isinstance(a_list, list)
        assert isinstance(b_list, list)
        assert round_number == 1

        assert len(a_list) == 3
        assert len(b_list) == 4

        assert a_list[0] == None
        assert b_list[0] == None

    def test_constants(self):
        # Here we are just testing that nobody accidentally
        # messed with the constants in init.py

        assert chessnouns.BEGINNER == 1
        assert chessnouns.INTERMEDIATE == 2
        assert chessnouns.ADVANCED == 3

        assert chessnouns.WHITE_WINS == 0
        assert chessnouns.BLACK_WINS == 1
        assert chessnouns.DRAW == 2

        assert chessnouns.COLOR_BLACK == 1
        assert chessnouns.COLOR_WHITE == 0

        assert chessnouns.NO_NAME == "None"
        assert chessnouns.BYE_NAME == "Bye"
        assert chessnouns.DEFAULT_FIRST_PLAYER_NAME == "John Smith"
        assert chessnouns.DEFAULT_SECOND_PLAYER_NAME == "Jane Smith"

        assert chessnouns.STANDARD_GAME_TIME == 10
        assert chessnouns.STANDARD_GAME_GAP_TIME == 5
        assert chessnouns.STANDARD_EVENT_LENGTH == 120
        assert chessnouns.STANDARD_PLAYOFF_LENGTH == 20

    def test_playoff_initialization(self):
        pass

    def test_playoff_set_colors(self):
        pass

    def test_playoff_get_game(self):
        # Here we are going to test that our selected options
        # actually changed the underlying game options
        pass