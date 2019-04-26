"""
These are all the utility functions that we will need
for our chess tournament solver
"""

import math
import chessnouns
from chessnouns import player
from random import *
import sqlite3 as sqlite


def get_set_of_players():
    con = sqlite.connect("../db/chess.db")

    players = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            players.append(player.Player(row[0], row[1], level=int(row[3]), late=False, vip=(1 == int(row[4]))))

    return players


def get_number_of_boards_and_tweaks(number_players):
    """
    This method works by understanding that dividing the number of players by four tells you want to do.
    This is the case because since two people play a game, and everyone skips rounds, dividing by 4
        tells you whether it will be neat or not. The remainder after 4 tells you the scenario

    if (players mod 4) == 0 then we know it's going to be OK, And then players divided by 4 is the number of boards,
            with the same number of boards used every round.

    if (players mod 4) == 1 then we know players div 4 is the number of boards, but we have one player get a bye one
            of the two rounds

    if (players mod 4) == 2 then we know we have a lopsided result inside a round - but we know we have
            players div + 1 as the number of boards. So for 18 players, you need nine, but you keep
            alternating between 8 and 9 boards used.

    if (players mod 4) == 3 then we know we have a lopsided result and a player getting a bye in alternate
            rounds, so players div 4 + 1 is the number of boards

    :param number_players: how many players in the tournament
    :return: a tuple (number of boards we need, an indicator if it's lopsided, and if there are byes
    """

    minimum_boards = math.trunc(number_players / 4)

    if (number_players % 4) == 0:
        # number of boards, is lopsided, has bye
        return minimum_boards, False, False
    elif (number_players % 4) == 1:
        # number of boards, is lopsided, has bye
        return minimum_boards, False, True
    elif (number_players % 4) == 2:
        # number of boards plus one, is lopsided, has bye
        return minimum_boards + 1, True, False
    else:
        # number of boards plus one, is lopsided, has bye
        return minimum_boards + 1, True, True


def level_to_text(level):
    """
    This function converts the level constants to text for
    debugging and display purposes

    :param level: what level the player is
    :return: text indicating the level
    """

    if not isinstance(level, int):
        raise TypeError("You have to submit a number")

    if level not in range(chessnouns.BEGINNER, chessnouns.KING + 1):
        raise ValueError(
            "That number was not in the range of {} to {}".format(chessnouns.BEGINNER, chessnouns.KING))

    if level == chessnouns.BEGINNER:
        return "Beginner"
    elif level == chessnouns.IMPROVING:
        return "Improving"
    elif level == chessnouns.ADEPT:
        return "Adept"
    elif level == chessnouns.KNIGHT:
        return "Knight"
    else:
        return "King"


def get_random_game_result():
    return randint(chessnouns.WHITE_WINS, chessnouns.DRAW)


def get_random_skill_level():
    return randint(chessnouns.BEGINNER, chessnouns.KING)


def get_random_color():
    return randint(chessnouns.COLOR_WHITE, chessnouns.COLOR_BLACK)


def get_player_for_id(identifier):

    # We need to handle the bye here
    if identifier == chessnouns.BYE_ID:
        return player.Player(0, chessnouns.BYE_NAME)

    con = sqlite.connect('../db/chess.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM players WHERE id=' + str(identifier))

    rows = cur.fetchall()

    if rows[0] is not None:
        row = rows[0]
        return player.Player(row[0], row[1], level=int(row[3]), late=False, vip=(bool(int(row[4]))))
    else:
        return None


def print_player_draws(players):
    """
    This method will print all the players and their draw
    information to the command line
    :param players:
    :return:
    """
    for p in players:

        player_draw = p.get_draw()
        print(player_draw)