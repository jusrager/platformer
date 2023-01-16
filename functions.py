import os
import sys

import pygame


SIZE = width, height = 832, 512
run = True

pygame.init()
screen = pygame.display.set_mode((width, height))

WIDTH, HEIGHT = (200, 80)
X, Y = ((width - WIDTH) // 2, (height - HEIGHT) // 2)
text_x, text_y = ((width - WIDTH) // 2 + 10, (height - HEIGHT) // 2 - 100)
text_x1, text_y1 = ((width - WIDTH) // 2 + 44, (height - HEIGHT) // 2 + 16)
text_x2, text_y2 = ((width - WIDTH) // 2 - 104, (height - HEIGHT) // 2 + 124)
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

