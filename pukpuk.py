import pygame as pg


def main():
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()



import pygame
import os
import sys

width = 832
height = 512

tile_width = tile_height = 64


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
        surf = pygame.Surface((tile_width, 4))
        self.mask = pygame.mask.from_surface(surf)
        self.image = player_image

        print(pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 2)

        self.run = {'right': [os.path.join('walk', 'right', file) for file in os.listdir(os.path.join('walk', 'right'))],
                    'left': [os.path.join('walk', 'left', file) for file in os.listdir(os.path.join('walk', 'left'))],
                    'up': [os.path.join('jump', file) for file in os.listdir(os.path.join('jump'))]}

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
            self.lending()
            self.cur_img = (self.cur_img + 1) % len(images)
            self.image = load_image(images[self.cur_img])
        else:
            self.image = load_image(images[0])

        if self.is_up:
            self.rect = self.rect.move(0, -7)
            if pygame.time.get_ticks() - self.up_time >= 400:
                print(pygame.time.get_ticks(), self.up_time)
                self.is_up = False
                self.is_falling = True

    def move(self):
        if self.direction == 'right':
            self.rect = self.rect.move(self.STEP, 0)

            # if not pygame.sprite.spritecollide.collide_mask(self, tiles_group):
            #    self.rect = self.rect.move(-self.STEP, 0)

            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(-self.STEP, 0)

        if self.direction == 'left':
            self.rect = self.rect.move(-self.STEP, 0)

            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(self.STEP, 0)

        # elif self.direction == 'up':
        #    if self.is_up:
        #        self.rect = self.rect.move(0, -10)

    def lending(self):
        self.is_falling = True
        self.rect = self.rect.move(0, self.STEP)

        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect = self.rect.move(0, - self.STEP)
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

level = ['        ',
         '        ',
         '        ',
         '        ',
         '        ',
         '  ##  @#  #',
         '##..###.##.###',
         '...............',]

new_player, x, y = generate_level(level)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, tiles_group):
        tiles_group.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, new_player):
        self.dx = -(new_player.rect.x + new_player.rect.w // 2 - width // 2)
        self.dy = -(new_player.rect.y + new_player.rect.h // 2 - height // 2)


camera = Camera()

while not_exit:
    pygame.display.set_caption('platformer')
    for event in pygame.event.get():
        camera.update(new_player)
        for sprite in all_sprites:
            camera.apply(sprite)

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
                new_player.direction = 'up'

        elif event.type == pygame.KEYUP:
            new_player.is_move = False

    new_player.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

