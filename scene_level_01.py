from typing import Union
from os.path import join as path_join
import pygame
import consts
from scene import Scene
from utils import load_image
from music_manager import music_play, sound_load


LEVEL: tuple[str, ...] = (
    "++++++                       ++++++",
    "++++++           =   =      ++++++",
    "++++++##          /?  /?   = ++++++",
    "++++++..#       =            ++++++",
    "++++++...#=    /?     =      ++++++",
    "++++++....#@         ##     =++++++",
    "++++++.....##########..## # #++++++",
    "++++++...................-.-.++++++",
)  # 25


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
        super().__init__()

        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )


class Border(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )


class Lava(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )


class Coin(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            load_image(TILE_IMAGES[tile_type]), consts.TILE_SIZE
        )
        self.rect = self.image.get_rect().move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y
        )
        # self.font = pygame.font.SysFont("Comic Sans MS", 30)
        # self.text_surface3 = self.font.render(str(self.player.count), False, (0, 0, 0))


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
    RUN = {
        "right": [path_join("walk", "right", "1"), path_join("walk", "right", "2")],
        "left": [path_join("walk", "left", "1"), path_join("walk", "left", "2")],
        "up": [path_join("jump", "1")],
    }

    def __init__(self, tiles: pygame.sprite.Group) -> None:
        super().__init__()

        self.tiles: pygame.sprite.Group = tiles

        self.image = pygame.transform.scale(load_image("player"), consts.TILE_SIZE)
        self.rect = self.image.get_rect()
        self.set_position(0, 0)

        self.coin_count: int = 0
        self.cur_img = 0
        self.is_move = False
        self.direction = "right"
        self.is_up = False
        self.up_time = 0
        self.is_falling = False

    def set_position(self, pos_x, pos_y):
        self.rect = self.rect.move(
            consts.TILE_WIDTH * pos_x, consts.TILE_HEIGHT * pos_y - 2
        )

    def update(self):
        if not pygame.sprite.spritecollideany(self, self.tiles) and self.is_falling:
            self.lending()

        images = self.RUN[self.direction]

        if self.is_up:
            self.rect = self.rect.move(0, -7)
            if pygame.time.get_ticks() - self.up_time >= 400:
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

            if pygame.sprite.spritecollideany(self, self.tiles):
                self.rect = self.rect.move(-self.STEP, 0)

        if self.direction == "left":
            self.rect = self.rect.move(-self.STEP, 0)

            if pygame.sprite.spritecollideany(self, self.tiles):
                self.rect = self.rect.move(self.STEP, 0)

    def lending(self):
        self.rect = self.rect.move(0, self.STEP)

        if pygame.sprite.spritecollideany(self, self.tiles):
            self.rect = self.rect.move(0, -self.STEP)
            if self.is_up:
                self.is_falling = False


class Scene_Level_01(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.background = pygame.transform.scale(
            load_image("background"), consts.SCREEN_SIZE
        )

        self.sound_coin = sound_load("mixkit-bonus-earned-in-video-game-2058.ogg")
        self.sound_lava = sound_load("mixkit-creature-cry-of-hurt-2208.ogg")

        self.tick_start: int = 0
        self.tick_stop: int = 0

        self.all_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.tiles_group: pygame.sprite.Group = pygame.sprite.Group()
        self.coin_group: pygame.sprite.Group = pygame.sprite.Group()
        self.border_group: pygame.sprite.Group = pygame.sprite.Group()
        self.lava_group: pygame.sprite.Group = pygame.sprite.Group()

        self.player = Player(self.tiles_group)
        self.all_sprites.add(self.player)

        self.camera = Camera()

        self.load_level(LEVEL)

    def show(self) -> None:
        self.tick_start = pygame.time.get_ticks()
        music_play(
            "music_zapsplat_game_music_childrens_soft_warm_cuddly_calm_015.mp3",
            volume=1.2,
        )

    def hide(self) -> None:
        self.tick_stop = pygame.time.get_ticks()

    def get_score(self) -> int:
        return (
            self.tick_stop - self.tick_start
            if self.tick_stop > 0
            else pygame.time.get_ticks() - self.tick_start
        ) // 10

    def load_level(self, level: tuple[str, ...]) -> None:
        for y in range(len(level)):
            for x in range(len(level[y])):
                entity: Union[pygame.sprite.Sprite, None] = None
                if level[y][x] == ".":
                    entity = Tile("empty", x, y)
                    self.tiles_group.add(entity)
                elif level[y][x] == "#":
                    entity = Tile("wall", x, y)
                    self.tiles_group.add(entity)
                elif level[y][x] == "+":
                    entity = Tile("stop", x, y)
                    self.tiles_group.add(entity)
                elif level[y][x] == "/":
                    entity = Tile("hanging_platform1", x, y)
                    self.tiles_group.add(entity)
                elif level[y][x] == "?":
                    entity = Tile("hanging_platform2", x, y)
                    self.tiles_group.add(entity)
                elif level[y][x] == "-":
                    entity = Lava("lava", x, y)
                    self.lava_group.add(entity)
                elif level[y][x] == "=":
                    entity = Coin("coin", x, y)
                    self.coin_group.add(entity)
                elif level[y][x] == "@":
                    self.player.set_position(x, y)

                if entity:
                    self.all_sprites.add(entity)

    def handle_event(self, event) -> str:
        if event.type == pygame.KEYDOWN:
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
        for sprite in self.all_sprites:
            self.camera.apply(sprite)

        self.all_sprites.update()

        coin: Union[pygame.sprite.Sprite, None] = pygame.sprite.spritecollideany(
            self.player, self.coin_group
        )
        if coin:
            self.player.coin_count += 1
            self.sound_coin.play()
            coin.kill()

            if len(self.coin_group) == 0:
                return consts.SCENE_ID_WIN

        if pygame.sprite.spritecollideany(self.player, self.lava_group):
            self.sound_lava.play()
            return consts.SCENE_ID_LOSE

        return consts.SCENE_ID_CURRENT

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        self.all_sprites.draw(screen)

        # вывод статистики
        score_font = pygame.font.SysFont("Comic Sans MS", 30)
        # количество собранных монет
        score_surface = score_font.render(str(self.player.coin_count), True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))
        # таймер
        score_surface = score_font.render(str(self.get_score()), True, (0, 0, 0))
        screen.blit(
            score_surface, (screen.get_width() - score_surface.get_width() - 10, 10)
        )
