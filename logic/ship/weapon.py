import random

import pygame

from logic.debug.debug import Debug
from logic.entity import Entity
from logic.ship.hit import Hit
from logic.ship.hitzone import Hitzone
from logic.ship.ship import Ship
from logic.ship_math.point import WeaponPoint, Point
from logic.turn.turn import active_turn


class WeaponType:

    def __init__(self, range):
        self.range = range

    @classmethod
    def beam_laser(cls):
        return WeaponType(300)

    @classmethod
    def turbo_laser(cls):
        return WeaponType(500)


class Weapon:
    def __init__(self, type: WeaponType):
        self.type = type

    def range(self):
        return self.type.range

    def fire(self, ship: Ship, hardpoint: WeaponPoint, target_zone: Hitzone):
        Debug().log("Boom!", Debug.COMBAT)
        hit_effect = target_zone.apply_hit(self.roll_hit_type())
        self.create_entity(ship, hardpoint, target_zone)

    def create_entity(self, ship, hardpoint, target_zone):
        pass

    def roll_hit_type(self):
        rand = random.randint(0,9)
        return self.hit_table()[rand]

    def hit_table(self):
        return [Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR]

    def color(self):
        return (0,0,0)


class BeamLaser(Weapon):
    def __init__(self):
        Weapon.__init__(self, WeaponType.beam_laser())

    def create_entity(self, ship: Ship, hardpoint: WeaponPoint, target_zone: Hitzone):
        active_turn().register_entity(BeamEffect(ship, hardpoint, target_zone.aiming_point))

    def hit_table(self):
        return [Hit.MISS, Hit.MISS, Hit.MISS, Hit.WEAK, Hit.WEAK, Hit.WEAK, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.PIERCING]

    def color(self):
        return (0,0,255)


class TurboLaser(Weapon):
    def __init__(self):
        Weapon.__init__(self, WeaponType.turbo_laser())

    def create_entity(self, ship: Ship, hardpoint: WeaponPoint, target_zone: Hitzone):
        active_turn().register_entity(TurboBeamEffect(ship, hardpoint, target_zone.aiming_point))

    def hit_table(self):
        return [Hit.MISS, Hit.MISS, Hit.MISS, Hit.WEAK, Hit.WEAK, Hit.WEAK, Hit.REGULAR, Hit.REGULAR, Hit.REGULAR, Hit.PIERCING]

    def color(self):
        return (255,0,0)


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


class TurboBeamEffect(Entity):
    def __init__(self, ship: Ship, hardpoint: WeaponPoint, to_location: Point):
        Entity.__init__(self)
        self.ship = ship
        self.hardpoint = hardpoint
        self.to_location = to_location
        self.max_duration = 2
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
                (255 * (perc/3), 0, 0),
                self.hardpoint.from_location(self.ship.location).as_int_tuple(),
                self.to_location.as_int_tuple(),
                7
            )
        if perc > 0.3:
            pygame.draw.line(
                screen,
                (255, 155 * (perc/2), 155 * (perc/2)),
                self.hardpoint.from_location(self.ship.location).as_int_tuple(),
                self.to_location.as_int_tuple(),
                5
            )
        pygame.draw.line(
            screen,
            (255, 255 * perc, 255 * perc),
            self.hardpoint.from_location(self.ship.location).as_int_tuple(),
            self.to_location.as_int_tuple(),
            3
        )

