"""Constants for the game Snake."""

from collections import namedtuple
from enum import Enum

# Game Config
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
TICK_RATE = 1000
SHOULD_RESTART_ON_GAME_OVER = False
MOVES_PER_SEGMENT = 100
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 155, 0)
BLACK = (20, 20, 20)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Enums
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Action(Enum):
    TURN_LEFT = 0
    TURN_RIGHT = 1
    GO_STRAIGHT = 2


# Misc

CLOCK_WISE_ARRAY = (Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP)
Point = namedtuple("Point", "x, y")
