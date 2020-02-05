from logic.entity import Entity
from logic.ship.image_data import ImageData
from logic.ship.ship import Ship
from logic.ship.subsystems import Subsystem
from logic.ship_math.point import Point


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
        for renderer in self.renderers:
            renderer.draw(screen, Point(700, 100 * i))
            i += 1
        pass

class SubsystemRenderer:

    images = {
        'neither': ImageData('ui/subsystems/neither.png', transparent=False),
        'aux': ImageData('ui/subsystems/aux_.png', transparent=False),
        'overload': ImageData('ui/subsystems/overload.png', transparent=False),
        'both': ImageData('ui/subsystems/both.png', transparent=False),
    }

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

    def draw(self, surface, offset: Point):
        rect = self.image.rect
        rect.center = offset.as_tuple()
        surface.blit(self.image.image, rect)