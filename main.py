import os
import sys
import random
import pygame
from pygame import *
import time

pygame.init()
pygame.display.set_caption('Amogus Life')

SIZE = WIDTH, HEIGHT = 1680, 1720
screen = pygame.display.set_mode(SIZE)
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
green = pygame.Color('green')
colors = {
    0: BLACK,
    1: WHITE
}
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_image(name: str, colorkey=None) -> pygame.Surface:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


stop_list = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile("wall", x, y)
                stop_list.append(Tile("wall", x, y))
            elif level[y][x] == '@':
                new_player = AnimatedHeroSprite(load_image("among_us.png", -1), 4, 1, x * 60, y * 60, 100)
            elif level[y][x] == "!":
                Enemy("enemy.png", x, y, 50, 1)
                stop_list.append(Enemy("enemy.png", x, y, 50, 1))
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            46 * pos_x, 43 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class AnimatedHeroSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, hp):
        super().__init__(all_sprites)
        self.frames = []
        self.hp = hp
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.frames2 = []
        self.right_cut_sheet(load_image('among_us_revers.png', -1), 4, 1)
        self.vector = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(100, 100, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def right_cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(100, 100, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames2.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if pygame.key.get_pressed()[pygame.K_DOWN] and not (
                pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect.y += 10
            self.vector = 2
        else:
            if self.vector == 0 or self.vector == 2 or self.vector == -1:
                self.image = load_image('stoi.png', -1)
            else:
                self.image = load_image('stoi_reverse.png', -1)
            pass
        if pygame.key.get_pressed()[pygame.K_UP] and not (
                pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect.y += -10
            self.vector = -1
        else:
            pass
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect.x += 10
            self.vector = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
            self.image = self.frames2[-self.cur_frame]
            self.rect.x += -10
            self.vector = 1
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = Bullet("bullet.png", self.rect.right - 50, self.rect.top, self.vector)
        for i in stop_list:

            if pygame.sprite.collide_mask(self, i):
                if self.vector == -1:
                    self.rect.top = i.rect.bottom
                if self.vector == 2:
                    self.rect.bottom = i.rect.top
                if self.vector == 1:
                    self.rect.left = i.rect.right
                if self.vector == 0:
                    self.rect.right = i.rect.left
                if isinstance(i, Enemy):
                    self.hp -= 10
                    print(self.hp)
                    if self.hp < 60:
                        AnimatedHeroSprite.kill(self)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Wall(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y):
        super().__init__(all_sprites)
        self.image = load_image(sheet, -1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

bulets = []
class Bullet(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, vector):
        super().__init__(all_sprites)
        self.image = load_image(sheet, -1)
        self.rect = self.image.get_rect()
        self.rect.move(x, y)
        self.rect.x = x
        self.rect.y = y
        self.vector = vector
        bulets.append(self)
    def update(self):
        if -WIDTH <= self.rect.x <= WIDTH and -HEIGHT <= self.rect.y <= HEIGHT:
            if self.vector == 1:
                self.rect.x -= 10
            if self.vector == 0:
                self.rect.x += 10
            if self.vector == -1:
                self.rect.y -= 10
            if self.vector == 2:
                self.rect.y += 10
        for j in stop_list:
            if pygame.sprite.collide_mask(self, j):
                self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, model, x, y, hp, vector):
        super().__init__(all_sprites)
        self.image = load_image(model, -1)
        self.hp = hp
        self.rect = self.image.get_rect().move(
            60 * x, 60 * y)
        self.image = Surface((self.rect.width, self.rect.height))
        self.image.fill(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.vector = vector

    def update(self):
        for j in bulets:
            if pygame.sprite.collide_mask(self, j):
                self.kill()


if __name__ == '__main__':

    screen.fill(WHITE)

    sprite = pygame.sprite.Sprite()
    clock = pygame.time.Clock()

    running = True
    camera = Camera()
    tiles_group = pygame.sprite.Group()
    tile_images = {
        'wall': load_image('block.png', -1), 'floor': load_image('floor1.png')
    }
    player, level_x, level_y = generate_level(load_level('map.txt'))
    c = 0
    while running:
        c += 1
        screen.fill(WHITE)
        camera.update(player)
        for sprite in all_sprites.sprites():
            camera.apply(sprite)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        tick = clock.tick(12)
        all_sprites.update()
        screen.fill(WHITE)
        for i in all_sprites.sprites():
            screen.blit(i.image, i.rect)
        pygame.display.flip()
    pygame.quit()
