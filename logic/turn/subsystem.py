from logic.ship.subsystems import Subsystem


class SubsystemPlanStep(object):
    pass

class SubsystemTurnOn(SubsystemPlanStep):
    def __init__(self, subsystem):
        self.subsystem = subsystem

    def execute(self):
        self.subsystem.turn_on()


class SubsystemPlan:
    def __init__(self):
        self.steps = []

    def add_step(self, step: SubsystemPlanStep):
        self.steps.append(step)

    def execute(self):
        for step in self.steps:
            step.execute()

def empty_subsystem_plan():
    return SubsystemPlan()
