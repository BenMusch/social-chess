"""
This is the file that will test our utility functions
"""
from chessutilities import utilities
import chessnouns
import pytest


def test_get_number_of_boards_and_tweaks():
    """
    This method tests the strange function that, when you give it a
    number of players, it will tell you how many boards you need
    set up, whether or not there will be byes for players, and
    if the number of games in each round will be lopsided.

    # The tuple returned is:
    # Number of required boards, is it lopsided, and is there a bye

    """

    # These variables will make the desired test results more obvious
    lopsided = True
    bye = True

    # 14 players
    #     Round 1A: 6 players, 3 boards
    #     Round 1B: 8 players, 4 boards
    assert (4, lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(14)

    # 15 players
    #     Round 1A: 6 players, 3 boards, one bye
    #     Round 1B: 8 players, 4 boards
    assert (4, lopsided, bye) == utilities.get_number_of_boards_and_tweaks(15)

    # 16 players
    #
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 8 players, 4 boards
    assert (4, not lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(16)

    # 17 players
    #     Round 1A: 8 players, 4 boards, 1 player sits out
    #     Round 1B: 8 players, 4 boards
    assert (4, not lopsided, bye) == utilities.get_number_of_boards_and_tweaks(17)

    # 18 players
    #     Round 1A: 8 players, 4 boards
    #     Round 1B: 10 players, 5 boards
    assert (5, lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(18)

    # 27 players
    #     Round 1A: 12 players, 6 boards, one bye
    #     Round 1B: 14 players, 7 boards
    assert (7, lopsided, bye) == utilities.get_number_of_boards_and_tweaks(27)

    # 31 players
    #     Round 1A: 14 players, 7 boards, one bye
    #     Round 1B: 16 players, 8 boards
    assert (8, lopsided, bye) == utilities.get_number_of_boards_and_tweaks(31)

    # 36 players
    #     Round 1A: 18 players, 9 boards
    #     Round 1B: 18 players, 9 boards
    assert (9, not lopsided, not bye) == utilities.get_number_of_boards_and_tweaks(36)

    # 75 players
    #     Round 1A: 36 players, 18 boards, one bye
    #     Round 1B: 38 players, 19 boards
    assert (19, lopsided, bye) == utilities.get_number_of_boards_and_tweaks(75)


def test_level_to_text():
    # Test for fail on passing in a string
    with pytest.raises(Exception):
        assert utilities.level_to_text("String")

    # Test for passing in too big a number
    with pytest.raises(Exception):
        assert utilities.level_to_text(8)

    assert "Beginner" == utilities.level_to_text(1)
    assert "Intermediate" == utilities.level_to_text(2)
    assert "Advanced" == utilities.level_to_text(3)
