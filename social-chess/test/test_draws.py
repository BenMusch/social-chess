import pytest
import chessnouns
from chessutilities import utilities
from chessnouns import player, game, draw
import sqlite3 as sqlite


@pytest.fixture(scope="module")
def get_players():
    """
    This fixture gets players
    :param self:
    :return:
    """
    con = sqlite.connect("../db/chess.db")

    players = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            players.append(player.Player(row[0], row[1], level=int(row[3]), late=False, vip=(1 == int(row[4]))))

    return players


def get_draws():
    players = get_players()

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

    clem.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)
    sarah.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)
    will.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)
    evan.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)
    jay.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)

    return clem.get_draw(), sarah.get_draw(), will.get_draw(), evan.get_draw(), jay.get_draw()


def get_one_draw():
    players = get_players()
    clem = players[0]
    assert clem.get_name() == "Clem Aeppli"
    clem.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)

    return clem.get_draw()


@pytest.fixture(scope="module")
def test_draw_class(get_players):

    players = get_players
    clem = players[0]
    sarah = players[1]
    will = players[2]
    evan = players[3]
    jay = players[4]

    clem_draw = get_one_draw()

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
