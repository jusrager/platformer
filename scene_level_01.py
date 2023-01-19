import pygame
import consts
from scene import Scene
from utils import load_image


LEVEL = [
    "++++++                       ++++++",
    "++++++ @          =   =      ++++++",
    "++++++##          /?  /?   = ++++++",
    "++++++..#       =            ++++++",
    "++++++...#     /?     =      ++++++",
    "++++++....# =        ##     =++++++",
    "++++++.....##########..## # #++++++",
    "++++++...................-.-.++++++",
]  # 25


TILE_IMAGES = {
    "wall": "ground_rock",
    "empty": "rock",
    "hanging_platform1": "hanging_platform1",
    "hanging_platform2": "hanging_platform2",
    "lava": "lava",
    "coin": "coin",
    "stop": "stop",
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )


class Coin(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, player):
        super().__init__(coin_group, all_sprites)
        self.player = player
        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.text_surface3 = self.font.render(str(self.player.count), False, (0, 0, 0))

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.image = pygame.transform.scale(self.image, (0, 0))
            self.player.count += 1
            self.text_surface3 = self.font.render(
                str(self.player.count), False, (0, 0, 0)
            )
            pygame.display.get_surface().blit(self.text_surface3, (10, 10))
            print(self.player.count)
            self.rect = self.rect.move(-100, -100)


class Border(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(border_group, all_sprites)
        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            # self.rect = self.player.rect.move(-2, 0)
            # print('SSSSSSSSSSS')
            # финиш экран
            return 5


class Lava(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(lava_group, all_sprites)
        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            # self.rect = self.player.move(-2, 0)
            print("SSSSSSSSSSS")
            # проигрыш экран
            return 4


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, tiles_group):
        tiles_group.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, player):
        # print(self.dx, self.dy)
        self.dx = -(player.rect.x + player.rect.w // 2 - consts.SCREEN_WIDTH // 2)
        self.dy = -(player.rect.y + player.rect.h // 2 - consts.SCREEN_WIDTH // 2)

        # self.dx = -(self.player.image.get_rect().x +
        #            self.player.image.get_rect().w // 2 - width // 2)
        # self.dy = 0


class Player(pygame.sprite.Sprite):
    STEP = 2

    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.mask = pygame.mask.from_surface(pygame.Surface((consts.TILE_WIDTH, 4)))
        self.image = pygame.transform.scale(load_image("player"), consts.TILE_SIZE)
        self.rect = self.image.get_rect()
        self.set_position(0, 0)

        self.run = {
            "right": ["walk/right/1", "walk/right/2"],
            "left": ["walk/left/1", "walk/left/2"],
            "up": ["jump/1"],
        }

        self.count = 0
        self.cur_img = 0
        self.is_move = False
        self.direction = "right"
        self.is_up = False
        self.up_time = 0
        self.is_falling = False

    def set_position(self, pos_x, pos_y):
        print(pos_x, pos_y)
        self.rect = self.rect.move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y - 2
        )

    def update(self):
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.is_falling:
            self.lending()

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
            self.image = pygame.transform.scale(
                load_image(images[self.cur_img]), consts.TILE_SIZE
            )
        else:
            self.image = pygame.transform.scale(load_image(images[0]), consts.TILE_SIZE)

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


all_sprites: pygame.sprite.Group = pygame.sprite.Group()
tiles_group: pygame.sprite.Group = pygame.sprite.Group()
player_group: pygame.sprite.Group = pygame.sprite.Group()
coin_group: pygame.sprite.Group = pygame.sprite.Group()
border_group: pygame.sprite.Group = pygame.sprite.Group()
lava_group: pygame.sprite.Group = pygame.sprite.Group()


def generate_level(level):
    player = Player()

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
                Coin("coin", x, y, player)
            elif level[y][x] == "@":
                player.set_position(x, y)
            elif level[y][x] == "+":
                Border("stop", x, y)

    return player


class Scene_Level_01(Scene):
    def __init__(self):
        self.background = pygame.transform.scale(
            load_image("background"), consts.SCREEN_SIZE
        )

        self.player = generate_level(LEVEL)
        self.camera = Camera()

    def handle_event(self, event) -> str:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return consts.SCENE_ID_LOSE

            if event.key == pygame.K_a:
                self.player.is_move = True
                self.player.direction = "left"

            if event.key == pygame.K_d:
                self.player.is_move = True
                self.player.direction = "right"

            if event.key == pygame.K_SPACE:
                self.player.up_time = pygame.time.get_ticks()
                self.player.is_up = True
                self.player.direction = "up"

        elif event.type == pygame.KEYUP:
            self.player.is_move = False

        return consts.SCENE_ID_CURRENT

    def update(self) -> str:
        self.camera.update(self.player)
        for sprite in all_sprites:
            self.camera.apply(sprite)

        self.player.update()
        coin_group.update()
        border_group.update()
        lava_group.update()

        return consts.SCENE_ID_CURRENT

    def draw(self) -> str:
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        all_sprites.draw(screen)

        return consts.SCENE_ID_CURRENT
