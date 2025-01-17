"""Snake Game"""
import sys

import numpy as np
import pygame

from constants import CELL_SIZE, TICK_RATE, Action, Direction, Point
from game_objects import Food, Snake

pygame.init()
font = pygame.font.Font("arial.ttf", 25)
# font = pygame.font.SysFont('arial', 25)


# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class SnakeGameAI:
    """Version of Snake game for AI to play"""

    direction: Direction
    head: Point
    snake: list[Point]
    score: int
    food: Food
    frame_iteration: int

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        """
        Reset the game's state.
        """
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - CELL_SIZE, self.head.y),
            Point(self.head.x - (2 * CELL_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = Food(self.w, self.h, CELL_SIZE)
        self.frame_iteration = 0

    def play_action(self, action: Action):
        """
        Play an action and return the game's state.
        Used for training the AI model.
        """
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food.position:
            self.score += 1
            reward = 10
            self.food.randomize_position(self.snake)
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(TICK_RATE)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        """Check if the snake collides with the boundary or itself"""
        if pt is None:
            pt = self.head
        # hits boundary
        if (
            pt.x > self.w - CELL_SIZE
            or pt.x < 0
            or pt.y > self.h - CELL_SIZE
            or pt.y < 0
        ):
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        """Updates the game's display"""
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE1, pygame.Rect(pt.x, pt.y, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
            )

        self.food.draw(self.display)

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action: Action):
        """Move the snake"""
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        match self.direction:
            case Direction.RIGHT:
                x += CELL_SIZE
            case Direction.LEFT:
                x -= CELL_SIZE
            case Direction.DOWN:
                y += CELL_SIZE
            case Direction.UP:
                y -= CELL_SIZE

        self.head = Point(x, y)
