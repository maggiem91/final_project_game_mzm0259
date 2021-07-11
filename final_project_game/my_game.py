import random
import sys

import pygame
from pygame import key
from pygame.time import Clock
from pygame.surface import Surface
from pygame.sprite import Sprite, Group, spritecollideany

from final_project_game import settings


class Background(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("final_project_game_images/HP0083.jpg.webp")
        self.image = pygame.transform.scale(self.image, (settings.WORLD_WIDTH, settings.WORLD_HEIGHT))
        #self.background = pygame.image.load("final_project_game_images/HP0083.jpg.webp")
        self.rect = self.image.get_rect()


        #self.image = pygame.transform.scale(self.background, (settings.WORLD_WIDTH, settings.WORLD_HEIGHT))
        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.WORLD_HEIGHT
        #assert self.world_rect.width == settings.WORLD_WIDTH

class Explosion(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("final_project_game_images/Hedgehog_Purple_Death_L.png").convert_alpha()
        #self.image.fill((0, 0, 200))
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self, *args, **kwargs):
        pass

class Player(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.hedgehog_right = pygame.image.load("final_project_game_images/Hedgehog_Purple_Stand_R.png").convert_alpha()
        self.hedgehog_left = pygame.image.load("final_project_game_images/Hedgehog_Purple_Stand_L.png").convert_alpha()
        self.image = self.hedgehog_right
        self.world_rect = self.image.get_rect().move(0, 300)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if self.world_rect.left > settings.WORLD_WIDTH:
            self.world_rect.left -= settings.WORLD_WIDTH
        if self.world_rect.left < 0:
            self.world_rect.left += settings.WORLD_WIDTH

        if keys[pygame.K_UP]:
            self.move_up()
        if keys[pygame.K_DOWN]:
            self.move_down()
        if self.world_rect.top < 0:
            self.world_rect.top += settings.WORLD_HEIGHT

        if self.world_rect.top > settings.WORLD_HEIGHT:
            self.world_rect.top -= settings.WORLD_HEIGHT
    def move_left(self):
        self.world_rect.left -= 20
        self.image = self.hedgehog_left

    def move_right(self):
        self.world_rect.left += 20
        self.image = self.hedgehog_right

    def move_up(self):
        self.world_rect.top -= 20
        self.image = self.hedgehog_right

    def move_down(self):
        self.world_rect.top += 20
        self.image = self.hedgehog_right

class OtherCharacters(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("final_project_game_images/Devil_Red_Stand_L.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self):
        self.world_rect.move_ip(random.randint(-10, 10), random.randint(-10, 10))

class Cloud(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("final_project_game_images/Cloud_Ball_White_Eyes_L.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self):
        self.world_rect.move_ip(random.randint(-15, 15), random.randint(-15, 15))


class Viewport:
    def __init__(self):
        self.left = 0

    def update(self, sprite):
        self.left = sprite.world_rect.left - 300
        if self.left > settings.WORLD_WIDTH:
            self.left -= settings.WORLD_WIDTH
        if self.left < 0:
            self.left += settings.WORLD_WIDTH
        #if self.left > settings.WORLD_HEIGHT:
         #   self.player.move_ip
        #if self.left < 0:
         #   self.left += settings.WORLD_HEIGHT


    def compute_rect(self, group, dx=0):
        for sprite in group:
            sprite.rect = sprite.world_rect.move(-self.left + dx, 0)

    def draw_group(self, group, surface):
        self.compute_rect(group)
        group.draw(surface)
        self.compute_rect(group, settings.WORLD_WIDTH)
        group.draw(surface)


class Game(Sprite):
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(("Play Game!"))



        self.player = Player()
        self.player_group = Group()
        self.player_group.add(self.player)
        self.other_characters = Group()
        self.cloud = Group()
        Game.next_level(self)
        #self.back = Background()
        self.static_sprites = Group()
        self.static_sprites.add(Background())
        #self.static_sprites.add(self.back)
        #self.static_sprites.add(background)

        self.viewport = Viewport()
        self.viewport.update(self.player)

    def game_loop(self):
        clock = Clock()

        # game = Game(level)
        #while Game.game_loop() is True:
         #   print("Next Level")
          #  level = level + 1
           # game = Game(level)

        #if level == 1 and self.player.alive() is True:
        #while self.player.alive() is True:
        #    Game.next_level(self)
        count = 0
        while True:
            count+=1
            self.handle_events()
            self.draw()
            self.update()
            pygame.display.flip()
            clock.tick(30)
            print(count)
            if count > 200*settings.LEVEL_COUNT and self.player.alive():

                Game.next_level(self)

    def next_level(self):
        settings.LEVEL_COUNT += 1
        level = settings.LEVEL_COUNT

        self.other_characters.remove()
        self.cloud.remove()

        for i in range(level*5):
            self.other_characters.add(OtherCharacters(random.randrange(0, settings.WORLD_WIDTH),
                                  random.randrange(0, settings.WINDOW_HEIGHT)))

        for i in range(level*5):
            self.cloud.add(Cloud(random.randrange(0, settings.WORLD_WIDTH),
                                  random.randrange(0, settings.WINDOW_HEIGHT)))


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and event.mod == pygame.KMOD_LCTRL:
                    pass

    def update(self):
        self.player_group.update(key.get_pressed())
        self.other_characters.update()
        self.cloud.update()
        self.viewport.update(self.player)
        self.check_collisions()

    def check_collisions(self):
        collided_with = spritecollideany(self.player, self.other_characters)
        if self.player.alive() and collided_with is not None:
            self.player.kill()
            collided_with.kill()
            self.player_group.add(Explosion(self.player.world_rect.left, self.player.rect.y))
                #self.player.rect.left, self.player.rect.top))

        collided_with_cloud = spritecollideany(self.player, self.cloud)
        if self.player.alive() and collided_with_cloud is not None:
            self.player.kill()
            collided_with_cloud.kill()
            self.player_group.add(Explosion(self.player.world_rect.left, self.player.rect.y))
            #self.player_group.add(Explosion(self.player.rect.left, self.player.rect.top))

    def draw(self):
        self.screen.fill((0, 0, 0))
        #self.screen.blit(self.back.background,(0,0),self.back.background.get_rect())
        #self.viewport.draw_group(self.static_sprites,
        self.viewport.draw_group(self.static_sprites, self.screen)
        self.viewport.draw_group(self.player_group, self.screen)
        self.viewport.draw_group(self.other_characters, self.screen)
        self.viewport.draw_group(self.cloud, self.screen)

        #self.viewport.update_rect(self.static_sprites)
        #self.viewport.update_rect(self.player_group)
        #self.viewport.update_rect(self.other_characters)
        #self.static_sprites.draw(self.screen)
        #self.player_group.draw(self.screen)
        #self.other_characters.draw(self.screen)


if __name__ == '__main__':
    Game().game_loop()

