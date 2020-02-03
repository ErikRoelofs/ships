from logic.debug.debug import Debug
from logic.ship_math.line import HitLine
from logic.ship_math.location import Location
from logic.ship_math.point import AimingPoint


class Hitzone:

    def __init__(self, aiming_point: AimingPoint, hit_lines: [HitLine], shields: int, name: str, origin=None):
        self.aiming_point = aiming_point
        self.hit_lines = hit_lines
        self.shields = shields
        self.ship = None
        self.name = name
        self.origin = origin

    def link_to_ship(self, ship):
        self.ship = ship

    def debug_draw(self, surface, location: Location):
        for line in self.hit_lines:
            line.debug_draw(surface, location)

        self.aiming_point.debug_draw(surface, location)

    def from_location(self, my_location: Location):
        return Hitzone(
            self.aiming_point.from_location(my_location),
            list(map(lambda x: x.from_location(my_location), self.hit_lines)),
            self.shields,
            self.name,
            origin=self
        )

    def apply_hit(self, hit_type):
        if self.origin:
            self.origin.apply_hit(hit_type)
        else:
            if self.shields > 0:
                self.shields -= 1
                Debug().log("Shields down to %s for %s!" % (self.shields, self.name), Debug.COMBAT)
            else:
                Debug().log("Shields depleted for %s!" % self.name, Debug.COMBAT)
                self.ship.apply_hit(hit_type)