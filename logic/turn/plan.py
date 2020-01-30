from logic.turn.movement import MovementPlan, empty_movement_plan
from logic.turn.turn import Turn


class Plan:
    def __init__(self, turn: Turn):
        self.turn = turn
        self.movement_plan = empty_movement_plan()

    def set_movement_plan(self, movement_plan: MovementPlan):
        self.movement_plan = movement_plan
