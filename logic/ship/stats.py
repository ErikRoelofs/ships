from logic.turn.movement import MovementPlan


class Stats:
    def __init__(self, hull_strength, reactor, command, hangar, engine):
        self.hull_strength = hull_strength
        self.reactor = reactor
        self.command = command
        self.hangar = hangar
        self.engines = engine


class Engine:
    def __init__(self, max_speed, turn_speed, thrust, turn_thrust):
        self.max_speed = max_speed
        self.max_turn_speed = turn_speed
        self.turn_thrust = turn_thrust
        self.thrust = thrust

        self.current_speed = 0
        self.current_turn = 0

    def get_heading_from_plan(self, plan: MovementPlan, dt):
        target_speed, target_turn = plan.get_current_heading()
        self.get_new_speed(target_speed, dt)
        self.get_new_turn(target_turn, dt)

        return self.current_speed, self.current_turn

    def get_new_speed(self, target_speed, dt):
        if target_speed > self.current_speed:
            self.current_speed += (self.thrust * dt)
        if target_speed < self.current_speed:
            self.current_speed -= (self.thrust * dt)
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        if self.current_speed < 0:
            self.current_speed = 0

    def get_new_turn(self, target_turn, dt):
        if target_turn > self.current_turn:
            self.current_turn += (self.turn_thrust * dt)
        if target_turn < self.current_turn:
            self.current_turn -= (self.turn_thrust * dt)
        if self.current_turn > self.max_turn_speed:
            self.current_turn = self.max_turn_speed
        if self.current_turn < -self.max_turn_speed:
            self.current_turn = -self.max_turn_speed
