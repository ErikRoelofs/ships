from content.ships.demo import Demo
from logic.ship.hitzone import Hitzone
from logic.ship.ship import Ship
from logic.ship.subsystems import Subsystem, Engineering
from logic.ship.targetzone import TargetZone


class ControlLayout:
    def __init__(self):
        self.controls = []

    def add_control(self, position: (int, int), system: Subsystem):
        self.controls.append((position[0], position[1], system))


def layout_from_ship(ship: Ship) -> ControlLayout:
    layout = ControlLayout()
    if isinstance(ship, Demo):
        shields = list(ship.subsystem.get_all_by_type(Hitzone))
        weapons = list(ship.subsystem.get_all_by_type(TargetZone))

        layout.add_control((1, 0), shields[1])
        layout.add_control((1, 1), weapons[1])
        layout.add_control((1, 2), ship.subsystem.get_bridge())
        layout.add_control((1, 3), ship.subsystem.get_reactor())
        layout.add_control((1, 4), ship.subsystem.get_one_by_type(Engineering))
        layout.add_control((1, 5), weapons[3])
        layout.add_control((1, 6), shields[3])
        layout.add_control((0, 2), shields[0])
        layout.add_control((0, 3), weapons[0])
        layout.add_control((2, 2), shields[2])
        layout.add_control((2, 3), weapons[2])
    return layout