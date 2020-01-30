import pygame
from visuals.colors import COLORS
from math import cos, sin


def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def as_int_tuple(self):
        return int(self.x), int(self.y)

    def add_point(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def from_location(self, location):
        new_x, new_y = rotate((0, 0), self.as_tuple(), location.rotation)
        return type(self)(location.x + new_x, location.y + new_y)

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


class WeaponPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def debug_draw(self, surface, location):
        pygame.draw.circle(surface, COLORS.HARDPOINT, self.from_location(location).as_int_tuple(), 3)


class AimingPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def debug_draw(self, surface, location):
        pygame.draw.circle(surface, COLORS.TARGETING_POINT, self.from_location(location).as_int_tuple(), 3)
