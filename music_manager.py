import pygame
import os

music_path: str = ""


def sound_load(path: str) -> pygame.mixer.Sound:
    path = os.path.join("assets", "sound", "fxs", path)
    return pygame.mixer.Sound(path)


def music_play(path: str, volume: float = 1.0, restart=False) -> None:
    global music_path

    path = os.path.join("assets", "sound", "loops", path)
    if pygame.mixer.music.get_busy():
        if path == music_path:
            if restart:
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1, start=0, fade_ms=1000)
        else:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, start=0, fade_ms=1000)
    else:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, start=0, fade_ms=1000)

    music_path = path


def music_stop() -> None:
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000)
