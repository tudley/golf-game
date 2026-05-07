import pygame
from components.Barrier import Barrier


class Ball():

    def __init__(
        self,
        barriers: Barrier,
        image: pygame.surface,
        screen: pygame.surface,
        x: int,
        y: int,
        vx: int = 0,
        vy: int = 0,

    ):
        self.screen = screen
        self.image = image
        self.barriers = barriers
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dvx = 0
        self.dvy = 0
        self.R = 15
        self.COLOR = (255, 255, 255)
        self.grounded = False

        self.x_e = 0.9
        self.y_e = 0.6

    def draw(self) -> None:
        pygame.draw.circle(
            surface=self.screen,
            color=self.COLOR,
            center=(self.x, self.y),
            radius=self.R,
        )
        self.screen.blit(source=self.image, dest=(self.x - 15, self.y - 15))

    def update(self) -> None:
        # if self.grounded:
        # print("grounded= ", self.grounded)
        self.handle_colissions()
        self.update_acceleration()
        self.update_velocity()
        self.update_position()

    def apply_gravity(self):
        self.dvy += 0.1

    def apply_resistance(self):
        # Apply air resistance
        self.dvx *= 0.7
        self.dvy *= 0.7

    def apply_friction(self):
        self.dvx *= 0.5

    def update_acceleration(self) -> None:
        self.apply_gravity()
        self.apply_resistance()
        if self.grounded:
            self.apply_friction()

    def update_velocity(self) -> None:
        self.vy += self.dvy
        self.vx += self.dvx
        # if self.vy < 0.5:
        #     self.vy = 0
        # print("self.vx = ", self.vx)
        # print("self.vy = ", self.vy)
        if abs(self.vx) < 0.5:
            self.dvx = 0
            self.vx = 0

    def update_position(self) -> None:
        self.y += self.vy
        self.x += self.vx

    def handle_colissions(self) -> None:
        for barrier in self.barriers:
            self.determine_colission(barrier)

    def determine_colission(self, barrier: Barrier) -> str | None:
        # Determine if Y colission

        # First determine if its within the X bound of the barrier
        if barrier.rect.left < self.x < barrier.rect.right:

            if self.y < barrier.rect.y:  # ball is above
                # print("ball is is above barrier")
                y_distance = abs(barrier.rect.top - self.y)
                # print(f"y_distance={y_distance}")
                if y_distance <= self.R:
                    self.grounded = True
                    self.correct_position(
                        offset="above", x=None, y=barrier.rect.top)
                    self.bounce(axis="y")
                else:
                    self.grounded = False

            elif self.y > barrier.rect.y:  # ball is below
                # print("balll is below barrier")
                y_distance = abs(barrier.rect.top - self.y)
                if y_distance < self.R:
                    self.correct_position(
                        offset="blelow", x=None, y=barrier.rect.bottom)
                    self.bounce(axis="y")

        # Determine if X colission

        # First determine if its within the Y bound of the barrier
        if barrier.rect.top < self.y < barrier.rect.bottom:

            if self.x < barrier.rect.left:  # ball is on the left
                closest_x = abs(barrier.rect.left - self.x)
                if closest_x < self.R:
                    self.correct_position(
                        offset="left", x=barrier.rect.left, y=None)
                    self.bounce(axis="x")

            elif self.x > barrier.rect.right:  # Ball is on the right
                closest_x = abs(
                    (barrier.rect.left + barrier.rect.width) - self.x)
                if closest_x < self.R:
                    self.correct_position(
                        offset="right", x=barrier.rect.right, y=None)
                    self.bounce(axis="x")

    def correct_position(self, offset: str, x: float = None, y: float = None):
        # print(f"correct_position called with offset={offset}, x={x}, y={y}")
        if x:
            if offset == "left":
                self.x = x - self.R
            elif offset == "right":
                self.x = x + self.R

        elif y:
            if offset == "above":
                self.y = y - self.R
            elif offset == "below":
                self.y = y + self.R

    def bounce(self, axis: str):
        # print(f"bounce called on axis={axis}")
        if axis == "y":
            self.vy *= -self.y_e
            self.dvy *= -self.y_e
            self.dvx *= self.x_e
            self.vx *= self.x_e
        elif axis == "x":
            self.dvx *= -self.y_e
            self.vx *= -self.y_e
