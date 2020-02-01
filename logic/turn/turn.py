from logic.space.space import Space


class Turn:
    active_turn = None

    def __init__(self, duration: int):
        self.duration = duration
        self.duration_left = duration
        self.entities = []
        Turn.active_turn = self

    def register_entity(self, entity):
        from logic.ship.ship import Ship
        self.entities.append(entity)
        if isinstance(entity, Ship):
            Space.register_ship(entity)

    def remove_entity(self, entity):
        from logic.ship.ship import Ship
        self.entities.remove(entity)
        if isinstance(entity, Ship):
            Space.remove_ship(entity)

    def update(self, dt):
        self.duration_left -= dt
        self.duration_left = max(self.duration_left, 0)
        for entity in self.entities:
            entity.update(dt)

    def draw(self, screen):
        for entity in self.entities:
            entity.draw(screen)

    def busy(self) -> bool:
        return self.duration_left > 0

    def percentage_left(self) -> float:
        return self.duration_left / self.duration

    def start_next(self):
        self.duration_left = self.duration


def active_turn() -> Turn:
    return Turn.active_turn
