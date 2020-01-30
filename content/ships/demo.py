from logic.ship.hitzone import Hitzone
from logic.ship.ship import Ship
from logic.ship.stats import Stats, Engine
from logic.ship.targetzone import TargetZone
from logic.ship.weapon import Weapon
from logic.ship_math.line import HitLine, FireArcLine
from logic.ship_math.point import Point, AimingPoint, WeaponPoint


class Demo:
    def __init__(self, location):
        self.ship = Ship(
            location,
            Stats(5, 6, 3, 3, Engine(4, 15)),
            [
                Hitzone( #up
                    AimingPoint(0, -20),
                    [
                        HitLine(Point(-30, -40), Point(30, -40))
                    ],
                    3
                ),
                Hitzone( #right
                    AimingPoint(20, 20),
                    [
                        HitLine(Point(30, -40), Point(30, 80))
                    ],
                    3
                ),
                Hitzone( #down
                    AimingPoint(0, 70),
                    [
                        HitLine(Point(30, 80), Point(-30, 80))
                    ],
                    3
                ),
                Hitzone( #left
                    AimingPoint(-20, 20),
                    [
                        HitLine(Point(-30, -40), Point(-30, 80))
                    ],
                    3
                ),
            ],
            [
                # TL -30, -40 (origin = 0, 0, center = 0, 20
                # TR  30, -40
                # BL -30, 80
                # BR 30, 80

                TargetZone(  # up
                    [
                        FireArcLine(Point(0, 20), Point(-30, -40)),
                        FireArcLine(Point(0, 20), Point(30, -40)),
                    ],
                    [
                        WeaponPoint(-15, -35),
                        WeaponPoint(0, -35),
                        WeaponPoint(15, -35),
                    ],
                    [
                        Weapon()
                    ]
                ),
                TargetZone(  # right
                    [
                        FireArcLine(Point(0, 20), Point(30, 80)),
                        FireArcLine(Point(0, 20), Point(30, -40)),
                    ],
                    [
                        WeaponPoint(25, -20),
                        WeaponPoint(25, 0),
                        WeaponPoint(25, 20),
                        WeaponPoint(25, 40),
                    ],
                    [
                        Weapon()
                    ]
                ),
                TargetZone(  # down
                    [
                        FireArcLine(Point(0, 20), Point(-30, 80)),
                        FireArcLine(Point(0, 20), Point(30, 80)),
                    ],
                    [
                        WeaponPoint(-15, 75),
                        WeaponPoint(0, 75),
                        WeaponPoint(15, 75),
                    ],
                    [
                        Weapon()
                    ]
                ),
                TargetZone(  # left
                    [
                        FireArcLine(Point(0, 20), Point(-30, 80)),
                        FireArcLine(Point(0, 20), Point(-30, -40)),
                    ],
                    [
                        WeaponPoint(-25, -20),
                        WeaponPoint(-25, 0),
                        WeaponPoint(-25, 20),
                        WeaponPoint(-25, 40),
                    ],
                    [
                        Weapon()
                    ]
                ),
            ]
        )

    def getShip(self):
        return self.ship