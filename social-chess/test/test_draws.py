import chessnouns

"""
Testing of the draw class
"""

def test_scoring(get_five_draws):
    print('\n---------------------------\nTesting Draw Scoring\n---------------------------')
    draws = get_five_draws
    assert len(draws) == 5

    candidate_draw = draws[0]

    # First, clem

    first_game = candidate_draw.get_games()[0]
    second_game = candidate_draw.get_games()[1]
    third_game = candidate_draw.get_games()[2]
    fourth_game = candidate_draw.get_games()[3]

    # Now we will loop through and set the winners
    first_game.make_player_one_white()
    first_game.set_result(chessnouns.WHITE_WINS)

    second_game.make_player_one_white()
    second_game.set_result(chessnouns.WHITE_WINS)

    third_game.make_player_one_white()
    third_game.set_result(chessnouns.WHITE_WINS)

    fourth_game.make_player_two_white()
    fourth_game.set_result(chessnouns.WHITE_WINS)

    clem_raw_points = candidate_draw.get_total_raw_points()
    clem_weighted_points = candidate_draw.get_total_weighted_score()

    assert clem_raw_points == 3
    assert clem_weighted_points == 3.6

    # OK, let's get the scores
    print("Points for player: {} ".format(clem_raw_points))
    print("Weighted score for player: {} ".format(clem_weighted_points))

    # Second, Will

    second_draw = draws[2]

    print(second_draw.get_player().get_name())

    first_game = second_draw.get_games()[0]
    second_game = second_draw.get_games()[1]
    third_game = second_draw.get_games()[2]
    fourth_game = second_draw.get_games()[3]

    # Now we will loop through and set the winners
    first_game.make_player_one_white()
    first_game.set_result(chessnouns.WHITE_WINS)

    second_game.make_player_one_white()
    second_game.set_result(chessnouns.WHITE_WINS)

    third_game.make_player_one_white()
    third_game.set_result(chessnouns.WHITE_WINS)

    fourth_game.make_player_two_white()
    fourth_game.set_result(chessnouns.WHITE_WINS)

    # Let's get the names
    print(first_game)
    print(second_game)
    print(third_game)
    print(fourth_game)

    will_raw_points = second_draw.get_total_raw_points()
    will_weighted_points = second_draw.get_total_weighted_score()

    print("Points for player: {} ".format(will_raw_points))
    print("Weighted score for player: {} ".format(will_weighted_points))

    assert will_raw_points == 3
    assert will_weighted_points == 2.1


def test_draw_class(get_all_players):
    print('\n---------------------------\nTesting Draw Class Properties\n---------------------------')
    players = get_all_players
    clem = players[0]
    sarah = players[1]
    will = players[2]
    evan = players[3]
    jay = players[4]

    assert clem.get_name() == "Clem Aeppli"
    clem.set_draw(chessnouns.DEFAULT_NUMBER_OF_GAMES)
    clem_draw = clem.get_draw()

    # Let's assert some things

    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 4
    assert len(clem_draw.get_games()) == 0
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 0

    # Now we want to add a game with Sarah

    clem_draw.add_game_by_player(sarah)

    # Now let's check those again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 3
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 1

    assert len(games) == 1

    assert games[0].contains_player(sarah)

    clem_draw.add_game_by_player(will)

    # Again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 2
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 2

    clem_draw.add_game_by_player(evan)

    # Again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 1
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 3

    clem_draw.add_game_by_player(jay)

    # Again
    assert clem_draw.get_number_of_rounds() == 4
    assert clem_draw.get_rounds_left() == 0
    games = clem_draw.get_games()
    assert games is not None
    assert clem_draw.has_full_draw() is True
    assert clem_draw.number_games_scheduled() == 4

    #print(clem_draw)

    # Now let's test the clear
    clem_draw.clear_games()
    assert clem_draw.get_rounds_left() == 4
    games = clem_draw.get_games()
    assert len(games) == 0
    assert clem_draw.has_full_draw() is False
    assert clem_draw.number_games_scheduled() == 0
