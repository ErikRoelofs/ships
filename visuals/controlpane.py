import pygame

from logic.entity import Entity
from logic.ship.image_data import ImageData
from logic.ship.ship import Ship
from logic.ship.subsystems import Subsystem
from logic.ship_math.point import Point
from visuals.fonts import Fonts


class ControlPane (Entity):
    def __init__(self, ship: Ship):
        Entity.__init__(self)
        self.renderers = []
        for system in ship.subsystem.get_all():
            self.renderers.append(SubsystemRenderer(system))

    def update(self, dt):
        pass

    def draw(self, screen):
        i = 0
        j = 0
        for renderer in self.renderers:
            renderer.draw(screen, Point(950 + j * 150, 50 + 100 * i))
            i += 1
            if i > 8:
                j += 1
                i = 0
        pass

class SubsystemRenderer:

    images = {
        'neither': ImageData('ui/subsystems/neither.png', transparent=False),
        'aux': ImageData('ui/subsystems/aux_.png', transparent=False),
        'overload': ImageData('ui/subsystems/overload.png', transparent=False),
        'both': ImageData('ui/subsystems/both.png', transparent=False),
    }
    light_on = pygame.Surface((20, 30))
    light_on.fill((0, 255, 0))
    light_off = pygame.Surface((20, 30))
    light_off.fill((255, 0, 0))


    def __init__(self, system: Subsystem):
        self.system = system
        if self.system.has_aux and self.system.has_overload:
            self.image = SubsystemRenderer.images['both']
        elif self.system.has_aux:
            self.image = SubsystemRenderer.images['aux']
        elif self.system.has_overload:
            self.image = SubsystemRenderer.images['overload']
        else:
            self.image = SubsystemRenderer.images['neither']

        self.label = Fonts.control_pane.render(system.name, True, (255, 255, 255))

    def draw(self, surface, offset: Point):
        # main pane
        rect = self.image.rect
        rect.center = offset.as_tuple()
        surface.blit(self.image.image, rect)

        # name
        text_position = (offset.x - 60, offset.y - 40)
        surface.blit(self.label, text_position)

        # indicator lights
        on_position = (offset.x, offset.y + 3)
        if self.system.state.on:
            surface.blit(SubsystemRenderer.light_on, on_position)
        else:
            surface.blit(SubsystemRenderer.light_off, on_position)
        if self.system.has_aux:
            aux_position = (offset.x, offset.y - 33)
            if self.system.state.aux:
                surface.blit(SubsystemRenderer.light_on, aux_position)
            else:
                surface.blit(SubsystemRenderer.light_off, aux_position)
        if self.system.has_overload:
            overload_position = (offset.x + 35, offset.y - 33)
            if self.system.state.overload:
                surface.blit(SubsystemRenderer.light_on, overload_position)
            else:
                surface.blit(SubsystemRenderer.light_off, overload_position)

        # status display
        status_surface = pygame.Surface((50, 50))
        status_surface.fill((195, 195, 195))
        self.system.draw_status(status_surface)
        surface.blit(status_surface, (offset.x - 58, offset.y - 15))