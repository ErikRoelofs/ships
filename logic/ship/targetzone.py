class TargetZone:
    def __init__(self, fire_arc_lines, hardpoints, weapons):
        self.fire_arc_lines = fire_arc_lines
        self.hardpoints = hardpoints
        self.weapons = weapons

    def debug_draw(self, surface, location):
        for line in self.fire_arc_lines:
            line.debug_draw(surface, location)
        for hardpoint in self.hardpoints:
            hardpoint.debug_draw(surface, location)
