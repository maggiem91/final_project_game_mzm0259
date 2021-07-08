import random
import sys

import pygame
from pygame import key
from pygame.time import Clock
from pygame.surface import Surface
from pygame.sprite import Sprite, Group, spritecollideany

from final_project_game import settings


class Ground(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = Surface((40, 40)).convert()
        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.WINDOW_HEIGHT
        assert self.world_rect.width == settings.WORLD_WIDTH

class Explosion(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Surface((50, 50)).convert()
        self.image.fill((0, 0, 300))
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self, *args, **kwargs):
        pass

class Player(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Surface((50, 50)).convert()
        self.image.fill((200, 200, 300))
        self.world_rect = self.image.get_rect().move(0, 350)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if self.world_rect.left > settings.WORLD_WIDTH:
            self.world_rect.left -= settings.WORLD_WIDTH
        if self.world_rect.left < 0:
            self.world_rect.left += settings.WORLD_WIDTH

    def move_left(self):
        self.world_rect.left -= 20

    def move_right(self):
        self.world_rect.left += 20

class OtherCharacters(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Surface((50, 50)).convert()
        self.image.fill((200, 0, 0))
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self):
        self.world_rect.move_ip(random.randint(-15, 15), random.randint(-10, 10))

class Viewport:
    def __init__(self):
        self.left = 0

    def update(self, sprite):
        self.left = sprite.left - 300

class Game:
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((settings.WORLD_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(("Play Game!"))
        self.player = Player()
        self.player_group = Group()
        self.player_group.add(self.player)
        self.other_characters = Group()
        for i in range(10):
            self.other_characters.add(OtherCharacters(random.randrange(0, settings.WORLD_WIDTH),
                                      random.randrange(0, settings.WINDOW_HEIGHT)))
        self.static_sprites = Group()
        self.static_sprites.add(Ground())
        self.viewport = Viewport()
        self.viewport.update(player)
