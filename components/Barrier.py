import pygame


class Barrier():
    def __init__(self, screen, image, x, y):
        self.image = image
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 200
        self.height = 50
        self.COLOR = (50, 50, 50)
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def draw(self):
        pygame.draw.rect(
            surface=self.screen,
            color=self.COLOR,
            rect=self.rect,
        )
        self.screen.blit(source=self.image, dest=(self.x, self.y))
