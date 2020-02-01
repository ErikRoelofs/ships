from logic.turn.turn import active_turn


class Entity:
    def __init__(self):
        active_turn().register_entity(self)

    def update(self, dt: float):
        pass

    def draw(self, screen):
        pass

    def kill(self):
        active_turn().remove_entity(self)