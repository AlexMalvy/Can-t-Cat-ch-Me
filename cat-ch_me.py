import pygame
import sys
import time
import random
import os
import sys
import pickle
import math
import img_load
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
ALMOST_BLACK = (1, 1, 1)

### Background

BG_GRAY_WALL = pygame.image.load(os.path.join("assets", "bg_gray_wall.jpg"))

## Cats Sprites

ORANGE_CAT_IDLE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle.png"], 1)
ORANGE_CAT_RUNNING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running.png"], 1)

#############

class general_use_class:
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

general_use = general_use_class()

class camera_class:
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

camera = camera_class()

class player_class:
    body = pygame.Rect(WIDTH//2, HEIGHT//2, 64, 64)
    speed = 10

    moving = False
    right = False

    frame = 0
    frame_timer = pygame.time.get_ticks()
    frame_cd = 120
    state = [ORANGE_CAT_IDLE, ORANGE_CAT_RUNNING]
    current_state = 0
    img = pygame.Surface((body.width, body.height))
    
    def update_visual(self):
        self.change_state()

        self.update_frame()

    def change_state(self):
        if self.moving and self.current_state != 1:
            self.current_state = 1
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        elif self.moving == False and self.current_state != 0:
            self.current_state = 0
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()


    def update_frame(self):
        if pygame.time.get_ticks() - self.frame_timer >= self.frame_cd:
            self.frame += 1
            self.frame_timer = pygame.time.get_ticks()
        if self.frame >= self.state[self.current_state].get_width()/self.state[self.current_state].get_height():
            self.frame = 0

        self.img.fill(ALMOST_BLACK)
        self.img.set_colorkey(ALMOST_BLACK)
        self.img.blit(self.state[self.current_state], (0,0), (self.state[self.current_state].get_height() * self.frame, 0, self.state[self.current_state].get_height(), self.state[self.current_state].get_height()))
        if self.right == False:
            self.img = pygame.transform.flip(self.img, 1, 0)

player = player_class()

class owner_class:
    def __init__(self):
        self.target = player

    body = pygame.Rect(100, 100, 50, 100)
    range = 50
    
    max_speed = 5
    speed = 5
    moving = True

    def move_toward_cat(self):
        if math.dist([self.target.body.centerx, self.target.body.centery], [self.body.centerx, self.body.centery]) > self.range:
            self.moving = True
            # Speed modifier
            if self.body.centerx != self.target.body.centerx and self.body.centery != self.target.body.centery:
                self.speed = self.max_speed/3 * 2
            else:
                self.speed = self.max_speed

            # Chase Target
            if self.target.body.centerx > self.body.centerx:
                    self.body.x += self.speed
                    self.right = True
            if self.target.body.centerx < self.body.centerx:
                    self.body.x -= self.speed
                    self.right = False
                    
            if self.target.body.centery > self.body.centery:
                    self.body.y += self.speed
            if self.target.body.centery < self.body.centery:
                    self.body.y -= self.speed

        else:
            self.moving = False

owner = owner_class()

class obstacle_class:

    wall1 = pygame.Rect(500, 500, 100, 15)
    wall2 = pygame.Rect(500, 500, 15, 100)
    list = [wall1, wall2]


obstacle = obstacle_class()

class animation_class:
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

animation = animation_class()

class main_game_class:

    def draw_window(self):
        camera.bg_blit()

        # animation.play_animations()

        # Obstacles
        for obs in obstacle.list:
            pygame.draw.rect(map, RED, obs)

        # Player (Cat)
        pygame.draw.rect(map, BLACK, player.body)
        map.blit(player.img, (player.body.x, player.body.y))

        # Owner
        pygame.draw.rect(map, YELLOW, owner.body)

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
                player.body.x -= player.speed
                player.right = False
                # Check if colliding with obstacle
                for obs in obstacle.list:
                    if player.body.colliderect(obs):
                        player.body.x += player.speed
            if right:
                player.body.x += player.speed
                player.right = True
                # Check if colliding with obstacle
                for obs in obstacle.list:
                    if player.body.colliderect(obs):
                        player.body.x -= player.speed
            if up:
                player.body.y -= player.speed
                # Check if colliding with obstacle
                for obs in obstacle.list:
                    if player.body.colliderect(obs):
                        player.body.y += player.speed
            if down:
                player.body.y += player.speed
                # Check if colliding with obstacle
                for obs in obstacle.list:
                    if player.body.colliderect(obs):
                        player.body.y -= player.speed

            if left or right or up or down:
                player.moving = True
            else:
                player.moving = False

            owner.move_toward_cat()

            player.update_visual()

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

main = main_game_class()

main.main_loop()


