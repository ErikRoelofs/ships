from logic.ship.targetzone import TargetZone
from logic.ship_math.location import Location
from logic.ship_math.point import WeaponPoint


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

    def fire(self, location: Location, hardpoint: WeaponPoint, target_zone: TargetZone):
        print("Boom!")


class BeamLaser(Weapon):
    def __init__(self):
        Weapon.__init__(self, WeaponType.beam_laser())