import pygame
import sqlite3

from scene import Scene
from scene_login import Scene_Login
from scene_start import Scene_Start
from scene_level_01 import Scene_Level_01
from scene_lose import Scene_Lose
from scene_win import Scene_Win
import consts


scores = sqlite3.connect("db/scores.sqlite")
cur = scores.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS scores(login TEXT, currentscore INT, bestscore INT)"""
)


def main() -> None:
    pygame.init()
    pygame.font.init()
    pygame.display.set_mode(consts.SCREEN_SIZE)
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    user_name = ""
    scenes = {
        consts.SCENE_ID_LOGIN: Scene_Login,
        consts.SCENE_ID_START: Scene_Start,
        consts.SCENE_ID_LEVEL: Scene_Level_01,
        consts.SCENE_ID_LOSE: Scene_Lose,
        consts.SCENE_ID_WIN: Scene_Win,
    }
    current_scene: Scene = Scene_Login()

    run: bool = True
    while run:
        next_scene_id: str = consts.SCENE_ID_CURRENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            next_scene_id = current_scene.handle_event(event)
            if next_scene_id != consts.SCENE_ID_CURRENT:
                break

        if next_scene_id == consts.SCENE_ID_CURRENT:
            next_scene_id = current_scene.update()

        if next_scene_id == consts.SCENE_ID_CURRENT:
            current_scene.draw()
            pygame.display.flip()

        if next_scene_id != consts.SCENE_ID_CURRENT:
            if type(current_scene) == Scene_Login:
                user_name = current_scene.user_name

            if next_scene_id in scenes:
                current_scene = scenes[next_scene_id]()

            if type(current_scene) in (Scene_Login, Scene_Win, Scene_Lose):
                current_scene.set_user_name(user_name)

        clock.tick(consts.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
