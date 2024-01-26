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
map = pygame.Surface((2500, 1500))

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

class player:
    body = pygame.Rect(WIDTH//2, HEIGHT//2, 64, 64)
    movespeed = 10

class obstacle_class:

    #Full Map
    topWall = pygame.Rect(0, 0, map.get_width(), 15)
    bottomWall = pygame.Rect(0, map.get_height() - 115, map.get_width(), 15)
    leftWall = pygame.Rect(0, 0, 15, map.get_height()-100)
    rightWall = pygame.Rect(map.get_width() - 15, 0, 15, map.get_height()-100)
    #Bedroom
    bedRoomBottomLeftHalf = pygame.Rect(0, 500, 500, 15)
    bedRoomBottomRightHalf = pygame.Rect(650, 500, 350, 15)
    bedRoomRightTopHalf= pygame.Rect(1000, 0, 15, 200)
    bedRoomRightBottomHalf = pygame.Rect(1000, 315, 15, 200)
    bed = pygame.Rect(200, 10, 120, 180)
    #Bathroom
    bathRoomBottomLeftHalf = pygame.Rect(0, 1000, 400, 15)
    bathRoomBottomRightHalf = pygame.Rect(550, 1000, 300, 15)
    bathRoomRightTopHalf= pygame.Rect(850, 500, 15, 200)
    bathRoomRightBottomHalf = pygame.Rect(850, 815, 15, 200)
    toilets = pygame.Rect(15, 700, 75, 75)
    shower = pygame.Rect(750, 515, 100, 100)
    #Hallway
    halwayRightTopHalf = pygame.Rect(850, 1015, 15, 200)
    halwayRightBottomHalf = pygame.Rect(850, 1300, 15, 100)
    shoeCase = pygame.Rect(15, map.get_height() - 165, 100, 50)
    #Living Room
    couch = pygame.Rect(1200, 850, 250, 100)
    tv = pygame.Rect(1275, map.get_height()-190, 150, 75)
    library = pygame.Rect(map.get_width()-115, 550, 100, 300)
    #Office
    officeLeftBottomHalf = pygame.Rect(map.get_width()-800, map.get_height()-600 , 400, 15)
    officeRightBottomHalf = pygame.Rect(map.get_width()-250, map.get_height()-600 , 250, 15)
    officeTopLeftHalf= pygame.Rect(map.get_width()-800, map.get_height()-600 , 15, 200)
    officeTopRightHalf = pygame.Rect(map.get_width()-800, map.get_height()-300 , 15, 200)
    desk = pygame.Rect(map.get_width()-600, map.get_height()-250, 350, 150)
    #Kitchen
    kitchenBottom = pygame.Rect(map.get_width()-800, map.get_height()-1000 , 800, 15)
    table = pygame.Rect(map.get_width()-900, map.get_height()-1300, 300, 150)
    oven= pygame.Rect(map.get_width()-165, 15, 150, 150)
    fridge= pygame.Rect(map.get_width()-450, 15, 150, 100)
    trashcan= pygame.Rect(map.get_width()-250, 15, 50, 50)
  
    kitchen= [kitchenBottom,table, oven, fridge, trashcan]
    office= [officeLeftBottomHalf, officeRightBottomHalf, officeTopLeftHalf, officeTopRightHalf, desk]
    livingRoom = [couch, tv, library]
    halway= [halwayRightTopHalf, halwayRightBottomHalf, shoeCase]
    bathRoom= [toilets, shower, bathRoomBottomLeftHalf, bathRoomBottomRightHalf, bathRoomRightTopHalf, bathRoomRightBottomHalf]
    bedRoom = [bed, bedRoomBottomLeftHalf, bedRoomBottomRightHalf, bedRoomRightTopHalf, bedRoomRightBottomHalf]
    fullMap = [topWall, bottomWall, leftWall, rightWall]
    list = [fullMap, bedRoom, bathRoom, livingRoom, halway, office, kitchen]

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

        pygame.draw.rect(map, BLACK, player.body)
        for room in obstacle.list:
            for obs in room:
                pygame.draw.rect(map, RED, obs)

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
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.x += player.movespeed
            if right:
                player.body.x += player.movespeed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.x -= player.movespeed
            if up:
                player.body.y -= player.movespeed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.y += player.movespeed
            if down:
                player.body.y += player.movespeed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
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

main = main_game_class()

main.main_loop()


