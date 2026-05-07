import pygame
import os
import math
import sys

from components.Ball import Ball
from components.Barrier import Barrier
from components.VerticalBarrier import VerticalBarrier
from components.Green import Green
from components.Arrow import Arrow
from components.GameState import GameState

# Init
pygame.init()
screen = pygame.display.set_mode((1280, 720))

# Load assets
background = pygame.image.load(os.path.join(
    "golf-game", "assets", "background.png")).convert()

barrier_img = pygame.image.load(os.path.join(
    "golf-game", "assets", "barrier.png")).convert()

vertical_barrier_left_img = pygame.image.load(os.path.join(
    "golf-game", "assets", "vertical_barrier_left.png")).convert()

vertical_barrier_right_img = pygame.image.load(os.path.join(
    "golf-game", "assets", "vertical_barrier_right.png")).convert()

green_img = pygame.image.load(os.path.join(
    "golf-game", "assets", "green.png")).convert_alpha()

ball_img = pygame.image.load(os.path.join(
    "golf-game", "assets", "ball.png")).convert_alpha()

# Create objects


mouse_pos = pygame.mouse.get_pos()
clock = pygame.time.Clock()
running = True

barriers = []

# Start floor barrier
barrier_1 = Barrier(
    screen=screen,
    image=barrier_img,
    x=0,
    y=650,
    # width=600,
    # height=50,
)

# Floor barrier
barrier_2 = Barrier(
    screen=screen,
    image=barrier_img,
    x=200,
    y=600,
    # width=380,
    # height=50,
)

# Floor barrier
barrier_3 = Barrier(
    screen=screen,
    image=barrier_img,
    x=400,
    y=550,
    # width=50,
    # height=720,
)


# Floor barrier
barrier_4 = Barrier(
    screen=screen,
    image=barrier_img,
    x=600,
    y=500,
    # width=50,
    # height=720,
)

# End floor barrier
barrier_5 = Barrier(
    screen=screen,
    image=barrier_img,
    x=800,
    y=450,
    # width=50,
    # height=720,
)

# Green
green = Green(
    screen=screen,
    image=green_img,
    x=1000,
    y=400,
    # width=200,
    # height=50
)

# End vertical barrier
vertical_left_barrier_1 = VerticalBarrier(
    screen=screen,
    image=vertical_barrier_left_img,
    x=0,
    y=450,
    # width=50,
    # height=720,
)

# End vertical barrier
vertical_left_barrier_2 = VerticalBarrier(
    screen=screen,
    image=vertical_barrier_left_img,
    x=0,
    y=250,
    # width=50,
    # height=720,
)

# End vertical barrier
vertical_left_barrier_3 = VerticalBarrier(
    screen=screen,
    image=vertical_barrier_left_img,
    x=0,
    y=50,
    # width=50,
    # height=720,
)

# End vertical barrier
vertical_right_barrier_1 = VerticalBarrier(
    screen=screen,
    image=vertical_barrier_right_img,
    x=1200,
    y=450,
    # width=50,
    # height=720,
)

# End vertical barrier
vertical_right_barrier_2 = VerticalBarrier(
    screen=screen,
    image=vertical_barrier_right_img,
    x=1200,
    y=250,
    # width=50,
    # height=720,
)

# End vertical barrier
vertical_right_barrier_3 = VerticalBarrier(
    screen=screen,
    image=vertical_barrier_right_img,
    x=1200,
    y=50,
    # width=50,
    # height=720,
)


barriers.extend([barrier_1, barrier_2, barrier_3, barrier_4, barrier_5])
barriers.extend(
    [vertical_left_barrier_1, vertical_left_barrier_2, vertical_left_barrier_3])
barriers.extend([vertical_right_barrier_1,
                vertical_right_barrier_2, vertical_right_barrier_3])
barriers.append(green)

ball = Ball(
    barriers=barriers,
    image=ball_img,
    screen=screen,
    x=90,
    y=550,
    vx=5,
    vy=-3

)

arrow = Arrow(
    screen=screen,
    ball=ball,
    mouse=mouse_pos
)

game_state = GameState()


# Functions
def draw_screen(game_state):

    # Background
    screen.fill("red")
    screen.blit(source=background, dest=(0, 0))

    # Barriers
    for barrier in barriers:
        barrier.draw()

    if game_state.aiming:
        arrow.draw()

    # Ball
    ball.draw()


def update(mouse_pos, game_state: GameState, ball: Ball):
    mouse_pos = pygame.mouse.get_pos()
    if game_state.aiming:
        arrow.update(mouse_pos[0], mouse_pos[1])
    else:
        ball.update()
        if (abs(ball.vx) + abs(ball.vy)) < 1 and ball.grounded:
            print("Return to aiming")
            game_state.aiming = True


def handle_events(game_state: GameState, arrow: Arrow, ball: Ball):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False

        if game_state.aiming:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("MouseDown")
                convert_mouse_to_power(arrow, ball)
                game_state.aiming = False


def convert_mouse_to_power(arrow: Arrow, ball: Ball):
    power = math.hypot((arrow.start_x - arrow.end_x),
                       (arrow.start_y - arrow.end_y)) / 50
    angle = math.atan2((arrow.end_y - arrow.start_y),
                       (arrow.end_x - arrow.start_x))  # opp / adj

    ball.vy = power * math.sin(angle)
    ball.vx = power * math.cos(angle)
    print("converting arrow to power...")
    print(f"ball.vx = {ball.vx}, ball.vy = {ball.vy}")


def check_for_win(ball: Ball, green: Green, game_state: GameState):
    if game_state.aiming and ball.grounded and (green.rect.left < ball.x < green.rect.right):
        game_state.has_won = True


def handle_win(game_state: GameState):
    if game_state.has_won:
        sys.exit()

# Main loop


while running:
    # print("Aiming = ", game_state.aiming)
    check_for_win(ball, green, game_state)
    handle_win(game_state)
    handle_events(game_state, arrow, ball)
    update(mouse_pos, game_state, ball)
    draw_screen(game_state)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
