from logic.space.space import Space
from logic.turn.turn import Turn
from random import randint, choice


class FireControl:
    def __init__(self, ship):
        self.fire_solutions = []
        self.ship = ship
        self.timer = 0

    def prepare(self, turn: Turn):
        self.fire_solutions = []
        self.timer = 0
        for firezone in self.ship.targetzones:
            weapon_count = len(firezone.weapons)
            base_spread = turn.duration / (weapon_count + 1)
            next_timer = base_spread
            weapons = firezone.weapons.copy()
            # shuffle the weapons
            while weapons:
                self.fire_solutions.append((weapons.pop(), firezone, next_timer + (randint(-200, 200)/1000)))
                next_timer += base_spread

    def update(self, dt):
        self.timer += dt
        for solution in self.fire_solutions:
            if self.timer > solution[2]:
                hostile_ships = Space.get_hostiles(self.ship.faction)
                targets = []
                for ship in hostile_ships:
                    for zone in ship.get_hittable_zones():
                        targets.append(zone)
                weapon = solution[0]
                zone = solution[1]
                potential_shots = zone.get_valid_targets(self.ship.location, targets, weapon.range())
                if len(potential_shots) > 0:
                    final_target = choice(potential_shots)
                    weapon.fire(self.ship, final_target[0], final_target[1])
                self.fire_solutions.remove(solution)



# when preparing:
    # for each firezone
        # randomize order of fire
        # space out all weapons over the turn's duration
            # roughly evenly over the turn
            # small stagger to prevent all sides from firing at once

# when updating
    # increase timer
    # fire all weapons whose timer has passed, then remove them from the waiting list
        # randomly iterate all hardpoints
            # scan for a target
            # if targets found:
                # pick the best target
                # open fire
                # done!