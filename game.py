import random
from enum import Enum

import numpy as np
import pygame

from constants import CELL_SIZE, TICK_RATE, Action, Direction, Point

pygame.init()
font = pygame.font.Font("arial.ttf", 25)
# font = pygame.font.SysFont('arial', 25)


# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class Food:
    """Food class."""

    position: Point

    def __init__(self, screen_width: int, screen_height: int, size: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.randomize_position()

    def randomize_position(self, snake: list[Point] = ()) -> None:
        """Randomize the position of the food."""
        x = random.randrange(0, self.screen_width - self.size, self.size)
        y = random.randrange(0, self.screen_height - self.size, self.size)
        self.position = Point(x, y)
        if self.position in snake:
            self.randomize_position(snake)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the food on the screen."""
        rect = pygame.Rect(self.position, (self.size, self.size))
        pygame.draw.rect(screen, RED, rect)


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
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
                quit()

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
