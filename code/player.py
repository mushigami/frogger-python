import pygame
from settings import *
import os
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
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

        # collisions
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

    def collision(self, direction):
        if direction == 'horizontal':
            # horizontal collision
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

        else:
            # vertical collision
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):

        # normalize vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

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

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width/2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
