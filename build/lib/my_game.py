import random
import sys
import math

import pygame
from pygame import key
from pygame import math
from pygame.time import Clock
from pygame.surface import Surface
from pygame.sprite import Sprite, Group, spritecollideany

from final_project_game import settings


class Background(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("final_project_game_images/scrolling_mushroom_background.png")
        self.image = Game.aspect_scale(self.image, int(settings.WORLD_WIDTH), int(settings.WORLD_HEIGHT))
        # self.image = pygame.transform.scale(self.image, (settings.WORLD_WIDTH, settings.WORLD_HEIGHT))
        # self.background = pygame.image.load("final_project_game_images/HP0083.jpg.webp")
        self.rect = self.image.get_rect()

        # self.image = pygame.transform.scale(self.background, (settings.WORLD_WIDTH, settings.WORLD_HEIGHT))
        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.WORLD_HEIGHT
        # assert self.world_rect.width == settings.WORLD_WIDTH


class Explosion(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("final_project_game_images/dead_hedgehog.png").convert_alpha()
        # self.image.fill((0, 0, 200))
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self, *args, **kwargs):
        pass


class Player(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.hedgehog_right = pygame.image.load("final_project_game_images/hedgehog_right.png").convert_alpha()
        self.hedgehog_left = pygame.image.load("final_project_game_images/hedgehog_left.png").convert_alpha()
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
        self.image = pygame.image.load("final_project_game_images/red_monster.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self):
        self.world_rect.move_ip(random.randint(-5, 5), random.randint(-5, 5))


class Cloud(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("final_project_game_images/blue_monster.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)

    def update(self):
        self.world_rect.move_ip(random.randint(-15, 15), random.randint(-15, 15))


class AngryEnemy(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("final_project_game_images/yellow_monster.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    # Same thing using only pygame utilities
    def update(self, player):
        self.speed=settings.LEVEL_COUNT
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        if dirvect.length() >0:
            dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
            dirvect.scale_to_length(self.speed)
        self.world_rect.move_ip(dirvect)



class Viewport:
    def __init__(self):
        self.left = 0

    def update(self, sprite):
        self.left = sprite.world_rect.left - 300
        if self.left > settings.WORLD_WIDTH:
            self.left -= settings.WORLD_WIDTH
        if self.left < 0:
            self.left += settings.WORLD_WIDTH
        # if self.left > settings.WORLD_HEIGHT:
        #   self.player.move_ip
        # if self.left < 0:
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
        self.angry_characters = Group()
        Game.next_level(self)
        # self.back = Background()
        self.static_sprites = Group()
        self.static_sprites.add(Background())
        # self.static_sprites.add(self.back)
        # self.static_sprites.add(background)

        self.viewport = Viewport()
        self.viewport.update(self.player)

    def game_loop(self):
        clock = Clock()

        # game = Game(level)
        # while Game.game_loop() is True:
        #   print("Next Level")
        #  level = level + 1
        # game = Game(level)

        # if level == 1 and self.player.alive() is True:
        # while self.player.alive() is True:
        #    Game.next_level(self)
        count = 0
        while True:
            count += 1
            self.handle_events()
            self.draw()
            self.update()
            pygame.display.flip()
            clock.tick(30)
            print(count)
            if count > 200 * settings.LEVEL_COUNT and self.player.alive():
                Game.fade(self, settings.WORLD_WIDTH, settings.WORLD_HEIGHT)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                waiting = False

                Game.next_level(self)

    def fade(self, width, height):
        level_image = pygame.image.load("final_project_game_images/space_bar.png")
        level_image = Game.aspect_scale(level_image, int(settings.WINDOW_WIDTH), int(settings.WINDOW_HEIGHT))

        # level_image = pygame.transform.scale(level_image, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        self.fade = pygame.Surface((width, height))
        self.fade.fill((0, 0, 0))
        alpha = 0
        alpha_vel = 1
        for alpha in range(0, 300):
            if alpha >= 255 or alpha <= 0:
                alpha_vel *= -1
                alpha += alpha_vel
                self.fade.set_alpha(alpha)
                # redrawWindow()
                level_image.set_alpha(alpha)
                self.screen.blit(level_image, (0, 0))
                pygame.display.update()
                pygame.time.delay(1)

    def next_level(self):
        settings.LEVEL_COUNT += 1
        level = settings.LEVEL_COUNT

        self.other_characters.remove()
        self.cloud.remove()
        self.angry_characters.remove()

        # k = input("input something")
        # if k is not None:
        #    pass
        for i in range(level * 3):
            self.other_characters.add(OtherCharacters(random.randrange(0, settings.WORLD_WIDTH),
                                                      random.randrange(0, settings.WINDOW_HEIGHT)))

        for i in range(level * 3):
            self.cloud.add(Cloud(random.randrange(0, settings.WORLD_WIDTH),
                                 random.randrange(0, settings.WINDOW_HEIGHT)))

        for i in range(level * 2):
            self.angry_characters.add(AngryEnemy(random.randrange(0, settings.WORLD_WIDTH),
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
        self.angry_characters.update(self.player)
        self.viewport.update(self.player)
        self.check_collisions()

    def check_collisions(self):
        collided_with = spritecollideany(self.player, self.other_characters)
        if self.player.alive() and collided_with is not None:
            self.player.kill()
            collided_with.kill()
            self.player_group.add(Explosion(self.player.world_rect.left, self.player.rect.y))
            # self.player.rect.left, self.player.rect.top))

        collided_with_cloud = spritecollideany(self.player, self.cloud)
        if self.player.alive() and collided_with_cloud is not None:
            self.player.kill()
            collided_with_cloud.kill()
            self.player_group.add(Explosion(self.player.world_rect.left, self.player.rect.y))
            # self.player_group.add(Explosion(self.player.rect.left, self.player.rect.top))

        collided_with_angry_characters = spritecollideany(self.player, self.angry_characters)
        if self.player.alive() and collided_with_angry_characters is not None:
            self.player.kill()
            collided_with_angry_characters.kill()
            self.player_group.add(Explosion(self.player.world_rect.left, self.player.rect.y))

    def draw(self):
        self.screen.fill((0, 0, 0))
        # self.screen.blit(self.back.background,(0,0),self.back.background.get_rect())
        # self.viewport.draw_group(self.static_sprites,
        self.viewport.draw_group(self.static_sprites, self.screen)
        self.viewport.draw_group(self.player_group, self.screen)
        self.viewport.draw_group(self.other_characters, self.screen)
        self.viewport.draw_group(self.cloud, self.screen)
        self.viewport.draw_group(self.angry_characters, self.screen)

        # self.viewport.update_rect(self.static_sprites)
        # self.viewport.update_rect(self.player_group)
        # self.viewport.update_rect(self.other_characters)
        # self.static_sprites.draw(self.screen)
        # self.player_group.draw(self.screen)
        # self.other_characters.draw(self.screen)

    def aspect_scale(img, bx, by):
        """ Scales 'img' to fit into box bx/by.
         This method will retain the original image's aspect ratio """
        ix, iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx / float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by / float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx / float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by
        return pygame.transform.scale(img, (int(sx), int(sy)))


if __name__ == '__main__':
    Game().game_loop()
