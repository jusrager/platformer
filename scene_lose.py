import pygame
import consts
from scene import Scene
from utils import load_image
from music_manager import music_play, sound_load
from db_manager import dbscores_get_best, dbscores_put_current


COLOR_TEXT = pygame.Color("black")


class Scene_Lose(Scene):
    def __init__(self):
        super().__init__()

        self.background = pygame.transform.scale(
            load_image("background"), consts.SCREEN_SIZE
        )

        self.sound_button = sound_load("mixkit-arcade-mechanical-bling-210.ogg")

        self.width, self.height = (200, 80)
        self.x, self.y = (
            (consts.SCREEN_WIDTH - self.width) // 2,
            (consts.SCREEN_HEIGHT - self.height) // 2 + 100,
        )

        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text_x, self.text_y = (
            (consts.SCREEN_WIDTH - self.width) // 2 - 45,
            (consts.SCREEN_HEIGHT - self.height) // 2 - 100,
        )
        self.text_x1, self.text_y1 = (
            (consts.SCREEN_WIDTH - self.width) // 2,
            (consts.SCREEN_HEIGHT - self.height) // 2 - 25,
        )
        self.text_x2, self.text_y2 = (
            (consts.SCREEN_WIDTH - self.width) // 2 + 50,
            (consts.SCREEN_HEIGHT - self.height) // 2 + 115,
        )

        self.font35 = pygame.font.SysFont("Comic Sans MS", 35)
        self.font30 = pygame.font.SysFont("Comic Sans MS", 30)
        self.surface_button = self.font30.render("Заново", False, COLOR_TEXT)

        self.user_name = ""
        self.score_current = 0
        self.score_best = 0

    def show(self) -> None:
        music_play(
            "music_zapsplat_game_music_fun_tropical_caribean_steel_drums_percussion_008.mp3",
            volume=0.7,
        )

        self.score_best = dbscores_get_best(self.user_name)

    def set_user_name(self, user_name):
        self.user_name = user_name

    def set_score(self, score):
        self.score_current = score

    def handle_event(self, event) -> str:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.sound_button.play()
                return consts.SCENE_ID_START

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

        surface = self.font35.render(
            f"{self.user_name}, вы проиграли", False, COLOR_TEXT
        )
        screen.blit(surface, (self.text_x, self.text_y))
        screen.blit(self.surface_button, (self.text_x2, self.text_y2))

        surface = self.font30.render(
            f"Ваш результат: {self.score_current}", False, COLOR_TEXT
        )
        screen.blit(surface, (self.text_x, self.text_y1))

        if self.score_best != -1:
            surface = self.font30.render(
                f"Ваш рекорд: {self.score_best}", False, COLOR_TEXT
            )
            screen.blit(surface, (self.text_x, self.text_y1 + 45))
