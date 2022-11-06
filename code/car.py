import pygame
import os
from random import choice


class Car(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        dirs = [x for x in os.walk("../graphics/cars")][0]
        surf_path = dirs[0] + '/' + choice(dirs[2])
        self.image = pygame.image.load(surf_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        # if the car spawns on the right side image should flip on x to show it.
        self.pos = pygame.math.Vector2(self.rect.center)
        if pos[0] < 200:
            self.direction = pygame.math.Vector2(1, 0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image, True, False)  # (_,x,y)
        self.speed = 300

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not -200 < self.rect.x < 3400:
            self.kill()
