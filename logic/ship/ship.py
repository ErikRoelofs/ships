from logic.entity import Entity
from logic.ship.hitzone import Hitzone
from logic.turn.plan import Plan


class Ship (Entity):
    def __init__(self, location, stats, hitzones: [Hitzone], targetzones):
        # base stats
        self.stats = stats
        self.hitzones = hitzones
        self.targetzones = targetzones

        # active information
        self.location = location
        self.current_speed = 0
        self.current_turn = 0
        self.plan = None

    def debug_draw(self, surface):
        self.location.debug_draw(surface)
        for hitzone in self.hitzones:
            hitzone.debug_draw(surface, self.location)

        for targetZone in self.targetzones:
            targetZone.debug_draw(surface, self.location)

    def update(self, dt):
        move_plan = self.plan.movement_plan
        move_plan.update(dt)
        heading = move_plan.get_current_heading()
        self.location.advance(heading[0] * dt)
        self.location.rotate(heading[1] * dt)

    def get_hittable_zones(self):
        return list(map(
            lambda x: x.from_location(self.location),
            self.hitzones
        ))

    def set_plan(self, plan: Plan):
        self.plan = plan

    def execute_plan(self):
        pass  # no initial executable statements yet
