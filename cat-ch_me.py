import pygame
import sys
import time
import random
import os
import sys
import pickle
import math
import img_load
import maze_solver
import threading
import video
from copy import deepcopy
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Can't cat-ch me !")
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
SQUARE = 60
map = pygame.Surface((42*SQUARE, 29*SQUARE))


WIDTH, HEIGHT = screen.get_width(), screen.get_height()

clock = pygame.time.Clock()

#############

### Font

font = pygame.font.SysFont("sherif", 40)
small_font = pygame.font.SysFont("sherif", 10)

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

### Cats Sprites
## Orange
# Normal
ORANGE_CAT_IDLE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle.png"], 3)
ORANGE_CAT_WALKING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-walking.png"], 3)
ORANGE_CAT_RUNNING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running.png"], 3)
ORANGE_CAT_SCRATCHING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-scratching.png"], 3)

ORANGE_CAT_LICKING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-licking.png"], 3)
ORANGE_CAT_LOAF_BREAD = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-loaf-bread.png"], 3)

# Potte
ORANGE_CAT_IDLE_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle-potte.png"], 3)
ORANGE_CAT_WALKING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-walking-potte.png"], 3)
ORANGE_CAT_RUNNING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running-potte.png"], 3)
ORANGE_CAT_SCRATCHING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-scratching-potte.png"], 3)

ORANGE_CAT_LICKING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-licking-potte.png"], 3)
ORANGE_CAT_LOAF_BREAD_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-loaf-bread-potte.png"], 3)

# Nyan
ORANGE_CAT_IDLE_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle-nyan.png"], 3)
ORANGE_CAT_WALKING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-walking-nyan.png"], 3)
ORANGE_CAT_RUNNING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running-nyan.png"], 3)
ORANGE_CAT_SCRATCHING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-scratching-nyan.png"], 3)

ORANGE_CAT_LICKING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-licking-nyan.png"], 3)

## Black
# Normal
BLACK_CAT_IDLE = img_load.image_loader.load(["assets", "black-cat", "black-cat-idle.png"], 3)
BLACK_CAT_WALKING = img_load.image_loader.load(["assets", "black-cat", "black-cat-walking.png"], 3)
BLACK_CAT_RUNNING = img_load.image_loader.load(["assets", "black-cat", "black-cat-running.png"], 3)
BLACK_CAT_SCRATCHING = img_load.image_loader.load(["assets", "black-cat", "black-cat-scratching.png"], 3)

BLACK_CAT_LICKING = img_load.image_loader.load(["assets", "black-cat", "black-cat-licking.png"], 3)
BLACK_CAT_LOAF_BREAD = img_load.image_loader.load(["assets", "black-cat", "black-cat-loaf-bread.png"], 3)

# Potte
BLACK_CAT_IDLE_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-idle-potte.png"], 3)
BLACK_CAT_WALKING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-walking-potte.png"], 3)
BLACK_CAT_RUNNING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-running-potte.png"], 3)
BLACK_CAT_SCRATCHING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-scratching-potte.png"], 3)

BLACK_CAT_LICKING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-licking-potte.png"], 3)
BLACK_CAT_LOAF_BREAD_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-loaf-bread-potte.png"], 3)

# Nyan
BLACK_CAT_IDLE_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-idle-nyan.png"], 3)
BLACK_CAT_WALKING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-walking-nyan.png"], 3)
BLACK_CAT_RUNNING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-running-nyan.png"], 3)
BLACK_CAT_SCRATCHING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-scratching-nyan.png"], 3)

BLACK_CAT_LICKING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-licking-nyan.png"], 3)

## Orange
# Normal
SIAMESE_CAT_IDLE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-idle.png"], 3)
SIAMESE_CAT_WALKING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-walking.png"], 3)
SIAMESE_CAT_RUNNING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-running.png"], 3)
SIAMESE_CAT_SCRATCHING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-scratching.png"], 3)

SIAMESE_CAT_LICKING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-licking.png"], 3)
SIAMESE_CAT_LOAF_BREAD = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-loaf-bread.png"], 3)

# Potte
SIAMESE_CAT_IDLE_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-idle-potte.png"], 3)
SIAMESE_CAT_WALKING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-walking-potte.png"], 3)
SIAMESE_CAT_RUNNING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-running-potte.png"], 3)
SIAMESE_CAT_SCRATCHING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-scratching-potte.png"], 3)

SIAMESE_CAT_LICKING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-licking-potte.png"], 3)
SIAMESE_CAT_LOAF_BREAD_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-loaf-bread-potte.png"], 3)

# Nyan
SIAMESE_CAT_IDLE_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-idle-nyan.png"], 3)
SIAMESE_CAT_WALKING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-walking-nyan.png"], 3)
SIAMESE_CAT_RUNNING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-running-nyan.png"], 3)
SIAMESE_CAT_SCRATCHING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-scratching-nyan.png"], 3)

SIAMESE_CAT_LICKING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-licking-nyan.png"], 3)

## Buttons

BACK_BUTTON = pygame.Rect(10, HEIGHT - 60, 100, 50)
NEXT_BUTTON = pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 50)

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


class music_class:
    def play_music():
        pygame.mixer.music.load(os.path.join('Assets', os.path.join("music", "main_theme.mp3")))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()


class camera_class:
    bg = pygame.transform.scale(BG_GRAY_WALL, (map.get_width(), map.get_height()))
    # bg = pygame.Surface((map.get_width(), map.get_height()))
    # bg.fill(GRAY)
    def bg_blit(self):
        map.blit(self.bg, (0,0))

    camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

    def update(self):
        self.camera_rect.x = player.hitbox.centerx - WIDTH/2
        if self.camera_rect.x < 0:
            self.camera_rect.x = 0
        if self.camera_rect.right > map.get_width():
            self.camera_rect.right = map.get_width()
        self.camera_rect.y = player.hitbox.centery - HEIGHT/2
        if self.camera_rect.y < 0:
            self.camera_rect.y = 0
        if self.camera_rect.bottom > map.get_height():
            self.camera_rect.bottom = map.get_height()
        screen.blit(map, (0,0), self.camera_rect)

class game_variable_class:
    score = 0
    multiplier = 1

    all_cats = ["orange", "black", "siamese"]
    selected_cat = "orange"
    
    all_owners = ["owner M", "owner F"]
    selected_owner = "owner M"

    def reset_all_variable(self):
        self.score = 0
        self.multiplier = 1
        player.hp = 3
        player.hitbox.x = SQUARE*18
        player.hitbox.y = SQUARE*18
        owner.body_hitbox.x = 1200
        owner.body_hitbox.y = 600

def redefineMaze(oldMaze):
    oldMazeLen = len(oldMaze)
    row = []
    newMaze = []
    for x in oldMaze:
        x.reverse()
    for i in range(0, (len(oldMaze[0]))):
        for x in oldMaze:
            row.append(x[-1])
            del(x[-1])
            if(len(row) == oldMazeLen):
                newMaze.append(row)
                row = []
    return newMaze

class player_class:
    body = pygame.Rect(SQUARE*18, SQUARE*18, 192, 192)

    base_speed = 8
    bonus_speed = 0
    speed = 8
    hp = 3
    hitbox = pygame.Rect(body.x, body.bottom, 60, 60)

    moving = False
    right = False

    caught = False

    i_frame = False
    i_frame_timer = 0
    i_frame_duration = 2

    miaou_cd = 5
    miaou_timer = 0


    frame = 0
    frame_timer = pygame.time.get_ticks()
    frame_cd = 120
    state = [ORANGE_CAT_IDLE, ORANGE_CAT_WALKING, ORANGE_CAT_RUNNING]
    current_state = 0

    idle_bis = False
    idle_bis_counter = 0
    idle_bis_state = 0
    idle_bis_list = [ORANGE_CAT_LICKING]

    potte = False
    state_potte = [ORANGE_CAT_IDLE_POTTE, ORANGE_CAT_WALKING_POTTE, ORANGE_CAT_RUNNING_POTTE]
    state_potte_idle_bis = [ORANGE_CAT_LICKING_POTTE]

    nyan = False
    state_nyan = [ORANGE_CAT_IDLE_NYAN, ORANGE_CAT_WALKING_NYAN, ORANGE_CAT_RUNNING_NYAN]
    state_nyan_idle_bis = [ORANGE_CAT_LICKING_NYAN]

    img = pygame.Surface((body.width, body.height))
    
    def update(self):
        self.align_body()

        self.change_state()

        self.update_frame()

        self.apply_bonuses()


    def apply_bonuses(self):
        self.bonus_speed = 0
        if self.i_frame:
            self.bonus_speed += 5

        self.speed = self.base_speed + self.bonus_speed


    def change_state(self):
        if self.moving and interactible.interact_timer and self.current_state != 3:
            self.current_state = 2
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
            self.idle_bis = False
            self.idle_bis_counter = 0
        if self.moving and self.i_frame and self.current_state != 2:
            self.current_state = 2
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
            self.idle_bis = False
            self.idle_bis_counter = 0
        if self.moving and not self.i_frame and self.current_state != 1:
            self.current_state = 1
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
            self.idle_bis = False
            self.idle_bis_counter = 0
        elif self.moving == False and self.current_state != 0:
            self.current_state = 0
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        elif self.moving == False and self.current_state == 0 and self.idle_bis_counter == 3:
            self.idle_bis_counter = 0
            self.idle_bis = True
            # self.idle_bis_state = random.randint(0, 1)
            self.idle_bis_state = 0

    def update_frame(self):
        # Get the correct img slate
        if self.potte:
            if self.idle_bis:
                state = self.state_potte_idle_bis
                current_state = self.idle_bis_state
            else:
                state = self.state_potte
                current_state = self.current_state
        elif self.nyan:
            if self.idle_bis:
                state = self.state_nyan_idle_bis
                current_state = self.idle_bis_state
            else:
                state = self.state_nyan
                current_state = self.current_state
        else:
            if self.idle_bis:
                state = self.idle_bis_list
                current_state = self.idle_bis_state
            else:
                state = self.state
                current_state = self.current_state

        if pygame.time.get_ticks() - self.frame_timer >= self.frame_cd:
            self.frame += 1
            self.frame_timer = pygame.time.get_ticks()
        if self.frame >= state[current_state].get_width()/state[current_state].get_height():
            self.frame = 0

            if self.current_state == 0:
                if self.idle_bis:
                    self.idle_bis = False
                else:
                    self.idle_bis_counter += 1

        self.img.fill(ALMOST_BLACK)
        self.img.set_colorkey(ALMOST_BLACK)
        self.img.blit(state[current_state], (0,0), (state[current_state].get_height() * self.frame, 0, state[current_state].get_height(), state[current_state].get_height()))
        if self.right == False:
            self.img = pygame.transform.flip(self.img, 1, 0)

    def align_body(self):
        self.body.centerx = self.hitbox.centerx
        self.body.centery = self.hitbox.centery

    def change_cat_skin(self):
        if game_variable.selected_cat == "orange":
            self.state = [ORANGE_CAT_IDLE, ORANGE_CAT_WALKING, ORANGE_CAT_RUNNING]
            self.idle_bis_list = [ORANGE_CAT_LICKING]
            self.state_potte = [ORANGE_CAT_IDLE_POTTE, ORANGE_CAT_WALKING_POTTE, ORANGE_CAT_RUNNING_POTTE]
            self.state_potte_idle_bis = [ORANGE_CAT_LICKING_POTTE]
            self.state_nyan = [ORANGE_CAT_IDLE_NYAN, ORANGE_CAT_WALKING_NYAN, ORANGE_CAT_RUNNING_NYAN]
            self.state_nyan_idle_bis = [ORANGE_CAT_LICKING_NYAN]
        elif game_variable.selected_cat == "black":
            self.state = [BLACK_CAT_IDLE, BLACK_CAT_WALKING, BLACK_CAT_RUNNING]
            self.idle_bis_list = [BLACK_CAT_LICKING]
            self.state_potte = [BLACK_CAT_IDLE_POTTE, BLACK_CAT_WALKING_POTTE, BLACK_CAT_RUNNING_POTTE]
            self.state_potte_idle_bis = [BLACK_CAT_LICKING_POTTE]
            self.state_nyan = [BLACK_CAT_IDLE_NYAN, BLACK_CAT_WALKING_NYAN, BLACK_CAT_RUNNING_NYAN]
            self.state_nyan_idle_bis = [BLACK_CAT_LICKING_NYAN]
        elif game_variable.selected_cat == "siamese":
            self.state = [SIAMESE_CAT_IDLE, SIAMESE_CAT_WALKING, SIAMESE_CAT_RUNNING]
            self.idle_bis_list = [SIAMESE_CAT_LICKING]
            self.state_potte = [SIAMESE_CAT_IDLE_POTTE, SIAMESE_CAT_WALKING_POTTE, SIAMESE_CAT_RUNNING_POTTE]
            self.state_potte_idle_bis = [SIAMESE_CAT_LICKING_POTTE]
            self.state_nyan = [SIAMESE_CAT_IDLE_NYAN, SIAMESE_CAT_WALKING_NYAN, SIAMESE_CAT_RUNNING_NYAN]
            self.state_nyan_idle_bis = [SIAMESE_CAT_LICKING_NYAN]
        # Default Skin
        else:
            self.state = [ORANGE_CAT_IDLE, ORANGE_CAT_WALKING]
            self.idle_bis_list = [ORANGE_CAT_LICKING]
            self.state_potte = [ORANGE_CAT_IDLE_POTTE, ORANGE_CAT_WALKING_POTTE]
            self.state_potte_idle_bis = [ORANGE_CAT_LICKING_POTTE]
            self.state_nyan = [ORANGE_CAT_IDLE_NYAN, ORANGE_CAT_WALKING_NYAN]
            self.state_nyan_idle_bis = [ORANGE_CAT_LICKING_NYAN]


class owner_class:
    
    range = 20
    rage = 0
    max_rage = 100
    body = pygame.Rect(1200, 600, SQUARE, SQUARE*2)
    body_hitbox = pygame.Rect(body.x, body.y, SQUARE, SQUARE)
    
    max_speed = 5
    speed = 5
    max_bonus_speed = 15
    bonus_speed = 0
    moving = True

    target = None
    path = []

    last_rage_deduction_time = time.time()
    

    def update(self):
        # self.move_toward_cat()

        self.update_move_speed()

        # Mettez à jour la position de la hitbox
        self.body.x= self.body_hitbox.x
        self.body.bottom = self.body_hitbox.bottom  

    def move_toward_cat(self):
        # print(self.path)
        if self.target != None:
            if math.dist([self.target[0], self.target[1]], [self.body_hitbox.centerx, self.body_hitbox.centery]) > self.range:
                self.moving = True
                # Speed modifier
                self.speed = self.max_speed + self.bonus_speed

                # Chase Target
                if self.target[0] > self.body_hitbox.centerx:
                        self.body_hitbox.x += self.speed
                        self.right = True
                if self.target[0] < self.body_hitbox.centerx:
                        self.body_hitbox.x -= self.speed
                        self.right = False
                        
                if self.target[1] > self.body_hitbox.centery:
                        self.body_hitbox.y += self.speed
                if self.target[1] < self.body_hitbox.centery:
                        self.body_hitbox.y -= self.speed
            else:
                self.path.pop(0)
                if len(self.path) > 0:
                    self.target = self.path[0]
                else:
                    self.target = None
        else:
            self.moving = False

    def add_rage(self, amount):
        self.rage += amount

    def remove_rage(self, amount):
        current_time = time.time()
        time_elapsed = current_time - self.last_rage_deduction_time

        # Deduct 1 from rage every 5 seconds
        if time_elapsed >= 5 and self.rage > 0:
            self.rage -= amount
            self.last_rage_deduction_time = current_time

    def update_move_speed(self):
        self.bonus_speed = self.max_bonus_speed * (self.rage / self.max_rage)


class obstacle_class:

    #Full Map
    topWall = pygame.Rect(0, 0, map.get_width(), SQUARE*5)
    bottomWall = pygame.Rect(0, map.get_height() - SQUARE*2, map.get_width(), SQUARE)
    leftWall = pygame.Rect(0, SQUARE*4, 60, map.get_height()-SQUARE*2)
    rightWall = pygame.Rect(map.get_width() - SQUARE, SQUARE*4, SQUARE, map.get_height()-SQUARE*2)
    #Bedroom
    bedRoomBottomLeftHalf = pygame.Rect(SQUARE, SQUARE*12, SQUARE*6, SQUARE)
    bedRoomBottomRightHalf = pygame.Rect(SQUARE*11, SQUARE*12, SQUARE*6, SQUARE)
    bedRoomRightTopHalf= pygame.Rect(SQUARE*16, SQUARE*4, SQUARE, SQUARE*2)
    bedRoomRightBottomHalf = pygame.Rect(SQUARE*16, SQUARE*10, SQUARE, SQUARE*2)
    bed = pygame.Rect(SQUARE*5, SQUARE*6, SQUARE*4, SQUARE*4)
    nightStandBedroom = pygame.Rect(SQUARE*10, SQUARE*6, SQUARE, SQUARE)
    #Bathroom
    bathRoomBottomLeftHalf = pygame.Rect(0, SQUARE*20, SQUARE*7, SQUARE)
    bathRoomBottomRightHalf = pygame.Rect(SQUARE*9, SQUARE*20, SQUARE*6, SQUARE)
    bathRoomRightTopHalf= pygame.Rect(SQUARE*14, SQUARE*12, SQUARE, SQUARE*3)
    bathRoomRightBottomHalf = pygame.Rect(SQUARE*14, SQUARE*17, SQUARE, SQUARE*3)
    toiletsBathroom = pygame.Rect(SQUARE, SQUARE*15, SQUARE, SQUARE)
    showerBathroom = pygame.Rect(SQUARE*12, SQUARE*12, SQUARE*2, SQUARE*2)
    #Hallway
    halwayRightTopHalf = pygame.Rect(SQUARE*14, SQUARE*20, SQUARE, SQUARE*3)
    halwayRightBottomHalf = pygame.Rect(SQUARE*14, SQUARE*25, SQUARE, SQUARE*2)
    shoeCaseHallway = pygame.Rect(SQUARE, map.get_height() - SQUARE*3, SQUARE*6, SQUARE)
    #Living Room
    couchLivingRoom = pygame.Rect(SQUARE*20, SQUARE*18, SQUARE*4, SQUARE*2)
    tvLivingRoom = pygame.Rect(SQUARE*21, map.get_height()-SQUARE*3, SQUARE*2, SQUARE*2)
    libraryLivingRoom = pygame.Rect(map.get_width()-SQUARE*2, SQUARE*15, SQUARE*2, SQUARE*3)
    plantLivingRoom = pygame.Rect(SQUARE*15, map.get_height()-SQUARE*3, SQUARE, SQUARE)
    #Office
    officeTopLeftHalf = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*10 , SQUARE*6, SQUARE)
    officeTopRightHalf = pygame.Rect(map.get_width()-SQUARE*3, map.get_height()-SQUARE*10 , SQUARE*3, SQUARE)
    officeLeftTopHalf= pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*10 , SQUARE, SQUARE*2)
    officeLeftBottomHalf = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*4 , SQUARE, SQUARE*2)
    desk = pygame.Rect(map.get_width()-SQUARE*10, map.get_height()-SQUARE*4, SQUARE*6, SQUARE*2)
    #Kitchen
    kitchenBottom = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*16 , SQUARE*13, SQUARE)
    table = pygame.Rect(map.get_width()-SQUARE*15, map.get_height()-SQUARE*22, SQUARE*5, SQUARE*3)
    chairKitchen1 = pygame.Rect(map.get_width()-SQUARE*16, map.get_height()-SQUARE*21, SQUARE, SQUARE)
    chairKitchen2 = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*19, SQUARE, SQUARE)
    chairKitchen3 = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*23, SQUARE, SQUARE)
    oven= pygame.Rect(map.get_width()-SQUARE*3, SQUARE*5, SQUARE*2, SQUARE*2)
    fridge= pygame.Rect(map.get_width()-SQUARE*8, SQUARE*5, SQUARE*2, SQUARE*2)
    trashCanKitchen= pygame.Rect(map.get_width()-SQUARE*5, SQUARE*5, SQUARE, SQUARE)
  
    kitchen= [kitchenBottom,table, oven, fridge, trashCanKitchen, chairKitchen1, chairKitchen2]
    office= [officeLeftBottomHalf, officeLeftTopHalf, officeTopLeftHalf, officeTopRightHalf, desk]
    livingRoom = [couchLivingRoom, tvLivingRoom, libraryLivingRoom]
    hallWay= [halwayRightTopHalf, halwayRightBottomHalf, shoeCaseHallway, plantLivingRoom]
    bathRoom= [toiletsBathroom, showerBathroom, bathRoomBottomLeftHalf, bathRoomBottomRightHalf, bathRoomRightTopHalf, bathRoomRightBottomHalf]
    bedRoom = [bedRoomBottomLeftHalf, bedRoomBottomRightHalf, bedRoomRightTopHalf,bed, bedRoomRightBottomHalf, nightStandBedroom]
    fullMap = [topWall, bottomWall, leftWall, rightWall]
    list = [fullMap, bedRoom, bathRoom, hallWay, livingRoom, office, kitchen]


class interactible_class():
    type_chair = {"score" : 100, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5, "rage_amount" : 5}
    type_couch = {"score" : 200, "multiplier" : 0.3, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10, "rage_amount" : 10}
    type_trashCan = {"score" : 400, "multiplier" : 0.4, "duration" : 4, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 15, "rage_amount" : 15}
    type_library = {"score" : 1000, "multiplier" : 0.5, "duration" : 5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 20, "rage_amount" : 20}
    type_plug = {"score" : 300, "multiplier" : 0.3, "duration" : 3, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10, "rage_amount" : 5}
    type_plugOffice = {"score" : 1000, "multiplier" : 0.5, "duration" : 5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 30, "rage_amount" : 50}
    type_shoeCase = {"score" : 500, "multiplier" : 0.5, "duration" : 5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 15, "rage_amount" : 25}
    type_toilets = {"score" : 200, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5, "rage_amount" : 5}
    type_shower = {"score" : 300, "multiplier" : 0.3, "duration" : 3, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10, "rage_amount" : 10}
    type_plant = {"score" : 1000, "multiplier" : 0.5, "duration" : 1, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 20, "rage_amount" : 20}
    type_Rug = {"score" : 100, "multiplier" : 0.2, "duration" : 1, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3, "rage_amount" : 5}


    chair =  {"rect" : pygame.Rect(map.get_width()-SQUARE*17, map.get_height()-SQUARE*22, SQUARE*2, SQUARE*3), "type" : type_chair.copy()}
    chair2 = {"rect" : pygame.Rect(map.get_width()-SQUARE*14, map.get_height()-SQUARE*19, SQUARE*3, SQUARE*2), "type" : type_chair.copy()}
    couch =  {"rect" : pygame.Rect(map.get_width()-SQUARE*23, map.get_height()-SQUARE*12, SQUARE*6, SQUARE*3), "type" : type_couch.copy()}
    trash =  {"rect" : pygame.Rect(map.get_width()-SQUARE*6, SQUARE, SQUARE*3, SQUARE*2), "type" : type_trashCan.copy()}
    tvPlug =  {"rect" : pygame.Rect(map.get_width()-SQUARE*19, map.get_height()-SQUARE*3, SQUARE*3, SQUARE*1), "type" : type_plug.copy()}
    library =  {"rect" : pygame.Rect(map.get_width()-SQUARE*3, SQUARE*10, SQUARE*2, SQUARE*5), "type" : type_library.copy()}
    shoeCase =  {"rect" : pygame.Rect(SQUARE, map.get_height()-SQUARE*4, SQUARE*7, SQUARE*2), "type" : type_shoeCase.copy()}
    shower = {"rect" : pygame.Rect(SQUARE*11, SQUARE*8, SQUARE*3, SQUARE*3), "type" : type_shower.copy()}
    toilets= {"rect" : pygame.Rect(SQUARE, SQUARE*10, SQUARE*2, SQUARE*3), "type" : type_toilets.copy()}
    plant= {"rect" : pygame.Rect(SQUARE*15, map.get_height()-SQUARE*4, SQUARE*2, SQUARE*2), "type" : type_plant.copy()}
    officePlug = {"rect" : pygame.Rect(map.get_width()-SQUARE*4, map.get_height()-SQUARE*4, SQUARE*3, SQUARE*2), "type" : type_plugOffice.copy()}
    rug= {"rect" : pygame.Rect(map.get_width()-SQUARE*22, map.get_height()-SQUARE*8, SQUARE*4, SQUARE*4), "type" : type_Rug.copy()}
    nightStandPlug = {"rect" : pygame.Rect(SQUARE*10, SQUARE, SQUARE*5, SQUARE*2), "type" : type_plug.copy()}


    


    # list = [chair, chair2, couch, tvPlug, library, shoeCase, shower, officePlug, rug, nightStandPlug]
    list=[]

    isOn = None
    interact_timer = None
    
    PROGRESS_BAR = pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//3 * 2 + 150, 200, 25)
    PROGRESS_BAR_FILL = pygame.Rect(PROGRESS_BAR.x + 1, PROGRESS_BAR.y + 1, 0, PROGRESS_BAR.height - 2)

    def update(self):
        self.isOnInteractible()
        self.restore_interactibles()

    def isOnInteractible(self):
        for item in self.list:
            if item["rect"].collidepoint(player.hitbox.center) and item["type"]["is_enabled"]:
                self.isOn = item
                return
        
        self.isOn = None

    def interact(self):
        if self.isOn:
            if self.interact_timer == None:
                self.interact_timer = time.time()
            elif time.time() - self.interact_timer > self.isOn["type"]["duration"]:
                game_variable.score += int(self.isOn["type"]["score"] * game_variable.multiplier)
                game_variable.multiplier += self.isOn["type"]["multiplier"]
                index = self.list.index(self.isOn)
                self.list[index]["type"]["is_enabled"] = False
                self.list[index]["type"]["disabled_timer"] = time.time()
                self.interact_timer = None
                owner.add_rage(self.list[index]["type"]["rage_amount"])

            self.update_progress_bar()

    def cancel_interact(self):
        self.interact_timer = None

    def update_progress_bar(self):
        if self.interact_timer:
            self.PROGRESS_BAR_FILL.width = (self.PROGRESS_BAR.width - 2) * (1 - (time.time() - self.interact_timer) / self.isOn["type"]["duration"])

    def restore_interactibles(self):
        for item in self.list:
            if not item["type"]["is_enabled"]:
                if time.time() - item["type"]["disabled_timer"] > item["type"]["disabled_duration"]:
                    item["type"]["disabled_timer"] = None
                    item["type"]["is_enabled"] = True


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


class grid_class:
    def __init__(self):
        self.initialGrid()
        self.get_cat_position()
        self.get_owner_position()

    grid = []
    maze = []
    cat_position = None
    owner_position = None

    

    def update(self):
        self.get_cat_position()
        self.get_owner_position()

        # if time.time() - self.solver_timer > self.solver_cd:
        #     pathfinder.create_path()

    def initialGrid(self):
        blockSize = SQUARE #Set the size of the grid block
        id = 1
        pos_x = 0
        pos_y = 0
        y_list = []
        maze_y_list = []
        for x in range(0, map.get_width() , blockSize):
            for y in range(0, map.get_height() , blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                # Check if obstacle
                for room in obstacle.list:
                    if rect.collidelist(room) == -1:
                        rect_info = {"id" : id, "pos_x" : pos_x, "pos_y" : pos_y,"rect" : rect, "obstacle" : 1}
                        # rect_info = 0
                    else:
                        rect_info = {"id" : id, "pos_x" : pos_x, "pos_y" : pos_y,"rect" : rect, "obstacle" : 0}
                        # rect_info = 1
                        break

                y_list.append(rect_info)
                maze_y_list.append(rect_info["obstacle"])
                id += 1
                pos_y += 1
            pos_x += 1
            pos_y = 0
            self.grid.append(y_list)
            y_list = []
            self.maze.append(maze_y_list)
            maze_y_list = []

    def get_cat_position(self):
        for row in self.grid:
            for case in row:
                if case["rect"].collidepoint(player.hitbox.center):
                    self.cat_position = case
                    return

    def get_owner_position(self):
        for row in self.grid:
            for case in row:
                if case["rect"].collidepoint(owner.body_hitbox.center):
                    self.owner_position = case
                    return
                
       
class Pathfinder: 
    def __init__(self, matrix):
        
        # setup
        self.matrix =  matrix
        self.grid = Grid(matrix=matrix)
        self.cat_pos = 0
        self.owner_pos = 0
        self.path = []
    

    def create_path(self):

        #start
        start_x, start_y = self.owner_pos['pos_x'], self.owner_pos['pos_y']
        start = self.grid.node(start_x, start_y)
        #end
        end_x, end_y = self.cat_pos['pos_x'], self.cat_pos['pos_y']
        end = self.grid.node(end_x, end_y)
        #path
        finder = AStarFinder(diagonal_movement= DiagonalMovement.never)
        self.path, i = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        path = []
        for point in self.path:
            x = point.x * 60 + 30
            y = point.y * 60 + 30
            path.append([x, y])

  
        owner.path = path
        owner.target = path[0]
        

class game_over_class:
    def draw_window(self):
        screen.fill(GRAY)
        
        title_text = font.render("Game Over !", 1, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 200 - title_text.get_height()//2))

        screen.blit(player.img, (WIDTH//2 - player.body.width//2, HEIGHT//2 - player.body.height//2))

        score_text = font.render(f"Score : {game_variable.score}", 1, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 50))

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        miaou = False
        click = False
        
        # grid.solver()
        while run:
            clock.tick(60)

            player.update()

            if click or interact:
                run = False

            miaou = False
            interact = False
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
                    if event.key == K_e:
                        interact = True
                    if event.key == K_SPACE:
                        miaou = True
            self.draw_window()


class button_smash_class:
    IMG_1 = pygame.image.load(os.path.join("assets", os.path.join("minigame", "ORA1.svg")))
    IMG_2 = pygame.image.load(os.path.join("assets", os.path.join("minigame", "ORA2.svg")))

    LEFT_BUTTON = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 50, 50)
    RIGHT_BUTTON = pygame.Rect(WIDTH//2 + 100, HEIGHT//2, 50, 50)

    TIMER_BAR = pygame.Rect(WIDTH//2 - 101, HEIGHT//4 - 1, 202, 52)
    TIMER_BAR_PROGRESS = pygame.Rect(WIDTH//2 - 100, HEIGHT//4, 200, 50)

    break_free = 10
    timer = 0
    max_timer = 2
    smash_right = True
    
    def update_progress_bar(self):
        if self.timer:
            self.TIMER_BAR_PROGRESS.width = (self.TIMER_BAR.width - 2) * (1 - (time.time() - self.timer) / self.max_timer)

    def draw_window(self):
        screen.fill(WHITE)
        if self.smash_right:
            screen.blit(self.IMG_1, (0,0))
        else:
            screen.blit(self.IMG_2, (0,0))
        
        break_free_text = font.render(f"{self.break_free}", 1, BLACK)
        screen.blit(break_free_text, (WIDTH//2 - break_free_text.get_width()//2 - 50, HEIGHT//2 - 300))
        
        if not self.smash_right:
            pygame.draw.rect(screen, RED, (self.LEFT_BUTTON.x - 1, self.LEFT_BUTTON.y - 1, self.LEFT_BUTTON.width + 2, self.LEFT_BUTTON.height + 2))
        pygame.draw.rect(screen, DARK_GRAY, self.LEFT_BUTTON)
        q_button_text = font.render("Q", 1, WHITE)
        screen.blit(q_button_text, (self.LEFT_BUTTON.centerx - q_button_text.get_width()//2, self.LEFT_BUTTON.centery - q_button_text.get_height()//2))

        if self.smash_right:
            pygame.draw.rect(screen, RED, (self.RIGHT_BUTTON.x - 1, self.RIGHT_BUTTON.y - 1, self.RIGHT_BUTTON.width + 2, self.RIGHT_BUTTON.height + 2))
        pygame.draw.rect(screen, DARK_GRAY, self.RIGHT_BUTTON)
        d_button_text = font.render("D", 1, WHITE)
        screen.blit(d_button_text, (self.RIGHT_BUTTON.centerx - d_button_text.get_width()//2, self.RIGHT_BUTTON.centery - d_button_text.get_height()//2))

        pygame.draw.rect(screen, BLACK, self.TIMER_BAR)
        self.update_progress_bar()
        pygame.draw.rect(screen, YELLOW, self.TIMER_BAR_PROGRESS)

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        self.smash_right = True
        self.break_free = 10
        self.timer = time.time()
        
        while run:
            clock.tick(60)

            if time.time() - self.timer > self.max_timer:
                return False
            
            if self.smash_right and right:
                self.smash_right = False
                self.break_free -= 1
            if not self.smash_right and left:
                self.smash_right = True
                self.break_free -= 1

            if self.break_free <= 0:
                return True

            left = False
            right = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
            self.draw_window()


class main_game_class:

    def draw_window(self):
        camera.bg_blit()

        for row in grid.grid:
            for case in row:
                if not case["obstacle"]:
                    pygame.draw.rect(map, RED, case["rect"], 1)
                else:
                    pygame.draw.rect(map, WHITE, case["rect"], 1)

        # animation.play_animations()

        # Obstacles
        # pygame.draw.rect(map, BLACK, player.body)
        for room in obstacle.list:
            for obs in room:
                pygame.draw.rect(map, RED, obs)

        # Interactibles
        for item in interactible.list:
            if item["type"]["is_enabled"]:
                pygame.draw.rect(map, YELLOW, item["rect"])

        # Player (Cat)
        # pygame.draw.rect(map, BLACK, player.body)
        # pygame.draw.rect(map, GREEN, player.hitbox)
        # if player.i_frame:
        #     pygame.draw.rect(map, GREEN, player.hitbox)
        map.blit(player.img, (player.body.x, player.body.y))

        # Grid Position
        # pygame.draw.rect(map, GREEN, grid.cat_position["rect"])

        # Owner
        pygame.draw.rect(map, YELLOW, owner.body)

        # Owner Body Hitbox
        pygame.draw.rect(map, BLACK, owner.body_hitbox)
        
        # Grid position
        pygame.draw.rect(map, GREEN, grid.owner_position["rect"])


        camera.update()

        score_text = font.render(f"Score : {game_variable.score}", 1, WHITE)
        screen.blit(score_text, (10, 10))

        multiplier_text = font.render(f"Multiplier : {game_variable.multiplier}", 1, WHITE)
        screen.blit(multiplier_text, (10, 50))

        life_text = font.render(f"Lives : {player.hp}", 1, WHITE)
        screen.blit(life_text, (10, 90))

        selected_cat_text = font.render(f"Cat : {game_variable.selected_cat}", 1, WHITE)
        screen.blit(selected_cat_text, (10, 130))

        selected_owner_text = font.render(f"Owner : {game_variable.selected_owner}", 1, WHITE)
        screen.blit(selected_owner_text, (10, 170))

        owner_rage_text = font.render(f"Rage : {owner.rage}", 1, WHITE)
        screen.blit(owner_rage_text, (WIDTH - owner_rage_text.get_width() - 10, 10))

        owner_speed_text = font.render(f"Speed : {owner.speed}", 1, WHITE)
        screen.blit(owner_speed_text, (WIDTH - owner_speed_text.get_width() - 10, 50))

        if interactible.isOn:
            press_interact_text = font.render(f"Press E", 1, WHITE)
            screen.blit(press_interact_text, (screen.get_width()//2 - press_interact_text.get_width()//2, screen.get_height()//3 * 2))

        if interactible.interact_timer != None:
            pygame.draw.rect(screen, WHITE, interactible.PROGRESS_BAR)
            pygame.draw.rect(screen, YELLOW, interactible.PROGRESS_BAR_FILL)

        pygame.display.update()

    def main_loop(self):
        game_variable.reset_all_variable()
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        miaou = False
        click = False
        
        while run:
            clock.tick(60)
            owner.remove_rage(1)

            # Collision with cat
            if grid.owner_position["rect"].colliderect(grid.cat_position["rect"]) and not player.i_frame:
                player.i_frame = True

                # Start button smash to try to escape
                result = button_smash.main_loop()
                left = False
                right = False
                up = False
                down = False
                interact = False
                miaou = False
                click = False

                player.i_frame_timer = time.time()
                if not result:
                    player.hp -= 1
                    if player.hp <= 0:
                        game_over.main_loop()
                        run = False

            # i-frame logic
            if player.i_frame:
                if time.time() - player.i_frame_timer >= player.i_frame_duration:
                    player.i_frame = False
            
            # Player Go Left
            if left and not interact:
                player.hitbox.x -= player.speed
                player.right = False
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.hitbox.colliderect(obs):
                            player.hitbox.x += player.speed
            # Player Go Right
            if right and not interact:
                player.hitbox.x += player.speed
                player.right = True
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.hitbox.colliderect(obs):
                            player.hitbox.x -= player.speed
            # Player Go Up
            if up and not interact:
                player.hitbox.y -= player.speed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.hitbox.colliderect(obs):
                            player.hitbox.y += player.speed
            # Player Go Down
            if down and not interact:
                player.hitbox.y += player.speed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.hitbox.colliderect(obs):
                            player.hitbox.y -= player.speed
                            
            if left or right or up or down:
                player.moving = True
            else:
                player.moving = False

            interactible.update()

            if interact:
                interactible.interact()
            elif interactible.interact_timer != None:
                interactible.cancel_interact()

            if miaou and time.time() - player.miaou_timer > player.miaou_cd:
                print("miaou")

            owner.update()

            player.update()

            grid.update()
            pathfinder.owner_pos, pathfinder.cat_pos = grid.owner_position, grid.cat_position
            if random.randrange(0, 10) == 1:
                pathfinder.create_path()

            if click:
                owner.rage += 10

            miaou = False
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
                        # general_use.close_the_game()
                    if event.key == K_e:
                        interact = True
                    if event.key == K_SPACE:
                        miaou = True
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_z:
                        up = True
                    if event.key == K_s:
                        down = True
                if event.type == KEYUP:
                    if event.key == K_e:
                        interact = False
                    if event.key == K_q:
                        left = False
                    if event.key == K_d:
                        right = False
                    if event.key == K_z:
                        up = False
                    if event.key == K_s:
                        down = False
            self.draw_window()

class owner_selection_class:
    OWNER_1_CARD = pygame.Rect(WIDTH//2 - 500, HEIGHT//2 - 100, 400, 400)
    OWNER_2_CARD = pygame.Rect(WIDTH//2 + 100, HEIGHT//2 - 100, 400, 400)

    button_list = [BACK_BUTTON, OWNER_1_CARD, OWNER_2_CARD]
    index = 1

    def draw_window(self):
        screen.fill(WHITE)
        
        title_text = font.render("Title", 1, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 200 - title_text.get_height()//2))

        if self.index == 0:
            pygame.draw.rect(screen, RED, pygame.Rect(BACK_BUTTON.x - 1, BACK_BUTTON.y - 1, BACK_BUTTON.width + 2, BACK_BUTTON.height + 2))
        pygame.draw.rect(screen, GRAY, BACK_BUTTON)
        back_button_text = font.render("Back", 1, BLACK)
        screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

        if self.index == 1:
            pygame.draw.rect(screen, RED, pygame.Rect(self.OWNER_1_CARD.x - 1, self.OWNER_1_CARD.y - 1, self.OWNER_1_CARD.width + 2, self.OWNER_1_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.OWNER_1_CARD)
        owner_1_text = font.render("Owner 1", 1, BLACK)
        screen.blit(owner_1_text, (self.OWNER_1_CARD.centerx - owner_1_text.get_width()//2, self.OWNER_1_CARD.centery - owner_1_text.get_height()//2))

        if self.index == 2:
            pygame.draw.rect(screen, RED, pygame.Rect(self.OWNER_2_CARD.x - 1, self.OWNER_2_CARD.y - 1, self.OWNER_2_CARD.width + 2, self.OWNER_2_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.OWNER_2_CARD)
        owner_2_text = font.render("Owner 2", 1, BLACK)
        screen.blit(owner_2_text, (self.OWNER_2_CARD.centerx - owner_2_text.get_width()//2, self.OWNER_2_CARD.centery - owner_2_text.get_height()//2))

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        click = False
        while run:
            clock.tick(60)

            if (up or left) and self.index > 0:
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                self.index += 1

            if click or interact:
                if self.index == 0:
                    run = False
                if self.index == 1:
                    game_variable.selected_owner = game_variable.all_owners[0]
                    main.main_loop()
                if self.index == 2:
                    game_variable.selected_owner = game_variable.all_owners[1]
                    main.main_loop()

            left = False
            right = False
            up = False
            down = False
            interact = False
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
                        pass
                    if event.key == K_SPACE:
                        click = True
                    if event.key == K_e:
                        interact = True
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_z:
                        up = True
                    if event.key == K_s:
                        down = True
            self.draw_window()

class cat_selection_class:
    CAT_1_CARD = pygame.Rect(WIDTH//2 - 700, HEIGHT//2 - 100, 400, 400)
    CAT_2_CARD = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 400)
    CAT_3_CARD = pygame.Rect(WIDTH//2 + 300 , HEIGHT//2 - 100, 400, 400)

    button_list = [BACK_BUTTON, CAT_1_CARD, CAT_2_CARD, CAT_3_CARD]
    index = 1

    def draw_window(self):
        screen.fill(WHITE)
        
        title_text = font.render("Title", 1, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 200 - title_text.get_height()//2))

        if self.index == 0:
            pygame.draw.rect(screen, RED, pygame.Rect(BACK_BUTTON.x - 1, BACK_BUTTON.y - 1, BACK_BUTTON.width + 2, BACK_BUTTON.height + 2))
        pygame.draw.rect(screen, GRAY, BACK_BUTTON)
        back_button_text = font.render("Back", 1, BLACK)
        screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

        if self.index == 1:
            pygame.draw.rect(screen, RED, pygame.Rect(self.CAT_1_CARD.x - 1, self.CAT_1_CARD.y - 1, self.CAT_1_CARD.width + 2, self.CAT_1_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.CAT_1_CARD)
        cat_1_text = font.render("Nougat", 1, BLACK)
        screen.blit(cat_1_text, (self.CAT_1_CARD.centerx - cat_1_text.get_width()//2, self.CAT_1_CARD.y + 10))
        player.img.fill(ALMOST_BLACK)
        player.img.set_colorkey(ALMOST_BLACK)
        player.img.blit(ORANGE_CAT_IDLE, (0,0), (ORANGE_CAT_IDLE.get_height() * 1, 0, ORANGE_CAT_IDLE.get_height(), ORANGE_CAT_IDLE.get_height()))
        screen.blit(player.img, ((self.CAT_1_CARD.centerx - player.img.get_width()//2, self.CAT_1_CARD.centery - player.img.get_height()//2)))

        if self.index == 2:
            pygame.draw.rect(screen, RED, pygame.Rect(self.CAT_2_CARD.x - 1, self.CAT_2_CARD.y - 1, self.CAT_2_CARD.width + 2, self.CAT_2_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.CAT_2_CARD)
        cat_2_text = font.render("Hypnolos", 1, BLACK)
        screen.blit(cat_2_text, (self.CAT_2_CARD.centerx - cat_2_text.get_width()//2, self.CAT_2_CARD.y + 10))
        player.img.fill(ALMOST_BLACK)
        player.img.set_colorkey(ALMOST_BLACK)
        player.img.blit(BLACK_CAT_IDLE, (0,0), (BLACK_CAT_IDLE.get_height() * 1, 0, BLACK_CAT_IDLE.get_height(), BLACK_CAT_IDLE.get_height()))
        screen.blit(player.img, ((self.CAT_2_CARD.centerx - player.img.get_width()//2, self.CAT_2_CARD.centery - player.img.get_height()//2)))

        if self.index == 3:
            pygame.draw.rect(screen, RED, pygame.Rect(self.CAT_3_CARD.x - 1, self.CAT_3_CARD.y - 1, self.CAT_3_CARD.width + 2, self.CAT_3_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.CAT_3_CARD)
        cat_3_text = font.render("Her Majesty", 1, BLACK)
        screen.blit(cat_3_text, (self.CAT_3_CARD.centerx - cat_3_text.get_width()//2, self.CAT_3_CARD.y + 10))
        player.img.fill(ALMOST_BLACK)
        player.img.set_colorkey(ALMOST_BLACK)
        player.img.blit(SIAMESE_CAT_IDLE, (0,0), (SIAMESE_CAT_IDLE.get_height() * 1, 0, SIAMESE_CAT_IDLE.get_height(), SIAMESE_CAT_IDLE.get_height()))
        screen.blit(player.img, ((self.CAT_3_CARD.centerx - player.img.get_width()//2, self.CAT_3_CARD.centery - player.img.get_height()//2)))


        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        click = False
        while run:
            clock.tick(60)

            if (up or left) and self.index > 0:
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                self.index += 1

            if click or interact:
                if self.index == 0:
                    run = False
                if self.index == 1:
                    game_variable.selected_cat = game_variable.all_cats[0]
                    player.change_cat_skin()
                    owner_selection.main_loop()
                if self.index == 2:
                    game_variable.selected_cat = game_variable.all_cats[1]
                    player.change_cat_skin()
                    owner_selection.main_loop()
                if self.index == 3:
                    game_variable.selected_cat = game_variable.all_cats[2]
                    player.change_cat_skin()
                    owner_selection.main_loop()


            left = False
            right = False
            up = False
            down = False
            interact = False
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
                    if event.key == K_SPACE:
                        click = True
                    if event.key == K_e:
                        interact = True
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_z:
                        up = True
                    if event.key == K_s:
                        down = True
            self.draw_window()

class menu_class:
    # List of buttons objects
    PLAY_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    CREDITS_BUTTON = pygame.Rect(WIDTH//2 - 100, HEIGHT // 2 + 80, 200, 50)
    QUIT_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50)
    SETTINGS_BUTTON = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)

    button_list = [PLAY_BUTTON, CREDITS_BUTTON, QUIT_BUTTON, SETTINGS_BUTTON]
    index = 0

    def __init__(self, exitedGameProperty):
        self.exitedGameProperty = exitedGameProperty

    def draw_window(self):
        screen.fill(WHITE)
        
        title_text = font.render("Cat-CH ME !", 1, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 200 - title_text.get_height()//2))

        if self.index == 0:
            pygame.draw.rect(screen, RED, pygame.Rect(self.PLAY_BUTTON.x - 1, self.PLAY_BUTTON.y - 1, self.PLAY_BUTTON.width + 2, self.PLAY_BUTTON.height + 2))
        pygame.draw.rect(screen, GRAY, self.PLAY_BUTTON)
        play_text = font.render("Play", 1, BLACK)
        screen.blit(play_text, (self.PLAY_BUTTON.centerx - play_text.get_width()//2, self.PLAY_BUTTON.centery - play_text.get_height()//2))

        if self.index == 1:
            pygame.draw.rect(screen, RED, pygame.Rect(self.CREDITS_BUTTON.x - 1, self.CREDITS_BUTTON.y - 1, self.CREDITS_BUTTON.width + 2, self.CREDITS_BUTTON.height + 2))
        pygame.draw.rect(screen, GRAY, self.CREDITS_BUTTON)
        credits_text = font.render("Credits", 1, BLACK)
        screen.blit(credits_text, (self.CREDITS_BUTTON.centerx - credits_text.get_width()//2, self.CREDITS_BUTTON.centery - credits_text.get_height()//2))

        if self.index == 2:
            pygame.draw.rect(screen, RED, pygame.Rect(self.QUIT_BUTTON.x - 1, self.QUIT_BUTTON.y - 1, self.QUIT_BUTTON.width + 2, self.QUIT_BUTTON.height + 2))
        pygame.draw.rect(screen, GRAY, self.QUIT_BUTTON)
        exit_text = font.render("Exit", 1, BLACK)
        screen.blit(exit_text, (self.QUIT_BUTTON.centerx - exit_text.get_width()//2, self.QUIT_BUTTON.centery - exit_text.get_height()//2))

        if self.index == 3:
            pygame.draw.rect(screen, RED, pygame.Rect(self.SETTINGS_BUTTON.x - 1, self.SETTINGS_BUTTON.y - 1, self.SETTINGS_BUTTON.width + 2, self.SETTINGS_BUTTON.height + 2))
        pygame.draw.rect(screen, GRAY, self.SETTINGS_BUTTON)
        settings_text = font.render("Settings", 1, BLACK)
        screen.blit(settings_text, (self.SETTINGS_BUTTON.centerx - settings_text.get_width()//2, self.SETTINGS_BUTTON.centery - settings_text.get_height()//2))

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        click = False
        # music_class.play_music()
        while run:
            clock.tick(60)

            if (up or left) and self.index > 0:
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                self.index += 1

            if click or interact:
                if self.index == 0:
                    cat_selection.main_loop()
                if self.index == 1:
                    video_path  = os.path.join(r'./assets/videos', 'test.mp4')
                    # print("credits")
                if self.index == 2: # QUIT GAME
                    run = False
                    self.exitedGameProperty = True
                    pass # Break loop iteration and goes to the next
                if self.index == 3:
                    settings.main_loop()

            left = False
            right = False
            up = False
            down = False
            interact = False
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
                    if event.key == K_SPACE:
                        click = True
                    if event.key == K_e:
                        interact = True
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_z:
                        up = True
                    if event.key == K_s:
                        down = True
            self.draw_window()

# Class representing settings menu
class settings_class:
    # List of buttons objects
    MAP_UP_BTN = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    MAP_LEFT_BTN = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)
    MAP_DOWN_BTN = pygame.Rect(WIDTH//2 - 100, HEIGHT // 2 + 160, 200, 50)
    MAP_RIGHT_BTN = pygame.Rect(WIDTH//2 - 100, HEIGHT // 2 +  240, 200, 50)
    BACK_BTN = pygame.Rect(WIDTH//2 - 100, HEIGHT // 2 + 380, 200, 50)

    button_list = [MAP_UP_BTN, MAP_LEFT_BTN, MAP_DOWN_BTN, MAP_RIGHT_BTN, BACK_BTN]

    def __init__(self):
        self.index = 0

    def draw_window(self):
        screen.fill(WHITE)
        
        title_text = font.render("Paramètres", 1, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 200 - title_text.get_height()//2))

        if self.index == 0:
            pygame.draw.rect(screen, RED, pygame.Rect(self.MAP_UP_BTN.x - 1, self.MAP_UP_BTN.y - 1, self.MAP_UP_BTN.width + 2, self.MAP_UP_BTN.height + 2))
        pygame.draw.rect(screen, GRAY, self.MAP_UP_BTN)
        play_text = font.render("Touche directionnelle haut", 1, BLACK)
        screen.blit(play_text, (self.MAP_UP_BTN.centerx - play_text.get_width()//2, self.MAP_UP_BTN.centery - play_text.get_height()//2))

        if self.index == 1:
            pygame.draw.rect(screen, RED, pygame.Rect(self.MAP_LEFT_BTN.x - 1, self.MAP_LEFT_BTN.y - 1, self.MAP_LEFT_BTN.width + 2, self.MAP_LEFT_BTN.height + 2))
        pygame.draw.rect(screen, GRAY, self.MAP_LEFT_BTN)
        credits_text = font.render("Touche directionnelle gauche", 1, BLACK)
        screen.blit(credits_text, (self.MAP_LEFT_BTN.centerx - credits_text.get_width()//2, self.MAP_LEFT_BTN.centery - credits_text.get_height()//2))

        if self.index == 2:
            pygame.draw.rect(screen, RED, pygame.Rect(self.MAP_DOWN_BTN.x - 1, self.MAP_DOWN_BTN.y - 1, self.MAP_DOWN_BTN.width + 2, self.MAP_DOWN_BTN.height + 2))
        pygame.draw.rect(screen, GRAY, self.MAP_DOWN_BTN)
        exit_text = font.render("Touche directionnelle bas", 1, BLACK)
        screen.blit(exit_text, (self.MAP_DOWN_BTN.centerx - exit_text.get_width()//2, self.MAP_DOWN_BTN.centery - exit_text.get_height()//2))

        if self.index == 3:
            pygame.draw.rect(screen, RED, pygame.Rect(self.MAP_RIGHT_BTN.x - 1, self.MAP_RIGHT_BTN.y - 1, self.MAP_RIGHT_BTN.width + 2, self.MAP_RIGHT_BTN.height + 2))
        pygame.draw.rect(screen, GRAY, self.MAP_RIGHT_BTN)
        settings_text = font.render("Touche directionnelle droite", 1, BLACK)
        screen.blit(settings_text, (self.MAP_RIGHT_BTN.centerx - settings_text.get_width()//2, self.MAP_RIGHT_BTN.centery - settings_text.get_height()//2))

        if self.index == 4:
            pygame.draw.rect(screen, RED, pygame.Rect(self.BACK_BTN.x - 1, self.BACK_BTN.y - 1, self.BACK_BTN.width + 2, self.BACK_BTN.height + 2))
        pygame.draw.rect(screen, GRAY, self.BACK_BTN)
        settings_text = font.render("Retour", 1, BLACK)
        screen.blit(settings_text, (self.BACK_BTN.centerx - settings_text.get_width()//2, self.BACK_BTN.centery - settings_text.get_height()//2))

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        click = False
        while run:
            clock.tick(60)

            if (up or left) and self.index > 0:
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                self.index += 1

            if click or interact:
                match self.index:
                    case 0:
                        print('UP')
                        break
                    case 1:
                        print('LEFT')
                        break
                    case 2:
                        print('DOWN')
                        break
                    case 3:
                        print('RIGHT')
                        break
                    case _:
                        run = False
                        print('RETURN')
                        # Reset navigation index
                        self.index = 0
                        break
            

            # Events handler
            left = False
            right = False
            up = False
            down = False
            interact = False
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
                    if event.key == K_SPACE:
                        click = True
                    if event.key == K_e:
                        interact = True
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_z:
                        up = True
                    if event.key == K_s:
                        down = True
            self.draw_window()

# Class representing credits
class credits_class:
    # List of buttons objects
    BACK_BTN = pygame.Rect(WIDTH - 60, HEIGHT // 2 + 300, 50, 50)

    button_list = [BACK_BTN]
    index = 0

# Property designed to quit the game
exitedGameProperty = False

general_use = general_use_class()
game_variable = game_variable_class()
camera = camera_class()
player = player_class()
owner = owner_class()
obstacle = obstacle_class()
grid = grid_class()
interactible = interactible_class()
animation = animation_class()
game_over = game_over_class()
button_smash = button_smash_class()
main = main_game_class()
cat_selection = cat_selection_class()
owner_selection = owner_selection_class()
menu = menu_class(exitedGameProperty)
settings = settings_class()
grid.maze = redefineMaze(grid.maze)
pathfinder = Pathfinder(grid.maze)

# for x in grid.maze:
#     print(x)

# main.main_loop()
menu.main_loop()

if exitedGameProperty:
    general_use.close_the_game()