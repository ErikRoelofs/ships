

class Input:

    @classmethod
    def handle_mouse(cls, pos, button):
        from logic.space.space import Space
        from visuals.hud import Hud

        if button == 'left':
            ship = Space.get_ship_at_location(pos)
            if ship:
                Hud.set_active_ship(ship)