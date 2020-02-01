import pygame

from logic.entity import Entity
from logic.ship.hitzone import Hitzone
from logic.ship.ship import Ship
from logic.ship_math.point import WeaponPoint, Point
from logic.turn.turn import active_turn


class Hit:
    MISS = 0
    WEAK = 1
    REGULAR = 2
    PIERCING = 3


class WeaponType:

    def __init__(self, range):
        self.range = range

    @classmethod
    def beam_laser(cls):
        return WeaponType(300)


class Weapon:
    def __init__(self, type: WeaponType):
        self.type = type

    def range(self):
        return self.type.range

    def fire(self, ship: Ship, hardpoint: WeaponPoint, target_zone: Hitzone):
        print("Boom!")
        target_zone.apply_hit(Hit.REGULAR)
        self.create_entity(ship, hardpoint, target_zone)

    def create_entity(self, ship, hardpoint, target_zone):
        pass


class BeamLaser(Weapon):
    def __init__(self):
        Weapon.__init__(self, WeaponType.beam_laser())

    def create_entity(self, ship: Ship, hardpoint: WeaponPoint, target_zone: Hitzone):
        active_turn().register_entity(BeamEffect(ship, hardpoint, target_zone.aiming_point))


class BeamEffect(Entity):
    def __init__(self, ship: Ship, hardpoint: WeaponPoint, to_location: Point):
        Entity.__init__(self)
        self.ship = ship
        self.hardpoint = hardpoint
        self.to_location = to_location
        self.max_duration = 1
        self.duration = self.max_duration

    def update(self, dt):
        self.duration -= dt
        if self.duration < 0:
            active_turn().remove_entity(self)

    def draw(self, screen):
        perc = self.duration / self.max_duration
        perc = max(perc, 0)
        if perc > 0.6:
            pygame.draw.line(
                screen,
                (0, 0, 255 * (perc/3)),
                self.hardpoint.from_location(self.ship.location).as_int_tuple(),
                self.to_location.as_int_tuple(),
                5
            )
        if perc > 0.3:
            pygame.draw.line(
                screen,
                (155 * (perc/2), 155 * (perc/2), 255),
                self.hardpoint.from_location(self.ship.location).as_int_tuple(),
                self.to_location.as_int_tuple(),
                3
            )
        pygame.draw.line(
            screen,
            (255 * perc, 255 * perc, 255),
            self.hardpoint.from_location(self.ship.location).as_int_tuple(),
            self.to_location.as_int_tuple(),
            1
        )

