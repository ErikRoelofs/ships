import random

from logic.ship.hitzone import Hitzone
from logic.ship.image_data import ImageData
from logic.ship.ship import Ship
from logic.ship.stats import Stats, Engine, Bridge, Reactor, Communications
from logic.ship.targetzone import TargetZone
from logic.ship.weapon import Weapon, BeamLaser, TurboLaser
from logic.ship_math.line import HitLine, FireArcLine
from logic.ship_math.point import Point, AimingPoint, WeaponPoint


class Demo:
    def __init__(self, location, faction):

        height = 60
        width = 120
        center_x = 20
        center_y = 0
        top = -(0.5 * height) - center_y
        left = -(0.5 * width) - center_x
        bottom = (0.5 * height) - center_y
        right = (0.5 * width) - center_x
        aim_point_offset = 0.85

        self.ship = Ship(
            location,
            Stats(Reactor(6), Bridge(5, 3), Communications(3), Engine(40, 0.2, 15, 0.1)),
            [
                Hitzone(
                    AimingPoint(-center_x, aim_point_offset * top),
                    [
                        HitLine(Point(left, top), Point(right, top))
                    ],
                    1,
                    0,
                    name='up @ %s' % faction
                ),
                Hitzone(
                    AimingPoint(aim_point_offset * right, 0),
                    [
                        HitLine(Point(right, top), Point(right, bottom))
                    ],
                    1,
                    0,
                    name='right @ %s' % faction
                ),
                Hitzone(
                    AimingPoint(-center_x, aim_point_offset * bottom),
                    [
                        HitLine(Point(right, bottom), Point(left, bottom))
                    ],
                    1,
                    0,
                    name='down @ %s' % faction
                ),
                Hitzone(
                    AimingPoint(aim_point_offset * left, 0),
                    [
                        HitLine(Point(left, bottom), Point(left, top))
                    ],
                    1,
                    0,
                    name='left @ %s' % faction
                ),
            ],
            [
                TargetZone(
                    [
                        FireArcLine(Point(-center_x, -center_y), Point(left, top)),
                        FireArcLine(Point(-center_x, -center_y), Point(right, top)),
                    ],
                    [
                        WeaponPoint(-center_x + (0.25 * width), 0.9 * top),
                        WeaponPoint(-center_x, 0.9 * top),
                        WeaponPoint(-center_x + (-0.25 * width), 0.9 * top),
                    ],
                    [
                        BeamLaser(), BeamLaser(), BeamLaser(),
                        TurboLaser(), TurboLaser(), TurboLaser(),
                    ],
                    []
                ),
                TargetZone(
                    [
                        FireArcLine(Point(-center_x, -center_y), Point(right, top)),
                        FireArcLine(Point(-center_x, -center_y), Point(right, bottom)),
                    ],
                    [
                        WeaponPoint(0.9 * right, -center_y + (0.25 * height)),
                        WeaponPoint(0.9 * right, -center_y),
                        WeaponPoint(0.9 * right, -center_y + (-0.25 * height)),
                    ],
                    [
                        BeamLaser(), BeamLaser(), BeamLaser(), BeamLaser()
                    ],
                    []
                ),
                TargetZone(
                    [
                        FireArcLine(Point(-center_x, -center_y), Point(right, bottom)),
                        FireArcLine(Point(-center_x, -center_y), Point(left, bottom)),
                    ],
                    [
                        WeaponPoint(-center_x + (0.25 * width), 0.9 * bottom),
                        WeaponPoint(-center_x, 0.9 * bottom),
                        WeaponPoint(-center_x + (-0.25 * width), 0.9 * bottom),
                    ],
                    [
                        BeamLaser(), BeamLaser(), BeamLaser(), BeamLaser()
                    ],
                    []
                ),
                TargetZone(
                    [
                        FireArcLine(Point(-center_x, -center_y), Point(left, top)),
                        FireArcLine(Point(-center_x, -center_y), Point(left, bottom)),
                    ],
                    [
                        WeaponPoint(0.9 * left, -center_y + (0.25 * height)),
                        WeaponPoint(0.9 * left, -center_y),
                        WeaponPoint(0.9 * left, -center_y + (-0.25 * height)),
                    ],
                    [
                        BeamLaser(), BeamLaser(), BeamLaser()
                    ],
                    []
                ),
            ],
            faction,
            ImageData('ships/demo/ship'+str(random.randint(1, 7))+'.png')
        )

    def getShip(self):
        return self.ship