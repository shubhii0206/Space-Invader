import pygame
import math
from pygame import mixer
import random

pygame.init()  # initialise pygame

screen = pygame.display.set_mode((800, 600))  # create screen

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background_img = pygame.image.load('space_background.jpg')
background = pygame.transform.scale(background_img, (800, 600))
mixer.music.load("background.wav")
mixer.music.play(-1)

player_image1 = pygame.image.load('ufo1.png')
player_image = pygame.transform.scale(player_image1, (52, 52))
player_X, player_Y = 380, 470
player_X_change = 0

enemy1 = pygame.image.load('invader.png')
enemy_img = pygame.transform.scale(enemy1, (52, 52))

enemy_list, enemy_X, enemy_Y, enemy_X_change, enemy_Y_change, number_of_enemies = [], [], [], [], [], 6
for i in range(number_of_enemies):
    enemy_list.append(enemy_img)
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_change.append(0.5)
    enemy_Y_change.append(20)

bullet1 = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet1, (32, 32))
bullet_X, bullet_Y = 0, 480
bullet_X_change, bullet_Y_change = 0, 5
bullet_state = "ready"

score_value = 0
text_X, text_Y = 10, 10
font = pygame.font.Font("freesansbold.ttf", 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 124)


def display_score_on_screen(x, y, score_value):
    score = font.render("Score: " + str(score_value), True, (0, 180, 30))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_list[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def collison(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt(math.pow((enemy_X - bullet_X), 2) + math.pow((enemy_Y - bullet_Y), 2))
    return distance < 27


def game_over_text():
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    game_over = font.render("GAME OVER HARSH BRO!", True, (255, 255, 255))
    screen.blit(game_over, (230, 280))


running = True

while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_X_change = -3
            if event.key == pygame.K_RIGHT:
                player_X_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bullet_X = player_X
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_X_change = 0

    player_X += player_X_change

    if player_X <= 0:
        player_X = 0
    if player_X > 736:
        player_X = 736

    for i in range(number_of_enemies):
        if enemy_Y[i] > 300:
            for j in range(number_of_enemies):
                enemy_Y[j] = 2000
            game_over_text()
            break
        enemy_X[i] += enemy_X_change[i]
        if enemy_X[i] <= 0:
            enemy_X_change[i] = 2
            enemy_Y[i] += enemy_Y_change[i]
        if enemy_X[i] > 736:
            enemy_X_change[i] = -2
            enemy_Y[i] += enemy_Y_change[i]

        if collison(enemy_Y[i], enemy_X[i], bullet_X, bullet_Y):
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bullet_Y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_X[i], enemy_Y[i] = random.randint(0, 736), random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)

    if bullet_Y < 20:
        bullet_Y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change

    player(player_X, player_Y)
    display_score_on_screen(text_X, text_Y, score_value)

    pygame.display.update()
pygame.quit()
