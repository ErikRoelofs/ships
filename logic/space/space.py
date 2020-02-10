class Space:
    ships = []

    @classmethod
    def register_ship(cls, ship):
        Space.ships.append(ship)

    @classmethod
    def get_friendlies(cls, faction):
        return filter(
            lambda x: x.faction == faction,
            Space.ships
        )

    @classmethod
    def get_hostiles(cls, faction):
        return filter(
            lambda x: x.faction != faction,
            Space.ships
        )

    @classmethod
    def remove_ship(cls, ship):
        Space.ships.remove(ship)

    @classmethod
    def get_ships(cls):
        return Space.ships

    @classmethod  # world location, not screen location!
    def get_ship_at_location(cls, pos):
        for ship in Space.ships:
            if ship.position_is_in_ship(pos):
                return ship
        return None