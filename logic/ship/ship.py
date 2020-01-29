class Ship:
    def __init__(self, location, stats, hitzones, targetzones):
        self.location = location
        self.stats = stats
        self.hitzones = hitzones
        self.targetzones = targetzones

    def debug_draw(self, surface):
        for hitzone in self.hitzones:
            hitzone.debug_draw(surface, self.location)

        for targetZone in self.targetzones:
            targetZone.debug_draw(surface, self.location)