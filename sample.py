#!/usr/bin/env python

# import

import pygame
from pygame.locals import *

from content.ships.demo import Demo
from logic.ship_math.location import Location
from logic.ship_math.point import Point
from logic.turn.movement import MovementPlan, MovementSegment
from logic.turn.plan import Plan
from logic.turn.turn import Turn

if not pygame.image.get_extended():
    raise SystemExit("Requires the extended image loading from SDL_image")


# constants
FRAMES_PER_SEC = 40
SCREENRECT = pygame.Rect(0, 0, 1200, 900)

# some globals for friendly access
dirtyrects = []  # list of update_rects
next_tick = 0  # used for timing


def main():
    global dirtyrects

    # Initialize SDL components
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, 0)
    clock = pygame.time.Clock()

    turn = Turn(10)

    demoship1 = Demo(Location(Point(150, 450), -0.2), 1).getShip()
    demoship2 = Demo(Location(Point(450, 250), -0.1), 2).getShip()

    movement_plan = MovementPlan([
        MovementSegment(40, 0.2, 2),
        MovementSegment(20, -0.2, 2),
        MovementSegment(20, 0.1, 2),
        MovementSegment(60, -0.2, 4),
    ])
    plan = Plan(turn)
    plan.set_movement_plan(movement_plan)

    demoship1.set_plan(plan)
    demoship2.set_plan(Plan(turn))
    demoship1.execute_plan()

    space_down = False
    pause = False
    while 1:
        pygame.event.pump()
        clock.tick(FRAMES_PER_SEC)
        dt = clock.get_time() / 1000
        screen.fill((0, 0, 0))

        if not pause:
            turn.update(dt)
            turn.draw(screen)

            pygame.display.update()

        keystate = pygame.key.get_pressed()
        if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            break
        if keystate[K_SPACE]:
            if not space_down:
                pause = not pause
            space_down = True
        else:
            space_down = False

# if python says run, let's run!
if __name__ == '__main__':
    main()

