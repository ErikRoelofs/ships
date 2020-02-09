#!/usr/bin/env python

# import

import pygame
from pygame.locals import *

pygame.init()

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
    screen = pygame.display.set_mode(SCREENRECT.size, 0)
    clock = pygame.time.Clock()

    turn = Turn(10)

    demoship1 = Demo(Location(Point(150, 450), -0.2), 1)
    demoship2 = Demo(Location(Point(450, 250), -0.1), 2)

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

    space_down = False
    pause = False

    from visuals.controlpane import ControlPane  # import after init
    from visuals.controllayout import layout_from_ship
    layout = layout_from_ship(demoship1)
    panel = ControlPane(demoship1, layout)

    turn.start_next()

    while 1:
        pygame.event.pump()
        clock.tick(FRAMES_PER_SEC)
        dt = clock.get_time() / 1000
        screen.fill((0, 0, 0))

        if not pause:
            turn.update(dt)
            turn.draw(screen)

            pygame.display.update()

            if turn.done():
                turn.end_turn()
                turn.start_next()

            panel.draw(screen)

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

