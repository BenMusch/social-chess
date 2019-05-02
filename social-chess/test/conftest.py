import pytest
import sqlite3 as sqlite
from chessnouns import player, game
import chessutilities

"""
This will hold the fixtures that are needed across test files
"""


@pytest.fixture(scope="module")
def get_all_players():
    """
    This fixture gets players
    :param self:
    :return:
    """
    con = sqlite.connect(chessutilities.DATABASE_TEST_LOCATION)

    players = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            players.append(player.Player(row[0], row[1], level=int(row[3]), late=False, vip=(1 == int(row[4]))))

    return players


@pytest.fixture(scope="module")
def get_five_players(get_all_players):
    five_players = get_all_players[0:5]
    return five_players


@pytest.fixture(scope="module")
def get_five_draws(get_all_players):
    draws = []
    five_players = get_all_players[0:5]

    # Now we need to set up the draws

    for ind_player in five_players:
        ind_player.set_draw(4)

    for ind_player in five_players:
        while not ind_player.get_draw().has_full_draw():
            schedule_draw_games(ind_player, five_players)
        draws.append(ind_player.get_draw())

    return draws


def schedule_draw_games(candidate_player, player_list):
    for other_player in player_list:
        if other_player.get_id() == candidate_player.get_id():
            continue
        if not other_player.get_draw().has_full_draw() and not candidate_player.get_draw().has_played_player_id(
                other_player.get_id()):
            candidate_player.get_draw().add_game(other_player)
            other_player.get_draw().add_game(candidate_player)


@pytest.fixture(scope="module")
def get_four_games():
    """
    We need to create some games
    :return:
    """
    games = []
    return games


@pytest.fixture(scope="module")
def get_even_players(get_all_players):
    """
    We are going to get a number of players
    that divide by 4 evenly
    :return:
    """
    return get_all_players[0:41]


@pytest.fixture(scope="module")
def get_mod_one_players(get_all_players):
    """
    We are going to get a number of players
    that divide by 4 with one remaining
    :return:

    """
    return get_all_players[0:36]


@pytest.fixture(scope="module")
def get_mod_two_players(get_all_players):
    """
    We are going to get a number of players
    that divide by 4 with two remaining
    :return:
    """
    return get_all_players[0:37]


@pytest.fixture(scope="module")
def get_mod_three_players(get_all_players):
    """
    We are going to get a number of players
    that divide by 4 with three remaining
    :return:
    """
    return get_all_players[0:38]
