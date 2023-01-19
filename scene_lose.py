import pygame
import consts
from scene import Scene
from utils import load_image


COLOR_TEXT = pygame.Color("black")


class Scene_Lose(Scene):
    def __init__(self):
        self.background = pygame.transform.scale(
            load_image("background"), consts.SCREEN_SIZE
        )
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

        font35 = pygame.font.SysFont("Comic Sans MS", 35)
        font30 = pygame.font.SysFont("Comic Sans MS", 30)
        self.text_surface1 = font35.render("Вы проиграли", False, COLOR_TEXT)
        self.text_surface2 = font30.render("Ваш результат:", False, COLOR_TEXT)
        self.text_surface3 = font30.render("Ваш рекорд:", False, COLOR_TEXT)
        self.text_surface4 = font30.render("Заново", False, COLOR_TEXT)

        self.user_name = ""

    def set_user_name(self, user_name):
        self.user_name = user_name

    def handle_event(self, event) -> str:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                return consts.SCENE_ID_START

        return consts.SCENE_ID_CURRENT

    def draw(self) -> str:
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        pygame.draw.rect(
            screen,
            (54, 54, 54),
            [self.x - 5, self.y - 5, self.width + 10, self.height + 10],
        )
        pygame.draw.rect(screen, (204, 204, 204), self.button_rect)

        screen.blit(self.text_surface1, (self.text_x, self.text_y))
        screen.blit(self.text_surface2, (self.text_x, self.text_y1))
        screen.blit(self.text_surface3, (self.text_x, self.text_y1 + 45))
        screen.blit(self.text_surface4, (self.text_x2, self.text_y2))

        return consts.SCENE_ID_CURRENT
