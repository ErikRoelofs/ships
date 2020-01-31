from logic.debug.debug import Debug
from logic.ship.hitzone import Hitzone
from logic.ship_math.line import Line
from logic.ship_math.location import Location
from logic.ship_math.point import WeaponPoint


def get_target_line(my_location: Location, hardpoint: WeaponPoint, target: Hitzone) -> Line:
    return Line(hardpoint.from_location(my_location), target.aiming_point)


class TargetZone:
    def __init__(self, fire_arc_lines, hardpoints, weapons):
        self.fire_arc_lines = fire_arc_lines
        self.hardpoints = hardpoints
        self.weapons = weapons

    def get_valid_targets(self, my_location, targets, range):
        valid_targets = []
        for point in self.hardpoints:
            for target in targets:
                if self.is_valid_target(my_location, point, target, range):
                    valid_targets.append(target)
        return valid_targets

    def is_valid_target(self, my_location: Location, hardpoint: WeaponPoint, target, range):
        debug = Debug()
        # range check
        target_line = get_target_line(my_location, hardpoint, target)
        debug.log("Targetline: %s" % target_line, debug.MATH)

        if target_line.length() > range:
            debug.log("Line length: %s versus range of %s; cannot reach!" % (target_line.length(), range), debug.MATH)
            return False

        # intersects at least one hitline check
        intersects_hit_line = False
        for hitline in target.hit_lines:
            debug.log("Hitline: %s " % hitline, debug.MATH)
            if hitline.intersects(target_line):
                intersects_hit_line = True

        if not intersects_hit_line:
            debug.log("Not intersecting any of the hit-lines!", debug.MATH)
            return False

        # does not intersect the (extended) fire arcs
        for fire_arc_line in self.fire_arc_lines:
            if fire_arc_line.extended_by(range).from_location(my_location).intersects(target_line):
                debug.log("Crossing one of our own fire arcs!", debug.MATH)
                return False

        debug.log("Valid shot!", debug.MATH)
        return True

    def debug_draw(self, surface, location):
        for line in self.fire_arc_lines:
            line.debug_draw(surface, location)
        for hardpoint in self.hardpoints:
            hardpoint.debug_draw(surface, location)

    def debug_draw_targeting_lines(self, surface, location, targets, range):
        for hardpoint in self.hardpoints:
            for target in targets:
                if self.is_valid_target(location, hardpoint, target, range):
                    target_line = get_target_line(location, hardpoint, target)
                    target_line.debug_draw_raw(surface, color=(0, 255, 0))

    def debug_draw_specific_targeting_line(self, surface, hardpoint, location, targets, range):
        for target in targets:
            if self.is_valid_target(location, hardpoint, target, range):
                target_line = get_target_line(location, hardpoint, target)
                target_line.debug_draw_raw(surface, color=(0, 255, 0))
            else:
                target_line = get_target_line(location, hardpoint, target)
                target_line.debug_draw_raw(surface, color=(255, 0, 0))