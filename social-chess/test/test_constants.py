import pytest
import chessnouns

"""
We are just making sure the constants were not accidentally altered
"""


def test_constants():
    # Here we are just testing that nobody accidentally
    # messed with the constants in init.py

    assert chessnouns.DEFAULT_NUMBER_OF_GAMES == 4

    assert chessnouns.BEGINNER == 1
    assert chessnouns.IMPROVING == 2
    assert chessnouns.ADEPT == 3
    assert chessnouns.KNIGHT == 4
    assert chessnouns.KING == 5

    assert chessnouns.WHITE_WINS == 0
    assert chessnouns.BLACK_WINS == 1
    assert chessnouns.DRAW == 2
    assert chessnouns.NO_RESULT == 3

    assert chessnouns.COLOR_BLACK == 1
    assert chessnouns.COLOR_WHITE == 0

    assert chessnouns.NO_NAME == "None"
    assert chessnouns.BYE_NAME == "Bye"
    assert chessnouns.BYE_ID == 0
    assert chessnouns.DEFAULT_FIRST_PLAYER_NAME == "John Smith"
    assert chessnouns.DEFAULT_SECOND_PLAYER_NAME == "Jane Smith"

    assert chessnouns.STANDARD_GAME_TIME == 10
    assert chessnouns.STANDARD_GAME_GAP_TIME == 5
    assert chessnouns.STANDARD_EVENT_LENGTH == 120
    assert chessnouns.STANDARD_PLAYOFF_LENGTH == 20

    assert chessnouns.NO_COLOR_SELECTED == 0
    assert chessnouns.PLAYER_ONE_IS_WHITE == 1
    assert chessnouns.PLAYER_ONE_IS_BLACK == 2

    assert chessnouns.ORGANIZE_BY_LEVEL is True
    assert chessnouns.BYE_IN_EARLIER_ROUND is True
    assert chessnouns.AUTO_GENERATE_PLAYOFF_MATCH is False
    assert chessnouns.TIEBREAK_BY_LEVEL is True
    assert chessnouns.TIEBREAK_BY_MATCHUPS is False
