class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class WeaponPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)


class AimingPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
