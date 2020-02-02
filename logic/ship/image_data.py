import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]  # Program's directory


def load_image(file, transparent):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, '../../graphics', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, pygame.RLEACCEL)
    return surface.convert()


class ImageData:
    def __init__(self, imagename):
        self.image = load_image(imagename, True)
        self.rect = self.image.get_rect()
