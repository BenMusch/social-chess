import chessnouns
from chessnouns import player, game

"""
This group of tests are for the game class
Fixtures are first, then the tests
"""


def test_game_init(get_all_players):
    test_players = get_all_players
    new_game = game.Game(test_players[0], test_players[1])


def test_game_players(get_all_players):
    test_players = get_all_players
    new_game = game.Game(test_players[0], test_players[1])

    # Set white as player one
    new_game.make_player_one_white()

    assert "Clem Aeppli" == new_game.get_white_player().get_name()
    assert "Sarah Betancourt" == new_game.get_black_player().get_name()

    # Set black as player one
    new_game.make_player_two_white()

    assert "Sarah Betancourt" == new_game.get_white_player().get_name()
    assert "Clem Aeppli" == new_game.get_black_player().get_name()

    # Test the flip

    new_game.flip_colors()

    assert "Clem Aeppli" == new_game.get_white_player().get_name()
    assert "Sarah Betancourt" == new_game.get_black_player().get_name()

    new_game.flip_colors()

    assert "Sarah Betancourt" == new_game.get_white_player().get_name()
    assert "Clem Aeppli" == new_game.get_black_player().get_name()


def test_game_bye(get_all_players):
    test_players = get_all_players
    new_game = game.Game.create_bye_game(test_players[0])

    assert new_game.is_bye() is True


def test_game_colors(get_four_games):
    pass


def test_game_results(get_four_games):
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
