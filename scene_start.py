import pygame
import consts
from scene import Scene
from utils import load_image
from music_manager import music_play


COLOR_TEXT = pygame.Color("black")


class Scene_Start(Scene):
    def __init__(self):
        super().__init__()

        self.background = pygame.transform.scale(
            load_image("background"), consts.SCREEN_SIZE
        )

        self.sound_button = pygame.mixer.Sound(
            "assets/sound/fxs/mixkit-arcade-mechanical-bling-210.ogg"
        )

        self.width, self.height = (200, 80)
        self.x, self.y = (
            (consts.SCREEN_WIDTH - self.width) // 2,
            (consts.SCREEN_HEIGHT - self.height) // 2,
        )

        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text_x, self.text_y = (
            (consts.SCREEN_WIDTH - self.width) // 2 + 10,
            (consts.SCREEN_HEIGHT - self.height) // 2 - 100,
        )
        self.text_x1, self.text_y1 = (
            (consts.SCREEN_WIDTH - self.width) // 2 + 44,
            (consts.SCREEN_HEIGHT - self.height) // 2 + 16,
        )
        self.text_x2, self.text_y2 = (
            (consts.SCREEN_WIDTH - self.width) // 2 - 104,
            (consts.SCREEN_HEIGHT - self.height) // 2 + 124,
        )

        font35 = pygame.font.SysFont("Comic Sans MS", 35)
        font30 = pygame.font.SysFont("Comic Sans MS", 30)
        font23 = pygame.font.SysFont("Comic Sans MS", 23)

        self.text_surface1 = font35.render("Platformer", False, COLOR_TEXT)
        self.text_surface2 = font30.render("START!", False, COLOR_TEXT)
        self.text_surface3 = font23.render(
            "A, D - вправо, влево; Пробел - прыжок", False, COLOR_TEXT
        )

    def show(self) -> None:
        music_play(
            "assets/sound/loops/music_zapsplat_game_music_fun_tropical_caribean_steel_drums_percussion_008.mp3",
            volume=0.7,
        )

    def handle_event(self, event) -> str:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.sound_button.play()
                return consts.SCENE_ID_LEVEL

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.sound_button.play()
                return consts.SCENE_ID_LOGIN

            if event.key == pygame.K_RETURN:
                self.sound_button.play()
                return consts.SCENE_ID_LEVEL

        return consts.SCENE_ID_CURRENT

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))

        pygame.draw.rect(
            screen,
            (54, 54, 54),
            [self.x - 5, self.y - 5, self.width + 10, self.height + 10],
        )
        pygame.draw.rect(screen, (204, 204, 204), self.button_rect)
        screen.blit(self.text_surface1, (self.text_x, self.text_y))
        screen.blit(self.text_surface2, (self.text_x1, self.text_y1))
        screen.blit(self.text_surface3, (self.text_x2, self.text_y2))
