from logic.debug.debug import Debug
from logic.ship.subsystems import Subsystem, State
from logic.ship_math.line import HitLine
from logic.ship_math.location import Location
from logic.ship_math.point import AimingPoint


class Hitzone(Subsystem):

    def __init__(self, aiming_point: AimingPoint, hit_lines: [HitLine], shields: int, aux_shields: int, can_harden=False, name: str='', origin=None):
        initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, aux_shields > 0, can_harden)
        self.aiming_point = aiming_point
        self.hit_lines = hit_lines
        self.shields = shields
        self.aux_shields = aux_shields
        self.can_harden = can_harden
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
            self.aux_shields,
            self.can_harden,
            name=self.name,
            origin=self
        )

    def apply_hit(self, hit_type):
        if self.origin:
            self.origin.apply_hit(hit_type)
        else:
            if self.state.aux and self.aux_shields > 0:
                self.aux_shields -= 1
                Debug().log("Aux shields down to %s for %s!" % (self.aux_shields, self.name), Debug.COMBAT)
            elif self.state.on and self.shields > 0:
                self.shields -= 1
                Debug().log("Shields down to %s for %s!" % (self.shields, self.name), Debug.COMBAT)
            else:
                Debug().log("Shields depleted (or off) for %s!" % self.name, Debug.COMBAT)
                self.ship.apply_hit(hit_type)