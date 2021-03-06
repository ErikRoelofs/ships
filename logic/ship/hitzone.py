from pygame.surface import Surface

from logic.debug.debug import Debug
from logic.ship.hit import Hit, Impact
from logic.ship.subsystems import Subsystem, State
from logic.ship_math.line import HitLine
from logic.ship_math.location import Location
from logic.ship_math.point import AimingPoint
from visuals.fonts import Fonts


class Hitzone(Subsystem):

    def __init__(self, aiming_point: AimingPoint, hit_lines: [HitLine], shields: int, aux_shields: int, can_harden=False, debug_name: str='', origin=None):
        initial_state = State(on=False, aux=False, overload=False)
        Subsystem.__init__(self, "Shields", initial_state, aux_shields > 0, can_harden)
        self.aiming_point = aiming_point
        self.hit_lines = hit_lines
        self.max_shields = shields
        self.shields = shields
        self.max_aux_shields = aux_shields
        self.aux_shields = aux_shields
        self.can_harden = can_harden
        self.ship = None
        self.debug_name = debug_name
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
            debug_name=self.name,
            origin=self
        )

    def apply_hit(self, hit_type):
        if self.origin:
            return self.origin.apply_hit(hit_type)
        else:
            if hit_type == Hit.MISS:
                Debug().log("It's a miss for %s!" % self.debug_name, Debug.COMBAT)
                return Impact.MISS
            if hit_type == Hit.PIERCING:
                Debug().log("It's a piercing hit for %s!" % self.debug_name, Debug.COMBAT)
                self.ship.apply_hit(hit_type)
                if (self.state.aux and self.aux_shields > 0) or (self.state.on and self.shields > 0):
                    return Impact.PENETRATED
                return Impact.ON_HULL
            if self.state.aux and self.aux_shields > 0:
                self.aux_shields -= 1
                Debug().log("Aux shields down to %s for %s!" % (self.aux_shields, self.debug_name), Debug.COMBAT)
                return Impact.SHIELDED
            elif self.state.on and self.shields > 0:
                self.shields -= 1
                Debug().log("Shields down to %s for %s!" % (self.shields, self.debug_name), Debug.COMBAT)
                return Impact.SHIELDED
            else:
                Debug().log("Shields depleted (or off) for %s!" % self.debug_name, Debug.COMBAT)
                self.ship.apply_hit(hit_type)
                return Impact.ON_HULL

    def draw_status(self, surface: Surface):
        text = Fonts.shields.render(str(self.shields) + '/' + str(self.max_shields), True, (0, 0, 255))
        text2 = Fonts.shields.render(str(self.aux_shields) + '/' + str(self.max_aux_shields), True, (0, 0, 255))
        surface.blit(text, (0, 30))
        surface.blit(text2, (0, 10))
