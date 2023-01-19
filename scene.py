import pygame
import consts


class Scene:
    def handle_event(self, event: pygame.event.Event) -> str:
        return consts.SCENE_ID_CURRENT

    def update(self) -> str:
        return consts.SCENE_ID_CURRENT

    def draw(self) -> str:
        return consts.SCENE_ID_CURRENT
