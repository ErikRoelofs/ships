import math

import pygame

from logic.debug.debug import Debug
from logic.entity import Entity
from logic.ship.firecontrol import FireControl
from logic.ship.hitzone import Hitzone
from logic.ship.image_data import ImageData
from logic.ship.stats import Stats
from logic.ship.targetzone import TargetZone
from logic.ship_math.location import Location
from logic.ship_math.point import Point
from logic.turn.plan import Plan


class Ship (Entity):
    def __init__(self, location: Location, stats: Stats, hitzones: [Hitzone], targetzones: [TargetZone], faction: int, images: ImageData):
        Entity.__init__(self)
        # base stats
        self.stats = stats
        self.hitzones = hitzones
        self.targetzones = targetzones
        self.images = images
        for hitzone in self.hitzones:
            hitzone.link_to_ship(self)
        for targetzone in self.targetzones:
            targetzone.link_to_ship(self)

        # active information
        self.location = location
        self.plan = None
        self.fire_control = FireControl(self)
        self.faction = faction

    def draw(self, surface):
        if Debug().is_active():
            self.debug_draw(surface)
        else:
            rotated = pygame.transform.rotate(self.images.image, -math.degrees(self.location.rotation))
            rect = rotated.get_rect()

            # ewww
            def rotate(origin, point, angle):
                ox, oy = origin
                px, py = point

                qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
                qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
                return qx, qy

            draw_from = rotate((self.location.point.x, self.location.point.y), (self.location.point.x-20, self.location.point.y), self.location.rotation)

            rect.center = draw_from
            surface.blit(rotated, rect)

    def debug_draw(self, surface):
        self.location.debug_draw(surface)
        for hitzone in self.hitzones:
            hitzone.debug_draw(surface, self.location)

        for targetZone in self.targetzones:
            targetZone.debug_draw(surface, self.location)

    def update(self, dt):
        move_plan = self.plan.movement_plan
        move_plan.update(dt)
        heading = self.stats.engines.get_heading_from_plan(move_plan, dt)
        self.location.advance(heading[0] * dt)
        self.location.rotate(heading[1] * dt)
        self.fire_control.update(dt)

    def get_hittable_zones(self):
        return list(map(
            lambda x: x.from_location(self.location),
            self.hitzones
        ))

    def set_plan(self, plan: Plan):
        self.plan = plan

    def execute_plan(self):
        self.fire_control.prepare(self.plan.turn)

    def apply_hit(self, hit_type):
        if self.stats.bridge.current_hull > 1:
            self.stats.bridge.current_hull -= 1
            Debug().log("Hull reduced to %s!" % self.stats.bridge.current_hull, Debug.COMBAT)
        else:
            Debug().log("Hull down!", Debug.COMBAT)
            self.kill()
