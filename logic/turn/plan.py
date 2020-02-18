from logic.turn.subsystem import SubsystemPlan, empty_subsystem_plan
from logic.turn.movement import MovementPlan, empty_movement_plan
from logic.turn.turn import Turn, active_turn


class Plan:
    def __init__(self, turn: Turn):
        self.turn = turn
        self.movement_plan = empty_movement_plan()
        self.subsystem_plan = empty_subsystem_plan()

    def set_movement_plan(self, movement_plan: MovementPlan):
        self.movement_plan = movement_plan

    def set_subsystem_plan(self, subsystem_plan: SubsystemPlan):
        self.subsystem_plan = subsystem_plan


def empty_plan():
    return Plan(active_turn())