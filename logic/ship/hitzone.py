from logic.ship_math.line import HitLine
from logic.ship_math.location import Location
from logic.ship_math.point import AimingPoint


class Hitzone:

    def __init__(self, aiming_point: AimingPoint, hit_lines: [HitLine], shields: int):
        self.aiming_point = aiming_point
        self.hit_lines = hit_lines
        self.shields = shields

    def debug_draw(self, surface, location: Location):
        for line in self.hit_lines:
            line.debug_draw(surface, location)

        self.aiming_point.debug_draw(surface, location)

    def from_location(self, my_location: Location):
        return Hitzone(
            self.aiming_point.from_location(my_location),
            list(map(lambda x: x.from_location(my_location), self.hit_lines)),
            self.shields
        )
