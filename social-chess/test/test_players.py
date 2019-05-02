import pytest
import chessnouns
from chessnouns import player


def test_create_player_exceptions():
    print('\n---------------------------\nTesting Player Exceptions\n---------------------------')
    # Test for fail on player name is not a string
    with pytest.raises(TypeError):
        assert player.Player(1, 999)

    # Test for fail with invalid level
    with pytest.raises(ValueError):
        assert player.Player(1, "Ed Lyons", 0, False, False)


def test_player_attributes():
    print('\n---------------------------\nTesting Player Attributes\n---------------------------')
    p = player.Player(1, "Ed Lyons", chessnouns.KING, False, False)

    assert p.get_name() == "Ed Lyons"
    assert not p.is_late()
    assert not p.is_vip()

    # Make flag changes
    p.make_late()
    assert p.is_late()

    p.make_on_time()
    assert not p.is_late()
