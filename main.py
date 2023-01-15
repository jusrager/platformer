import pygame
import os
import sys
import random
import sqlite3
from first_window import Scene1
from second_window import Scene2
SIZE = WIDTH, HEIGHT = 832, 384

run = True

width, height = (200, 80)
X, Y = ((WIDTH - width) // 2, (HEIGHT - height) // 2)
text_x, text_y = ((WIDTH - width) // 2 + 10, (HEIGHT - height) // 2 - 100)
text_x1, text_y1 = ((WIDTH - width) // 2 + 44, (HEIGHT - height) // 2 + 16)
text_x2, text_y2 = ((WIDTH - width) // 2 - 104, (HEIGHT - height) // 2 + 124)
tile_width = tile_height = 64

scores = sqlite3.connect("db/scores.sqlite")
cur = scores.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS scores(login TEXT, currentscore INT, bestscore INT)""")


def load_image(fullname, colorkey=None):
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if fullname != 'background.png':
        image = pygame.transform.scale(image, (tile_width, tile_height))

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
screen = pygame.display.set_mode((width, height))
FPS = 40
clock = pygame.time.Clock()
x, y = 0, 0
r = 10
not_exit = True
clicked = False


tile_images = {
    'wall': load_image('ground_rock.png'),
    'empty': load_image('rock.png'),
    'hanging_platform1': load_image('hanging_platform1.png'),
    'hanging_platform2': load_image('hanging_platform2.png')
}
player_image = load_image('player.png')
background_image = load_image('background.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.image = pygame.transform.scale(
            self.image, (tile_width, tile_height))


class Player(pygame.sprite.Sprite):
    STEP = 2

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image

        print(pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 2)

        self.run = {'right': [os.path.join('walk', 'right', file) for file in os.listdir(os.path.join('walk', 'right'))],
                    'left': [os.path.join('walk', 'left', file) for file in os.listdir(os.path.join('walk', 'left'))]}

        print(self.run)

        self.cur_img = 0
        self.is_move = False
        self.direction = 'right'
        self.is_up = False
        self.up_time = 0
        self.is_falling = False

    def update(self) -> None:
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.is_falling:
            self.lending()

        # print(pygame.time.get_ticks())

        images = self.run[self.direction]

        if self.is_move:
            self.move()
            self.cur_img = (self.cur_img + 1) % len(images)
            self.image = load_image(images[self.cur_img])
        else:
            self.image = load_image(images[0])

        if self.is_up:
            if pygame.time.get_ticks() - self.up_time >= 400:
                print(pygame.time.get_ticks(), self.up_time)
                self.is_up = False

    def move(self):
        if self.direction == 'right':
            self.rect = self.rect.move(self.STEP, 0)

            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(-self.STEP, 0)
        elif self.direction == 'left':
            self.rect = self.rect.move(-self.STEP, 0)

            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(self.STEP, 0)

        if self.is_up:
            self.rect = self.rect.move(
                self.rect.x, self.rect.y - self.STEP)

    def lending(self):
        self.rect = self.rect.move(
            self.rect.x, self.rect.y + self.STEP)

        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect = self.rect.move(
                self.rect.x, self.rect.y - self.STEP)
            self.is_falling = False


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = background_image
        self.rect = self.image.get_rect().move(0, 0)


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '/':
                Tile('hanging_platform1', x, y)
            elif level[y][x] == '?':
                Tile('hanging_platform2', x, y)

            elif level[y][x] == '@':
                new_player = Player(x, y)

    return new_player, x, y


background = Background()

level = ['      ',
         '     /?',
         '     ',
         '@ ##  ##  #',
         '##..##..##.###',
         '...............',]

new_player, x, y = generate_level(level)


if __name__ == '__main__':
    scenes = [Scene1, Scene2]
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Platformer')
    current_scene = Scene1(SIZE, screen)
    not_exit = True

    while not_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_exit = False
            else:
                res = current_scene.render(event)
        current_scene.update()
        if res:
            current_scene = scenes[res - 1](SIZE, screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_exit = False
            else:
                res = current_scene.render(event)
        current_scene.update()
        if res:
            current_scene = scenes[res - 1](SIZE, screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_exit = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    new_player.is_move = True
                    new_player.direction = 'left'

                if event.key == pygame.K_d:
                    new_player.is_move = True
                    new_player.direction = 'right'

                if event.key == pygame.K_SPACE:
                    print('драсте забор покрасьте')
                    new_player.up_time = pygame.time.get_ticks()
                    new_player.is_up = True
                    new_player.direction = 'right'

            elif event.type == pygame.KEYUP:
                new_player.is_move = False

        new_player.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    print(clock)
    pygame.quit()
