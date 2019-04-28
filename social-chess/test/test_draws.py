import pytest
import chessnouns
from chessutilities import utilities
from chessnouns import player, game


def test_draw_class():
    # FIXME: change to fixture
    players = utilities.get_set_of_players()

    clem = players[0]
    sarah = players[1]
    will = players[2]
    evan = players[3]
    jay = players[4]

    assert clem.get_name() == "Clem Aeppli"
    assert sarah.get_name() == "Sarah Betancourt"
    assert will.get_name() == "Will Brown"
    assert evan.get_name() == "Evan Bruning"
    assert jay.get_name() == "Jay Cincotti"

    clem_draw = draw.Draw(clem, 4)

    # Let's assert some things

    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 4
    assert len(clem_draw.get_games()) == 0
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 0

    # Now we want to add a game with Sarah

    clem_draw.add_game(sarah)

    # Now let's check those again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 3
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 1

    assert len(games) == 1

    assert games[0].contains_player(sarah)

    clem_draw.add_game(will)

    # Again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 2
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 2

    clem_draw.add_game(evan)

    # Again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 1
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 3

    clem_draw.add_game(jay)

    # Again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 0
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is True
    assert clem_draw.number_games_scheduled() == 4

    print(clem_draw)

    # Now let's test the clear
    clem_draw.clear_games()
    assert clem_draw.get_rounds_left() == 4
    games = clem_draw.get_games()
    assert len(games) == 0
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 0
