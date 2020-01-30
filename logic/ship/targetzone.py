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
        #print = lambda x: x
        # range check
        target_line = get_target_line(my_location, hardpoint, target)
        print("Targetline: %s" % target_line)

        if target_line.length() > range:
            print("Line length: %s versus range of %s; cannot reach!" % (target_line.length(), range))
            return False

        # intersects at least one hitline check
        intersects_hit_line = False
        for hitline in target.hit_lines:
            print("Hitline: %s " % hitline)
            if hitline.intersects(target_line):
                intersects_hit_line = True

        if not intersects_hit_line:
            print("Not intersecting any of the hit-lines!")
            return False

        # does not intersect the (extended) fire arcs
        for fire_arc_line in self.fire_arc_lines:
            if fire_arc_line.extended_by(range).from_location(my_location).intersects(target_line):
                print("Crossing one of our own fire arcs!")
                return False

        print("Valid shot!")
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