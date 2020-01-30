from logic.entity import Entity


class Turn:
    def __init__(self, duration: int, entities: [Entity]):
        self.duration = duration
        self.duration_left = duration
        self.entities = entities

    def update(self, dt):
        self.duration_left -= dt
        self.duration_left = max(self.duration_left, 0)
        for entity in self.entities:
            entity.update(dt)

    def busy(self) -> bool:
        return self.duration_left > 0

    def percentage_left(self) -> float:
        return self.duration_left / self.duration

    def start_next(self):
        self.duration_left = self.duration
