import pytest
import sqlite3 as sqlite
import chessnouns
from chessnouns import player, round, game


def test_round_object():
    test_round = round.Round(2, 2)

    a_list = test_round.get_games()
    b_list = test_round.get_games()
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

    test_round.add_game_to_round(game_one)

    # What is the state of the round?

    # First, let's see if the round is done
    assert test_round.round_is_finished() is False
    assert len(test_round.get_games()) == 1

    # And let's be sure that the b games are intact
    assert len(test_round.get_games()) == 0