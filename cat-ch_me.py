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

### Vod

# VOD = 

### Background

BG_GRAY_WALL = pygame.image.load(os.path.join("assets", "bg_gray_wall.jpg"))

## Cats Sprites

ORANGE_CAT_IDLE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle.png"], 1)
ORANGE_CAT_RUNNING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running.png"], 1)

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

class game_variable_class:
    score = 0
    multiplier = 1
    life = 3

    all_cats = ["cat 1", "cat 2", "cat 3"]
    selected_cat = "cat 1"
    
    all_owners = ["owner M", "owner F"]
    selected_owner = "owner M"

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


class owner_class:
    body = pygame.Rect(1100, 400, 50, 100)
    range = 20
    rage = 0
    max_rage = 100
    
    max_speed = 5
    speed = 5
    max_bonus_speed = 15
    bonus_speed = 0
    moving = True

    target = None
    path = []

    def update(self):
        self.move_toward_cat()

        self.update_move_speed()


    def move_toward_cat(self):
        if self.target != None:
            if math.dist([self.target["rect"].centerx, self.target["rect"].centery], [self.body.centerx, self.body.centery]) > self.range:
                self.moving = True
                # Speed modifier
                if self.body.centerx != self.target["rect"].centerx and self.body.centery != self.target["rect"].centery:
                    self.speed = (self.max_speed + self.bonus_speed)/3 * 2
                else:
                    self.speed = self.max_speed + self.bonus_speed

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

    def add_rage(self, amount):
        self.rage += amount

    def update_move_speed(self):
        self.bonus_speed = self.max_bonus_speed * (self.rage / self.max_rage)



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
    bed = pygame.Rect(SQUARE*5, SQUARE*2, SQUARE*4, SQUARE*4)
    nightStandBedroom = pygame.Rect(SQUARE*10, SQUARE*2, SQUARE, SQUARE)
    #Bathroom
    bathRoomBottomLeftHalf = pygame.Rect(0, SQUARE*16, SQUARE*7, SQUARE)
    bathRoomBottomRightHalf = pygame.Rect(SQUARE*9, SQUARE*16, SQUARE*6, SQUARE)
    bathRoomRightTopHalf= pygame.Rect(SQUARE*14, SQUARE*8, SQUARE, SQUARE*3)
    bathRoomRightBottomHalf = pygame.Rect(SQUARE*14, SQUARE*13, SQUARE, SQUARE*3)
    toiletsBathroom = pygame.Rect(SQUARE, SQUARE*11, SQUARE, SQUARE)
    showerBathroom = pygame.Rect(SQUARE*12, SQUARE*8, SQUARE*2, SQUARE*2)
    #Hallway
    halwayRightTopHalf = pygame.Rect(SQUARE*14, SQUARE*16, SQUARE, SQUARE*3)
    halwayRightBottomHalf = pygame.Rect(SQUARE*14, SQUARE*21, SQUARE, SQUARE*2)
    shoeCaseHallway = pygame.Rect(SQUARE, map.get_height() - SQUARE*3, SQUARE*6, SQUARE)
    #Living Room
    couchLivingRoom = pygame.Rect(SQUARE*20, SQUARE*14, SQUARE*4, SQUARE*2)
    tvLivingRoom = pygame.Rect(SQUARE*21, map.get_height()-SQUARE*3, SQUARE*2, SQUARE*2)
    libraryLivingRoom = pygame.Rect(map.get_width()-SQUARE*2, SQUARE*11, SQUARE*2, SQUARE*3)
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
    oven= pygame.Rect(map.get_width()-SQUARE*3, SQUARE, SQUARE*2, SQUARE*2)
    fridge= pygame.Rect(map.get_width()-SQUARE*8, SQUARE, SQUARE*2, SQUARE*2)
    trashCanKitchen= pygame.Rect(map.get_width()-SQUARE*5, SQUARE, SQUARE, SQUARE)
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
  
    kitchen= [kitchenBottom,table, oven, fridge, trashCanKitchen, chairKitchen1, chairKitchen2]
    office= [officeLeftBottomHalf, officeLeftTopHalf, officeTopLeftHalf, officeTopRightHalf, desk]
    livingRoom = [couchLivingRoom, tvLivingRoom, libraryLivingRoom]
    hallWay= [halwayRightTopHalf, halwayRightBottomHalf, shoeCaseHallway, plantLivingRoom]
    bathRoom= [toiletsBathroom, showerBathroom, bathRoomBottomLeftHalf, bathRoomBottomRightHalf, bathRoomRightTopHalf, bathRoomRightBottomHalf]
    bedRoom = [bedRoomBottomLeftHalf, bedRoomBottomRightHalf, bedRoomRightTopHalf,bed, bedRoomRightBottomHalf, nightStandBedroom]
    fullMap = [topWall, bottomWall, leftWall, rightWall]
    testMap= [testMapHalfTopHalf, testMapHalfBottomHalf2, testMapHalfBottomHalf, testMapHalfBottomHalf3, testMapHalfBottomHalf4, testMapHalfTopHalfsecond, testMapHalfBottomHalf2second, testMapHalfBottomHalfsecond, testMapHalfBottomHalf3second, testMapHalfBottomHalf4second]
    list = [fullMap, bedRoom, bathRoom, hallWay, livingRoom, office, kitchen]


class interactible_class():
    type_chair = {"score" : 100, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5}
    type_couch = {"score" : 200, "multiplier" : 0.3, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10}
    type_trashCan = {"score" : 400, "multiplier" : 0.4, "duration" : 4, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 15}
    type_library = {"score" : 1000, "multiplier" : 0.5, "duration" : 5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 20}
    type_plug = {"score" : 300, "multiplier" : 0.3, "duration" : 3, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10}
    type_plugOffice = {"score" : 1000, "multiplier" : 0.5, "duration" : 7, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 30}
    type_shoeCase = {"score" : 500, "multiplier" : 0.5, "duration" : 5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 15}
    type_toilets = {"score" : 200, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5}
    type_shower = {"score" : 300, "multiplier" : 0.3, "duration" : 3, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10}
    type_plant = {"score" : 1000, "multiplier" : 0.5, "duration" : 1, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 20}
    type_Rug = {"score" : 100, "multiplier" : 0.2, "duration" : 1, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3}


    # chairKitchen1 = pygame.Rect(map.get_width()-SQUARE*16, map.get_height()-SQUARE*21, SQUARE, SQUARE)
    # chairKitchen2 = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*19, SQUARE, SQUARE)
    # chairKitchen3 = pygame.Rect(map.get_width()-SQUARE*13, map.get_height()-SQUARE*23, SQUARE, SQUARE)
    #  couch = pygame.Rect(SQUARE*20, SQUARE*14, SQUARE*4, SQUARE*2)
    # tv = pygame.Rect(SQUARE*21, map.get_height()-SQUARE*3, SQUARE*2, SQUARE*2)
    # library = pygame.Rect(map.get_width()-SQUARE*2, SQUARE*9, SQUARE*2, SQUARE*5)
    # trashCanKitchen= pygame.Rect(map.get_width()-SQUARE*5, SQUARE, SQUARE, SQUARE)
    # toilets = pygame.Rect(SQUARE, SQUARE*11, SQUARE, SQUARE)
    # shower = pygame.Rect(SQUARE*12, SQUARE*8, SQUARE*2, SQUARE*2)
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


    


    list = [chair, chair2, couch, tvPlug, library, shoeCase, shower, officePlug, rug, nightStandPlug]

    isOn = None
    interact_timer = None
    
    PROGRESS_BAR = pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//3 * 2 + 150, 200, 25)
    PROGRESS_BAR_FILL = pygame.Rect(PROGRESS_BAR.x + 1, PROGRESS_BAR.y + 1, 0, PROGRESS_BAR.height - 2)

    def update(self):
        self.isOnInteractible()
        self.restore_interactibles()

    def isOnInteractible(self):
        for item in self.list:
            if item["rect"].collidepoint(player.body.center) and item["type"]["is_enabled"]:
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
                # owner.add_rage()

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
            if item["type"]["is_enabled"]:
                pygame.draw.rect(map, YELLOW, item["rect"])

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

        score_text = font.render(f"Score : {game_variable.score}", 1, WHITE)
        screen.blit(score_text, (10, 10))

        multiplier_text = font.render(f"Multiplier : {game_variable.multiplier}", 1, WHITE)
        screen.blit(multiplier_text, (10, 50))

        life_text = font.render(f"Lives : {game_variable.life}", 1, WHITE)
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
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
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

            interactible.update()

            if interact:
                interactible.interact()
            elif interactible.interact_timer != None:
                interactible.cancel_interact()

            owner.update()

            player.update_visual()

            grid.update()

            if click:
                owner.rage += 10

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
        cat_1_text = font.render("Cat 1", 1, BLACK)
        screen.blit(cat_1_text, (self.CAT_1_CARD.centerx - cat_1_text.get_width()//2, self.CAT_1_CARD.centery - cat_1_text.get_height()//2))

        if self.index == 2:
            pygame.draw.rect(screen, RED, pygame.Rect(self.CAT_2_CARD.x - 1, self.CAT_2_CARD.y - 1, self.CAT_2_CARD.width + 2, self.CAT_2_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.CAT_2_CARD)
        cat_2_text = font.render("Cat 2", 1, BLACK)
        screen.blit(cat_2_text, (self.CAT_2_CARD.centerx - cat_2_text.get_width()//2, self.CAT_2_CARD.centery - cat_2_text.get_height()//2))

        if self.index == 3:
            pygame.draw.rect(screen, RED, pygame.Rect(self.CAT_3_CARD.x - 1, self.CAT_3_CARD.y - 1, self.CAT_3_CARD.width + 2, self.CAT_3_CARD.height + 2))
        pygame.draw.rect(screen, GRAY, self.CAT_3_CARD)
        cat_3_text = font.render("Cat 3", 1, BLACK)
        screen.blit(cat_3_text, (self.CAT_3_CARD.centerx - cat_3_text.get_width()//2, self.CAT_3_CARD.centery - cat_3_text.get_height()//2))


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
                    owner_selection.main_loop()
                if self.index == 2:
                    game_variable.selected_cat = game_variable.all_cats[1]
                    owner_selection.main_loop()
                if self.index == 3:
                    game_variable.selected_cat = game_variable.all_cats[2]
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

class menu_class:
    PLAY_BUTTON = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
    CREDITS_BUTTON = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
    SETTINGS_BUTTON = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)

    button_list = [PLAY_BUTTON, CREDITS_BUTTON, SETTINGS_BUTTON]
    index = 0

    def draw_window(self):
        screen.fill(WHITE)
        
        title_text = font.render("Title", 1, BLACK)
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
                    # print("credits")
                    video.PlayedVideo(screen, "assets/videos/test.mp4", "")
                if self.index == 2:
                    print("settings")

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


general_use = general_use_class()
game_variable = game_variable_class()
camera = camera_class()
player = player_class()
owner = owner_class()
obstacle = obstacle_class()
grid = grid_class()
interactible = interactible_class()
animation = animation_class()
main = main_game_class()
cat_selection = cat_selection_class()
owner_selection = owner_selection_class()
menu = menu_class()

# print(grid.grid)

# main.main_loop()
menu.main_loop()

