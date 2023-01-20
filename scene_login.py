import pygame
import consts
from scene import Scene
from utils import load_image
from music_manager import music_play


COLOR_INPUT_ACTIVE = pygame.Color("lightskyblue")
COLOR_INPUT_INACTIVE = pygame.Color("lightslategrey")


class Scene_Login(Scene):
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

        self.input_rect = pygame.Rect(
            (consts.SCREEN_WIDTH - 160) // 2 - 20,
            (consts.SCREEN_HEIGHT - 32) // 2 - 35,
            160,
            32,
        )
        self.button_rect = pygame.Rect(
            self.x, self.y + 40, self.width, self.height + 40
        )

        self.input_font = pygame.font.SysFont("Comic Sans MS", 32)

        font35 = pygame.font.SysFont("Comic Sans MS", 35)
        font30 = pygame.font.SysFont("Comic Sans MS", 30)
        font23 = pygame.font.SysFont("Comic Sans MS", 23)
        self.text_surface3 = font35.render("Введите логин", False, (0, 0, 0))
        self.text_surface4 = font30.render("OK", False, (0, 0, 0))
        self.text_surface5 = font23.render(
            "Введите логин! 8 букв, латиница", False, (247, 19, 24)
        )

        self.input_active = False
        self.input_error = False
        self.user_name = ""

    def show(self) -> None:
        music_play(
            "assets/sound/loops/music_zapsplat_game_music_fun_tropical_caribean_steel_drums_percussion_008.mp3",
            volume=0.7,
        )

    def set_user_name(self, user_name):
        self.user_name = user_name

    def handle_event(self, event) -> str:
        check_user_name = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.input_active = self.input_rect.collidepoint(event.pos)
            if self.button_rect.collidepoint(event.pos):
                self.sound_button.play()
                check_user_name = True

        if event.type == pygame.KEYDOWN:
            self.input_error = False

            if self.input_active:
                if event.key == pygame.K_RETURN:
                    self.sound_button.play()
                    check_user_name = True
                elif event.key == pygame.K_BACKSPACE:
                    self.user_name = self.user_name[:-1]
                else:
                    if len(self.user_name) < 8:
                        self.user_name += event.unicode

        if check_user_name:
            if len(self.user_name) >= 8:
                return consts.SCENE_ID_START

            self.input_error = True

        return consts.SCENE_ID_CURRENT

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))

        input_color = COLOR_INPUT_ACTIVE if self.input_active else COLOR_INPUT_INACTIVE

        txt_surface = self.input_font.render(self.user_name, True, input_color)

        self.input_rect.w = max(200, txt_surface.get_width() + 10)

        pygame.draw.rect(screen, input_color, self.input_rect, 2)
        pygame.draw.rect(
            screen,
            (54, 54, 54),
            [self.x - 5, self.y + 35, self.width + 10, self.height + 10],
        )
        pygame.draw.rect(
            screen, (204, 204, 204), [
                self.x, self.y + 40, self.width, self.height]
        )

        screen.blit(
            txt_surface,
            (self.input_rect.x + 5, self.input_rect.y - 10),
        )
        screen.blit(self.text_surface3, (self.text_x - 37, self.text_y))
        screen.blit(self.text_surface4, (self.text_x1 + 30, self.text_y1 + 40))

        if self.input_error:
            screen.blit(self.text_surface5,
                        (self.text_x2 + 20, self.text_y2 + 15))
