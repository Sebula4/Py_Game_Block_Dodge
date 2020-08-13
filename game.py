# ------------------------
# Python Game
# Author: Sebastian Hollabaugh
# Desc: Following Keith Galli YT tutorial
# --------------------------

# ---------------------------------
# Project: Python Chess
# Authors: Sebastian Hollabaugh & Austin Koehler
# Date: 8-12-2020
# Desc: A basic game of chess made in python
# ----------------------------------

import sys
import pygame
import random

pygame.init()

Width = 800
Height = 600

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BACKGROUND_COLOR = (0, 0, 0)

# --------player attributes-------------------------------------------------------------------------------------------------------------

player_size = 50
player_pos = [Width/2, Height-2*player_size]
margin_of_error = .15  # margin of error for hitbox detenction
player_leniency = margin_of_error * player_size  # roughly 5px on each side

# ---------------------------------------------------------------------------------------------------------------------------------------
# --------enemy attributes---------------------------------------------------------------------------------------------------------------

enemy_size = 50
enemy_pos = [random.randint(0, (Width-enemy_size)), 0]
enemy_list = [enemy_pos]
enemy_speed = 10

# ---------------------------------------------------------------------------------------------------------------------------------------
# --------game attributes----------------------------------------------------------------------------------------------------------------

screen = pygame.display.set_mode((Width, Height))
game_over = False
clock = pygame.time.Clock()
score = 0
score_counter = 0
myFont = pygame.font.SysFont("monospace", 35)

# ---------------------------------------------------------------------------------------------------------------------------------------
# --------functions---------------------------------------------------------------------------------------------------------------------


def set_level(score, speed):
    # if score < 20:
    #     speed = 5
    # elif score < 40:
    #     speed = 10
    # elif score < 60:
    #     speed = 15
    # else:
    #     speed = 20
    # return speed
    speed = score/5 + 10
    return speed


def update_scorecounter(score_counter, score):
    if (score + 1) % 10 == 0:
        score_counter = score
    return score_counter


def set_background(BACKGROUND_COLOR, score, score_counter):
    if (score + 1) % 10 == 0 and score_counter != score:
        BACKGROUND_COLOR = (random.randint(0, 220), random.randint(
            0, 255), random.randint(0, 220))
    return BACKGROUND_COLOR


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, Width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(
            screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < Height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    # my code to check for colissions
    if (e_x + enemy_size) >= (p_x + player_leniency) and e_x < (p_x + player_size - player_leniency):
        if (e_y + enemy_size) >= (p_y + player_leniency) and e_y < (p_y + player_size - player_leniency):
            return True

    # video tutorial code to check for colisions
    # if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
    #     if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
    #         return True
    return False

# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------Game Loop---------------------------------------------------------------------------------------------------------------------


while not game_over:

    # set the exit condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # set the player controls
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and player_pos[0] != 0:
            player_pos[0] -= player_size
        elif event.key == pygame.K_RIGHT and player_pos[0] != (Width-player_size):
            player_pos[0] += player_size
        elif event.key == pygame.K_UP and player_pos[1] != 0:
            player_pos[1] -= player_size
        elif event.key == pygame.K_DOWN and player_pos[1] != (Height-player_size):
            player_pos[1] += player_size

    screen.fill(BACKGROUND_COLOR)

    # draw the player rectangle
    pygame.draw.rect(
        screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # draw the enemies
    drop_enemies(enemy_list)
    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(enemy_list)

    enemy_speed = set_level(score, enemy_speed)

    # set the score
    score = update_enemy_positions(enemy_list, score)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, WHITE)
    screen.blit(label, (Width-200, Height-40))

    # update the game and background
    BACKGROUND_COLOR = set_background(BACKGROUND_COLOR, score, score_counter)
    score_counter = update_scorecounter(score_counter, score)
    clock.tick(30)
    pygame.display.update()
# -------------------------------------------------------------------------------------------------------------------------------------------
