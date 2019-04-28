import pytest
import sqlite3 as sqlite
import chessnouns
from chessnouns import player


@pytest.fixture(scope="module")
def get_players(self):
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


def test_create_player_exceptions():
    # Test for fail on player name is not a string
    with pytest.raises(TypeError):
        assert player.Player(1, 999)

    # Test for fail with invalid level
    with pytest.raises(ValueError):
        assert player.Player(1, "Ed Lyons", 0, False, False)


def test_player_attributes():
    p = player.Player(1, "Ed Lyons", chessnouns.KING, False, False)

    assert p.get_name() == "Ed Lyons"
    assert not p.is_late()
    assert not p.is_vip()

    # Make flag changes
    p.make_late()
    assert p.is_late()

    p.make_on_time()
    assert not p.is_late()
