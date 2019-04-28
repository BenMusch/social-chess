import pytest
import chessnouns
from chessnouns import player, game

"""
This group of tests are for the game class
Fixtures are first, then the tests
"""


@pytest.fixture(scope="module")
def get_games(self):
    """
    This fixture gets games
    :param self:
    :return:
    """
    games = []
    return games


def test_game_init():
    new_game = game.Game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False),
                         player.Player(2, "Michael Smith", chessnouns.KING, False, False))


def test_game_players(get_games):
    new_game = game.Game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False),
                         player.Player(2, "Michael Smith", chessnouns.KING, False, False))

    # Set white as player one
    new_game.make_player_one_white()

    assert "Ed Lyons" == new_game.get_white_player().get_name()
    assert "Michael Smith" == new_game.get_black_player().get_name()

    # Set black as player one
    new_game.make_player_two_white()

    assert "Ed Lyons" == new_game.get_black_player().get_name()
    assert "Michael Smith" == new_game.get_white_player().get_name()

    # Test the flip

    new_game.flip_colors()

    assert "Ed Lyons" == new_game.get_white_player().get_name()
    assert "Michael Smith" == new_game.get_black_player().get_name()

    new_game.flip_colors()

    assert "Ed Lyons" == new_game.get_black_player().get_name()
    assert "Michael Smith" == new_game.get_white_player().get_name()


def test_game_bye():
    new_game = game.Game.create_bye_game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False))

    assert new_game.is_bye() is True


def test_game_colors(get_games):
    pass


def test_game_results(get_games):
    new_game = game.Game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False),
                         player.Player(2, "Michael Smith", chessnouns.KING, False, False))

    new_game.make_player_one_white()

    assert new_game.get_result() == chessnouns.NO_RESULT
    assert new_game.is_game_over() is False

    new_game.set_result(chessnouns.WHITE_WINS)

    assert new_game.is_game_over() is True
    assert new_game.get_result() == chessnouns.WHITE_WINS

    winner = new_game.get_winning_player()
    assert winner.get_name() == "Ed Lyons"

    new_game.set_result(chessnouns.BLACK_WINS)

    winner = new_game.get_winning_player()
    assert winner.get_name() == "Michael Smith"
