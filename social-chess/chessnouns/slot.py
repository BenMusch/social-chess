import functools


@functools.total_ordering #This is to help sort methods at bottom
class Slot(object):
    """
    This class is just a place on the leaderboard
    """

    def __init__(self, player_name, raw_points, weighted_points):
        self._player_name = player_name
        self._raw_points = raw_points
        self._weighted_points = weighted_points

    def __str__(self):
        return "{} |{}|{}".format(self._player_name, self._raw_points, self._weighted_points)

    def __repr__(self):
        return "{} |{}|{}".format(self._player_name, self._raw_points, self._weighted_points)

    def get_line(self):
        """
        This will return a tuple that corresponds to the three values
        :return: tuple of attributes
        """
        return self._player_name, self._raw_points, self._weighted_points

    def get_weighted_score(self):
        return self._weighted_points

    """
    These two methods will ensure a list of these is sorted by weighted points
    """
    def __lt__(self, other):
        return   other._weighted_points < self._weighted_points

    def __eq__(self, other):
        return self._weighted_points == other._weighted_points


