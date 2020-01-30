from math import cos, sin

import pygame

from logic.ship_math.point import Point
from visuals.colors import COLORS


class Location:
    def __init__(self, point, rotation):
        self.point = point
        self.rotation = rotation
        self.x = self.point.x
        self.y = self.point.y

    def advance(self, distance):
        dx = cos(self.rotation) * distance
        dy = sin(self.rotation) * distance
        self.x += dx
        self.y += dy
        self.point = Point(self.x, self.y)

    def rotate(self, rotation):
        self.rotation += rotation

    def debug_draw(self, surface):
        pygame.draw.circle(surface, COLORS.REGULAR_POINT, self.point.as_int_tuple(), 3)
