import pygame

import os
import sys

width = 832
height = 512

tile_width = tile_height = 64


def load_image(image_name: str, colorkey: pygame.Color | None = None) -> pygame.Surface:
    image_path: str = f"assets/{image_name}.png"

    if not os.path.isfile(image_path):
        print(f"Файл с изображением '{image_path}' не найден")
        sys.exit()

    image: pygame.Surface = pygame.image.load(image_path)

    if image_name != "background":
        image = pygame.transform.scale(image, (tile_width, tile_height))

    if colorkey:
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
    "wall": load_image("ground_rock"),
    "empty": load_image("rock"),
    "hanging_platform1": load_image("hanging_platform1"),
    "hanging_platform2": load_image("hanging_platform2"),
    "lava": load_image("lava"),
    "coin": load_image("coin"),
    "stop": load_image("stop"),
}
player_image = load_image("player")
background_image = load_image("background")


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))


class Player(pygame.sprite.Sprite):
    STEP = 2

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        surf = pygame.Surface((tile_width, 4))
        self.mask = pygame.mask.from_surface(surf)
        self.image = player_image

        print(pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 2
        )

        self.run = {
            "right": ["walk/right/1", "walk/right/2"],
            "left": ["walk/left/1", "walk/left/2"],
            "up": ["jump/1"],
        }

        print(self.run)

        self.count = 0

        self.cur_img = 0
        self.is_move = False
        self.direction = "right"
        self.is_up = False
        self.up_time = 0
        self.is_falling = False

    def update(self) -> None:
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.is_falling:
            self.lending()

        # print(pygame.time.get_ticks())

        images = self.run[self.direction]

        if self.is_up:
            self.rect = self.rect.move(0, -7)
            if pygame.time.get_ticks() - self.up_time >= 400:
                print(pygame.time.get_ticks(), self.up_time)
                self.is_up = False
                self.is_falling = True

        if self.is_move:
            self.move()
            self.lending()
            self.cur_img = (self.cur_img + 1) % len(images)
            self.image = load_image(images[self.cur_img])
        else:
            self.image = load_image(images[0])

    def move(self):
        if self.direction == "right":
            self.rect = self.rect.move(self.STEP, 0)

            # if not pygame.sprite.spritecollide.collide_mask(self, tiles_group):
            #    self.rect = self.rect.move(-self.STEP, 0)

            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(-self.STEP, 0)

        if self.direction == "left":
            self.rect = self.rect.move(-self.STEP, 0)

            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(self.STEP, 0)

        # elif self.direction == 'up':
        #    if self.is_up:
        #        self.rect = self.rect.move(0, -10)

    def lending(self):
        self.rect = self.rect.move(0, self.STEP)

        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect = self.rect.move(0, -self.STEP)
            if self.is_up:
                self.is_falling = False


class Coin(pygame.sprite.Sprite):
    def __init__(self, screen, tile_type, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.screen = screen
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.image = pygame.transform.scale(self.image, (0, 0))
            new_player.count += 1
            text_surface3 = self.font.render(str(new_player.count), True, (0, 0, 0))
            self.screen.blit(text_surface3, (10, 10))
            print(new_player.count)
            # self.rect = self.rect.move(-100, -100)


class Border(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(border_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.rect = new_player.rect.move(-2, 0)
            print("SSSSSSSSSSS")
            # финиш экран


class Lava(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(lava_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            # self.rect = new_player.move(-2, 0)
            print("SSSSSSSSSSS")
            # проигрыш экран


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = background_image
        self.rect = self.image.get_rect().move(0, 0)


all_sprites: pygame.sprite.Group = pygame.sprite.Group()
tiles_group: pygame.sprite.Group = pygame.sprite.Group()
player_group: pygame.sprite.Group = pygame.sprite.Group()
coin_group: pygame.sprite.Group = pygame.sprite.Group()
border_group: pygame.sprite.Group = pygame.sprite.Group()
lava_group: pygame.sprite.Group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == "/":
                Tile("hanging_platform1", x, y)
            elif level[y][x] == "?":
                Tile("hanging_platform2", x, y)
            elif level[y][x] == "-":
                Lava("lava", x, y)
            elif level[y][x] == "=":
                Coin(screen, "coin", x, y)
            elif level[y][x] == "+":
                Border("stop", x, y)

            elif level[y][x] == "@":
                new_player = Player(x, y)

    return new_player, x, y


background = Background()

level = [
    "++++++                       ++++++",
    "++++++=            =   =     ++++++",
    "++++++##=         /?  /?   = ++++++",
    "++++++..#                    ++++++",
    "++++++...#     /?     =      ++++++",
    "++++++....# @        ##     =++++++",
    "++++++.....##########..## # #++++++",
    "++++++...................-.-.++++++",
]  # 25

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
        # print(self.dx, self.dy)
        self.dx = -(new_player.rect.x + new_player.rect.w // 2 - width // 2)
        self.dy = -(new_player.rect.y + new_player.rect.h // 2 - height // 2)

        # self.dx = -(new_player.image.get_rect().x +
        #            new_player.image.get_rect().w // 2 - width // 2)
        # self.dy = 0


camera = Camera()

while not_exit:
    pygame.display.set_caption("platformer")
    for event in pygame.event.get():
        camera.update(new_player)
        for sprite in all_sprites:
            camera.apply(sprite)

        if event.type == pygame.QUIT:
            not_exit = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                new_player.is_move = True
                new_player.direction = "left"

            if event.key == pygame.K_d:
                new_player.is_move = True
                new_player.direction = "right"

            if event.key == pygame.K_SPACE:
                print("драсте забор покрасьте")
                new_player.up_time = pygame.time.get_ticks()
                new_player.is_up = True
                new_player.direction = "up"

        elif event.type == pygame.KEYUP:
            new_player.is_move = False

    new_player.update()
    all_sprites.draw(screen)
    coin_group.update()
    # border_group.update()
    # lava_group.update()
    pygame.display.flip()
    clock.tick(FPS)
