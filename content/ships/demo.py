from logic.ship.ship import Ship
from logic.ship.weapon import Weapon
from logic.ship.hitzone import Hitzone
from logic.ship.targetzone import TargetZone
from logic.ship.stats import Stats, Engine
from logic.ship_math.point import Point, AimingPoint, WeaponPoint
from logic.ship_math.location import Location
from logic.ship_math.line import HitLine, FireArcLine

class Demo:
    def __init__(self):
        self.ship = Ship(
            Location(Point(50, 50), 0),
            Stats(5, 6, 3, 3, Engine(4, 15)),
            [
                Hitzone(
                    AimingPoint(60, 60),
                    [
                        HitLine(Point(10, 10), Point(100, 10))
                    ],
                    3
                )
            ],
            [
                TargetZone(
                    [
                        FireArcLine(Point(10, 10), Point(100, 10))
                    ],
                    [
                        WeaponPoint(75, 75)
                    ],
                    [
                        Weapon()
                    ]
                )
            ]
        )