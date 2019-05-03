import chessnouns
from chessnouns import player, game
import pytest
import chessexceptions
from chessexceptions import game_error

"""
This group of tests are for the game class
"""


def test_game_strings(get_all_players):
    """
    A game will get rendered in different ways,
    sometimes in a schedule, sometimes in a
    leaderboard, sometimes with levels,
    sometimes without
    """
    print('\n---------------------------\nTesting Game String Ouputs\n---------------------------')
    test_players = get_all_players
    new_game = game.Game(test_players[0], test_players[1])
    second_game = game.Game(test_players[2], test_players[5])

    # First let us test both strings without colors assigned

    assert str(new_game) == "Clem Aeppli(1)[N] vs. Sarah Betancourt(2)[N]"
    assert str(second_game) == "Will Brown(5)[N] vs. Tracy Corley(2)[N]"

    # Now we need to assign colors

    new_game.make_player_one_white()
    second_game.make_player_two_white()

    # Leaderboard

    assert new_game.get_leaderboard_string_white_first() == "Clem Aeppli vs. Sarah Betancourt"
    assert second_game.get_leaderboard_string_white_first() == "Tracy Corley vs. Will Brown"

    string_array = new_game.get_leaderboard_array_white_first()

    assert string_array[0] == "Clem Aeppli"
    assert string_array[1] == "Sarah Betancourt"

    # Traditional

    assert str(new_game) == "Clem Aeppli(1)[W] vs. Sarah Betancourt(2)[B]"
    assert str(second_game) == "Tracy Corley(2)[W] vs. Will Brown(5)[B]"

    # Let's switch colors

    new_game.flip_colors()
    second_game.flip_colors()

    assert new_game.get_leaderboard_string_white_first() == "Sarah Betancourt vs. Clem Aeppli"
    assert second_game.get_leaderboard_string_white_first() == "Will Brown vs. Tracy Corley"

    assert str(new_game) == "Sarah Betancourt(2)[W] vs. Clem Aeppli(1)[B]"
    assert str(second_game) == "Will Brown(5)[W] vs. Tracy Corley(2)[B]"

    # Let's try a bye

    bye_game = game.Game.create_bye_game(test_players[5])

    assert str(bye_game) == "Tracy Corley has a bye"

    assert bye_game.get_leaderboard_string_white_first() == "Tracy Corley | Bye"

    string_array = bye_game.get_leaderboard_array_white_first()

    assert string_array[0] == "Tracy Corley"
    assert string_array[1] == chessnouns.BYE_NAME


def test_winner_and_loser(get_all_players):
    print('\n---------------------------\nTesting Game Winner and Loser\n---------------------------')

    test_players = get_all_players

    new_game = game.Game(test_players[0], test_players[1])

    # First let us make sure we can't get it yet
    with pytest.raises(game_error.GameError):
        assert new_game.get_winning_and_losing_player()

    new_game.make_player_one_white()
    new_game.set_result(chessnouns.WHITE_WINS)

    winner, loser = new_game.get_winning_and_losing_player()

    assert winner is not None
    assert loser is not None

    assert winner.get_id() == test_players[0].get_id()
    assert loser.get_id() == test_players[1].get_id()


def test_game_players_and_colors(get_all_players):
    print('\n---------------------------\nTesting Game Players and Colors\n---------------------------')
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
    print('\n---------------------------\nTesting Game Bye\n---------------------------')

    test_players = get_all_players
    new_game = game.Game.create_bye_game(test_players[0])

    assert new_game.is_bye() is True


def test_game_results(get_all_players):
    print('\n---------------------------\nTesting Game Results\n---------------------------')

    test_players = get_all_players

    new_game = game.Game(test_players[0],
                         test_players[1])

    new_game.make_player_one_white()

    assert new_game.get_result() == chessnouns.NO_RESULT
    assert new_game.is_game_over() is False

    new_game.set_result(chessnouns.WHITE_WINS)

    assert new_game.is_game_over() is True
    assert new_game.get_result() == chessnouns.WHITE_WINS

    winner, _ = new_game.get_winning_and_losing_player()
    assert winner.get_name() == "Clem Aeppli"

    new_game.set_result(chessnouns.BLACK_WINS)

    winner, _ = new_game.get_winning_and_losing_player()
    assert winner.get_name() == "Sarah Betancourt"
