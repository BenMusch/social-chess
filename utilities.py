"""
These are all the utility functions that we will need
for our chess tournament solver
"""

import math


def get_number_of_boards_and_tweaks(number_players):
    """
    This method works by understanding that dividing the number of players by four tells you want to do.
    This is the case because since two people play a game, and everyone skips rounds, dividing by 4
        tells you whether it will be neat or not

    if (players mod 4) == 0 then we know it's going to be OK, And then players div 4 is the number of boards.
    So if there are 16 players - half of them (8) can play on 4 boards, and then the next

    if (players mod 4) == 1 then we know players div 4 is the answer, but we have one player out each round

    if (players mod 4) == 2 then we know we have a lopsided result - but we know we have players div + 1 as the boards

    if (players mod 4) == 3 then we know we have a lopsided result and 1 player sitting gout, but we know we have
        players div + 1 as the boards

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
        return minimum_boards+1, True, False
    else:
        # number of boards plus one, is lopsided, has bye
        return minimum_boards + 1, True, False