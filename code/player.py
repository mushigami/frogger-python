import pygame
from settings import *
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        # image
        self.animations = {}
        self.import_assets()
        self.frame_index = 0
        self.status = "right"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

    def move(self, dt):

        # normalize vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def import_assets(self):
        os_walk = [x for x in os.walk('../graphics/player')]
        root = os_walk[0][0]
        dirs = os_walk[0][1]
        files = os_walk[1][2]

        for _dir in dirs:
            self.animations[_dir] = []
            for file in files:
                self.animations[_dir].append(pygame.image.load(root + '/' + _dir + '/' + file).convert_alpha())

    def input(self):
        keys = pygame.key.get_pressed()

        # horizontal
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        # vertical
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

    def animate(self, dt):
        current_animation = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 8 * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
