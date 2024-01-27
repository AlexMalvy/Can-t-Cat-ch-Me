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
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Can't cat-ch me !")
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
map = pygame.Surface((2520, 1500))
SQUARE = 60

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
    speed = 12

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
    body = pygame.Rect(1100, 400, 50, 100)
    range = 20
    
    max_speed = 5
    speed = 5
    moving = True

    target = None
    path = []

    def move_toward_cat(self):
        if self.target != None:
            if math.dist([self.target["rect"].centerx, self.target["rect"].centery], [self.body.centerx, self.body.centery]) > self.range:
                self.moving = True
                # Speed modifier
                if self.body.centerx != self.target["rect"].centerx and self.body.centery != self.target["rect"].centery:
                    self.speed = self.max_speed/3 * 2
                else:
                    self.speed = self.max_speed

                # Chase Target
                if self.target["rect"].centerx > self.body.centerx:
                        self.body.x += self.speed
                        self.right = True
                if self.target["rect"].centerx < self.body.centerx:
                        self.body.x -= self.speed
                        self.right = False
                        
                if self.target["rect"].centery > self.body.centery:
                        self.body.y += self.speed
                if self.target["rect"].centery < self.body.centery:
                        self.body.y -= self.speed
            else:
                self.path.pop(0)
                if len(self.path) > 0:
                    self.target = grid.grid[self.path[0][0]][self.path[0][1]]
                else:
                    self.target = None
        else:
            self.moving = False


    def move_toward_cat_old(self):
        if math.dist([self.target["rect"].centerx, self.target["rect"].centery], [self.body.centerx, self.body.centery]) > self.range:
            self.moving = True
            # Speed modifier
            if self.body.centerx != self.target["rect"].centerx and self.body.centery != self.target["rect"].centery:
                self.speed = self.max_speed/3 * 2
            else:
                self.speed = self.max_speed

            # Chase Target
            if self.target["rect"].centerx > self.body.centerx:
                    self.body.x += self.speed
                    self.right = True
            if self.target["rect"].centerx < self.body.centerx:
                    self.body.x -= self.speed
                    self.right = False
                    
            if self.target["rect"].centery > self.body.centery:
                    self.body.y += self.speed
            if self.target["rect"].centery < self.body.centery:
                    self.body.y -= self.speed

        else:
            self.moving = False

owner = owner_class()

class obstacle_class:

    #Full Map
    topWall = pygame.Rect(0, 0, map.get_width(), SQUARE)
    bottomWall = pygame.Rect(0, map.get_height() - SQUARE*2, map.get_width(), SQUARE)
    leftWall = pygame.Rect(0, 0, 60, map.get_height()-SQUARE*2)
    rightWall = pygame.Rect(map.get_width() - SQUARE, 0, SQUARE, map.get_height()-SQUARE*2)
    #Bedroom
    bedRoomBottomLeftHalf = pygame.Rect(SQUARE, SQUARE*8, SQUARE*6, SQUARE)
    bedRoomBottomRightHalf = pygame.Rect(SQUARE*11, SQUARE*8, SQUARE*6, SQUARE)
    bedRoomRightTopHalf= pygame.Rect(SQUARE*16, 0, SQUARE, SQUARE*2)
    bedRoomRightBottomHalf = pygame.Rect(SQUARE*16, SQUARE*6, SQUARE, SQUARE*2)
    bed = pygame.Rect(SQUARE*4, SQUARE*2, SQUARE*2, SQUARE*3)
    #Bathroom
    bathRoomBottomLeftHalf = pygame.Rect(0, SQUARE*16, SQUARE*7, SQUARE)
    bathRoomBottomRightHalf = pygame.Rect(SQUARE*9, SQUARE*16, SQUARE*6, SQUARE)
    bathRoomRightTopHalf= pygame.Rect(SQUARE*14, SQUARE*8, SQUARE, SQUARE*3)
    bathRoomRightBottomHalf = pygame.Rect(SQUARE*14, SQUARE*13, SQUARE, SQUARE*3)
    toilets = pygame.Rect(SQUARE, SQUARE*11, SQUARE*2, SQUARE*2)
    shower = pygame.Rect(SQUARE*12, SQUARE*8, SQUARE*2, SQUARE*2)
    #Hallway
    halwayRightTopHalf = pygame.Rect(SQUARE*14, SQUARE*16, SQUARE, SQUARE*3)
    halwayRightBottomHalf = pygame.Rect(SQUARE*14, SQUARE*21, SQUARE, SQUARE*2)
    shoeCase = pygame.Rect(SQUARE, map.get_height() - SQUARE*3, SQUARE*2, SQUARE)
    #Living Room
    couch = pygame.Rect(SQUARE*20, SQUARE*14, SQUARE*4, SQUARE*2)
    tv = pygame.Rect(SQUARE*21, map.get_height()-SQUARE*3, SQUARE*2, SQUARE*2)
    library = pygame.Rect(map.get_width()-SQUARE*2, SQUARE*9, SQUARE*2, SQUARE*5)
    #Office
    officeTopLeftHalf = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*10 , SQUARE*6, SQUARE)
    officeTopRightHalf = pygame.Rect(map.get_width()-SQUARE*3, map.get_height()-SQUARE*10 , SQUARE*3, SQUARE)
    officeLeftTopHalf= pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*10 , SQUARE, SQUARE*2)
    officeLeftBottomHalf = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*4 , SQUARE, SQUARE*2)
    desk = pygame.Rect(map.get_width()-SQUARE*10, map.get_height()-SQUARE*4, SQUARE*6, SQUARE*2)
    #Kitchen
    kitchenBottom = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*16 , SQUARE*13, SQUARE)
    table = pygame.Rect(map.get_width()-SQUARE*15, map.get_height()-SQUARE*22, SQUARE*5, SQUARE*2)
    oven= pygame.Rect(map.get_width()-SQUARE*3, SQUARE, SQUARE*2, SQUARE*2)
    fridge= pygame.Rect(map.get_width()-SQUARE*8, SQUARE, SQUARE*2, SQUARE*2)
    trashcan= pygame.Rect(map.get_width()-SQUARE*5, SQUARE, SQUARE, SQUARE)
    #testMap
    testMapHalfTopHalf = pygame.Rect(20*SQUARE, 0, SQUARE, SQUARE*4)
    testMapHalfBottomHalf = pygame.Rect(20*SQUARE, 6*SQUARE, SQUARE, SQUARE*3)
    testMapHalfBottomHalf2 = pygame.Rect(20*SQUARE, 10*SQUARE, SQUARE, SQUARE*4)
    testMapHalfBottomHalf3 = pygame.Rect(20*SQUARE, 15*SQUARE, SQUARE, SQUARE*4)
    testMapHalfBottomHalf4 = pygame.Rect(20*SQUARE, 21*SQUARE, SQUARE, SQUARE*4)
    testMapHalfTopHalfsecond = pygame.Rect(20*SQUARE, 0, SQUARE, SQUARE*4)
    testMapHalfBottomHalfsecond = pygame.Rect(10*SQUARE, 6*SQUARE, SQUARE, SQUARE*3)
    testMapHalfBottomHalf2second = pygame.Rect(10*SQUARE, 10*SQUARE, SQUARE, SQUARE*4)
    testMapHalfBottomHalf3second = pygame.Rect(10*SQUARE, 15*SQUARE, SQUARE, SQUARE*4)
    testMapHalfBottomHalf4second = pygame.Rect(10*SQUARE, 21*SQUARE, SQUARE, SQUARE*4)
    # map = pygame.Surface((2520(SQUARE42), 1500(SQUARE25)))
  
    kitchen= [kitchenBottom,table, oven, fridge, trashcan]
    office= [officeLeftBottomHalf, officeLeftTopHalf, officeTopLeftHalf, officeTopRightHalf, desk]
    livingRoom = [couch, tv, library]
    hallWay= [halwayRightTopHalf, halwayRightBottomHalf, shoeCase]
    bathRoom= [toilets, shower, bathRoomBottomLeftHalf, bathRoomBottomRightHalf, bathRoomRightTopHalf, bathRoomRightBottomHalf]
    bedRoom = [bedRoomBottomLeftHalf, bedRoomBottomRightHalf, bedRoomRightTopHalf,bed, bedRoomRightBottomHalf]
    fullMap = [topWall, bottomWall, leftWall, rightWall]
    testMap= [testMapHalfTopHalf, testMapHalfBottomHalf2, testMapHalfBottomHalf, testMapHalfBottomHalf3, testMapHalfBottomHalf4, testMapHalfTopHalfsecond, testMapHalfBottomHalf2second, testMapHalfBottomHalfsecond, testMapHalfBottomHalf3second, testMapHalfBottomHalf4second]
    list = [fullMap, bedRoom, bathRoom, hallWay, livingRoom, office, kitchen]

obstacle = obstacle_class()

class interactible_class():
    chair = pygame.Rect(1500, 400, 60, 60)
    chair2 = pygame.Rect(1600, 400, 60, 60)

    list = [chair, chair2]

interactible = interactible_class()

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

class grid_class:
    def __init__(self):
        self.initialGrid()
        self.get_cat_position()
        self.get_owner_position()

    grid = []
    maze = []
    cat_position = None
    owner_position = None

    solver_timer = 0
    solver_cd = 1

    def update(self):
        self.get_cat_position()
        self.get_owner_position()

        if time.time() - self.solver_timer > self.solver_cd:
            self.solver()

    def initialGrid(self):
        blockSize = 60 #Set the size of the grid block
        id = 1
        pos_x = 0
        pos_y = 0
        y_list = []
        maze_y_list = []
        for x in range(0, map.get_width(), blockSize):
            for y in range(0, map.get_height(), blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                # Check if obstacle
                for room in obstacle.list:
                    if rect.collidelist(room) == -1:
                        rect_info = {"id" : id, "pos_x" : pos_x, "pos_y" : pos_y,"rect" : rect, "obstacle" : 0}
                        # rect_info = 0
                    else:
                        rect_info = {"id" : id, "pos_x" : pos_x, "pos_y" : pos_y,"rect" : rect, "obstacle" : 1}
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
                if case["rect"].collidepoint(player.body.center):
                    self.cat_position = case
                    return

    def get_owner_position(self):
        for row in self.grid:
            for case in row:
                if case["rect"].collidepoint(owner.body.center):
                    self.owner_position = case
                    return
                
    def solver(self):
        start = (self.owner_position["pos_x"], self.owner_position["pos_y"])
        end = (self.cat_position["pos_x"], self.cat_position["pos_y"])

        path = []

        def astar_thread():
            nonlocal path
            try:
                path = maze_solver.astar(self.maze, start, end)
            except:
                pass

        thread = threading.Thread(target=astar_thread)
        if thread.is_alive():
             self.stop_thread.clear()
        else:
            thread.start()
            thread.join(timeout=0.2)  # Attendez jusqu'à 3 secondes maximum

        if path:
            owner.path = path
            owner.target = grid.grid[path[0][0]][path[0][1]]
        else:
            owner.path = []
            owner.target = None

        self.solver_timer = time.time()

       


grid = grid_class()

class main_game_class:
    def draw_window(self):
        camera.bg_blit()

        for row in grid.grid:
            for case in row:
                if case["obstacle"]:
                    pygame.draw.rect(map, RED, case["rect"], 1)
                else:
                    pygame.draw.rect(map, WHITE, case["rect"], 1)

        # animation.play_animations()

        # Obstacles
        pygame.draw.rect(map, BLACK, player.body)
        for room in obstacle.list:
            for obs in room:
                pygame.draw.rect(map, RED, obs)

        # Interactibles
        for item in interactible.list:
            pygame.draw.rect(map, YELLOW, item)

        # Player (Cat)
        pygame.draw.rect(map, BLACK, player.body)
        map.blit(player.img, (player.body.x, player.body.y))

        # Grid Position
        pygame.draw.rect(map, GREEN, grid.cat_position["rect"])

        # Owner
        pygame.draw.rect(map, YELLOW, owner.body)
        
        # Grid position
        pygame.draw.rect(map, RED, grid.owner_position["rect"])

        camera.update()

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        click = False
        grid.solver()
        while run:
            clock.tick(60)

            if left:
                player.body.x -= player.speed
                player.right = False
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.x += player.speed
            if right:
                player.body.x += player.speed
                player.right = True
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.x -= player.speed
            if up:
                player.body.y -= player.speed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.y += player.speed
            if down:
                player.body.y += player.speed
                # Check if colliding with obstacle
                for room in obstacle.list:
                    for obs in room:
                        if player.body.colliderect(obs):
                            player.body.y -= player.speed
                            
            if left or right or up or down:
                player.moving = True
            else:
                player.moving = False

            owner.move_toward_cat()

            player.update_visual()

            grid.update()

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

# print(grid.grid)

main.main_loop()

