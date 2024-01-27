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
    table = pygame.Rect(1500, 500, 250, 250)
    #Office
    officeLeftBottomHalf = pygame.Rect(map.get_width()-800, map.get_height()-600 , 400, 15)
    officeRightBottomHalf = pygame.Rect(map.get_width()-250, map.get_height()-600 , 250, 15)
    officeTopLeftHalf= pygame.Rect(map.get_width()-800, map.get_height()-600 , 15, 200)
    officeTopRightHalf = pygame.Rect(map.get_width()-800, map.get_height()-300 , 15, 200)
    #Kitchen
    kitchenLeftBottomHalf = pygame.Rect(map.get_width()-800, map.get_height()-600 , 400, 15)
    kitchenLeftRightHalf = pygame.Rect(map.get_width()-250, map.get_height()-600 , 250, 15)

    office= [officeLeftBottomHalf, officeRightBottomHalf, officeTopLeftHalf, officeTopRightHalf]
    livingRoom = [table]
    halway= [halwayRightTopHalf, halwayRightBottomHalf, shoeCase]
    bathRoom= [toilets, shower, bathRoomBottomLeftHalf, bathRoomBottomRightHalf, bathRoomRightTopHalf, bathRoomRightBottomHalf]
    bedRoom = [bed, bedRoomBottomLeftHalf, bedRoomBottomRightHalf, bedRoomRightTopHalf, bedRoomRightBottomHalf]
    fullMap = [topWall, bottomWall, leftWall, rightWall]
    list = [fullMap, bedRoom, bathRoom, livingRoom, halway, office]

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
        # print(start)
        # print(end)

        path = maze_solver.astar(self.maze, start, end)
        # print(path)
        owner.path = path
        owner.target = grid.grid[path[0][0]][path[0][1]]

        self.solver_timer = time.time()
        # print(owner.target)


grid = grid_class()

class main_game_class:
    def draw_window(self):
        camera.bg_blit()

        # for case in grid.grid:
        #     if case["obstacle"]:
        #         pygame.draw.rect(map, RED, case["rect"], 1)
            # else:
            #     pygame.draw.rect(map, WHITE, case["rect"], 1)

        # animation.play_animations()

        # Obstacles
        pygame.draw.rect(map, BLACK, player.body)
        for room in obstacle.list:
            for obs in room:
                pygame.draw.rect(map, RED, obs)

        # Player (Cat)
        pygame.draw.rect(map, BLACK, player.body)
        map.blit(player.img, (player.body.x, player.body.y))

        pygame.draw.rect(map, GREEN, grid.cat_position["rect"])

        # Owner
        pygame.draw.rect(map, YELLOW, owner.body)
        
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


