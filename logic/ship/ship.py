from logic.ship.hitzone import Hitzone


class Ship:
    def __init__(self, location, stats, hitzones: [Hitzone], targetzones):
        # base stats
        self.stats = stats
        self.hitzones = hitzones
        self.targetzones = targetzones

        # active information
        self.location = location
        self.current_speed = 0
        self.current_turn = 0

    def set_motion(self, speed, angle):
        self.current_speed = speed
        self.current_turn = angle

    def debug_draw(self, surface):
        self.location.debug_draw(surface)
        for hitzone in self.hitzones:
            hitzone.debug_draw(surface, self.location)

        for targetZone in self.targetzones:
            targetZone.debug_draw(surface, self.location)

    def update(self, dt):
        self.location.advance(self.current_speed * dt)
        self.location.rotate(self.current_turn * dt)

    def get_hittable_zones(self):
        return list(map(
            lambda x: x.from_location(self.location),
            self.hitzones
        ))
