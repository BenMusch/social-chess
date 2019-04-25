from chessnouns import player, round, game, draw
import chessnouns
import pytest
from chessutilities import utilities
from chessexceptions import game_error


class TestNouns(object):

    def test_create_player_exceptions(self):
        # Test for fail on player name is not a string
        with pytest.raises(TypeError):
            assert player.Player(1, 999)

        # Test for fail with invalid level
        with pytest.raises(ValueError):
            assert player.Player(1, "Ed Lyons", 0, False, False)

    def test_player_attributes(self):
        p = player.Player(1, "Ed Lyons", chessnouns.KING, False, False)

        assert p.get_name() == "Ed Lyons"
        assert not p.is_late()
        assert not p.is_vip()

        # Make flag changes
        p.make_late()
        assert p.is_late()

        p.make_on_time()
        assert not p.is_late()

    def test_round_object(self):
        test_round = round.Round(2, 2, 1)

        a_list = test_round.get_a_games()
        b_list = test_round.get_b_games()
        round_number = test_round.get_round_number()

        assert isinstance(a_list, list)
        assert isinstance(b_list, list)
        assert round_number == 1

        assert len(a_list) == 0
        assert len(b_list) == 0

        # OK, so let us add some games
        # We need four total games with 8 players

        player_one = player.Player(1, "John", chessnouns.IMPROVING, False, False)
        player_two = player.Player(2, "Sally", chessnouns.IMPROVING, False, False)
        player_three = player.Player(3, "Sue", chessnouns.IMPROVING, False, False)
        player_four = player.Player(4, "Mark", chessnouns.IMPROVING, False, False)
        player_five = player.Player(5, "George", chessnouns.IMPROVING, False, False)
        player_six = player.Player(6, "Larry", chessnouns.IMPROVING, False, False)
        player_seven = player.Player(7, "Marcus", chessnouns.IMPROVING, False, False)
        player_eight = player.Player(8, "Janus", chessnouns.IMPROVING, False, False)

        # We now need some games
        game_one = game.Game(player_one, player_two)
        game_two = game.Game(player_one, player_three)
        game_three = game.Game(player_two, player_three)
        game_four = game.Game(player_five, player_seven)

        # Now let's add some to the round

        test_round.add_to_round(game_one)

        # What is the state of the round?

        # First, let's see if the round is done
        assert test_round.round_is_finished() is False
        assert len(test_round.get_a_games()) == 1

        # And let's be sure that the b games are intact
        assert len(test_round.get_b_games()) == 0

    def test_constants(self):
        # Here we are just testing that nobody accidentally
        # messed with the constants in init.py

        assert chessnouns.BEGINNER == 1
        assert chessnouns.IMPROVING == 2
        assert chessnouns.ADEPT == 3
        assert chessnouns.KNIGHT == 4
        assert chessnouns.KING == 5

        assert chessnouns.WHITE_WINS == 0
        assert chessnouns.BLACK_WINS == 1
        assert chessnouns.DRAW == 2

        assert chessnouns.COLOR_BLACK == 1
        assert chessnouns.COLOR_WHITE == 0

        assert chessnouns.NO_NAME == "None"
        assert chessnouns.BYE_NAME == "Bye"
        assert chessnouns.DEFAULT_FIRST_PLAYER_NAME == "John Smith"
        assert chessnouns.DEFAULT_SECOND_PLAYER_NAME == "Jane Smith"

        assert chessnouns.STANDARD_GAME_TIME == 10
        assert chessnouns.STANDARD_GAME_GAP_TIME == 5
        assert chessnouns.STANDARD_EVENT_LENGTH == 120
        assert chessnouns.STANDARD_PLAYOFF_LENGTH == 20

    def test_game_init(self):
        new_game = game.Game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False),
                             player.Player(2, "Michael Smith", chessnouns.KING, False, False))

    def test_game_players(self):
        new_game = game.Game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False),
                             player.Player(2, "Michael Smith", chessnouns.KING, False, False))

        # Set white as player one
        new_game.make_player_one_white()

        assert "Ed Lyons" == new_game.get_white_player().get_name()
        assert "Michael Smith" == new_game.get_black_player().get_name()

        # Set black as player one
        new_game.make_player_two_white()

        assert "Ed Lyons" == new_game.get_black_player().get_name()
        assert "Michael Smith" == new_game.get_white_player().get_name()

        # Test the flip

        new_game.flip_colors()

        assert "Ed Lyons" == new_game.get_white_player().get_name()
        assert "Michael Smith" == new_game.get_black_player().get_name()

        new_game.flip_colors()

        assert "Ed Lyons" == new_game.get_black_player().get_name()
        assert "Michael Smith" == new_game.get_white_player().get_name()

    def test_game_bye(self):
        new_game = game.Game.create_bye_game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False))

        assert new_game.is_bye() is True

    def test_game_colors(self):
        pass

    def test_game_results(self):
        new_game = game.Game(player.Player(1, "Ed Lyons", chessnouns.KING, False, False),
                             player.Player(2, "Michael Smith", chessnouns.KING, False, False))

        new_game.make_player_one_white()

        assert new_game.get_result() == chessnouns.NO_RESULT
        assert new_game.is_game_over() is False

        new_game.set_result(chessnouns.WHITE_WINS)

        assert new_game.is_game_over() is True
        assert new_game.get_result() == chessnouns.WHITE_WINS

        winner = new_game.get_winning_player()
        assert winner.get_name() == "Ed Lyons"

        new_game.set_result(chessnouns.BLACK_WINS)

        winner = new_game.get_winning_player()
        assert winner.get_name() == "Michael Smith"

    def test_draw_class(self):
        players = utilities.get_set_of_players()

        clem = players[0]
        sarah = players[1]
        will = players[2]
        evan = players[3]
        jay = players[4]

        assert clem.get_name() == "Clem Aeppli"
        assert sarah.get_name() == "Sarah Betancourt"
        assert will.get_name() == "Will Brown"
        assert evan.get_name() == "Evan Bruning"
        assert jay.get_name() == "Jay Cincotti"

        clem_draw = draw.Draw(clem, 4)

        # Let's assert some things

        assert clem_draw.get_number_of_rounds() == 4
        assert clem_draw.get_rounds_left() == 4
        assert len(clem_draw.get_matchups()) == 0
        assert clem_draw.has_full_draw() is False
        assert clem_draw.number_matchups_scheduled() == 0

        # Now we want to add a game with Sarah

        clem_draw.add_matchup(sarah)

        # Now let's check those again
        assert clem_draw.get_number_of_rounds() == 4
        assert clem_draw.get_rounds_left() == 3
        matches = clem_draw.get_matchups()
        assert matches is not None
        assert clem_draw.has_full_draw() is False
        assert clem_draw.number_matchups_scheduled() == 1

        assert len(matches) == 1
        assert matches[0] == sarah.get_id()

        clem_draw.add_matchup(will)

        # Again
        assert clem_draw.get_number_of_rounds() == 4
        assert clem_draw.get_rounds_left() == 2
        matches = clem_draw.get_matchups()
        assert matches is not None
        assert clem_draw.has_full_draw() is False
        assert clem_draw.number_matchups_scheduled() == 2

        clem_draw.add_matchup(evan)

        # Again
        assert clem_draw.get_number_of_rounds() == 4
        assert clem_draw.get_rounds_left() == 1
        matches = clem_draw.get_matchups()
        assert matches is not None
        assert clem_draw.has_full_draw() is False
        assert clem_draw.number_matchups_scheduled() == 3

        clem_draw.add_matchup(jay)

        # Again
        assert clem_draw.get_number_of_rounds() == 4
        assert clem_draw.get_rounds_left() == 0
        matches = clem_draw.get_matchups()
        assert matches is not None
        assert clem_draw.has_full_draw() is True
        assert clem_draw.number_matchups_scheduled() == 4

        print(clem_draw)

        # Now let's test the clear
        clem_draw.clear_matchups()
        assert clem_draw.get_rounds_left() == 4
        matches = clem_draw.get_matchups()
        assert len(matches) == 0
        assert clem_draw.has_full_draw() is False
        assert clem_draw.number_matchups_scheduled() == 0
