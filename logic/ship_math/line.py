from visuals.colors import COLORS

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def intersects(self, otherLine):
        pass
    
    def distance_to(self, point):
        pass
    
    
class HitLine(Line):
    def __init__(self, p1, p2):
        Line.__init__(self, p1, p2)
        
        
class FireArcLine(Line):
    def __init__(self, p1, p2):
        Line.__init__(self, p1, p2)
        
        
class DebugHitLine(HitLine):
    def __init__(self, p1, p2):
        HitLine.__init__(self, p1, p2)
        self.color = COLORS.HIT_LINE


class DebugFireArcLine(FireArcLine):
    def __init__(self, p1, p2):
        FireArcLine.__init__(self, p1, p2)
        self.color = COLORS.FIRE_ARC_LINE
