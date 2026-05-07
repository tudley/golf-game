import pygame
import math

from components.Ball import Ball


class Arrow():
    def __init__(self, screen: pygame.surface, ball: Ball, mouse: pygame.mouse):
        self.screen = screen
        self.ball = ball
        self.start_x = ball.x
        self.start_y = ball.y
        self.mouse = mouse
        self.end_x = mouse[0]
        self.end_y = mouse[1]

        self.color = (255, 0, 0)

    def draw(self):
        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        length = math.hypot(dx, dy)

        # If mouse is on top of ball, there is no direction to draw.
        if length == 0:
            return

        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux

        head_length = 20
        head_half_width = 8

        tip = (self.end_x, self.end_y)
        base_x = self.end_x - ux * head_length
        base_y = self.end_y - uy * head_length

        left = (
            base_x + px * head_half_width,
            base_y + py * head_half_width,
        )
        right = (
            base_x - px * head_half_width,
            base_y - py * head_half_width,
        )

        line_end = (base_x, base_y)

        pygame.draw.line(
            surface=self.screen,
            color=self.color,
            start_pos=(self.start_x, self.start_y),
            end_pos=line_end,
            width=5,
        )

        pygame.draw.polygon(
            surface=self.screen,
            color=self.color,
            points=[tip, left, right],
        )

    def update(self, mouse_x, mouse_y):
        self.start_x = self.ball.x
        self.start_y = self.ball.y
        self.end_x = mouse_x
        self.end_y = mouse_y
