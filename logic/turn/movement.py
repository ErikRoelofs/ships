class MovementSegment:
    def __init__(self, speed: float, rotation: float, duration: float):
        self.duration = duration
        self.rotation = rotation
        self.speed = speed


class MovementPlan:
    def __init__(self, segments: [MovementSegment]):
        segments.append(MovementSegment(0, 0, 1000))
        self.segments = segments
        self.active_segment = segments.pop(0)

    def get_current_heading(self):
        return self.active_segment.speed, self.active_segment.rotation

    def update(self, dt):
        self.active_segment.duration -= dt
        if self.active_segment.duration < 0:
            self.active_segment = self.segments.pop(0)

def empty_movement_plan():
    return MovementPlan([MovementSegment(0, 0, 1000)])
