class Hitzone:
    def __init__(self, aiming_point, hit_lines, shields):
        self.aiming_point = aiming_point
        self.hit_lines = hit_lines
        self.shields = shields

    def debug_draw(self, surface, location):
        for line in self.hit_lines:
            line.debug_draw(surface, location)

        self.aiming_point.debug_draw(surface, location)
