"""
This is the file that will test our utility functions
"""
from chessutilities import utilities
import chessnouns


def test_get_number_of_boards_and_tweaks():
    """
    This method tests the strange function that, when you give it a
    number of players, it will tell you how many boards you need
    set up, whether or not there will be byes for players, and
    if the number of games in each round will be lopsided.

    Here are some test cases:

    16 players

    Round 1A: 8 players, 4 boards
    Round 1B: 8 players, 4 boards

    17 players

    Round 1A: 8 players, 4 boards, 1 player sits out
    Round 1B: 8 players, 4 boards


    18 players

    Round 1A: 8 players, 4 boards
    Round 1B: 10 players, 5 board

    19 players


    Round 1A: 8 players, 4 boards, 1 player sits out
    Round 1B: 10 players, 5 boards

    20 players

    Round 1A: 10 players, 5 boards
    Round 1B: 10 players, 5 boards

    """
    assert (5, False, False) == utilities.get_number_of_boards_and_tweaks(20)
