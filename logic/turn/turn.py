from logic.space.space import Space


class Turn:
    active_turn = None

    def __init__(self, duration: int):
        self.duration = duration
        self.duration_left = duration
        self.entities = []
        self.ended = True
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

    def done(self) -> bool:
        return self.duration_left <= 0

    def busy(self) -> bool:
        return self.duration_left > 0

    def percentage_left(self) -> float:
        return self.duration_left / self.duration

    def end_turn(self):
        self.ended = True
        for ship in Space.get_ships():
            ship.end_turn()

    def start_next(self):
        assert self.ended
        self.duration_left = self.duration
        self.ended = False
        for ship in Space.get_ships():
            ship.execute_plan()


def active_turn() -> Turn:
    return Turn.active_turn
