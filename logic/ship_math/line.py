import pygame
import math

from logic.ship_math.location import Location
from logic.ship_math.point import Point
from visuals.colors import COLORS


def slope(p1, p2):
    if (p2[0] - p1[0]) == 0:
        print('high sloping -> %s - %s' % (p2, p1))
        return 1e10
    return (p2[1] - p1[1]) * 1. / (p2[0] - p1[0])


def y_intercept(slope, p1):
    return p1[1] - 1. * slope * p1[0]


def intersect(line1, line2):
    min_allowed = 1e-5  # guard against overflow
    big_value = 1e10  # use instead (if overflow would have occurred)
    m1 = slope(line1[0], line1[1])
    b1 = y_intercept(m1, line1[0])
    m2 = slope(line2[0], line2[1])
    b2 = y_intercept(m2, line2[0])
    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    y2 = m2 * x + b2
    return int(round(x)), int(round(y))


def segment_intersect(line1, line2):
    intersection_pt = intersect(line1, line2)
#    print("point of intersection: %s" % Point(intersection_pt[0], intersection_pt[1]))

    if (line1[0][0] < line1[1][0]):
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
#            print( "exit 1" )
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
#            print("exit 2")
            return None

    if (line2[0][0] < line2[1][0]):
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
#            print("exit 3")
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
#            print("exit 4")
            return None

    return intersection_pt


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def as_primitive(self):
        return [self.p1.as_tuple(), self.p2.as_tuple()]

    def intersects(self, other_line):
        return segment_intersect(self.as_primitive(), other_line.as_primitive())

    def length(self):
        return math.sqrt((self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2)

    def from_location(self, location: Location):
        return type(self)(self.p1.from_location(location), self.p2.from_location(location))

    def add_point(self, point: Point):
        return type(self)(self.p1.add_point(point), self.p2.add_point(point))

    def debug_draw(self, surface, location, color):
        return pygame.draw.line(
            surface,
            color,
            self.p1.from_location(location).as_int_tuple(),
            self.p2.from_location(location).as_int_tuple(),
            2
        )

    def debug_draw_raw(self, surface, color):
        return pygame.draw.line(
            surface,
            color,
            self.p1.as_int_tuple(),
            self.p2.as_int_tuple(),
            2
        )

    def __str__(self):
        return str(self.p1) + ' - ' + str(self.p2)

class HitLine(Line):
    def __init__(self, p1, p2):
        Line.__init__(self, p1, p2)

    def debug_draw(self, surface, location, color=None):
        return pygame.draw.line(
            surface,
            COLORS.HIT_LINE,
            self.p1.from_location(location).as_int_tuple(),
            self.p2.from_location(location).as_int_tuple(),
            2
        )


class FireArcLine(Line):
    def __init__(self, p1, p2):
        Line.__init__(self, p1, p2)

    def debug_draw(self, surface, location, color=None):
        return pygame.draw.line(
            surface,
            COLORS.FIRE_ARC_LINE,
            self.p1.from_location(location).as_int_tuple(),
            self.p2.from_location(location).as_int_tuple(),
            2
        )

    def extended_by(self, range):
        len = self.length()
        new_len = len + range
        cx = self.p2.x + (self.p2.x - self.p1.x) / len * new_len
        cy = self.p2.y + (self.p2.y - self.p1.y) / len * new_len
        dx = self.p1.x - (self.p2.x - self.p1.x) / len * new_len
        dy = self.p1.y - (self.p2.y - self.p1.y) / len * new_len
        return FireArcLine(Point(cx, cy), Point(dx, dy))
