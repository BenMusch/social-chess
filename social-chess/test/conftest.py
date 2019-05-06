import pytest
import sqlite3 as sqlite
from chessnouns import player, game, schedule
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
            candidate_player.get_draw().add_game_by_player(other_player)
            other_player.get_draw().add_game_by_player(candidate_player)


@pytest.fixture(scope="module")
def get_four_games():
    """
    We need to create some games
    :return:
    """
    games = []
    return games

@pytest.fixture(scope="module")
def get_random_completed_schedule(get_all_players):
    pass

@pytest.fixture(scope="module")
def get_workhorse_completed_schedule():
    """
    This is the data for a tournament with a specific
    outcome, so we can test that outcome
    :return:
    """
    players_list = []
    for pl in raw_player_list:
        players_list.append(player.Player(pl[0],pl[1],pl[3],False,vip=(1 == int(pl[4]))))
    pass


# Here is our data
raw_player_list = \
    (1, "Clem Aeppli", "", 1, 0),\
    (2, "Sarah Betancourt", "", 2, 0),\
    (3, "Will Brown", "", 5, 0),\
    (4, "Evan Bruning", "", 2, 0),\
    (5, "Jay Cincotti", "", 2, 0),\
    (6, "Tracy Corley", "", 2, 0),\
    (7, "Stefanie Coxe", "", 3, 0),\
    (8, "Brendan Crighton", "", 3, 1),\
    (9, "Josh Cutler", "", 2, 1),\
    (10, "Rachel Dec", "", 4, 0),\
    (11, "Mike Deehan", "", 2, 0),\
    (12, "Joe Deering", "", 4, 0),\
    (13, "Gintautas Dumcius", "", 2, 0),\
    (14, "Preston Epps", "", 5, 0),\
    (15, "Matt Giancola", "", 4, 0),\
    (16, "Libby Gormley", "", 1, 0),\
    (17, "Joe Gravellese", "", 3, 0),\
    (18, "Christian Greve", "", 4, 0),\
    (19, "Brian Jencunas", "", 3, 0),\
    (20, "Maya Jonas-Silver", "", 4, 0),\
    (21, "Steve Koczela", "", 5, 0),\
    (22, "Ed Lyons", "", 5, 0),\
    (23, "Juana Matias", "", 3, 0),\
    (24, "Andy Metzger", "", 5, 0),\
    (25, "Mike Morales", "", 4, 0),\
    (26, "Ashira Morris", "", 3, 0),\
    (27, "Stephanie Murray", "", 1, 0),\
    (28, "Ben Muschol", "", 5, 0),\
    (29, "Christine Prignano", "", 3, 0),\
    (30, "Will Rasky", "", 3, 0),\
    (31, "Becca Rausch", "", 3, 1),\
    (32, "Jodi Reed", "", 1, 0),\
    (33, "Hirak Shah", "", 4, 0),\
    (34, "Aaron Van Leesten", "", 3, 0),\
    (35, "Pete Wilson", "", 3, 0),\
    (36, "Brad Wyatt", "", 5, 0),\
    (37, "Jon Santiago", "", 3, 1),\
    (38, "Cory Amzon", "", 1, 0),\
    (39, "Jim Aloisi", "", 3, 1)
