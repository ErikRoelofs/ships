from pygame.surface import Surface

class WeaponRenderer:
    surfaces = {}

    @classmethod
    def get_weapon_surface(cls, weapon):
        if not weapon in cls.surfaces:
            surface = Surface((8, 8))
            surface.fill(weapon.color())
            cls.surfaces[weapon] = surface
        return cls.surfaces[weapon]