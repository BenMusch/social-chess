from chessnouns import player
import chessnouns
import pytest

class TestNouns(object):

    def test_create_player_exceptions(self):

        # Test for fail on player name is not a string
        with pytest.raises(Exception):
            assert player.Player(999)

        # Test for fail with invalid level
        with pytest.raises(Exception):
            assert player.Player("Ed Lyons", 0, False, False)


    def test_constants(self):

        # Here we are just testing that nobody accidentally
        # messed with the constants in init.py

        assert chessnouns.BEGINNER == 1
        assert chessnouns.INTERMEDIATE == 2
        assert chessnouns.ADVANCED == 3

        assert chessnouns.WHITE_WINS == 0
        assert chessnouns.BLACK_WINS == 1
        assert chessnouns.DRAW == 2




