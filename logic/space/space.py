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