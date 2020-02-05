from logic.turn.movement import MovementPlan


class State:
    def __init__(self, on, aux, overload):
        self.on = on
        self.aux = aux
        self.overload = overload


class Subsystem:
    def __init__(self, initial_state: State, has_aux, has_overload, uses_energy=True, can_power_down=True):
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
            use += 1
        if self.state.aux:
            use += 1
        if self.state.overload:
            use += 1
        return use

    def power_down(self):
        if not self.can_power_down:
            return
        self.state.on = False
        self.state.aux = False
        self.state.overload = False

    def start_turn(self, ship):
        pass

    def end_turn(self, ship):
        pass

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


class Bridge(Subsystem):
    def __init__(self, hull, command):
        initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, False, False, False, False)
        self.max_hull = hull
        self.command = command
        self.current_hull = hull


class Reactor(Subsystem):
    def __init__(self, reactor_value, overload_value=0):
        initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, False, overload_value>0, False, False)
        self.reactor_value = reactor_value
        self.overload_value = overload_value


class Engineering(Subsystem):
    def __init__(self, repair_value: int, can_fix_hull=False, can_prevent_fires=False):
        initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, can_fix_hull, can_prevent_fires)
        self.repair_value = repair_value

    def end_turn(self, ship):
        if self.state.on:
            bridge = ship.subsystem.get_bridge()
            print("repairing from %s / %s !" % ( bridge.current_hull, bridge.max_hull ))
            bridge.current_hull += self.repair_value
            bridge.current_hull = min(bridge.current_hull, bridge.max_hull)
            print("repaired to %s / %s !" % ( bridge.current_hull, bridge.max_hull ))


class ShieldControl(Subsystem):
    def __init__(self, repair_value: int, aux_repair_value: int=0, can_overlap=False):
        initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, aux_repair_value > 0, can_overlap)
        self.repair_value = repair_value
        self.aux_repair_value = aux_repair_value

    def end_turn(self, ship):
        restore_value = 0
        if self.state.on:
            restore_value = self.repair_value
        if self.state.aux:
            restore_value += self.aux_repair_value

        while restore_value > 0:
            # repair one at a time
                # find the most damaged shield (by %)
                # increase it by 1
                # if nothing is damaged, return
            restore_value -= 1


class Communications(Subsystem):
    def __init__(self, squadron_command, can_boost=False, can_enhance=False):
        initial_state = State(on=True, aux=False, overload=False)
        Subsystem.__init__(self, initial_state, can_boost, can_enhance)
        self.squadron_command = squadron_command


class Subsystems:
    def __init__(self, reactor: Reactor, bridge: Bridge):
        self.subsystems = [reactor, bridge]

    def add_system(self, system: Subsystem):
        self.subsystems.append(system)

    def get_bridge(self):
        return self.get_one_by_type(Bridge)

    def get_one_by_type(self, type):
        for system in self.subsystems:
            if isinstance(system, type):
                return system
        return None

    def get_all_by_type(self, type):
        return filter(lambda x: isinstance(x, type), self.subsystems)

    def get_power_available(self):
        power_available = 0
        for reactor in self.get_all_by_type(Reactor):
            power_available += reactor.reactor_value
            if reactor.state.overload:
                power_available += reactor.overload_value
        return power_available

    def get_power_usage(self):
        usage = 0
        for system in self.subsystems:
            usage += system.power_use()
        return usage

    def get_all(self):
        return self.subsystems