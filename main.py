import pygame
import os
import sys
import random
import sqlite3
from first_window import Scene1
from second_window import Scene2
from third_window import Scene3
from lose_window import SceneLose
from win_window import SceneWin
from functions import *


scores = sqlite3.connect("db/scores.sqlite")
cur = scores.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS scores(login TEXT, currentscore INT, bestscore INT)""")


FPS = 40
clock = pygame.time.Clock()
x, y = 0, 0
r = 10
not_exit = True
clicked = False


if __name__ == '__main__':
    scenes = [Scene1, Scene2, Scene3, SceneLose, SceneWin]
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Platformer')
    current_scene = Scene1(SIZE, screen)
    not_exit = True

    while not_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_exit = False
            else:
                res = current_scene.render(event)
        current_scene.update()
        if res:
            if isinstance(current_scene, Scene1):
                print('instance')
                user = res[1]
                current_scene = scenes[res[0] - 1](SIZE, screen)
            elif isinstance(current_scene, SceneLose) or isinstance(current_scene, SceneWin):
                current_scene = scenes[res[0] - 1](SIZE, screen, user)
            else:
                current_scene = scenes[res[0] - 1](SIZE, screen)
        pygame.display.flip()
    print(clock)
    pygame.quit()
