#!/usr/bin/env python

# import
import os.path
import random

import pygame
from pygame.locals import *

from logic.ship.ship import Ship
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

class Img: pass  # container for images

main_dir = os.path.split(os.path.abspath(__file__))[0]  # Program's directory


# first, we define some utility functions

def load_image(file, transparent):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()


def main():
    "Run me for adrenaline"
    global dirtyrects

    # Initialize SDL components
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, 0)
    clock = pygame.time.Clock()

    demoship1 = Demo(Location(Point(150, 450), -0.2)).getShip()
    demoship2 = Demo(Location(Point(450, 250), 0.001)).getShip()

    turn = Turn(10, [demoship1, demoship2])

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
    while 1:
        pygame.event.pump()
        clock.tick(FRAMES_PER_SEC)
        dt = clock.get_time() / 1000
        screen.fill((0, 0, 0))

        if not pause:
            turn.update(dt)

            demoship1.debug_draw(screen)
            demoship2.debug_draw(screen)

            #for fire_zone in demoship1.targetzones:
            #    fire_zone.debug_draw_targeting_lines(screen, demoship1.location, demoship2.get_hittable_zones(), 400)
            demoship1.targetzones[0].debug_draw_specific_targeting_line(
                screen,
                demoship1.targetzones[0].hardpoints[1],
                demoship1.location,
                demoship2.get_hittable_zones(),
                400
            )

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

