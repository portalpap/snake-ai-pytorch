"""
Snake class
"""

import random
from abc import ABC, abstractmethod

import pygame
from pygame.surface import Surface

from constants import (
    CLOCK_WISE_ARRAY,
    DARK_GREEN,
    LIGHT_GREEN,
    RED,
    Direction,
)


class GameObject(ABC):
    """Base class for game objects."""

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the object on the screen."""


class Food(GameObject):
    """Food class."""

    position: tuple[int, int]

    def __init__(self, screen_width: int, screen_height: int, size: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.randomize_position()

    @property
    def x(self) -> int:
        """Return the x coordinate of the food."""
        return self.position[0]

    @property
    def y(self) -> int:
        """Return the y coordinate of the food."""
        return self.position[1]

    def randomize_position(self) -> None:
        """Randomize the position of the food."""
        self.position = (
            random.randrange(0, self.screen_width - self.size, self.size),
            random.randrange(0, self.screen_height - self.size, self.size),
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the food on the screen."""
        rect = pygame.Rect(self.position, (self.size, self.size))
        pygame.draw.rect(screen, RED, rect)


class Snake(GameObject):
    """Snake class."""

    def __init__(self, x: int, y: int, size: int) -> None:
        self.body_segments: list[tuple[int, int]] = [(x, y)]
        self.direction: Direction = Direction.RIGHT
        self.size = size

    @property
    def head(self) -> tuple[int, int]:
        """Return the head of the snake."""
        return self.body_segments[0]

    def change_direction(self, new_direction: Direction) -> None:
        """Change the direction of the snake."""
        self.direction = new_direction

    def turn_left(self) -> Direction:
        """Turn the snake left."""
        current_direction_index = CLOCK_WISE_ARRAY.index(self.direction)

        new_direction_index = (current_direction_index - 1) % 4
        self.direction = CLOCK_WISE_ARRAY[new_direction_index]

        return self.direction

    def turn_right(self) -> Direction:
        """Turn the snake right."""
        current_direction_index = CLOCK_WISE_ARRAY.index(self.direction)

        new_direction_index = (current_direction_index + 1) % 4
        self.direction = CLOCK_WISE_ARRAY[new_direction_index]

        return self.direction

    def move(self) -> None:
        """Move the snake."""
        x, y = self.body_segments[0]
        if self.direction == Direction.UP:
            y -= self.size
        elif self.direction == Direction.RIGHT:
            x += self.size
        elif self.direction == Direction.DOWN:
            y += self.size
        elif self.direction == Direction.LEFT:
            x -= self.size

        self.body_segments.insert(0, (x, y))
        self.body_segments.pop()

    def check_collision_with_boundaries(self, width: int, height: int) -> bool:
        """Check if the snake has collided with the boundaries."""
        x, y = self.body_segments[0]
        return x >= width or x < 0 or y >= height or y < 0

    def check_collision_with_self(self) -> bool:
        """Check if the snake has collided with itself."""
        return self.body_segments[0] in self.body_segments[1:]

    def check_collision_with_food(self, food: Food) -> bool:
        """Check if the snake has eaten the food."""
        return food.position in self.body_segments

    def grow(self) -> None:
        """Add a new segment to the snake."""
        self.body_segments.append(self.body_segments[-1])

    def draw(self, screen: Surface) -> None:
        """Draw the snake on the screen."""
        for _, segment in enumerate(self.body_segments):
            full_rect = pygame.Rect(segment, (self.size, self.size))
            small_size = int(self.size * 0.8)
            offset = int((self.size - small_size) / 2)
            smaller_rect = pygame.Rect(
                (segment[0] + offset, segment[1] + offset), (small_size, small_size)
            )
            pygame.draw.rect(screen, DARK_GREEN, full_rect)
            pygame.draw.rect(screen, LIGHT_GREEN, smaller_rect)

    def __len__(self) -> int:
        return len(self.body_segments)

    def __getitem__(self, index: int) -> tuple[int, int]:
        return self.body_segments[index]
