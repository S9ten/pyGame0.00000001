import os
import sys
import random

import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
pygame.display.set_caption('Герой двигается!')

SIZE = WIDTH, HEIGHT = 1500, 500
v = 60
FPS = 60
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
    # если файл не существует, то выходим
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
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if pygame.key.get_pressed()[pygame.K_1]:
            self.cut_sheet(load_image("weapon_walk.png"), 2, 1)
            if pygame.key.get_pressed()[pygame.K_DOWN] and self.rect.y < HEIGHT - 261:
                self.cur_frame = (self.cur_frame + 2) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.rect.y += 10
            else:
                self.image = load_image("chel2.png", -1)
            if pygame.key.get_pressed()[pygame.K_UP] and self.rect.y > 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.rect.y += -10
            if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x > 0:
                self.cur_frame = (self.cur_frame + 2) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.rect.x += -10
        else:
            if pygame.key.get_pressed()[pygame.K_DOWN] and self.rect.y < HEIGHT - 261:
                self.cur_frame = (self.cur_frame + 2) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.rect.y += 10
            else:
                self.image = load_image("chel2.png", -1)
            if pygame.key.get_pressed()[pygame.K_UP] and self.rect.y > 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.rect.y += -10
            if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x > 0:
                self.cur_frame = (self.cur_frame + 2) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.rect.x += -10

        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x < WIDTH - 105:
            self.cur_frame = (self.cur_frame + 2) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect.x += 10

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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):

        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Mountain(pygame.sprite.Sprite):
    image = load_image("img.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = HEIGHT


if __name__ == '__main__':

    screen.fill(BLACK)

    sprite = pygame.sprite.Sprite()
    clock = pygame.time.Clock()
    balls_sprites = pygame.sprite.Group()
    running = True
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    camera = Camera()
    mountain = Mountain()
    player = AnimatedSprite(load_image("walk2.png"), 3, 1, 50, 50)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tick = clock.tick(5)
        screen.fill(BLACK)
        all_sprites.draw(screen)
        all_sprites.update()

        pygame.display.flip()
    pygame.quit()
