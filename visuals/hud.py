from pygame.surface import Surface

from logic.ship.ship import Ship
from visuals.controlpane import ControlPane
from visuals.controllayout import layout_from_ship


class Hud:
    active = None
    panel = None

    @classmethod
    def set_active_ship(cls, ship: Ship):
        cls.active = ship

        layout = layout_from_ship(ship)
        cls.panel = ControlPane(ship, layout)

    @classmethod
    def clear_active_ship(cls):
        if cls.panel:
            cls.panel.kill()
        cls.active = None
        cls.panel = None
