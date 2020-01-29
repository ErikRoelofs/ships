import pygame

from visuals.colors import COLORS


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def from_location(self, location):
        return type(self)(location.x + self.x, location.y + self.y)


class WeaponPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def debug_draw(self, surface, location):
        pygame.draw.circle(surface, COLORS.HARDPOINT, self.from_location(location).as_tuple(), 3)

class AimingPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def debug_draw(self, surface, location):
        pygame.draw.circle(surface, COLORS.TARGETING_POINT, self.from_location(location).as_tuple(), 3)
