import pygame
import sys
import time
import random
import os
import sys
import pickle
import math
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Can't cat-ch me !")
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
map = pygame.Surface((2000, 2000))

WIDTH, HEIGHT = screen.get_width(), screen.get_height()

clock = pygame.time.Clock()

#############

### Font

font = pygame.font.SysFont("sherif", 40)

### Colors

RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
YELLOW = (255,235,42)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GRAYISH = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 128, 0)
BROWN = (83, 61, 50)

### Colors

BG_GRAY_WALL = pygame.image.load(os.path.join("assets", "bg_gray_wall.jpg"))

#############

class general_use:
    background_color = WHITE

    def display_background(self):
        screen.fill(self.background_color)

    def close_the_game(self):
        pygame.quit()
        sys.exit()

    def middle_coordinate_x(self, item):
        x = WIDTH//2 - item.get_width()//2
        return x
    
    def middle_coordinate_y(self, item):
        y = HEIGHT//2 - item.get_height()//2
        return y

general_use = general_use()

class camera:
    bg = pygame.transform.scale(BG_GRAY_WALL, (map.get_width(), map.get_height()))
    # bg = pygame.Surface((map.get_width(), map.get_height()))
    # bg.fill(GRAY)
    def bg_blit(self):
        map.blit(self.bg, (0,0))

    camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

    def update(self):
        self.camera_rect.x = player.body.centerx - WIDTH/2
        if self.camera_rect.x < 0:
            self.camera_rect.x = 0
        if self.camera_rect.right > map.get_width():
            self.camera_rect.right = map.get_width()
        self.camera_rect.y = player.body.centery - HEIGHT/2
        if self.camera_rect.y < 0:
            self.camera_rect.y = 0
        if self.camera_rect.bottom > map.get_height():
            self.camera_rect.bottom = map.get_height()
        screen.blit(map, (0,0), self.camera_rect)

camera = camera()

class player:
    body = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)
    movespeed = 10

class obstacle:
    list = []
    obs_wall1 = pygame.Rect(500, 500, 100, 50)

    def all_obstacle(self):
        temp = dir(self)


obstacle = obstacle()

class animation:
    list = []

    def note_hit_animation(self, note):
        anim = {"type" : "note hit", "rect" : note["rect"], "frame" : 0, "max_frame" : 12}
        animation.list.append(anim)

    def play_animations(self):
        to_be_removed = []
        for item in self.list:
            if item["type"] == "note hit":
                pygame.draw.circle(screen, DARK_RED, item["rect"].center, 15 + int(5 * (item["frame"] / item["max_frame"])))
            
            item["frame"] += 1
            if item["frame"] >= item["max_frame"]:
                to_be_removed.append(item)

        for item in to_be_removed:
            self.list.remove(item)

animation = animation()

class main_game:

    def draw_window(self):
        camera.bg_blit()

        # animation.play_animations()

        pygame.draw.rect(map, BLACK, player.body)
        pygame.draw.rect(map, RED, obstacle.wall1)

        camera.update()

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        click = False
        while run:
            clock.tick(60)

            if left:
                player.body.x -= player.movespeed
                # Check if colliding with obstacle
                if player.body.colliderect(obstacle.wall1):
                    player.body.x += player.movespeed
            if right:
                player.body.x += player.movespeed
                # Check if colliding with obstacle
                if player.body.colliderect(obstacle.wall1):
                    player.body.x -= player.movespeed
            if up:
                player.body.y -= player.movespeed
                # Check if colliding with obstacle
                if player.body.colliderect(obstacle.wall1):
                    player.body.y += player.movespeed
            if down:
                player.body.y += player.movespeed
                # Check if colliding with obstacle
                if player.body.colliderect(obstacle.wall1):
                    player.body.y -= player.movespeed


            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    general_use.close_the_game()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                        general_use.close_the_game()
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_z:
                        up = True
                    if event.key == K_s:
                        down = True
                if event.type == KEYUP:
                    if event.key == K_q:
                        left = False
                    if event.key == K_d:
                        right = False
                    if event.key == K_z:
                        up = False
                    if event.key == K_s:
                        down = False
            self.draw_window()

main = main_game()

main.main_loop()


