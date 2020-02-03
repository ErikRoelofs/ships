from logic.turn.movement import MovementPlan


class State:
    def __init__(self, on, aux, overload):
        self.on = on
        self.aux = aux
        self.overload = overload


class Subsystem:
    def __init__(self, initial_state: State, has_aux, has_overload, uses_energy = True, can_power_down = True):
        self.can_power_down = can_power_down
        self.uses_energy = uses_energy
        self.has_overload = has_overload
        self.has_aux = has_aux
        self.state = initial_state

    def power_use(self):
        if not self.uses_energy:
            return 0
        use = 0
        if self.state.on:
            use+=1
        if self.state.aux:
            use+=1
        if self.state.overload:
            use+=1
        return use

    def power_down(self):
        if not self.can_power_down:
            return
        self.state.on = False
        self.state.aux = False
        self.state.overload = False


class Engine(Subsystem):
    def __init__(self, max_speed, turn_speed, thrust, turn_thrust, can_boost=False, can_evade=False, initial_state: State=None):
        if not initial_state:
            initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, can_boost, can_evade)
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
        if not self.state.on:
            return self.current_speed

        if target_speed > self.current_speed:
            self.current_speed += (self.thrust * dt)
        if target_speed < self.current_speed:
            self.current_speed -= (self.thrust * dt)
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        if self.current_speed < 0:
            self.current_speed = 0

    def get_new_turn(self, target_turn, dt):
        if not self.state.on:
            return 0
        if self.state.aux:
            current_max_turn_speed = self.max_turn_speed * 2
        else:
            current_max_turn_speed = self.max_turn_speed

        if target_turn > self.current_turn:
            self.current_turn += (self.turn_thrust * dt)
        if target_turn < self.current_turn:
            self.current_turn -= (self.turn_thrust * dt)
        if self.current_turn > current_max_turn_speed:
            self.current_turn = current_max_turn_speed
        if self.current_turn < -current_max_turn_speed:
            self.current_turn = -current_max_turn_speed


class Stats:
    def __init__(self, hull_strength, reactor, command, hangar, engine: Engine):
        self.hull_strength = hull_strength
        self.reactor = reactor
        self.command = command
        self.hangar = hangar
        self.engines = engine
