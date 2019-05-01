import chessnouns
from chessnouns import player, game

"""
This group of tests are for the game class
Fixtures are first, then the tests
"""


def test_game_init(get_all_players):
    test_players = get_all_players
    new_game = game.Game(test_players[0], test_players[1])

def test_game_strings(get_all_players):
    """
    A game will get rendered in different ways

    """
    print('\n---------------------------\nTesting Game String Ouputs\n---------------------------')
    test_players = get_all_players
    new_game = game.Game(test_players[0], test_players[1])
    second_game = game.Game(test_players[2], test_players[5])

    # First let us test both strings without colors assigned

    print(new_game)
    print(second_game)

    assert str(new_game) == "Clem Aeppli(1)[N] vs. Sarah Betancourt(2)[N]"
    assert str(second_game)== "Will Brown(5)[N] vs. Tracy Corley(2)[N]"

    # Now we need to assign colors

    new_game.make_player_one_white()
    second_game.make_player_two_white()

    # Leaderboard

    print(new_game.get_leaderboard_string_white_first())
    print(second_game.get_leaderboard_string_white_first())

    assert new_game.get_leaderboard_string_white_first() == "Clem Aeppli vs. Sarah Betancourt"
    assert second_game.get_leaderboard_string_white_first() == "Tracy Corley vs. Will Brown"

    string_array = new_game.get_leaderboard_array_white_first()

    assert string_array[0] == "Clem Aeppli"
    assert string_array[1] == "Sarah Betancourt"

    # Traditional

    print(new_game)
    print(second_game)

    assert str(new_game) == "Clem Aeppli(1)[W] vs. Sarah Betancourt(2)[B]"
    assert str(second_game) == "Tracy Corley(2)[W] vs. Will Brown(5)[B]"

    # Let's switch colors

    new_game.flip_colors()
    second_game.flip_colors()

    assert new_game.get_leaderboard_string_white_first() == "Sarah Betancourt vs. Clem Aeppli"
    assert second_game.get_leaderboard_string_white_first() == "Will Brown vs. Tracy Corley"

    print(new_game)
    print(second_game)

    assert str(new_game) == "Sarah Betancourt(2)[W] vs. Clem Aeppli(1)[B]"
    assert str(second_game) == "Will Brown(5)[W] vs. Tracy Corley(2)[B]"

    # Let's try a bye

    bye_game = game.Game.create_bye_game(test_players[5])
    print(bye_game)

    assert str(bye_game) == "Tracy Corley has a bye"

    print(bye_game.get_leaderboard_string_white_first())

    assert bye_game.get_leaderboard_string_white_first() == "Tracy Corley | Bye"

    string_array = bye_game.get_leaderboard_array_white_first()

    assert string_array[0] == "Tracy Corley"
    assert string_array[1] == chessnouns.BYE_NAME


def test_winner_and_loser(get_all_players):
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

    winner, _ = new_game.get_winning_and_losing_player()
    assert winner.get_name() == "Ed Lyons"

    new_game.set_result(chessnouns.BLACK_WINS)

    winner, _ = new_game.get_winning_and_losing_player()
    assert winner.get_name() == "Michael Smith"
