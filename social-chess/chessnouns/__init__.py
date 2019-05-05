# We will define our chess noun constants here
BEGINNER = 1
IMPROVING = 2
ADEPT = 3
KNIGHT = 4
KING = 5

SHOW_LEVELS = True

DEFAULT_NUMBER_OF_GAMES = 4
DEFAULT_NUMBER_OF_ROUNDS = 8
WEIGHTED_SCORE_DECIMAL_PRECISION = 2

WHITE_WINS = 0
BLACK_WINS = 1
DRAW = 2
NO_RESULT = 3

COLOR_WHITE = 0
COLOR_BLACK = 1

NO_COLOR_SELECTED = 0
PLAYER_ONE_IS_WHITE = 1
PLAYER_ONE_IS_BLACK = 2

DID_NOT_PLAY = 0
PLAYER_ONE_WON = 1
PLAYER_TWO_WON = 2

NO_NAME = "None"
BYE_NAME = "Bye"
BYE_ID = 0
DEFAULT_FIRST_PLAYER_NAME = "John Smith"
DEFAULT_SECOND_PLAYER_NAME = "Jane Smith"

STANDARD_GAME_TIME = 10
STANDARD_GAME_GAP_TIME = 5
STANDARD_EVENT_LENGTH = 120
STANDARD_PLAYOFF_LENGTH = 20

# These are parameters for creating
# the tournament pairings
ORGANIZE_BY_LEVEL = True
BYE_IN_EARLIER_ROUND = True
AUTO_GENERATE_PLAYOFF_MATCH = False
TIEBREAK_BY_LEVEL = True
TIEBREAK_BY_MATCHUPS = False

# Tie breakers
LEVEL_ONE_LEVEL_WIN = 0.5
LEVEL_ONE_UPSET_WIN = 0.9
LEVEL_TWO_LEVEL_WIN = 0.8
LEVEL_TWO_UPSET_WIN = 1.2
LEVEL_THREE_LEVEL_WIN = 1.1
LEVEL_THREE_UPSET_WIN = 1.5
LEVEL_FOUR_LEVEL_WIN = 1.4
LEVEL_FOUR_UPSET_WIN = 1.8
LEVEL_FIVE_LEVEL_WIN = 2

ROUND_TIMES = ["6:00-6:10", "6:15-6:25", "6:30-6:40", "6:45-6:55",
         "7:00-7:10", "7:15-7:25", "7:30-7:40", "7:45-7:55"]
