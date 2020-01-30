import pygame

from visuals.colors import COLORS

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def intersects(self, otherLine):
        pass
    
    def distance_to(self, point):
        pass
    
    
class HitLine(Line):
    def __init__(self, p1, p2):
        Line.__init__(self, p1, p2)

    def debug_draw(self, surface, location):
        return pygame.draw.line(
            surface,
            COLORS.HIT_LINE,
            self.p1.from_location(location).as_tuple(),
            self.p2.from_location(location).as_tuple(),
            2
        )


class FireArcLine(Line):
    def __init__(self, p1, p2):
        Line.__init__(self, p1, p2)

    def debug_draw(self, surface, location):
        return pygame.draw.line(
            surface,
            COLORS.FIRE_ARC_LINE,
            self.p1.from_location(location).as_tuple(),
            self.p2.from_location(location).as_tuple(),
            2
        )
