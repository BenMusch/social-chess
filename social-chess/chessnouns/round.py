class Round(object):
    """
    A round is actually two sets of games, where everyone plays
    or gets a bye. Normally, a round would be a set of games,
    but a key requirement for such a social event is that people
    need a break between games to eat, drink, and socialize.

    This means that only half play at once. So a round is two
    sets of games exercising all the players. We will refer
    to the two sets of games as A and B.

    """

    # There will be a list of Games for the first set
    # and one for the second. It is important to know
    # that these lists may not be the same size, to
    # accommodate unusual numbers of players

    _round_number = 1

    _a_games = []
    _b_games = []

    def __init__(self, number_a_games, number_b_games):
        """
        To set this up, we're going to initialize the arrays
        with  the correct number of games

        :param number_a_games:
        :param number_b_games:
        """
        self._a_games = [None] * number_a_games
        self._b_games = [None] * number_b_games


    def get_a_games(self):
        return self._a_games

    def get_b_games(self):
        return self._b_games


    def get_round_number(self):
        return self._round_number

