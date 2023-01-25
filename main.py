import os
import sys
import random
import pygame
from pygame import *
import datetime
import pygame_menu

pygame.init()
pygame.display.set_caption('Amogus Life')
SIZE = WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode(SIZE)
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
green = pygame.Color('green')
colors = {
    0: BLACK,
    1: WHITE
}
all_sprites = pygame.sprite.Group()
points = 0
kills = 0
bulets = []
enem_bulets = []
ABOUT = ['AMOGUS-LIFE V.1.0',
         'Developed by Korotishka', ]
HELP = ['           MOVING:                        FIRE/retry:',
        '                   [UP]                         [SPACE]',
        '   [LEFT][DOWN][RIGHT]',
        'PAUSE: [ESC]']


def n_name(value):
    user_name = value


def death_screen():
    global levle_numver
    bg = Surface(SIZE)
    bg.fill(BLACK)
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render(f"ТЫ УМЕР."
                       f" POINTS:{points} KILLS:{kills}", True, (255, 0, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                start_the_game()
                if levle_numver == 2:
                    start_the_game2()
        clock.tick(20)
        pygame.display.flip()
    pygame.quit()


def n_menu():
    global user_name
    menu = pygame_menu.Menu(height=HEIGHT,
                            width=WIDTH,
                            title='AMOGUS LIFE',
                            theme=pygame_menu.themes.THEME_DARK,
                            mouse_enabled=True
                            )
    about_theme = pygame_menu.themes.THEME_DARK.copy()
    about_theme.widget_margin = (0, 0)
    about_menu = pygame_menu.Menu(
        height=HEIGHT * 0.6,
        theme=about_theme,
        title='About',
        width=WIDTH * 0.6,
        mouse_enabled=True
    )
    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    about_menu.add.vertical_margin(30)
    help_theme = pygame_menu.themes.THEME_DARK.copy()
    help_theme.widget_margin = (0, 0)
    help_menu = pygame_menu.Menu(
        height=HEIGHT * 0.9,
        theme=help_theme,
        title='Help',
        width=WIDTH * 0.7,
        mouse_enabled=True
    )
    for m in HELP:
        help_menu.add.label(m, margin=(30, 0), align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    help_menu.add.vertical_margin(30)
    help_menu.add.button('Return to menu', pygame_menu.events.BACK)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)
    menu.add.button('Level 1', start_the_game)
    menu.add.button('Levle 2', start_the_game2)
    menu.add.button('About', about_menu)
    menu.add.button('Help', help_menu)
    menu.mainloop(screen)


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
hero_list = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile("wall", x, y)
                stop_list.append(Tile("wall", x, y))
            elif level[y][x] == '@':
                new_player = AnimatedHeroSprite(load_image("among_us.png", -1), 4, 1, x * 60, y * 60, 100)
                hero_list.append(new_player)
            elif level[y][x] == "!":
                Enemy("enemy.png", x, y, 50)
                stop_list.append(Enemy("enemy.png", x, y, 50))
            elif level[y][x] == "1":
                Weapon('ammo_box.png', x, y)
                stop_list.append(Weapon('ammo_box.png', x, y))
            elif level[y][x] == "3":
                Heal('door', x, y)
                stop_list.append(Heal('door', x, y))
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
        self.c = 0
        self.wait_anim = 7
        self.ammo = 30

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
        self.c += 1
        if self.hp <= 0:
            self.image = load_image('dead.png', -1)
            self.kill()
            hero_list.remove(self)
        else:
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if not self.c % self.wait_anim:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                self.rect.y += 10
                self.vector = 2

            elif pygame.key.get_pressed()[pygame.K_UP]:
                if not self.c % self.wait_anim:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                self.rect.y += -10
                self.vector = -1

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                if not self.c % self.wait_anim:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                self.rect.x += 10
                self.vector = 0
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if not self.c % self.wait_anim:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
                    self.image = self.frames2[-self.cur_frame]
                self.rect.x += -10
                self.vector = 1
            else:
                if self.vector == 0 or self.vector == 2 or self.vector == -1:
                    self.image = load_image('stoi.png', -1)
                else:
                    self.image = load_image('stoi_reverse.png', -1)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.ammo > 0:
                    bullet = Bullet("bullet.png", self.rect.right - 50, self.rect.top, self.vector)
                    bulets.append(bullet)
                    self.ammo -= 1
                    # print(self.ammo)
            for i in stop_list:
                if pygame.sprite.collide_rect(self, i):
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

                    if isinstance(i, Weapon):
                        while self.ammo < 30:
                            self.ammo += 1
                    if isinstance(i, Heal):
                        while self.hp < 100:
                            self.hp += 10


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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, vector):
        super().__init__(all_sprites)
        self.image = load_image(sheet, -1)
        self.rect = self.image.get_rect()
        self.rect.move(x, y)
        self.rect.x = x
        self.rect.y = y
        self.vector = vector

    def update(self):
        if self not in bulets:
            self.kill()
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
                if isinstance(j, Enemy):
                    j.hp -= 25
                    self.kill()
                    if j.hp <= 0:
                        global kills
                        kills += 1

                else:
                    self.kill()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, sheet, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(sheet, -1)
        self.rect = self.image.get_rect().move(
            46 * pos_x, 43 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, model, x, y, hp):
        super().__init__(all_sprites)
        self.image = load_image(model, -1)
        self.hp = hp
        self.rect = self.image.get_rect().move(
            46 * x, 43 * y)
        self.image = load_image(model, -1)
        self.mask = pygame.mask.from_surface(self.image)
        self.vector = 0
        self.delay = 0

    def update(self):
        self.delay += 1
        if self.hp <= 0:
            stop_list.remove(self)
            global points
            points += 10
        if self not in stop_list:
            self.kill()

        if self.delay % 44 == 0:
            for i in range(len(enem_bulets)):
                if i % 2 == 0:
                    if player.rect.y <= self.rect.y:
                        self.vector = -1
                    if player.rect.y >= self.rect.y:
                        self.vector = 2

                else:
                    if player.rect.x >= self.rect.x:
                        self.vector = 0
                    if player.rect.x <= self.rect.x:
                        self.vector = 1

            enemy_bullet = EnemyBullet("bullet.png", self.rect.right - 50, self.rect.top, self.vector)
            enem_bulets.append(enemy_bullet)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, vector):
        super().__init__(all_sprites)
        self.image = load_image(sheet, -1)
        self.rect = self.image.get_rect()
        self.rect.move(x, y)
        self.rect.x = x
        self.rect.y = y
        self.vector = vector

    def update(self):
        if self not in enem_bulets:
            self.kill()
        if -WIDTH <= self.rect.x <= WIDTH and -HEIGHT <= self.rect.y <= HEIGHT:
            if self.vector == 1:
                self.rect.x -= 10
            if self.vector == 0:
                self.rect.x += 5
            if self.vector == -1:
                self.rect.y -= 5
            if self.vector == 2:
                self.rect.y += 5
        for j in hero_list:
            if pygame.sprite.collide_mask(self, j):
                if isinstance(j, AnimatedHeroSprite):
                    j.hp -= 25
                    self.kill()
                else:
                    self.kill()
        for _ in stop_list:
            if pygame.sprite.collide_mask(self, _):
                if isinstance(_, Tile):
                    self.kill()
                    


class Heal(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            46 * pos_x, 43 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


def score():
    global player
    font = pygame.font.Font(None, 50)
    text = font.render(f"KILLS:{kills} POINTS:{points} AMMO:{player.ammo}", True, (0, 0, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = 30 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    if not player.alive():
        with open('data/record.txt', encoding='utf8', mode='w') as f:
            f.write(f"KILLS:{kills} POINTS:{points} AMMO:{player.ammo} DATE:{datetime.datetime.now()}")
            death_screen()


# screen.fill(WHITE)
# sprite = pygame.sprite.Sprite()
# clock = pygame.time.Clock()
#
# camera = Camera()
# tiles_group = pygame.sprite.Group()
# tile_images = {
#     'wall': load_image('block.png', -1), 'floor': load_image('floor1.png'),
#     'door': load_image('hp.png', -1)}
# player, level_x, level_y = generate_level(load_level('map.txt'))
# c = 0
# start = True
# bg = Surface(SIZE)
# bg = pygame.image.load("data/bg.png")
def start_the_game():
    global start, player, level_x, level_y, sprite, tile_images, tiles_group, camera, clock, points, kills, bulets, enem_bulets, all_sprites, stop_list
    levle_number = 1
    all_sprites = pygame.sprite.Group()
    points = 0
    kills = 0
    bulets = []
    enem_bulets = []
    stop_list = []
    screen.fill(WHITE)
    sprite = pygame.sprite.Sprite()
    clock = pygame.time.Clock()
    camera = Camera()
    tiles_group = pygame.sprite.Group()
    tile_images = {
        'wall': load_image('block.png', -1), 'floor': load_image('floor1.png'),
        'door': load_image('hp.png', -1)}
    player, level_x, level_y = generate_level(load_level('map.txt'))
    player.hp = 100
    player.ammo = 30
    c = 0
    start = True
    bg = Surface(SIZE)
    bg = pygame.image.load("data/bg.png")
    running = True
    while running:
        c += 1
        if kills == 3:
            start_the_game2()
        screen.blit(bg, (0, 0))
        camera.update(player)
        for sprite in all_sprites.sprites():
            camera.apply(sprite)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                start = not start
        if start:
            tick = clock.tick(30)
            all_sprites.update()
            for i in all_sprites.sprites():
                screen.blit(i.image, i.rect)
            score()
        else:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render('PAUSE.PRESS ESCAPE TO CONTINUE', True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = (WIDTH - intro_rect[2]) / 2
            intro_rect.top = HEIGHT * 3 / 4 - intro_rect[3] / 2
            screen.blit(string_rendered, intro_rect)
            for i in all_sprites.sprites():
                screen.blit(i.image, i.rect)
        pygame.display.flip()
    pygame.quit()


def start_the_game2():
    global start, player, level_x, level_y, sprite, tile_images, tiles_group, camera, clock, points, kills, bulets, enem_bulets, all_sprites, stop_list, levle_number
    levle_number = 2
    all_sprites = pygame.sprite.Group()
    points = 0
    kills = 0
    bulets = []
    enem_bulets = []
    stop_list = []
    screen.fill(WHITE)
    sprite = pygame.sprite.Sprite()
    clock = pygame.time.Clock()
    camera = Camera()
    tiles_group = pygame.sprite.Group()
    tile_images = {
        'wall': load_image('block.png', -1), 'floor': load_image('floor1.png'),
        'door': load_image('hp.png', -1)}
    player, level_x, level_y = generate_level(load_level('map2.txt'))
    player.hp = 100
    player.ammo = 30
    c = 0
    start = True
    bg = Surface(SIZE)
    bg = pygame.image.load("data/bg.png")
    running = True
    while running:
        if kills == 42:
            n_menu()
        c += 1
        screen.blit(bg, (0, 0))
        camera.update(player)
        for sprite in all_sprites.sprites():
            camera.apply(sprite)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                start = not start
        if start:
            tick = clock.tick(30)
            all_sprites.update()
            for i in all_sprites.sprites():
                screen.blit(i.image, i.rect)
            score()
        else:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render('PAUSE.PRESS ESCAPE TO CONTINUE', True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = (WIDTH - intro_rect[2]) / 2
            intro_rect.top = HEIGHT * 3 / 4 - intro_rect[3] / 2
            screen.blit(string_rendered, intro_rect)
            for i in all_sprites.sprites():
                screen.blit(i.image, i.rect)
        pygame.display.flip()
    pygame.quit()


n_menu()
