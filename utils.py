from typing import Union
import os
import sys
import pygame


def load_image(
    image_name: str, colorkey: Union[pygame.Color, None] = None
) -> pygame.Surface:
    image_path: str = os.path.join("assets", "gfx", f"{image_name}.png")
    if not os.path.isfile(image_path):
        print(f"Файл с изображением '{image_path}' не найден")
        sys.exit()

    image: pygame.Surface = pygame.image.load(image_path)

    if colorkey:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image
