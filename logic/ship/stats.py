class Stats:
    def __init__(self, hull_strength, reactor, command, hangar, engine):
        self.hull_strength = hull_strength
        self.reactor = reactor
        self.command = command
        self.hangar = hangar
        self.engines = engine


class Engine:
    def __init__(self, max_speed, max_turn):
        self.max_speed = max_speed
        self.max_turn = max_turn