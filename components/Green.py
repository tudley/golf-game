import pygame

from components.Barrier import Barrier


class Green(Barrier):
    def __init__(self, screen, image, x, y):
        super().__init__(screen, image, x, y)
        self.COLOR = (0, 255, 150)

    def draw(self):
        pygame.draw.rect(
            surface=self.screen,
            color=self.COLOR,
            rect=self.rect,
        )
        self.screen.blit(source=self.image, dest=(self.x, self.y - 61))
