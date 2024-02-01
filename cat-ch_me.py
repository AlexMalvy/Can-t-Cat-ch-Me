import pygame
import sys
import time
import random
import os
import sys
import math
import img_load
from copy import deepcopy
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Can't cat-ch me !")
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
SQUARE = 60
map = pygame.Surface((42*SQUARE, 38*SQUARE))


WIDTH, HEIGHT = screen.get_width(), screen.get_height()

clock = pygame.time.Clock()

#############

### Font

sys_font = pygame.font.SysFont("sherif", 40)
small_sys_font = pygame.font.SysFont("sherif", 10)

font = pygame.font.Font(os.path.join("assets", os.path.join("font", "PixelOperator-Bold.ttf")), 40)
big_font = pygame.font.Font(os.path.join("assets", os.path.join("font", "PixelOperator-Bold.ttf")), 120)

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

BG_MAP = pygame.image.load(os.path.join("assets", "new-map.jpg"))
BG_GAME_UI = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "background-game-ui-1920x1080.jpg")))

### Cats Sprites
## Orange
# Normal
ORANGE_CAT_IDLE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle.png"], 3)
ORANGE_CAT_WALKING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-walking.png"], 3)
ORANGE_CAT_RUNNING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running.png"], 3)
ORANGE_CAT_SCRATCHING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-scratching.png"], 3)
ORANGE_CAT_JUMPING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-jumping.png"], 3)
ORANGE_CAT_PEE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-pee.png"], 3)
ORANGE_CAT_PUKE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-puke.png"], 3)

ORANGE_CAT_LICKING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-licking.png"], 3)
ORANGE_CAT_LOAF_BREAD = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-loaf-bread.png"], 3)
ORANGE_CAT_SLEEPING = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-sleeping-zz.png"], 3)
ORANGE_CAT_TRANSFORM = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-transform-chaiyan.png"], 3)

# Potte
ORANGE_CAT_IDLE_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle-potte.png"], 3)
ORANGE_CAT_WALKING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-walking-potte.png"], 3)
ORANGE_CAT_RUNNING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running-potte.png"], 3)
ORANGE_CAT_SCRATCHING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-scratching-potte.png"], 3)
ORANGE_CAT_JUMPING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-jumping-potte.png"], 3)
ORANGE_CAT_PEE_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-peeing-potte.png"], 3)
ORANGE_CAT_PUKE_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-puking-potte.png"], 3)

ORANGE_CAT_LICKING_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-licking-potte.png"], 3)
ORANGE_CAT_LOAF_BREAD_POTTE = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-loaf-bread-potte.png"], 3)

# Nyan
ORANGE_CAT_IDLE_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-idle-nyan.png"], 3)
ORANGE_CAT_WALKING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-walking-nyan.png"], 3)
ORANGE_CAT_RUNNING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-running-nyan.png"], 3)
ORANGE_CAT_SCRATCHING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-scratching-nyan.png"], 3)
ORANGE_CAT_JUMPING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-jumping-nyan.png"], 3)
ORANGE_CAT_PEE_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-peeing-nyan.png"], 3)
ORANGE_CAT_PUKE_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-puking-nyan.png"], 3)

ORANGE_CAT_LICKING_NYAN = img_load.image_loader.load(["assets", "orange-cat", "orange-cat-licking-nyan.png"], 3)

## Black
# Normal
BLACK_CAT_IDLE = img_load.image_loader.load(["assets", "black-cat", "black-cat-idle.png"], 3)
BLACK_CAT_WALKING = img_load.image_loader.load(["assets", "black-cat", "black-cat-walking.png"], 3)
BLACK_CAT_RUNNING = img_load.image_loader.load(["assets", "black-cat", "black-cat-running.png"], 3)
BLACK_CAT_SCRATCHING = img_load.image_loader.load(["assets", "black-cat", "black-cat-scratching.png"], 3)
BLACK_CAT_JUMPING = img_load.image_loader.load(["assets", "black-cat", "black-cat-jumping.png"], 3)
BLACK_CAT_PEE = img_load.image_loader.load(["assets", "black-cat", "black-cat-pee.png"], 3)
BLACK_CAT_PUKE = img_load.image_loader.load(["assets", "black-cat", "black-cat-puke.png"], 3)

BLACK_CAT_LICKING = img_load.image_loader.load(["assets", "black-cat", "black-cat-licking.png"], 3)
BLACK_CAT_LOAF_BREAD = img_load.image_loader.load(["assets", "black-cat", "black-cat-loaf-bread.png"], 3)
BLACK_CAT_SLEEPING = img_load.image_loader.load(["assets", "black-cat", "black-cat-sleeping-zz.png"], 3)
BLACK_CAT_TRANSFORM = img_load.image_loader.load(["assets", "black-cat", "black-cat-transform-chaiyan.png"], 3)

# Potte
BLACK_CAT_IDLE_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-idle-potte.png"], 3)
BLACK_CAT_WALKING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-walking-potte.png"], 3)
BLACK_CAT_RUNNING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-running-potte.png"], 3)
BLACK_CAT_SCRATCHING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-scratching-potte.png"], 3)
BLACK_CAT_JUMPING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-jumping-potte.png"], 3)
BLACK_CAT_PEE_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-peeing-potte.png"], 3)
BLACK_CAT_PUKE_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-puking-potte.png"], 3)

BLACK_CAT_LICKING_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-licking-potte.png"], 3)
BLACK_CAT_LOAF_BREAD_POTTE = img_load.image_loader.load(["assets", "black-cat", "black-cat-loaf-bread-potte.png"], 3)

# Nyan
BLACK_CAT_IDLE_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-idle-nyan.png"], 3)
BLACK_CAT_WALKING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-walking-nyan.png"], 3)
BLACK_CAT_RUNNING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-running-nyan.png"], 3)
BLACK_CAT_SCRATCHING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-scratching-nyan.png"], 3)
BLACK_CAT_JUMPING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-jumping-nyan.png"], 3)
BLACK_CAT_PEE_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-peeing-nyan.png"], 3)
BLACK_CAT_PUKE_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-puking-nyan.png"], 3)

BLACK_CAT_LICKING_NYAN = img_load.image_loader.load(["assets", "black-cat", "black-cat-licking-nyan.png"], 3)

## SIAMESE
# Normal
SIAMESE_CAT_IDLE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-idle.png"], 3)
SIAMESE_CAT_WALKING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-walking.png"], 3)
SIAMESE_CAT_RUNNING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-running.png"], 3)
SIAMESE_CAT_SCRATCHING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-scratching.png"], 3)
SIAMESE_CAT_JUMPING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-jumping.png"], 3)
SIAMESE_CAT_PEE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-pee.png"], 3)
SIAMESE_CAT_PUKE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-puke.png"], 3)

SIAMESE_CAT_LICKING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-licking.png"], 3)
SIAMESE_CAT_LOAF_BREAD = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-loaf-bread.png"], 3)
SIAMESE_CAT_SLEEPING = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-sleeping-zz.png"], 3)
SIAMESE_CAT_TRANSFORM = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-transform-chaiyan.png"], 3)

# Potte
SIAMESE_CAT_IDLE_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-idle-potte.png"], 3)
SIAMESE_CAT_WALKING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-walking-potte.png"], 3)
SIAMESE_CAT_RUNNING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-running-potte.png"], 3)
SIAMESE_CAT_SCRATCHING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-scratching-potte.png"], 3)
SIAMESE_CAT_JUMPING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-jumping-potte.png"], 3)
SIAMESE_CAT_PEE_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-peeing-potte.png"], 3)
SIAMESE_CAT_PUKE_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-puking-potte.png"], 3)

SIAMESE_CAT_LICKING_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-licking-potte.png"], 3)
SIAMESE_CAT_LOAF_BREAD_POTTE = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-loaf-bread-potte.png"], 3)

# Nyan
SIAMESE_CAT_IDLE_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-idle-nyan.png"], 3)
SIAMESE_CAT_WALKING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-walking-nyan.png"], 3)
SIAMESE_CAT_RUNNING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-running-nyan.png"], 3)
SIAMESE_CAT_SCRATCHING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-scratching-nyan.png"], 3)
SIAMESE_CAT_JUMPING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-jumping-nyan.png"], 3)
SIAMESE_CAT_PEE_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-peeing-nyan.png"], 3)
SIAMESE_CAT_PUKE_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-puking-nyan.png"], 3)

SIAMESE_CAT_LICKING_NYAN = img_load.image_loader.load(["assets", "siamese-cat", "siamese-cat-licking-nyan.png"], 3)


## CHAIYAN
CHAIYAN_CAT_IDLE = img_load.image_loader.load(["assets", "chaiyan", "cat-idle-chaiyan.png"], 3)
CHAIYAN_CAT_WALKING = img_load.image_loader.load(["assets", "chaiyan", "cat-walking-chaiyan.png"], 3)
CHAIYAN_CAT_RUNNING = img_load.image_loader.load(["assets", "chaiyan", "cat-running-chaiyan.png"], 3)
CHAIYAN_CAT_SCRATCHING = img_load.image_loader.load(["assets", "chaiyan", "cat-scratching-chaiyan.png"], 3)
CHAIYAN_CAT_JUMPING = img_load.image_loader.load(["assets", "chaiyan", "cat-jumping-chaiyan.png"], 3)
CHAIYAN_CAT_PEE = img_load.image_loader.load(["assets", "chaiyan", "cat-peeing-chaiyan.png"], 3)
CHAIYAN_CAT_PUKE = img_load.image_loader.load(["assets", "chaiyan", "cat-puking-chaiyan.png"], 3)

CHAIYAN_CAT_LICKING = img_load.image_loader.load(["assets", "chaiyan", "cat-licking-chaiyan.png"], 3)

## Owner

OWNER_MALE_IDLE = img_load.image_loader.load(["assets", "owner", "owner-male-idle.png"], 1.5)
OWNER_MALE_WALKING_HAPPY = img_load.image_loader.load(["assets", "owner", "owner-male-walking-happy.png"], 1.5)
OWNER_MALE_WALKING_MEH = img_load.image_loader.load(["assets", "owner", "owner-male-walking-meh.png"], 1.5)
OWNER_MALE_WALKING_ANGRY = img_load.image_loader.load(["assets", "owner", "owner-male-walking-angry.png"], 1.5)
OWNER_MALE_WALKING_RAGE = img_load.image_loader.load(["assets", "owner", "owner-male-walking-rage.png"], 1.5)

OWNER_FEMALE_IDLE = img_load.image_loader.load(["assets", "owner", "owner-female-idle.png"], 1.5)
OWNER_FEMALE_WALKING_HAPPY = img_load.image_loader.load(["assets", "owner", "owner-female-walking-happy.png"], 1.5)
OWNER_FEMALE_WALKING_MEH = img_load.image_loader.load(["assets", "owner", "owner-female-walking-meh.png"], 1.5)
OWNER_FEMALE_WALKING_ANGRY = img_load.image_loader.load(["assets", "owner", "owner-female-walking-angry.png"], 1.5)
OWNER_FEMALE_WALKING_RAGE = img_load.image_loader.load(["assets", "owner", "owner-female-walking-rage.png"], 1.5)

## Buttons

BACK_BUTTON_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-back.png")))
BACK_BUTTON_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-back-focus-hover.png")))

BACK_BUTTON = pygame.Rect(10, HEIGHT - 10 - BACK_BUTTON_IMG.get_height(), BACK_BUTTON_IMG.get_width(), BACK_BUTTON_IMG.get_height())

PLAY_BUTTON_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-play.png")))
PLAY_BUTTON_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-play-focus-hover.png")))

PLAY_BUTTON = pygame.Rect(WIDTH - 10 - PLAY_BUTTON_IMG.get_width(), HEIGHT - 10 - PLAY_BUTTON_IMG.get_height(), PLAY_BUTTON_IMG.get_width(), PLAY_BUTTON_IMG.get_height())

BLACK_FRAME = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "black-frame.png")))
ORANGE_FRAME = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "orange-hover-frame.png")))

#############

# class baseSettings:
#     # Create json controls config
#     def __init__(self):
#         # Set base config function
#         def setBaseConfig():
#             # Set a base configuration
#             self.up = 'w'
#             self.left = 'q'
#             self.down = 's'
#             self.right = 'd'
#             self.action = 'e'
#             self.select = 'space'
#             self.back = 'escape'
#         # Valid keys for config fle
#         valids = ['up', 'left', 'down', 'right', 'action', 'select', 'back']
#         # Config file name
#         config = 'config.json'
#         # Check file existence :
#         exists = os.path.isfile(config)
#         # Check json config file exists
#         if not exists:
#             # Set a base configuration
#             setBaseConfig()
#             # Create controls dictionary
#             controls = {
#                 "up": self.up,
#                 "left": self.left,
#                 "down": self.down,
#                 "right": self.right,
#                 "action": self.action,
#                 "select": self.select,
#                 "back": self.back,
#             }
#             # Create a json config file
#             with open(config, "w") as outfile: 
#                 json.dump(controls, outfile)
#         else :
#             # Flag to check json file validity
#             isConfigValid = True
#             # Read JSON file
#             with open(config, "r") as configFile:
#                 # Check if json is loadable
#                 try:
#                     # Create configuration dictionary
#                     configuration = json.load(configFile)
#                 except:
#                     # Mark as invalid json file
#                     isConfigValid = False
#                 finally:
#                     # Check numbner of expected keys
#                     if len(configuration) == len(valids):
#                         # Check keys validity
#                         for key in configuration.keys():
#                             if not(key in valids):
#                                 isConfigValid = False
#                         # If keys are valid, check values
#                         if isConfigValid :
#                             # Check values validity
#                             configValues = list(configuration.values())
#                             for value in configValues:
#                                 # A value is valid if unique
#                                 count = 0
#                                 # Loop on each values
#                                 for i in range(0, len(configValues)):
#                                     if configValues[i] == value:
#                                         count += 1
#                                 # If value occured more than 1 time : mark as invalid then break loop
#                                 if count > 1:
#                                     isConfigValid = False
#                                     break
#                     else:
#                         isConfigValid = False
#             # if file is not valid
#             if not isConfigValid :
#                 # delete
#                 os.remove(config)
#                 # set base config
#                 setBaseConfig()
#                 # Create controls dictionary
#                 controls = {
#                     "up": self.up,
#                     "left": self.left,
#                     "down": self.down,
#                     "right": self.right,
#                     "action": self.action,
#                     "select": self.select,
#                     "back": self.back,
#                 }
#                 # Create a valid json config file
#                 with open(config, "w") as outfile: 
#                     json.dump(controls, outfile)
#             # Else, if the file is valid => check mapping validity
#             else:
#                 print('valid file')

#     def eventListener(run = True, left = False, right = False, up = False, down = False, interact = False, click = False):
#         # Listen for each event in the game
#         for event in pygame.event.get():
#             # If quit is requested
#             if event.type == pygame.QUIT:
#                 run = False
#                 general_use.close_the_game()
#             # For each keydown
#             if event.type == KEYDOWN:

#                 if event.key == K_ESCAPE:
#                     run = False
#                     general_use.close_the_game()
#                 if event.key == K_SPACE:
#                     click = True
#                 if event.key == K_e:
#                     interact = True
#                 if event.key == K_q:
#                     left = True
#                 if event.key == K_d:
#                     right = True
#                 if event.key == K_z:
#                     up = True
#                 if event.key == K_s:
#                     down = True

# SETTINGS

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
    BUTTON = pygame.mixer.Sound(os.path.join("assets", os.path.join("music", "press-button.mp3")))
    BUTTON_SWITCH = pygame.mixer.Sound(os.path.join("assets", os.path.join("music", "bloop-sound.mp3")))
    BUTTON_CANCEL = pygame.mixer.Sound(os.path.join("assets", os.path.join("music", "bip-sound.mp3")))

    MEOW_1 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "cat-meow-1.mp3")))
    MEOW_2 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "cat-meow-2.mp3")))
    MEOW_3 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "cat-meow-3.mp3")))
    MEOW_4 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "cat-meow-4.mp3")))
    MEOW_5 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "cat-meow.mp3")))

    MEOWS = [MEOW_1, MEOW_2, MEOW_3, MEOW_4, MEOW_5]

    PURRING = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "cat-purring.mp3")))

    GLASS_BREAKING_1 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "glass-breaking-1.mp3")))
    GLASS_BREAKING_2 = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "glass-breaking-2.mp3")))

    SCRATCH = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "scratch-couch.mp3")))

    ELECTRIC = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "electric-sound.mp3")))

    FALLING_OBJECT = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "falling-can.mp3")))
    
    TOILET_PAPER = pygame.mixer.Sound(os.path.join('assets', os.path.join("music", "toilet-paper.mp3")))
    
    CHAIYAN = pygame.mixer.Sound(os.path.join('assets', os.path.join("chaiyan", os.path.join("transformation", "saiyan.mp3"))))

    NYAN_CAT_THEME = os.path.join('assets', os.path.join("music", "nyan-cat-theme.mp3"))
    POTTE_CAT_THEME = os.path.join('assets', os.path.join("music", "potte-cat-theme.mp3"))
    SUPER_CHAIYAN_THEME = os.path.join('assets', os.path.join("chaiyan", "super-chaiyan.mp3"))
    MAIN_THEME = os.path.join('assets', os.path.join("music", "main_theme.mp3"))

    LOSE = os.path.join('assets', os.path.join("music", "you-lose.mp3"))
    WIN = os.path.join('assets', os.path.join("music", "you-win.mp3"))


    selected_sound = None

    def play_sound(self, sound, volume = 0.5):
        self.selected_sound = sound
        self.selected_sound.play()
        self.selected_sound.set_volume(volume)

    def stop_sound(self, sound):
        sound.stop()

    def play_music(self, music):
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


class camera_class:
    bg = pygame.transform.scale(BG_MAP, (map.get_width(), map.get_height()))
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

    timer = 0
    max_timer = 100
    enraged = False

    win_timer = 2

    started = False

    win = False
    end_win_cinematic = False

    all_cats = ["orange", "black", "siamese"]
    selected_cat = "orange"
    
    all_owners = ["male", "female"]
    selected_owner = "male"

    def reset_all_variable(self):
        self.score = 0
        self.multiplier = 1
        self.started = False
        self.timer = 0
        self.enraged = False
        self.win = False

        player.reset()
        owner.reset()
        interactible.reset()
        animation.reset()
        grid.update()

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

# CHARACTERS

class player_class:
    def reset(self):
        self.body = pygame.Rect(SQUARE*18, SQUARE*18, 192, 192)
        self.hitbox = pygame.Rect(self.body.x, self.body.bottom, 60, 60)
        self.hp = 3
        self.right = True
        self.potte = False
        self.nyan = False
        self.chaiyan = False
        self.transforming = False
        self.i_frame = False
        self.i_frame_timer = 0

    body = pygame.Rect(SQUARE*18, SQUARE*18, 192, 192)

    base_speed = 12
    bonus_speed = 0
    speed = 12
    hp = 3
    hitbox = pygame.Rect(body.x, body.bottom, 60, 60)

    moving = False
    right = True

    i_frame = False
    i_frame_timer = 0
    i_frame_duration = 2
    i_frame_blinking_state = False
    i_frame_blinking_min_alpha = 130
    i_frame_blinking_timer = 0
    i_frame_blinking_duration = 200

    miaou = False
    miaou_cd = 3
    miaou_timer = 0
    miaou_duration = 3

    puke_cd = 15
    puke_timer = 0

    frame = 0
    frame_timer = pygame.time.get_ticks()
    frame_cd = 120
    state = [ORANGE_CAT_IDLE, ORANGE_CAT_WALKING, ORANGE_CAT_RUNNING, ORANGE_CAT_SCRATCHING, ORANGE_CAT_JUMPING, ORANGE_CAT_PEE, ORANGE_CAT_PUKE]
    current_state = 0

    idle_bis = False
    idle_bis_counter = 0
    idle_bis_state = 0
    idle_bis_list = [ORANGE_CAT_LICKING]

    potte = False
    state_potte = [ORANGE_CAT_IDLE_POTTE, ORANGE_CAT_WALKING_POTTE, ORANGE_CAT_RUNNING_POTTE, ORANGE_CAT_SCRATCHING_POTTE, ORANGE_CAT_JUMPING_POTTE, ORANGE_CAT_PEE_POTTE, ORANGE_CAT_PUKE_POTTE]
    state_potte_idle_bis = [ORANGE_CAT_LICKING_POTTE]

    nyan = False
    state_nyan = [ORANGE_CAT_IDLE_NYAN, ORANGE_CAT_WALKING_NYAN, ORANGE_CAT_RUNNING_NYAN, ORANGE_CAT_SCRATCHING_NYAN, ORANGE_CAT_JUMPING_NYAN, ORANGE_CAT_PEE_NYAN, ORANGE_CAT_PUKE_NYAN]
    state_nyan_idle_bis = [ORANGE_CAT_LICKING_NYAN]

    in_selection = False
    state_selection = [ORANGE_CAT_LOAF_BREAD]

    state_pregame = [ORANGE_CAT_SLEEPING]

    chaiyan = False
    transforming = False
    transforming_timer = 0
    state_chaiyan_transformation = [ORANGE_CAT_TRANSFORM]
    chaiyan_timer = 0
    chaiyan_duration = 10
    chaiyan_transform_cap = 1
    chaiyan_state = [CHAIYAN_CAT_IDLE, CHAIYAN_CAT_WALKING, CHAIYAN_CAT_RUNNING, CHAIYAN_CAT_SCRATCHING, CHAIYAN_CAT_JUMPING, CHAIYAN_CAT_PEE, CHAIYAN_CAT_PUKE]
    chaiyan_state_idle_bis = [CHAIYAN_CAT_LICKING]

    img = pygame.Surface((body.width, body.height))

    SPEECH_BUBBLE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bubble-yes.png")))
    
    def update(self):
        self.align_body()

        self.change_state()

        self.update_frame()

        self.apply_bonuses()

        self.iframe_blinking()

        self.apply_wall_filter()


    def apply_bonuses(self):
        if self.chaiyan:
            if game_variable.multiplier < self.chaiyan_transform_cap:
                self.chaiyan = False

        self.bonus_speed = 0
        if self.i_frame:
            self.bonus_speed += 5
        if self.chaiyan:
            self.bonus_speed += 3

        self.speed = self.base_speed + self.bonus_speed


    def change_state(self):
        if not game_variable.started and self.current_state != 0:
            self.current_state = 0
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
            self.idle_bis = False
            self.idle_bis_counter = 0
        elif self.transforming and self.current_state != 0:
            self.current_state = 0
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
            self.idle_bis = False
            self.idle_bis_counter = 0
        else:
            if not self.moving and interactible.interact_timer and self.current_state != 6 and interactible.isOn["type"]["animation_type"] == "puke":
                self.current_state = 6
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
                self.idle_bis = False
                self.idle_bis_counter = 0
            elif not self.moving and interactible.interact_timer and self.current_state != 5 and interactible.isOn["type"]["animation_type"] == "pee":
                self.current_state = 5
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
                self.idle_bis = False
                self.idle_bis_counter = 0
            elif not self.moving and interactible.interact_timer and self.current_state != 4 and interactible.isOn["type"]["animation_type"] == "jumping":
                self.current_state = 4
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
                self.idle_bis = False
                self.idle_bis_counter = 0
            elif not self.moving and interactible.interact_timer and self.current_state != 3 and interactible.isOn["type"]["animation_type"] == "scratching":
                self.current_state = 3
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
                self.idle_bis = False
                self.idle_bis_counter = 0
            elif self.moving and self.i_frame and self.current_state != 2:
                self.current_state = 2
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
                self.idle_bis = False
                self.idle_bis_counter = 0
            elif self.moving and not self.i_frame and self.current_state != 1:
                self.current_state = 1
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
                self.idle_bis = False
                self.idle_bis_counter = 0
            elif not self.moving and not interactible.interact_timer and self.current_state != 0:
                self.current_state = 0
                self.frame = 0
                self.frame_timer = pygame.time.get_ticks()
            elif not self.moving and not interactible.interact_timer and self.current_state == 0 and self.idle_bis_counter == 3:
                self.idle_bis_counter = 0
                self.idle_bis = True
                # self.idle_bis_state = random.randint(0, 1)
                self.idle_bis_state = 0

    def update_frame(self):
        frame_cd = self.frame_cd
        # Loaf Bread
        if self.in_selection:
            state = self.state_selection
            current_state = 0
        # Sleeping
        elif not game_variable.started:
            state = self.state_pregame
            current_state = 0
            frame_cd = 300
        # Transforming
        elif self.transforming:
            state = self.state_chaiyan_transformation
            current_state = 0
        # Chaiyan
        elif self.chaiyan:
            if self.idle_bis:
                state = self.chaiyan_state_idle_bis
                current_state = self.idle_bis_state
            else:
                state = self.chaiyan_state
                current_state = self.current_state
        # Potte
        elif self.potte:
            if self.idle_bis:
                state = self.state_potte_idle_bis
                current_state = self.idle_bis_state
            else:
                state = self.state_potte
                current_state = self.current_state
        # Nyan
        elif self.nyan:
            if self.idle_bis:
                state = self.state_nyan_idle_bis
                current_state = self.idle_bis_state
            else:
                state = self.state_nyan
                current_state = self.current_state
        # Normal
        else:
            if self.idle_bis:
                state = self.idle_bis_list
                current_state = self.idle_bis_state
            else:
                state = self.state
                current_state = self.current_state

        if pygame.time.get_ticks() - self.frame_timer >= frame_cd:
            self.frame += 1
            self.frame_timer = pygame.time.get_ticks()
        if self.frame >= state[current_state].get_width()/state[current_state].get_height():
            self.frame = 0

            if self.current_state == 0:
                if self.transforming:
                    self.transforming = False
                    music.stop_sound(music.CHAIYAN)
                    self.chaiyan = True
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

    def iframe_blinking(self):
        if self.i_frame:
            if pygame.time.get_ticks() - self.i_frame_blinking_timer > self.i_frame_blinking_duration or not self.i_frame_blinking_timer:
                self.i_frame_blinking_timer = pygame.time.get_ticks()
                if self.i_frame_blinking_state:
                    self.i_frame_blinking_state = False
                else:
                    self.i_frame_blinking_state = True

            if self.i_frame_blinking_state:
                new_alpha = self.i_frame_blinking_min_alpha + (255 - self.i_frame_blinking_min_alpha) * ((1 + pygame.time.get_ticks() - self.i_frame_blinking_timer)/self.i_frame_blinking_duration)
            else:
                new_alpha = 255 - (255 - self.i_frame_blinking_min_alpha) * ((1 + pygame.time.get_ticks() - self.i_frame_blinking_timer)/self.i_frame_blinking_duration)
            self.img.set_alpha(new_alpha)
        else:
            self.img.set_alpha(255)

    def apply_wall_filter(self):
        wall_collision = any(player.hitbox.colliderect(wall) for wall in behind_wall_class.walls)
        if wall_collision:
            self.img.set_alpha(50)
        elif not self.i_frame:
            # Si le joueur n'est pas derrière un mur, réinitialiser l'image sans filtre
            self.img.set_alpha(255)

    def change_cat_skin(self):
        if game_variable.selected_cat == "orange":
            self.state = [ORANGE_CAT_IDLE, ORANGE_CAT_WALKING, ORANGE_CAT_RUNNING, ORANGE_CAT_SCRATCHING, ORANGE_CAT_JUMPING, ORANGE_CAT_PEE, ORANGE_CAT_PUKE]
            self.idle_bis_list = [ORANGE_CAT_LICKING]
            self.state_potte = [ORANGE_CAT_IDLE_POTTE, ORANGE_CAT_WALKING_POTTE, ORANGE_CAT_RUNNING_POTTE, ORANGE_CAT_SCRATCHING_POTTE, ORANGE_CAT_JUMPING_POTTE, ORANGE_CAT_PEE_POTTE, ORANGE_CAT_PUKE_POTTE]
            self.state_potte_idle_bis = [ORANGE_CAT_LICKING_POTTE]
            self.state_nyan = [ORANGE_CAT_IDLE_NYAN, ORANGE_CAT_WALKING_NYAN, ORANGE_CAT_RUNNING_NYAN, ORANGE_CAT_SCRATCHING_NYAN, ORANGE_CAT_JUMPING_NYAN, ORANGE_CAT_PEE_NYAN, ORANGE_CAT_PUKE_NYAN]
            self.state_nyan_idle_bis = [ORANGE_CAT_LICKING_NYAN]
            self.state_pregame = [ORANGE_CAT_SLEEPING]
            self.state_chaiyan_transformation = [ORANGE_CAT_TRANSFORM]
        elif game_variable.selected_cat == "black":
            self.state = [BLACK_CAT_IDLE, BLACK_CAT_WALKING, BLACK_CAT_RUNNING, BLACK_CAT_SCRATCHING, BLACK_CAT_JUMPING, BLACK_CAT_PEE, BLACK_CAT_PUKE]
            self.idle_bis_list = [BLACK_CAT_LICKING]
            self.state_potte = [BLACK_CAT_IDLE_POTTE, BLACK_CAT_WALKING_POTTE, BLACK_CAT_RUNNING_POTTE, BLACK_CAT_SCRATCHING_POTTE, BLACK_CAT_JUMPING_POTTE, BLACK_CAT_PEE_POTTE, BLACK_CAT_PUKE_POTTE]
            self.state_potte_idle_bis = [BLACK_CAT_LICKING_POTTE]
            self.state_nyan = [BLACK_CAT_IDLE_NYAN, BLACK_CAT_WALKING_NYAN, BLACK_CAT_RUNNING_NYAN, BLACK_CAT_SCRATCHING_NYAN, BLACK_CAT_JUMPING_NYAN, BLACK_CAT_PEE_NYAN, BLACK_CAT_PUKE_NYAN]
            self.state_nyan_idle_bis = [BLACK_CAT_LICKING_NYAN]
            self.state_pregame = [BLACK_CAT_SLEEPING]
            self.state_chaiyan_transformation = [BLACK_CAT_TRANSFORM]
        elif game_variable.selected_cat == "siamese":
            self.state = [SIAMESE_CAT_IDLE, SIAMESE_CAT_WALKING, SIAMESE_CAT_RUNNING, SIAMESE_CAT_SCRATCHING, SIAMESE_CAT_JUMPING, SIAMESE_CAT_PEE, SIAMESE_CAT_PUKE]
            self.idle_bis_list = [SIAMESE_CAT_LICKING]
            self.state_potte = [SIAMESE_CAT_IDLE_POTTE, SIAMESE_CAT_WALKING_POTTE, SIAMESE_CAT_RUNNING_POTTE, SIAMESE_CAT_SCRATCHING_POTTE, SIAMESE_CAT_JUMPING_POTTE, SIAMESE_CAT_PEE_POTTE, SIAMESE_CAT_PUKE_POTTE]
            self.state_potte_idle_bis = [SIAMESE_CAT_LICKING_POTTE]
            self.state_nyan = [SIAMESE_CAT_IDLE_NYAN, SIAMESE_CAT_WALKING_NYAN, SIAMESE_CAT_RUNNING_NYAN, SIAMESE_CAT_SCRATCHING_NYAN, SIAMESE_CAT_JUMPING_NYAN, SIAMESE_CAT_PEE_NYAN, SIAMESE_CAT_PUKE_NYAN]
            self.state_nyan_idle_bis = [SIAMESE_CAT_LICKING_NYAN]
            self.state_pregame = [SIAMESE_CAT_SLEEPING]
            self.state_chaiyan_transformation = [SIAMESE_CAT_TRANSFORM]
        # Default Skin
        else:
            self.state = [ORANGE_CAT_IDLE, ORANGE_CAT_WALKING, ORANGE_CAT_RUNNING, ORANGE_CAT_SCRATCHING, ORANGE_CAT_JUMPING, ORANGE_CAT_PEE, ORANGE_CAT_PUKE]
            self.idle_bis_list = [ORANGE_CAT_LICKING]
            self.state_potte = [ORANGE_CAT_IDLE_POTTE, ORANGE_CAT_WALKING_POTTE, ORANGE_CAT_RUNNING_POTTE, ORANGE_CAT_SCRATCHING_POTTE, ORANGE_CAT_JUMPING_POTTE, ORANGE_CAT_PEE_POTTE, ORANGE_CAT_PUKE_POTTE]
            self.state_potte_idle_bis = [ORANGE_CAT_LICKING_POTTE]
            self.state_nyan = [ORANGE_CAT_IDLE_NYAN, ORANGE_CAT_WALKING_NYAN, ORANGE_CAT_RUNNING_NYAN, ORANGE_CAT_SCRATCHING_NYAN, ORANGE_CAT_JUMPING_NYAN, ORANGE_CAT_PEE_NYAN, ORANGE_CAT_PUKE_NYAN]
            self.state_nyan_idle_bis = [ORANGE_CAT_LICKING_NYAN]
            self.state_pregame = [ORANGE_CAT_SLEEPING]
            self.state_chaiyan_transformation = [ORANGE_CAT_TRANSFORM]


class owner_class:
    def reset(self):
        self.rage = 0
        self.rage_timer = 0
        self.body = pygame.Rect(1200, 600, 170 * 1.5, 170 * 1.5)
        self.body_hitbox = pygame.Rect(self.body.x, self.body.y, SQUARE, SQUARE)
        self.right = False
        self.target = None
        self.path = []
    
    range = 20
    rage = 0
    max_rage = 100
    rage_timer = 0
    body = pygame.Rect(1200, 600, 170 * 1.5, 170 * 1.5)
    body_hitbox = pygame.Rect(body.x, body.y, SQUARE, SQUARE)
    
    max_speed = 5
    speed = 5
    max_bonus_speed = 5
    bonus_speed = 0

    moving = False
    right = False

    target = None
    path = []

    last_rage_deduction_time = time.time()


    frame = 0
    frame_timer = pygame.time.get_ticks()
    frame_cd = 300
    state = [OWNER_MALE_IDLE, OWNER_MALE_WALKING_HAPPY, OWNER_MALE_WALKING_MEH, OWNER_MALE_WALKING_ANGRY, OWNER_MALE_WALKING_RAGE]
    current_state = 0
    
    img = pygame.Surface((body.width, body.height))

    

    def update(self):
        self.check_rage()

        if (game_variable.score > 0 or game_variable.enraged) and not player.transforming and not game_variable.win:
            self.move_toward_cat()
        else:
            self.moving = False

        self.update_move_speed()

        # Mettez à jour la position de la hitbox
        self.align_body()

        self.change_state()

        self.update_frame()
        
        self.apply_wall_filter()
        
    def change_state(self):
        # Rage
        if self.moving and self.rage / self.max_rage >= 1 and self.current_state != 4:
            self.current_state = 4
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Angry
        if self.moving and self.rage / self.max_rage < 1 and self.rage / self.max_rage >= 0.6 and self.current_state != 3:
            self.current_state = 3
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Meh
        if self.moving and self.rage / self.max_rage < 0.6 and self.rage / self.max_rage >= 0.3 and self.current_state != 2:
            self.current_state = 2
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Happy
        if self.moving and self.current_state != 1:
            self.current_state = 1
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Idle
        if not self.moving and self.current_state != 0:
            self.current_state = 0
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()

    def update_frame(self):
        # Get the correct img slate
        state = self.state
        current_state = self.current_state

        if pygame.time.get_ticks() - self.frame_timer >= self.frame_cd:
            self.frame += 1
            self.frame_timer = pygame.time.get_ticks()
        if self.frame >= state[current_state].get_width()/state[current_state].get_height():
            self.frame = 0

        self.img.fill(ALMOST_BLACK)
        self.img.set_colorkey(ALMOST_BLACK)
        self.img.blit(state[current_state], (0,0), (state[current_state].get_height() * self.frame, 0, state[current_state].get_height(), state[current_state].get_height()))
        if self.right == False:
            self.img = pygame.transform.flip(self.img, 1, 0)

    def align_body(self):
        self.body.centerx= self.body_hitbox.centerx
        self.body.bottom = self.body_hitbox.bottom

    def apply_wall_filter(self):
        wall_collision_owner = any(owner.body_hitbox.colliderect(wall) for wall in behind_wall_class.walls)
        if wall_collision_owner:
            self.img.set_alpha(50)
        else:
            self.img.set_alpha(255)

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
        if time_elapsed >= 2 and self.rage > 0:
            self.rage -= amount
            self.last_rage_deduction_time = current_time

    def check_rage(self):
        if self.rage >= self.max_rage:
            game_variable.enraged = True
            if not self.rage_timer:
                self.rage_timer = time.time()
            elif time.time() - self.rage_timer > game_variable.win_timer:
                player.current_state = 0
                player.moving = False
                game_variable.win = True

    def update_move_speed(self):
        self.bonus_speed = self.max_bonus_speed * (self.rage / self.max_rage)
        if game_variable.enraged:
            self.bonus_speed += 7 + (time.time() - game_variable.timer - game_variable.max_timer)
            if self.bonus_speed > 15:
                self.bonus_speed = 15

    def change_skin(self):
        if game_variable.selected_owner == "male":
            self.state = [OWNER_MALE_IDLE, OWNER_MALE_WALKING_HAPPY, OWNER_MALE_WALKING_MEH, OWNER_MALE_WALKING_ANGRY, OWNER_MALE_WALKING_RAGE]
        elif game_variable.selected_owner == "female":
            self.state = [OWNER_FEMALE_IDLE, OWNER_FEMALE_WALKING_HAPPY, OWNER_FEMALE_WALKING_MEH, OWNER_FEMALE_WALKING_ANGRY, OWNER_FEMALE_WALKING_RAGE]
        # Default Skin
        else:
            self.state = [OWNER_MALE_IDLE, OWNER_MALE_WALKING_HAPPY, OWNER_MALE_WALKING_MEH, OWNER_MALE_WALKING_ANGRY, OWNER_MALE_WALKING_RAGE]


# OBSTACLES

class obstacle_class:

    #Full Map
    topWall = pygame.Rect(0, 0, map.get_width(), SQUARE*4)
    bottomWall = pygame.Rect(0, map.get_height() - SQUARE*3, map.get_width(), SQUARE)
    leftWall = pygame.Rect(0, SQUARE*4, 60, map.get_height()-SQUARE*2)
    rightWall = pygame.Rect(map.get_width() - SQUARE, SQUARE*4, SQUARE, map.get_height()-SQUARE*2)
    #Bedroom
    bedRoomBottomLeftHalf = pygame.Rect(0, SQUARE*16, SQUARE*8, SQUARE)
    bedRoomBottomRightHalf = pygame.Rect(SQUARE*12, SQUARE*16, SQUARE*5, SQUARE)
    bedRoomRightTopHalf= pygame.Rect(SQUARE*17, 0, SQUARE, SQUARE*6)
    bedRoomRightBottomHalf = pygame.Rect(SQUARE*17, SQUARE*10, SQUARE, SQUARE*7)
    bed = pygame.Rect(SQUARE*6, SQUARE*4, SQUARE*6, SQUARE*1)
    nightStandBedroomRight = pygame.Rect(SQUARE*11, SQUARE*4, SQUARE*3, SQUARE)
    nightStandBedroomLeft = pygame.Rect(SQUARE*3, SQUARE*4, SQUARE*3, SQUARE)
    #Bathroom
    bathRoomBottomLeftHalf = pygame.Rect(0, SQUARE*27, SQUARE*8, SQUARE)
    bathRoomBottomRightHalf = pygame.Rect(SQUARE*12, SQUARE*27, SQUARE*5, SQUARE)
    bathRoomRightTopHalf= pygame.Rect(SQUARE*17, SQUARE*17, SQUARE, SQUARE)
    bathRoomRightBottomHalf = pygame.Rect(SQUARE*17, SQUARE*22, SQUARE, SQUARE*6)
    toiletsBathroom = pygame.Rect(SQUARE*3, SQUARE*17, SQUARE, SQUARE)
    bathtubBathroom = pygame.Rect(SQUARE, SQUARE*21, SQUARE*3, SQUARE*7)
    sinkBathroom = pygame.Rect(SQUARE*14, SQUARE*17, SQUARE*2, SQUARE)
    #Hallway
    halwayRightTopHalf = pygame.Rect(SQUARE*16, SQUARE*28, SQUARE, SQUARE*3)
    halwayRightBottomHalf = pygame.Rect(SQUARE*16, SQUARE*28, SQUARE, SQUARE*2)
    shoeCaseHallway = pygame.Rect(SQUARE*2, map.get_height() - SQUARE*10, SQUARE*5, SQUARE)
    plantHallway = pygame.Rect(SQUARE*13, map.get_height() - SQUARE*10, SQUARE*2, SQUARE)
    #Living Room
    couchLivingRoom = pygame.Rect(SQUARE*23, map.get_height()-SQUARE*10, SQUARE*5.5, SQUARE)
    chairLivingRoom = pygame.Rect(SQUARE*30, map.get_height()-SQUARE*8, SQUARE*2, SQUARE)
    tvLivingRoomAndPlant = pygame.Rect(SQUARE*23, map.get_height()-SQUARE*4, SQUARE*7, SQUARE*1)
    libraryLivingRoom = pygame.Rect(SQUARE*17, SQUARE*4, SQUARE*5, SQUARE)
    plantLivingRoom = pygame.Rect(SQUARE*15, map.get_height()-SQUARE*3, SQUARE, SQUARE)
    #Office
    desk = pygame.Rect(map.get_width()-SQUARE*10, SQUARE*22, SQUARE*6, SQUARE)
    deskChair= pygame.Rect(map.get_width()-SQUARE*10, SQUARE*23, SQUARE, SQUARE*2)
    libraryOffice = pygame.Rect(map.get_width()-SQUARE*4, SQUARE*23, SQUARE*3, SQUARE)
    #Kitchen
    kitchenBottom = pygame.Rect(map.get_width()-SQUARE*12,SQUARE*22 , SQUARE*13, SQUARE)
    table = pygame.Rect(map.get_width()-SQUARE*14, SQUARE*9, SQUARE*6, SQUARE*4)
    ovenAndStuff = pygame.Rect(map.get_width()-SQUARE*13, SQUARE*4, SQUARE*12, SQUARE)
    plantKitchen = pygame.Rect(map.get_width()-SQUARE*3, SQUARE*5, SQUARE*2, SQUARE)
  
    kitchen= [kitchenBottom, table, ovenAndStuff, plantKitchen]
    office= [desk, deskChair]
    livingRoom = [couchLivingRoom, tvLivingRoomAndPlant, libraryLivingRoom, chairLivingRoom]
    hallWay= [halwayRightTopHalf, halwayRightBottomHalf, shoeCaseHallway, plantHallway]
    bathRoom= [bathtubBathroom, bathRoomBottomLeftHalf, bathRoomBottomRightHalf, bathRoomRightTopHalf, bathRoomRightBottomHalf]
    bedRoom = [bedRoomBottomLeftHalf, bedRoomBottomRightHalf, bedRoomRightTopHalf,bed, bedRoomRightBottomHalf, nightStandBedroomRight, nightStandBedroomLeft]
    fullMap = [topWall, bottomWall, leftWall, rightWall]
    list = [fullMap, bedRoom, office, kitchen, bathRoom, hallWay, livingRoom]

class behind_wall_class:

    #Walls
    wallBathroomUpLeft = pygame.Rect(SQUARE, SQUARE*12, SQUARE*7, SQUARE*4)
    wallBathroomUpRight = pygame.Rect(SQUARE*12, SQUARE*12, SQUARE*5, SQUARE*4)
    wallKitchenBottom = pygame.Rect(map.get_width()-SQUARE*12, SQUARE*19, SQUARE*11, SQUARE*3)
    wallBathroomBottomRight = pygame.Rect(SQUARE*12, SQUARE*24, SQUARE*5, SQUARE*3)
    wallBathroomBottomLeft = pygame.Rect(SQUARE*4, SQUARE*24, SQUARE*4, SQUARE*3)
    wallTV = pygame.Rect(SQUARE*24, map.get_height()-SQUARE*5.5, SQUARE*4, SQUARE*2)
    wallCouch = pygame.Rect(SQUARE*23.2, map.get_height()-SQUARE*11, SQUARE*5.8, SQUARE)
    wallChairCouch = pygame.Rect(SQUARE*30, map.get_height()-SQUARE*9, SQUARE*2, SQUARE*2)
    wallTable = pygame.Rect(map.get_width()-SQUARE*14, SQUARE*8, SQUARE*6, SQUARE*5)

  
    walls= [wallBathroomUpLeft, wallBathroomUpRight, wallKitchenBottom, wallBathroomBottomRight, wallBathroomBottomLeft, wallTV, wallCouch, wallChairCouch, wallTable]
    list = [walls]

class interactible_class:
    # Sprites glowing
    # BED_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "bed-glowing.png")))
    BED_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "bed-glowing-static.png")))
    
    LIBRARY_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "library-glowing.png")))
    
    COUCH_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "couch-glowing.png")))
    
    CURTAINS_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "curtains-glowing.png")))
    
    BIG_LIBRARY_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "etagere-glowing.png")))
    
    LAMPE_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "lamp-glowing.png")))
    
    COMPUTER_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "computer-glowing.png")))
    
    PLANT_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "plant-glowing.png")))
    
    PQ_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "pq-glowing.png")))
    
    TOWEL_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "towel-glowing.png")))
    
    SHOES_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "shoes-furniture-glowing.png")))
    
    TABLE_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "table-glowing.png")))
    
    RUG_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "carpet-glowing.png")))
    
    COFFEE_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "cup-glowing.png")))
    
    TV_GLOWING = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tv-glowing.png")))


    # Sprites fixed
    BARF_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "barf.png")))

    BED_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "lit-1.png")))
    BED_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "lit-2.png")))

    LIBRARY_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "bibliotheque-1.png")))
    LIBRARY_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "bibliotheque-2.png")))

    COUCH_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "canape-fauteuil-1.png")))
    COUCH_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "canape-fauteuil-2.png")))

    CURTAINS_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "rideau-1.png")))
    CURTAINS_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "rideau-2.png")))

    BIG_LIBRARY_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "etagere-1.png")))
    BIG_LIBRARY_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "etagere-2.png")))

    LAMPE_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "lampe-1.png")))
    LAMPE_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "lampe-2.png")))

    COMPUTER_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "ordinateur-1.png")))
    COMPUTER_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "ordinateur-2.png")))

    PLANT_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "plante-1.png")))
    PLANT_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "plante-2.png")))

    TOILET_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "PQ-1.png")))
    TOILET_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "PQ-2.png")))

    TOWEL_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "serviette-1.png")))
    TOWEL_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "serviette-2.png")))

    SHOES_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "shoes-furniture-1.png")))
    SHOES_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "shoes-furniture-2.png")))

    TABLE_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "table-1.png")))
    TABLE_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "table-2.png")))
    
    RUG_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tapis-1.png")))
    RUG_PUKE_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tapis-barf-1.png")))

    COFFEE_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tasse-1.png")))
    COFFEE_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tasse-2.png")))

    TV_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tv-1.png")))
    TV_BROKEN_IMG = pygame.image.load(os.path.join("assets", os.path.join("interactive-assets", "tv-2.png")))



    # Types
    type_bed = {"type" : "bed", "score" : 500, "multiplier" : 0.5, "duration" : 3.5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3, "rage_amount" : 30, "animation_type" : "pee", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : BED_IMG, "sprite_broken" : BED_BROKEN_IMG}

    type_library = {"type" : "library", "score" : 250, "multiplier" : 0.5, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 20, "rage_amount" : 10, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : LIBRARY_IMG, "sprite_broken" : LIBRARY_BROKEN_IMG}

    type_couch = {"type" : "couch", "score" : 200, "multiplier" : 0.3, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10, "rage_amount" : 10, "animation_type" : "scratching", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : COUCH_IMG, "sprite_broken" : COUCH_BROKEN_IMG}

    type_curtains = {"type" : "curtains", "score" : 100, "multiplier" : 0.1, "duration" : 1, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3, "rage_amount" : 10, "animation_type" : "scratching", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : CURTAINS_IMG, "sprite_broken" : CURTAINS_BROKEN_IMG}

    type_big_library = {"type" : "big_library", "score" : 500, "multiplier" : 0.5, "duration" : 3.5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 20, "rage_amount" : 15, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : BIG_LIBRARY_IMG, "sprite_broken" : BIG_LIBRARY_BROKEN_IMG}

    type_plug = {"type" : "plug", "score" : 300, "multiplier" : 0.3, "duration" : 2.5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10, "rage_amount" : 20, "animation_type" : "scratching", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : LAMPE_IMG, "sprite_broken" : LAMPE_BROKEN_IMG}

    type_plugOffice = {"type" : "computer", "score" : 500, "multiplier" : 0.5, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 30, "rage_amount" : 10, "animation_type" : "scratching", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : COMPUTER_IMG, "sprite_broken" : COMPUTER_BROKEN_IMG}

    type_plant = {"type" : "plant", "score" : 1000, "multiplier" : 0.5, "duration" : 1, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 10, "rage_amount" : 15, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : PLANT_IMG, "sprite_broken" : PLANT_BROKEN_IMG}
   
    type_pq = {"type" : "toilet_paper", "score" : 100, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3, "rage_amount" : 5, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : TOILET_IMG, "sprite_broken" : TOILET_BROKEN_IMG}
   
    type_towel = {"type" : "towel", "score" : 300, "multiplier" : 0.3, "duration" : 2.5, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3, "rage_amount" : 5, "animation_type" : "scratching", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : TOWEL_IMG, "sprite_broken" : TOWEL_BROKEN_IMG}

    type_shoeCase = {"type" : "shoe_case", "score" : 500, "multiplier" : 0.5, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 15, "rage_amount" : 10, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : SHOES_IMG, "sprite_broken" : SHOES_BROKEN_IMG}
    
    type_chair = {"type" : "chair", "score" : 100, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5, "rage_amount" : 5, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : TABLE_IMG, "sprite_broken" : TABLE_BROKEN_IMG}

    type_Rug = {"type" : "rug", "score" : 200, "multiplier" : 0.3, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 3, "rage_amount" : 10, "animation_type" : "puke", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : RUG_IMG, "sprite_broken" : RUG_PUKE_IMG}

    type_coffee = {"type" : "coffee", "score" : 200, "multiplier" : 0.2, "duration" : 2, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5, "rage_amount" : 20, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : COFFEE_IMG, "sprite_broken" : COFFEE_BROKEN_IMG}

    type_tv = {"type" : "tv", "score" : 1000, "multiplier" : 0.5, "duration" : 3, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 5, "rage_amount" : 30, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : TV_IMG, "sprite_broken" : TV_BROKEN_IMG}

    # type_trashCan = {"type" : "trash_can", "score" : 400, "multiplier" : 0.4, "duration" : 4, "is_enabled" : True, "disabled_timer" : None, "disabled_duration" : 15, "rage_amount" : 15, "animation_type" : "jumping", "sprite_glowing" : None, "frame" : 0, "frame_timer" : 0, "frame_cd" : 120, "frame_max" : 0, "img" : pygame.Surface((10,10)), "sprite" : None, "sprite_broken" : None}

    # Objects
    rug= {"rect" : pygame.Rect(SQUARE*21, map.get_height()-SQUARE*12, SQUARE*10, SQUARE*7), "type" : type_Rug.copy()}
    bed = {"rect" : pygame.Rect(SQUARE*6, SQUARE*3, SQUARE*6, SQUARE*5), "type" : type_bed.copy()}
    libraryOffice = {"rect" : pygame.Rect(map.get_width()-SQUARE*4, SQUARE*22, SQUARE*3, SQUARE*3), "type" : type_library.copy()}
    couch =  {"rect" : pygame.Rect(map.get_width()-SQUARE*19, map.get_height()-SQUARE*11, SQUARE*6.5, SQUARE*3), "type" : type_couch.copy()}
    curtains_bedroom = {"rect" : pygame.Rect(SQUARE*12, SQUARE*1, SQUARE*4, SQUARE*5), "type" : type_curtains.copy()}
    curtains_living_room = {"rect" : pygame.Rect(SQUARE*24, SQUARE*1, SQUARE*4, SQUARE*5), "type" : type_curtains.copy()}
    shelf =  {"rect" : pygame.Rect(SQUARE*18, SQUARE*4, SQUARE*5, SQUARE*2), "type" : type_big_library.copy()}
    living_room_lamp =  {"rect" : pygame.Rect(map.get_width()-SQUARE*3, map.get_height()-SQUARE*5, SQUARE*2, SQUARE*2), "type" : type_plug.copy()}
    nightStandPlug = {"rect" : pygame.Rect(SQUARE, SQUARE*4, SQUARE*2, SQUARE*2), "type" : type_plug.copy()}
    computer = {"rect" : pygame.Rect(map.get_width()-SQUARE*9, SQUARE*21, SQUARE*2, SQUARE*3), "type" : type_plugOffice.copy()}
    plantHallway= {"rect" : pygame.Rect(SQUARE*13, map.get_height()-SQUARE*10, SQUARE*3, SQUARE*2), "type" : type_plant.copy()}
    plantKitchen= {"rect" : pygame.Rect(map.get_width()-SQUARE*3, SQUARE*5, SQUARE*2, SQUARE*2), "type" : type_plant.copy()}
    pq = {"rect" : pygame.Rect(SQUARE*5, SQUARE*15, SQUARE*2, SQUARE*3), "type" : type_pq.copy()}
    towel = {"rect" : pygame.Rect(SQUARE*12, SQUARE*15, SQUARE*2, SQUARE*3), "type" : type_towel.copy()}
    shoeCase =  {"rect" : pygame.Rect(SQUARE, map.get_height()- SQUARE*12, SQUARE*7, SQUARE*4), "type" : type_shoeCase.copy()}
    kitchen_table =  {"rect" : pygame.Rect(map.get_width()-SQUARE*15, SQUARE*8, SQUARE*8, SQUARE*7), "type" : type_chair.copy()}
    coffee = {"rect" : pygame.Rect(map.get_width()-SQUARE*6, SQUARE*22, SQUARE*2, SQUARE*2), "type" : type_coffee.copy()}
    tv = {"rect" : pygame.Rect(map.get_width()-SQUARE*19, map.get_height() - SQUARE*5, SQUARE*6, SQUARE*2), "type" : type_tv.copy()}
    # trash =  {"rect" : pygame.Rect(map.get_width()-SQUARE*6, SQUARE, SQUARE*3, SQUARE*2), "type" : type_trashCan.copy()}
    

    list = [rug, bed, libraryOffice, couch, curtains_bedroom, curtains_living_room, shelf, living_room_lamp, nightStandPlug, computer, plantHallway, plantKitchen, pq, towel, shoeCase, kitchen_table,  coffee, tv]
    # list = [kitchen_table, living_room_lamp, shelf, rug, shoeCase, nightStandPlug, plantHallway, plantKitchen, computer, coffee, couch, libraryOffice, pq, bed, curtains_bedroom, curtains_living_room]

    isOn = None
    interact_timer = None
    
    PROGRESS_BAR = pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//3 * 2 + 150, 200, 25)
    PROGRESS_BAR_FILL = pygame.Rect(PROGRESS_BAR.x + 1, PROGRESS_BAR.y + 1, 0, PROGRESS_BAR.height - 2)

    def update(self):
        self.isOnInteractible()
        # self.restore_interactibles()

        for item in self.list:
            if item["type"]["sprite_glowing"]:
                self.animate_interactibles(item)

    def reset(self):
        for item in self.list:
            item["type"]["is_enabled"] = True
            item["type"]["disabled_timer"] = None

    def isOnInteractible(self):
        for item in self.list:
            if item["rect"].collidepoint(player.hitbox.center) and item["type"]["is_enabled"]:
                self.isOn = item
                return
        
        self.isOn = None
        
    def animate_interactibles(self, item):
        if pygame.time.get_ticks() - item["type"]["frame_timer"] >= item["type"]["frame_cd"]:
            item["type"]["frame"] += 1
            item["type"]["frame_timer"] = pygame.time.get_ticks()
        if item["type"]["frame_max"]:
            if item["type"]["frame"] >= item["type"]["frame_max"] - 1:
                item["type"]["frame"] = 0
        elif item["type"]["frame"] >= item["type"]["sprite_glowing"].get_width()/item["type"]["sprite_glowing"].get_height():
            item["type"]["frame"] = 0


        if item["type"]["frame_max"]:
            frame_width = item["type"]["sprite_glowing"].get_width()/item["type"]["frame_max"]
        else:
            frame_width = item["type"]["sprite_glowing"].get_height()

        item["type"]["img"] = pygame.Surface((frame_width, item["type"]["sprite_glowing"].get_height()))
        item["type"]["img"].fill(ALMOST_BLACK)
        item["type"]["img"].set_colorkey(ALMOST_BLACK)
        item["type"]["img"].blit(item["type"]["sprite_glowing"], (0,0), (frame_width * item["type"]["frame"], 0, frame_width, item["type"]["sprite_glowing"].get_height()))

    def interact(self):
        if self.isOn:
            if self.interact_timer == None:
                self.interact_timer = time.time()
                if self.isOn["type"]["type"] == "toilet_paper":
                    music.play_sound(music.TOILET_PAPER, 1)

            elif time.time() - self.interact_timer > self.isOn["type"]["duration"]:
                game_variable.score += int(self.isOn["type"]["score"] * game_variable.multiplier)
                game_variable.multiplier += self.isOn["type"]["multiplier"]
                index = self.list.index(self.isOn)
                self.list[index]["type"]["is_enabled"] = False
                self.list[index]["type"]["disabled_timer"] = time.time()
                self.interact_timer = None
                owner.add_rage(self.list[index]["type"]["rage_amount"])
                if self.isOn["type"]["type"] == "bed":
                    music.play_sound(music.MEOW_1)
                elif self.isOn["type"]["type"] == "library":
                    music.play_sound(music.FALLING_OBJECT)
                elif self.isOn["type"]["type"] == "couch":
                    music.play_sound(music.SCRATCH)
                elif self.isOn["type"]["type"] == "curtains":
                    music.play_sound(music.SCRATCH)
                elif self.isOn["type"]["type"] == "big_library":
                    music.play_sound(music.GLASS_BREAKING_1)
                elif self.isOn["type"]["type"] == "plug":
                    music.play_sound(music.ELECTRIC)
                elif self.isOn["type"]["type"] == "computer":
                    player.nyan = True
                    player.potte = False
                    music.play_sound(music.MEOW_1)
                    music.play_music(music.NYAN_CAT_THEME)
                    animation.transformation_cloud_animation()
                elif self.isOn["type"]["type"] == "plant":
                    music.play_sound(music.GLASS_BREAKING_1)
                elif self.isOn["type"]["type"] == "toilet_paper":
                    music.stop_sound(music.TOILET_PAPER)
                elif self.isOn["type"]["type"] == "towel":
                    music.play_sound(music.TOILET_PAPER)
                elif self.isOn["type"]["type"] == "shoe_case":
                    player.potte = True
                    player.nyan = False
                    music.play_sound(music.MEOW_2)
                    music.play_music(music.POTTE_CAT_THEME)
                    animation.transformation_cloud_animation()
                elif self.isOn["type"]["type"] == "chair":
                    music.play_sound(music.FALLING_OBJECT)
                elif self.isOn["type"]["type"] == "rug":
                    music.play_sound(music.MEOW_3)
                elif self.isOn["type"]["type"] == "coffee":
                    music.play_sound(music.GLASS_BREAKING_2)
                elif self.isOn["type"]["type"] == "tv":
                    music.play_sound(music.GLASS_BREAKING_1)
                # elif self.isOn["type"]["type"] == "trash_can":
                #     pass


            self.update_progress_bar()

    def cancel_interact(self):
        self.interact_timer = None
        if self.isOn["type"]["type"] == "toilet_paper":
            music.stop_sound(music.TOILET_PAPER)

    def update_progress_bar(self):
        if self.interact_timer:
            self.PROGRESS_BAR_FILL.width = (self.PROGRESS_BAR.width - 2) * (1 - (time.time() - self.interact_timer) / self.isOn["type"]["duration"])

    def restore_interactibles(self):
        for item in self.list:
            if not item["type"]["is_enabled"]:
                if time.time() - item["type"]["disabled_timer"] > item["type"]["disabled_duration"]:
                    item["type"]["disabled_timer"] = None
                    item["type"]["is_enabled"] = True

    def display_interactibles(self):
        for item in interactible.list:
            item_type = item["type"]["type"]

            if item["type"]["sprite"]:
                sprite_position = (item["rect"].x, item["rect"].y)

                sprite = item["type"]["sprite"]

                if interactible.isOn == item:
                    if item["type"]["type"] == "bed":
                        sprite = interactible.BED_GLOWING
                    elif item["type"]["type"] == "library":
                        sprite = interactible.LIBRARY_GLOWING
                    elif item["type"]["type"] == "couch":
                        sprite = interactible.COUCH_GLOWING
                    elif item["type"]["type"] == "curtains":
                        sprite = interactible.CURTAINS_GLOWING
                    elif item["type"]["type"] == "big_library":
                        sprite = interactible.BIG_LIBRARY_GLOWING
                    elif item["type"]["type"] == "plug":
                        sprite = interactible.LAMPE_GLOWING
                    elif item["type"]["type"] == "computer":
                        sprite = interactible.COMPUTER_GLOWING
                    elif item["type"]["type"] == "plant":
                        sprite = interactible.PLANT_GLOWING
                    elif item["type"]["type"] == "toilet_paper":
                        sprite = interactible.PQ_GLOWING
                    elif item["type"]["type"] == "towel":
                        sprite = interactible.TOWEL_GLOWING
                    elif item["type"]["type"] == "shoe_case":
                        sprite = interactible.SHOES_GLOWING
                    elif item["type"]["type"] == "chair":
                        sprite = interactible.TABLE_GLOWING
                    elif item["type"]["type"] == "rug":
                        sprite = interactible.RUG_GLOWING
                    elif item["type"]["type"] == "coffee":
                        sprite = interactible.COFFEE_GLOWING
                    elif item["type"]["type"] == "tv":
                        sprite = interactible.TV_GLOWING

                sprite_dict = {
                    "bed": (item["rect"].x - 10, item["rect"].y - SQUARE),
                    "curtains": (item["rect"].x - 22, item["rect"].y - SQUARE + 15),
                    "toilet_paper": (item["rect"].x - 25, item["rect"].y - 15),
                    "plant": (item["rect"].x, item["rect"].y - SQUARE*2),
                    "plug": (item["rect"].x, item["rect"].y - SQUARE*2),
                    "library": (item["rect"].x - SQUARE*2, item["rect"].y - SQUARE*2),
                    "big_library": (item["rect"].x, item["rect"].y - SQUARE*2),
                    "chair": (item["rect"].x + SQUARE, item["rect"].y),
                    "shoe_case": (item["rect"].x + SQUARE, item["rect"].y),
                    "tv": (item["rect"].x + 30, item["rect"].y - SQUARE - 45)
                    # Ajoutez d'autres types avec leurs positions respectives ici
                }
                sprite_dict_broken = {
                    "bed": (item["rect"].x - 9, item["rect"].y - 14),
                    "toilet_paper": (item["rect"].x + 8, item["rect"].y + 22),
                    "towel": (item["rect"].x + 11, item["rect"].y + 33),
                    "plant": (item["rect"].x- SQUARE*2, item["rect"].y),
                    "plug": (item["rect"].x-20, item["rect"].y - SQUARE*2),
                    "library": (item["rect"].x - SQUARE*2, item["rect"].y - SQUARE*2),
                    "big_library": (item["rect"].x, item["rect"].y - SQUARE*2),
                    "chair": (item["rect"].x + 17, item["rect"].y - 24),
                    "shoe_case": (item["rect"].x + SQUARE, item["rect"].y),
                    "tv": (item["rect"].x + 50, item["rect"].y - SQUARE - 40)

                }

                if item["type"]["is_enabled"]:
                    map.blit(sprite, sprite_dict.get(item_type, sprite_position))
                else:
                    map.blit(item["type"]["sprite_broken"], sprite_dict_broken.get(item_type, sprite_position))

# TOOLS

class animation_class:
    def reset(self):
        self.list = []

    cloud_img = img_load.image_loader.load(["assets", "effects", "interaction-effect-potte.png"], 2)

    list = []

    def transformation_cloud_animation(self):
        anim = {"type" : "cloud", "positions" : player.hitbox, "img" : self.cloud_img, "surface" : pygame.Surface((self.cloud_img.get_width(), self.cloud_img.get_height())), "frame" : 0, "frame_timer" : pygame.time.get_ticks(), "frame_cd" : 60}
        animation.list.append(anim)

    def update_animation(self, anim):
        if pygame.time.get_ticks() - anim["frame_timer"] >= anim["frame_cd"]:
            anim["frame"] += 1
            anim["frame_timer"] = pygame.time.get_ticks()
        if anim["frame"] >= anim["img"].get_width()/anim["img"].get_height():
            anim["frame"] = -1

        anim["surface"].fill(ALMOST_BLACK)
        anim["surface"].set_colorkey(ALMOST_BLACK)
        anim["surface"].blit(anim["img"], (0,0), (anim["img"].get_height() * anim["frame"], 0, anim["img"].get_height(), anim["img"].get_height()))
        map.blit(anim["surface"], (anim["positions"].centerx - anim["img"].get_height()//2, anim["positions"].centery - anim["img"].get_height()//2))

    def play_animations(self):
        to_be_removed = []
        for anim in self.list:
            self.update_animation(anim)
            
            if anim["frame"] == -1:
                to_be_removed.append(anim)

        for anim in to_be_removed:
            self.list.remove(anim)


class grid_class:
    def __init__(self):
        self.initialGrid()
        self.get_cat_position()
        self.get_owner_position()

    grid = []
    maze = []
    cat_position = None
    owner_position = None

    solver_cd = 1
    solver_timer = 0

    def update(self):
        self.get_cat_position()
        self.get_owner_position()

        if time.time() - self.solver_timer > self.solver_cd:
            pathfinder.create_path()
            self.solver_timer = time.time()

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
        pathfinder.owner_pos, pathfinder.cat_pos = grid.owner_position, grid.cat_position
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

# MAIN GAME
        
class end_game_class:
    SPACESHIP_CLOSED = img_load.image_loader.load(["assets", "alien", "space-ship-closed.png"], 1)
    SPACESHIP_OPENING = img_load.image_loader.load(["assets", "alien", "space-ship-opening.png"], 1)
    SPACESHIP_OPEN = img_load.image_loader.load(["assets", "alien", "space-ship-open.png"], 1)
    SPACESHIP_OPEN_LASER = img_load.image_loader.load(["assets", "alien", "space-ship-open-laser.png"], 1)
    SPACESHIP_STEAL_CAT = img_load.image_loader.load(["assets", "alien", "space-ship-steal-cat.png"], 1)
    SPACESHIP_END_LASER = img_load.image_loader.load(["assets", "alien", "space-ship-end-laser.png"], 1)
    SPACESHIP_CLOSING = img_load.image_loader.load(["assets", "alien", "space-ship-closing.png"], 1)
    
    ALIEN_SOUND_1 = pygame.mixer.Sound(os.path.join("assets", os.path.join("music", "alien-spaceship-1.mp3")))
    ALIEN_SOUND_2 = pygame.mixer.Sound(os.path.join("assets", os.path.join("music", "alien-spaceship-2.mp3")))
    ALIEN_SOUND_3 = pygame.mixer.Sound(os.path.join("assets", os.path.join("music", "alien-spaceship-3.mp3")))

    opened = False
    cat_caught = False
    in_position = False
    laser_on = False

    img = pygame.Surface((SPACESHIP_CLOSED.get_height(), SPACESHIP_CLOSED.get_height()))

    alien_body = pygame.Rect(map.get_width() + img.get_width() + 50, 0, SPACESHIP_CLOSED.get_height(), SPACESHIP_CLOSED.get_height())
    alien_hitbox = pygame.Rect(map.get_width() + img.get_width() + 50, 0, 100, 100)

    frame = 0
    frame_timer = pygame.time.get_ticks()
    frame_cd = 300
    state = [SPACESHIP_CLOSED, SPACESHIP_OPENING, SPACESHIP_OPEN, SPACESHIP_OPEN_LASER, SPACESHIP_STEAL_CAT, SPACESHIP_END_LASER, SPACESHIP_CLOSING]
    current_state = 0

    def update(self):
        self.align_body()

        if game_variable.win:
            self.move()

        self.change_state()

        self.update_frame()

    def align_body(self):
        self.alien_body.centerx = self.alien_hitbox.centerx
        if not game_variable.win:
            self.alien_hitbox.y = player.hitbox.y - 200
        self.alien_body.y = self.alien_hitbox.y

    def move(self):
        if not self.in_position and not self.cat_caught:
            if self.alien_hitbox.centerx > player.hitbox.centerx:
                self.alien_hitbox.centerx -= 50
                if self.alien_hitbox.centerx < player.hitbox.centerx:
                    self.alien_hitbox.centerx = player.hitbox.centerx
                    self.in_position = True
                    print("in position : ", self.in_position)

        elif self.cat_caught and not self.laser_on and self.opened:
            self.alien_hitbox.centery -= 5
            if self.alien_hitbox.centery <= self.alien_hitbox.height - 100:
                game_variable.end_win_cinematic = True

    def change_state(self):
        # Closing
        if self.opened and self.in_position and not self.laser_on and self.cat_caught and self.current_state != 6:
            print("Closing")
            self.current_state = 6
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # End Laser
        elif self.opened and self.in_position and self.laser_on and self.cat_caught and self.current_state != 5:
            print("End Laser")
            self.current_state = 5
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Stealing cat
        elif self.opened and self.in_position and self.laser_on and not self.cat_caught and self.current_state != 4:
            print("Stealing cat")
            self.current_state = 4
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Open Laser
        elif self.opened and self.in_position and not self.laser_on and self.current_state != 3:
            print("Open Laser")
            self.current_state = 3
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Open
        # elif self.opened and self.in_position and self.current_state != 2:
        #     print("Open")
        #     self.current_state = 2
        #     self.frame = 0
        #     self.frame_timer = pygame.time.get_ticks()
        # Opening
        elif not self.opened and self.in_position and self.current_state != 1:
        # elif self.in_position and self.current_state != 1:
            print("opening")
            self.current_state = 1
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()
        # Closed
        elif not self.in_position and self.current_state != 0:
            self.current_state = 0
            self.frame = 0
            self.frame_timer = pygame.time.get_ticks()

    def update_frame(self):
        frame_cd = self.frame_cd
        state = self.state
        current_state = self.current_state

        if pygame.time.get_ticks() - self.frame_timer >= frame_cd:
            self.frame += 1
            self.frame_timer = pygame.time.get_ticks()
        if self.frame >= state[current_state].get_width()/state[current_state].get_height():
            self.frame = 0

            if current_state == 1:
                self.opened = True
            elif current_state == 3:
                self.laser_on = True
            elif current_state == 4:
                self.cat_caught = True
            elif current_state == 5:
                self.laser_on = False
            elif current_state == 6:
                self.opened = False


        self.img.fill(ALMOST_BLACK)
        self.img.set_colorkey(ALMOST_BLACK)
        self.img.blit(state[current_state], (0,0), (state[current_state].get_height() * self.frame, 0, state[current_state].get_height(), state[current_state].get_height()))

class game_win_class:
    GAME_WIN_BG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "you-win.jpg")))

    def draw_window(self):
        screen.blit(self.GAME_WIN_BG, (0,0))
        
        score_text = font.render(f"{game_variable.score}", 1, BLACK)
        screen.blit(score_text, (1000, 727))

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
        music.play_music(music.WIN)
        
        # grid.solver()
        while run:
            clock.tick(60)

            player.update()

            if click or interact:
                music.play_sound(music.BUTTON)
                run = False

            miaou = False
            interact = False
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON)
                        run = False
                    if event.key == K_e:
                        interact = True
                    if event.key == K_SPACE:
                        miaou = True
            self.draw_window()
            
        music.play_music(music.MAIN_THEME)

class game_over_class:
    GAME_OVER_BG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "game-over-screen.jpg")))

    def draw_window(self):
        screen.blit(self.GAME_OVER_BG, (0,0))
        
        score_text = font.render(f"{game_variable.score}", 1, BLACK)
        screen.blit(score_text, (1000, 727))

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
        music.play_music(music.LOSE)
        
        # grid.solver()
        while run:
            clock.tick(60)

            player.update()

            if click or interact:
                music.play_sound(music.BUTTON)
                run = False

            miaou = False
            interact = False
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON)
                        run = False
                    if event.key == K_e:
                        interact = True
                    if event.key == K_SPACE:
                        miaou = True
            self.draw_window()
            
        music.play_music(music.MAIN_THEME)

class game_ui_class:
    ACHIEVEMENT_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "achievement-unlock.png")))

    LOWER_LEFT_PANNEL_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "fond-gauche-jauges.png")))
    LOWER_LEFT_PANNEL_RECT = pygame.Rect(25, HEIGHT - 25 - LOWER_LEFT_PANNEL_IMG.get_height(), LOWER_LEFT_PANNEL_IMG.get_width(), LOWER_LEFT_PANNEL_IMG.get_height())

    LOWER_MIDDLE_PANNEL_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "timer-background.png")))
    LOWER_MIDDLE_PANNEL_RECT = pygame.Rect(WIDTH//2 - LOWER_MIDDLE_PANNEL_IMG.get_width()//2, HEIGHT - 25 - LOWER_MIDDLE_PANNEL_IMG.get_height(), LOWER_MIDDLE_PANNEL_IMG.get_width(), LOWER_MIDDLE_PANNEL_IMG.get_height())

    LOWER_RIGHT_PANNEL_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "white-background-area.png")))
    LOWER_RIGHT_PANNEL_RECT = pygame.Rect(WIDTH - 25 - LOWER_RIGHT_PANNEL_IMG.get_width(), HEIGHT - 25 - LOWER_RIGHT_PANNEL_IMG.get_height(), LOWER_RIGHT_PANNEL_IMG.get_width(), LOWER_RIGHT_PANNEL_IMG.get_height())

    HEART_0_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "heart-0-3.png")))
    HEART_1_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "heart-1-3.png")))
    HEART_2_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "heart-2-3.png")))
    HEART_3_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "heart-3-3.png")))
    
    HOURGLASS_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "hourglass-icon.png")))

    CAT_HEAD_ORANGE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "tete-chat-orange.png")))
    CAT_HEAD_BLACK_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "tete-chat-noir.png")))
    CAT_HEAD_SIAMESE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "tete-chat-siamese.png")))

    RAGE_BAR_0_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-1.png")))
    RAGE_BAR_1_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-2.png")))
    RAGE_BAR_2_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-3.png")))
    RAGE_BAR_3_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-4.png")))
    RAGE_BAR_4_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-5.png")))
    RAGE_BAR_5_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-6.png")))
    RAGE_BAR_6_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "jauge-niveau-7.png")))

    spacer = 40

    def draw_ui(self):
        # Left Pannel
        screen.blit(self.LOWER_LEFT_PANNEL_IMG, (self.LOWER_LEFT_PANNEL_RECT.x, self.LOWER_LEFT_PANNEL_RECT.y))
        
        if game_variable.selected_cat == "black":
            screen.blit(self.CAT_HEAD_BLACK_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.spacer * 1, self.LOWER_LEFT_PANNEL_RECT.centery - self.CAT_HEAD_BLACK_IMG.get_height()//2))
        elif game_variable.selected_cat == "siamese":
            screen.blit(self.CAT_HEAD_SIAMESE_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.spacer * 1, self.LOWER_LEFT_PANNEL_RECT.centery - self.CAT_HEAD_SIAMESE_IMG.get_height()//2))
        else:
            screen.blit(self.CAT_HEAD_ORANGE_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.spacer * 1, self.LOWER_LEFT_PANNEL_RECT.centery - self.CAT_HEAD_ORANGE_IMG.get_height()//2))
        
        if player.hp > 2:
            screen.blit(self.HEART_3_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.spacer * 2, self.LOWER_LEFT_PANNEL_RECT.centery - self.HEART_3_IMG.get_height()//2))
        elif player.hp > 1:
            screen.blit(self.HEART_2_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.spacer * 2, self.LOWER_LEFT_PANNEL_RECT.centery - self.HEART_2_IMG.get_height()//2))
        elif player.hp > 0:
            screen.blit(self.HEART_1_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.spacer * 2, self.LOWER_LEFT_PANNEL_RECT.centery - self.HEART_1_IMG.get_height()//2))
        else:
            screen.blit(self.HEART_0_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.spacer * 2, self.LOWER_LEFT_PANNEL_RECT.centery - self.HEART_0_IMG.get_height()//2))

        rage_meter = owner.rage / owner.max_rage
        if rage_meter >= 0.9:
            screen.blit(self.RAGE_BAR_6_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_6_IMG.get_height()//2))
        elif rage_meter < 0.9 and rage_meter >= 0.7:
            screen.blit(self.RAGE_BAR_5_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_5_IMG.get_height()//2))
        elif rage_meter < 0.7 and rage_meter >= 0.5:
            screen.blit(self.RAGE_BAR_4_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_4_IMG.get_height()//2))
        elif rage_meter < 0.5 and rage_meter >= 0.3:
            screen.blit(self.RAGE_BAR_3_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_3_IMG.get_height()//2))
        elif rage_meter < 0.3 and rage_meter >= 0.1:
            screen.blit(self.RAGE_BAR_2_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_2_IMG.get_height()//2))
        elif rage_meter < 0.1 and rage_meter > 0:
            screen.blit(self.RAGE_BAR_1_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_1_IMG.get_height()//2))
        else:
            screen.blit(self.RAGE_BAR_0_IMG, (self.LOWER_LEFT_PANNEL_RECT.x + self.CAT_HEAD_ORANGE_IMG.get_width() + self.HEART_3_IMG.get_width() + self.spacer * 3, self.LOWER_LEFT_PANNEL_RECT.centery - self.RAGE_BAR_0_IMG.get_height()//2))

        # Middle Pannel
        screen.blit(self.LOWER_MIDDLE_PANNEL_IMG, (self.LOWER_MIDDLE_PANNEL_RECT.x, self.LOWER_MIDDLE_PANNEL_RECT.y))
        if game_variable.started:
            if owner.rage_timer:
                if game_variable.win:
                    time_text = font.render(f"???", 1, BLACK)
                else:
                    time_text = font.render(f"{(game_variable.win_timer - (time.time() - owner.rage_timer)):.2f} s", 1, BLACK)
            elif game_variable.max_timer - (time.time() - game_variable.timer) < 0:
                time_text = font.render(f"RUN !", 1, BLACK)
            else:
                time_text = font.render(f"{game_variable.max_timer - (time.time() - game_variable.timer):.2f} s", 1, BLACK)
        else:
            time_text = font.render(f"{game_variable.max_timer} s", 1, BLACK)
        screen.blit(time_text, (self.LOWER_MIDDLE_PANNEL_RECT.right - time_text.get_width() - self.spacer * 1, self.LOWER_MIDDLE_PANNEL_RECT.centery - time_text.get_height()//2))


        # Right Pannel
        screen.blit(self.LOWER_RIGHT_PANNEL_IMG, (self.LOWER_RIGHT_PANNEL_RECT.x, self.LOWER_RIGHT_PANNEL_RECT.y))

        score_text = font.render(f"SCORE : {game_variable.score}", 1, BLACK)
        screen.blit(score_text, (self.LOWER_RIGHT_PANNEL_RECT.x + 20 , self.LOWER_RIGHT_PANNEL_RECT.centery - score_text.get_height()//2))

        multiplier_text = font.render(f"MULTIPLIER : {game_variable.multiplier:.1f}", 1, BLACK)
        screen.blit(multiplier_text, (self.LOWER_RIGHT_PANNEL_RECT.x + 20 + score_text.get_width() + self.spacer * 1, self.LOWER_RIGHT_PANNEL_RECT.centery - multiplier_text.get_height()//2))

class button_smash_class:
    IMG_1 = pygame.image.load(os.path.join("assets", os.path.join("minigame", "ORA1.png")))
    IMG_2 = pygame.image.load(os.path.join("assets", os.path.join("minigame", "ORA2.png")))

    SOUND = pygame.mixer.Sound(os.path.join('assets', os.path.join("minigame", "ora-ora.mp3")))

    LEFT_BUTTON = pygame.Rect(WIDTH//2 - 150, HEIGHT//4 * 3, 70, 70)
    RIGHT_BUTTON = pygame.Rect(WIDTH//2 + 100, HEIGHT//4 * 3, 70, 70)

    TIMER_BAR = pygame.Rect(WIDTH//2 - 101, HEIGHT//4 - 1, 202, 32)
    TIMER_BAR_PROGRESS = pygame.Rect(WIDTH//2 - 100, HEIGHT//4, 200, 30)

    max_break_free = 40
    break_free = 40
    timer = 0
    max_timer = 5
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
        screen.blit(break_free_text, (WIDTH//2 - break_free_text.get_width()//2, 150))
        
        if not self.smash_right:
            screen.blit(settings.Q_KEY_IMG, (self.LEFT_BUTTON.centerx - settings.Q_KEY_IMG.get_width()//2, self.LEFT_BUTTON.centery - settings.Q_KEY_IMG.get_height()//2))

        if self.smash_right:
            screen.blit(settings.D_KEY_IMG, (self.RIGHT_BUTTON.centerx - settings.D_KEY_IMG.get_width()//2, self.RIGHT_BUTTON.centery - settings.D_KEY_IMG.get_height()//2))

        pygame.draw.rect(screen, BLACK, self.TIMER_BAR)
        self.update_progress_bar()
        pygame.draw.rect(screen, YELLOW, self.TIMER_BAR_PROGRESS)

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        self.smash_right = True
        self.break_free = self.max_break_free
        self.timer = time.time()
        self.SOUND.play()
        self.SOUND.set_volume(0.5)
        
        while run:
            clock.tick(60)

            if time.time() - self.timer > self.max_timer:
                self.SOUND.stop()
                return False
            
            if self.smash_right and right:
                self.smash_right = False
                self.break_free -= 1
            elif not self.smash_right and left:
                self.smash_right = True
                self.break_free -= 1

            if self.break_free <= 0:
                self.SOUND.stop()
                return True

            left = False
            right = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.SOUND.stop()
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.SOUND.stop()
                        return False
                    if event.key == K_q:
                        left = True
                    if event.key == K_d:
                        right = True
            self.draw_window()

class super_chaiyan_class:
    IMG_1 = pygame.image.load(os.path.join("assets", os.path.join("chaiyan", os.path.join("transformation", "superChaiyan1.png"))))
    IMG_2 = pygame.image.load(os.path.join("assets", os.path.join("chaiyan", os.path.join("transformation", "superChaiyan2.png"))))
    IMG_3 = pygame.image.load(os.path.join("assets", os.path.join("chaiyan", os.path.join("transformation", "superChaiyan3.png"))))

    SOUND = pygame.mixer.Sound(os.path.join('assets', os.path.join("chaiyan", os.path.join("transformation", "saiyan.mp3"))))

    frame = 0
    frame_timer = 0
    frame_cd = 120

    def draw_window(self):
        screen.fill(WHITE)
        
        if self.frame == 0:
            screen.blit(self.IMG_1, (0,0))
        if self.frame == 1:
            screen.blit(self.IMG_2, (0,0))
        else:
            screen.blit(self.IMG_3, (0,0))

        player_img = pygame.transform.scale(player.img, (600, 600))
        screen.blit(player_img, (WIDTH//2 - player_img.get_width()//2, HEIGHT//2))

        pygame.display.update()

    def main_loop(self):
        self.frame_timer = pygame.time.get_ticks()
        player.moving = False
        player.current_state = 0
        self.SOUND.play()
        self.SOUND.set_volume(0.5)
        
        while player.transforming:
            clock.tick(60)

            player.update()

            if pygame.time.get_ticks() - self.frame_timer > self.frame_cd:
                self.frame += 1
                self.frame_timer = pygame.time.get_ticks()
                if self.frame > 2:
                    self.frame = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.SOUND.stop()
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.SOUND.stop()
                        return False
            self.draw_window()
        self.SOUND.stop()


class main_game_class:

    def draw_window(self):
        
        camera.bg_blit()

        # for row in grid.grid:
        #     for case in row:
        #         if not case["obstacle"]:
        #             pygame.draw.rect(map, RED, case["rect"], 1)
        #         else:
        #             pygame.draw.rect(map, WHITE, case["rect"], 1)

        # Obstacles
        # pygame.draw.rect(map, BLACK, player.body)
        # for room in obstacle.list:
        #     for obs in room:
        #         pygame.draw.rect(map, RED, obs)
                    
        # Behind_Walls
        # for room in behind.list:
        #     for obs in room:
        #         pygame.draw.rect(map, BLACK, obs)
                

    
        
        # Interactibles
        interactible.display_interactibles()

        for row in grid.grid:
            for case in row:
                if not case["obstacle"]:
                    pygame.draw.rect(map, RED, case["rect"], 1)
                else:
                    pygame.draw.rect(map, WHITE, case["rect"], 1)

        for item in interactible.list:
            pygame.draw.rect(map, GREEN, item["rect"], 3)

        # Player (Cat)
        # pygame.draw.rect(map, BLACK, player.body)
        # pygame.draw.rect(map, GREEN, player.hitbox)
        # if player.i_frame:
        #     pygame.draw.rect(map, GREEN, player.hitbox)
        map.blit(player.img, (player.body.x, player.body.y))
        if player.miaou:
            if player.right:
                map.blit(player.SPEECH_BUBBLE_IMG, (player.hitbox.x + player.hitbox.width//2, player.hitbox.y - player.SPEECH_BUBBLE_IMG.get_height()))
            else:
                map.blit(player.SPEECH_BUBBLE_IMG, (player.hitbox.x, player.hitbox.y - player.SPEECH_BUBBLE_IMG.get_height()))

        # Grid Position
        # pygame.draw.rect(map, GREEN, grid.cat_position["rect"])

        # Owner
        # pygame.draw.rect(map, YELLOW, owner.body)

        # # Owner Body Hitbox
        # pygame.draw.rect(map, BLACK, owner.body_hitbox)
        
        map.blit(owner.img, (owner.body.x, owner.body.y))
        
        # Grid position
        # pygame.draw.rect(map, GREEN, grid.owner_position["rect"])
        animation.play_animations()

        # if game_variable.win:
        # map.blit(end_game.img, (player.hitbox.x, player.hitbox.y))
        map.blit(end_game.img, (end_game.alien_body.x, end_game.alien_body.y))
        # pygame.draw.rect(map, BLACK, player.hitbox)
        # pygame.draw.rect(map, BLACK, end_game.alien_hitbox)
        # print(player.hitbox)
        # print(end_game.alien_hitbox)

        camera.update()

        # owner_rage_text = font.render(f"Rage : {owner.rage}", 1, WHITE)
        # screen.blit(owner_rage_text, (WIDTH - owner_rage_text.get_width() - 10, 10))

        # owner_speed_text = font.render(f"Speed : {owner.speed}", 1, WHITE)
        # screen.blit(owner_speed_text, (WIDTH - owner_speed_text.get_width() - 10, 50))

        if interactible.isOn:
            screen.blit(settings.E_KEY_IMG, (screen.get_width()//2 - settings.E_KEY_IMG.get_width()//2, screen.get_height()//3 * 2))
            if interactible.interact_timer != None:
                screen.blit(settings.E_KEY_PRESSED_IMG, (screen.get_width()//2 - settings.E_KEY_PRESSED_IMG.get_width()//2, screen.get_height()//3 * 2))
                pygame.draw.rect(screen, WHITE, interactible.PROGRESS_BAR)
                pygame.draw.rect(screen, YELLOW, interactible.PROGRESS_BAR_FILL)
            else:
                screen.blit(settings.E_KEY_IMG, (screen.get_width()//2 - settings.E_KEY_IMG.get_width()//2, screen.get_height()//3 * 2))


        game_ui.draw_ui()

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
        puke = False
        click = False
        music.play_sound(music.PURRING)
        
        while run:
            clock.tick(60)
            # owner.remove_rage(1)

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            if game_variable.started and not game_variable.win:

                if time.time() - game_variable.timer > game_variable.max_timer:
                    game_variable.enraged = True

                # Collision with cat
                if grid.owner_position["rect"].colliderect(grid.cat_position["rect"]) and not player.i_frame:
                    if game_variable.enraged:
                        game_over.main_loop()
                        run = False
                        break


                    # Start button smash to try to escape
                    result = button_smash.main_loop()
                    game_variable.multiplier = 1
                    left = False
                    right = False
                    up = False
                    down = False
                    interact = False
                    miaou = False
                    puke = False
                    click = False

                    player.i_frame_timer = time.time()
                    if result:
                        player.hp -= 1
                        player.i_frame = True
                    else:
                        player.hp = 0

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

                if miaou and time.time() - player.miaou_timer > player.miaou_cd and not player.miaou:
                    player.miaou_timer = time.time()
                    player.miaou = True
                    music.play_sound(random.choice(music.MEOWS))
                    if game_variable.multiplier >= player.chaiyan_transform_cap and not player.chaiyan:
                        player.transforming = True
                        super_chaiyan.main_loop()
                        player.chaiyan_timer = time.time()
                        music.play_music(music.SUPER_CHAIYAN_THEME)
                        left = False
                        right = False
                        up = False
                        down = False
                        interact = False
                        miaou = False
                        puke = False
                        click = False
                
                if player.chaiyan:
                    if time.time() - player.chaiyan_timer > player.chaiyan_duration:
                        player.chaiyan = False
                        pygame.mixer.music.fadeout(1000)

                if player.miaou and time.time() - player.miaou_timer > player.miaou_duration:
                    player.miaou_timer = time.time()
                    player.miaou = False

                if puke and time.time() - player.puke_timer > player.puke_cd:
                    player.puke_timer = time.time()

                owner.update()

                player.update()

                end_game.update()

                grid.update()

            
            elif (left or right or up or down) and not game_variable.win:
                game_variable.started = True
                game_variable.timer = time.time()
                music.stop_sound(music.PURRING)
            else:
                player.update()
                owner.update()
                interactible.update()
                end_game.update()
                

            miaou = False
            puke = False
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_over.main_loop()
                        run = False
                    if event.key == K_e:
                        interact = True
                    if event.key == K_SPACE:
                        miaou = True
                    if event.key == K_LSHIFT:
                        puke = True
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

# MENU
            
class settings_before_play_class:
    # Title
    TITLE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "title-how-to-play.png")))
    
    # How to play
    HOW_TO_PLAY_1_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "how-to-play-1.png")))
    HOW_TO_PLAY_2_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "how-to-play-2.png")))
    HOW_TO_PLAY_PANNEL = pygame.Rect(WIDTH//2 - HOW_TO_PLAY_1_IMG.get_width()//2 + 50, HEIGHT//3, HOW_TO_PLAY_1_IMG.get_width(), HOW_TO_PLAY_1_IMG.get_height())

    CUSTOM_PLAY_BUTTON_IMG = pygame.transform.scale(PLAY_BUTTON_IMG, (BACK_BUTTON_IMG.get_width(), BACK_BUTTON_IMG.get_height()))
    CUSTOM_PLAY_BUTTON_HOVER_IMG = pygame.transform.scale(PLAY_BUTTON_HOVER_IMG, (BACK_BUTTON_IMG.get_width(), BACK_BUTTON_IMG.get_height()))

    # Buttons list
    button_list = [BACK_BUTTON, PLAY_BUTTON]
    
    in_animation = False
    animation_timer = 0
    animation_duration = 0.7
    animation_cooldown = 0.7

    index = 1

    def draw_window(self):
        screen.blit(BG_GAME_UI, (0,0))
        
        screen.blit(self.TITLE_IMG, (WIDTH//2 - self.TITLE_IMG.get_width()//2, 160))

        if self.in_animation:
            screen.blit(self.HOW_TO_PLAY_1_IMG, (self.HOW_TO_PLAY_PANNEL))
        else:
            screen.blit(self.HOW_TO_PLAY_2_IMG, (self.HOW_TO_PLAY_PANNEL))

        if self.index == 0:
            screen.blit(BACK_BUTTON_HOVER_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))
        else:
            screen.blit(BACK_BUTTON_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))

        if self.index == 1:
            screen.blit(self.CUSTOM_PLAY_BUTTON_HOVER_IMG, (WIDTH - self.CUSTOM_PLAY_BUTTON_IMG.get_width() - 10, HEIGHT - self.CUSTOM_PLAY_BUTTON_IMG.get_height() - 10))
        else:
            screen.blit(self.CUSTOM_PLAY_BUTTON_IMG, (WIDTH - self.CUSTOM_PLAY_BUTTON_IMG.get_width() - 10, HEIGHT - self.CUSTOM_PLAY_BUTTON_IMG.get_height() - 10))

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

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            if self.in_animation:
                if time.time() - self.animation_timer > self.animation_duration:
                    self.in_animation = False
                    self.animation_timer = time.time()
            else:
                if time.time() - self.animation_timer > self.animation_cooldown:
                    self.in_animation = True
                    self.animation_timer = time.time()

            if (up or left) and self.index > 0:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index += 1

            if click or interact:
                music.play_sound(music.BUTTON)
                if self.index == 0:
                    self.index = 1
                    run = False
                elif self.index == 1:
                    main.main_loop()
                    run = False

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
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON_CANCEL, 0.2)
                        run = False
                    if event.key == K_SPACE:
                        interact = True
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

class owner_selection_class:
    OWNER_1_CARD = pygame.Rect(WIDTH//2 - BLACK_FRAME.get_width() - 100, HEIGHT//3, BLACK_FRAME.get_width(), BLACK_FRAME.get_height())
    OWNER_2_CARD = pygame.Rect(WIDTH//2 + 100, HEIGHT//3, 400, 400)
    
    OWNER_MALE_CHOICE_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", os.path.join("owner", "owner-male-choice-screen-1.png"))), (BLACK_FRAME.get_width(), BLACK_FRAME.get_width()))
    OWNER_MALE_CHOICE_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", os.path.join("owner", "owner-male-choice-screen-2.png"))), (BLACK_FRAME.get_width(), BLACK_FRAME.get_width()))
    
    OWNER_FEMALE_CHOICE_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", os.path.join("owner", "owner-female-choice-screen-1.png"))), (BLACK_FRAME.get_width(), BLACK_FRAME.get_width()))
    OWNER_FEMALE_CHOICE_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", os.path.join("owner", "owner-female-choice-screen-2.png"))), (BLACK_FRAME.get_width(), BLACK_FRAME.get_width()))

    TITLE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "title-choose-owner.png")))
    
    in_animation = False
    animation_timer = 0
    animation_duration = 0.15
    animation_cooldown = 2

    button_list = [BACK_BUTTON, OWNER_1_CARD, OWNER_2_CARD]
    index = 1

    def draw_window(self):
        screen.blit(BG_GAME_UI, (0,0))
        
        screen.blit(self.TITLE_IMG, (WIDTH//2 - self.TITLE_IMG.get_width()//2, 160))

        if self.index == 0:
            screen.blit(BACK_BUTTON_HOVER_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))
        else:
            screen.blit(BACK_BUTTON_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))

        # Male Owner
        if self.index == 1:
            screen.blit(ORANGE_FRAME, (self.OWNER_1_CARD.x, self.OWNER_1_CARD.y))
        else:
            screen.blit(BLACK_FRAME, (self.OWNER_1_CARD.x, self.OWNER_1_CARD.y))
        
        if self.in_animation:
            screen.blit(self.OWNER_MALE_CHOICE_1, (self.OWNER_1_CARD.x, self.OWNER_1_CARD.bottom - self.OWNER_MALE_CHOICE_1.get_height() - 8))
        else:
            screen.blit(self.OWNER_MALE_CHOICE_2, (self.OWNER_1_CARD.x, self.OWNER_1_CARD.bottom - self.OWNER_MALE_CHOICE_1.get_height() - 8))

        # Female Owner
        if self.index == 2:
            screen.blit(ORANGE_FRAME, (self.OWNER_2_CARD.x, self.OWNER_2_CARD.y))
        else:
            screen.blit(BLACK_FRAME, (self.OWNER_2_CARD.x, self.OWNER_2_CARD.y))
        if self.in_animation:
            screen.blit(self.OWNER_FEMALE_CHOICE_2, (self.OWNER_2_CARD.x, self.OWNER_2_CARD.bottom - self.OWNER_FEMALE_CHOICE_1.get_height() + 157))
        else:
            screen.blit(self.OWNER_FEMALE_CHOICE_1, (self.OWNER_2_CARD.x, self.OWNER_2_CARD.bottom - self.OWNER_FEMALE_CHOICE_1.get_height() + 157))

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        click = False
        player.in_selection = False
        while run:
            clock.tick(60)

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            if self.in_animation:
                if time.time() - self.animation_timer > self.animation_duration:
                    self.in_animation = False
                    self.animation_timer = time.time()
            else:
                if time.time() - self.animation_timer > self.animation_cooldown:
                    self.in_animation = True
                    self.animation_timer = time.time()

            if (up or left) and self.index > 0:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index += 1

            if click or interact:
                music.play_sound(music.BUTTON)
                if self.index == 0:
                    run = False
                if self.index == 1:
                    game_variable.selected_owner = game_variable.all_owners[0]
                    owner.change_skin()
                    before_game.main_loop()
                    run = False
                if self.index == 2:
                    game_variable.selected_owner = game_variable.all_owners[1]
                    owner.change_skin()
                    before_game.main_loop()
                    run = False

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
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON_CANCEL, 0.2)
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

class cat_selection_class:
    CAT_1_CARD = pygame.Rect(280, 330, 445, 565)
    CAT_2_CARD = pygame.Rect(740, 330, 445, 565)
    CAT_3_CARD = pygame.Rect(1200, 330, 445, 565)

    TITLE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "title.png")))

    CAT_ORANGE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "cat-choice-orange.png")))
    CAT_ORANGE_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "cat-choice-orange-focus-hover.png")))

    CAT_BLACK_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "cat-choice-black.png")))
    CAT_BLACK_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "cat-choice-black-focus-hover.png")))

    CAT_SIAMESE_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "cat-choice-siamese.png")))
    CAT_SIAMESE_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "cat-choice-siamese-focus-hover.png")))

    button_list = [BACK_BUTTON, CAT_1_CARD, CAT_2_CARD, CAT_3_CARD]
    index = 1

    def draw_window(self):
        screen.blit(BG_GAME_UI, (0,0))
        
        screen.blit(self.TITLE_IMG, (WIDTH//2 - self.TITLE_IMG.get_width()//2, 160))

        if self.index == 0:
            screen.blit(BACK_BUTTON_HOVER_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))
        else:
            screen.blit(BACK_BUTTON_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))

        if self.index == 1:
            screen.blit(self.CAT_ORANGE_HOVER_IMG, (280, 330))
        else:
            screen.blit(self.CAT_ORANGE_IMG, (280, 330))

        player.img.fill(ALMOST_BLACK)
        player.img.set_colorkey(ALMOST_BLACK)
        player.img.blit(ORANGE_CAT_LOAF_BREAD, (0,0), (ORANGE_CAT_LOAF_BREAD.get_height() * player.frame, 0, ORANGE_CAT_LOAF_BREAD.get_height(), ORANGE_CAT_LOAF_BREAD.get_height()))
        img = pygame.transform.scale(player.img, (player.img.get_width() * 3, player.img.get_height() * 3))
        screen.blit(img, ((self.CAT_1_CARD.centerx - img.get_width()//2, self.CAT_1_CARD.y + self.CAT_1_CARD.height//4 - img.get_height()//2)))

        if self.index == 2:
            screen.blit(self.CAT_BLACK_HOVER_IMG, (740, 330))
        else:
            screen.blit(self.CAT_BLACK_IMG, (740, 330))

        player.img.fill(ALMOST_BLACK)
        player.img.set_colorkey(ALMOST_BLACK)
        player.img.blit(BLACK_CAT_LOAF_BREAD, (0,0), (BLACK_CAT_LOAF_BREAD.get_height() * player.frame, 0, BLACK_CAT_LOAF_BREAD.get_height(), BLACK_CAT_LOAF_BREAD.get_height()))
        img = pygame.transform.scale(player.img, (player.img.get_width() * 3, player.img.get_height() * 3))
        screen.blit(img, ((self.CAT_2_CARD.centerx - img.get_width()//2, self.CAT_2_CARD.y + self.CAT_2_CARD.height//4 - img.get_height()//2)))

        if self.index == 3:
            screen.blit(self.CAT_SIAMESE_HOVER_IMG, (1200, 330))
        else:
            screen.blit(self.CAT_SIAMESE_IMG, (1200, 330))

        player.img.fill(ALMOST_BLACK)
        player.img.set_colorkey(ALMOST_BLACK)
        player.img.blit(SIAMESE_CAT_LOAF_BREAD, (0,0), (SIAMESE_CAT_LOAF_BREAD.get_height() * player.frame, 0, SIAMESE_CAT_LOAF_BREAD.get_height(), SIAMESE_CAT_LOAF_BREAD.get_height()))
        img = pygame.transform.scale(player.img, (player.img.get_width() * 3, player.img.get_height() * 3))
        screen.blit(img, ((self.CAT_3_CARD.centerx - img.get_width()//2, self.CAT_3_CARD.y + self.CAT_3_CARD.height//4 - img.get_height()//2)))


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

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            player.in_selection = True

            if (up or left) and self.index > 0:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index += 1

            if click or interact:
                music.play_sound(music.BUTTON)
                if self.index == 0:
                    self.index = 1
                    run = False
                elif self.index == 1:
                    game_variable.selected_cat = game_variable.all_cats[0]
                    player.change_cat_skin()
                    player.in_selection = False
                    owner_selection.main_loop()
                elif self.index == 2:
                    game_variable.selected_cat = game_variable.all_cats[1]
                    player.change_cat_skin()
                    player.in_selection = False
                    owner_selection.main_loop()
                elif self.index == 3:
                    game_variable.selected_cat = game_variable.all_cats[2]
                    player.change_cat_skin()
                    player.in_selection = False
                    owner_selection.main_loop()

            player.update_frame()

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
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON_CANCEL, 0.2)
                        self.index == 1
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

    LOGO_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "logo-game-ui.png")))
    LOGO_ANIMATION_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "logo-game-ui-animation.png")))

    PLAY_BUTTON_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-play.png")))
    PLAY_BUTTON_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-play-focus-hover.png")))

    CREDITS_BUTTON_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-credits.png")))
    CREDITS_BUTTON_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-credits-focus-hover.png")))

    EXIT_BUTTON_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-exit.png")))
    EXIT_BUTTON_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-exit-focus-hover.png")))

    SETTINGS_BUTTON_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-settings.png")))
    SETTINGS_BUTTON_HOVER_IMG = pygame.image.load(os.path.join("assets", os.path.join("game-ui", "bouton-settings-focus-hover.png")))

    in_animation = False
    animation_timer = 0
    animation_duration = 0.15
    animation_cooldown = 2

    button_list = [PLAY_BUTTON, CREDITS_BUTTON, QUIT_BUTTON, SETTINGS_BUTTON]
    index = 0

    def __init__(self, exitedGameProperty):
        self.exitedGameProperty = exitedGameProperty

    def draw_window(self):
        screen.blit(BG_GAME_UI, (0,0))
        
        if self.in_animation:
            screen.blit(self.LOGO_ANIMATION_IMG, (260, 210))
        else:
            screen.blit(self.LOGO_IMG, (260, 210))

        if self.index == 0:
            screen.blit(self.PLAY_BUTTON_HOVER_IMG, (1140, 315))
        else:
            screen.blit(self.PLAY_BUTTON_IMG, (1140, 315))

        if self.index == 1:
            screen.blit(self.CREDITS_BUTTON_HOVER_IMG, (1140, 485))
        else:
            screen.blit(self.CREDITS_BUTTON_IMG, (1140, 485))

        if self.index == 2:
            screen.blit(self.EXIT_BUTTON_HOVER_IMG, (1140, 645))
        else:
            screen.blit(self.EXIT_BUTTON_IMG, (1140, 645))

        if self.index == 3:
            screen.blit(self.SETTINGS_BUTTON_HOVER_IMG, (WIDTH - 200, HEIGHT - 190))
        else:
            screen.blit(self.SETTINGS_BUTTON_IMG, (WIDTH - 200, HEIGHT - 190))

        pygame.display.update()

    def main_loop(self):
        run = True
        left = False
        right = False
        up = False
        down = False
        interact = False
        click = False
        self.animation_timer = time.time()
        music.play_music(music.MAIN_THEME)
        while run:
            clock.tick(60)

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            if self.in_animation:
                if time.time() - self.animation_timer > self.animation_duration:
                    self.in_animation = False
                    self.animation_timer = time.time()
            else:
                if time.time() - self.animation_timer > self.animation_cooldown:
                    self.in_animation = True
                    self.animation_timer = time.time()

            if (up or left) and self.index > 0:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index += 1

            if click or interact:
                music.play_sound(music.BUTTON)
                if self.index == 0:
                    # Go to Cat selection
                    cat_selection.main_loop()
                if self.index == 1:
                    # Go to Credits
                    credits.main_loop()
                if self.index == 2: 
                    # QUIT GAME
                    run = False
                    self.exitedGameProperty = True
                    pass # Break loop iteration and goes to the next
                if self.index == 3:
                    # Go to settings
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
    # Title
    title_text = big_font.render("Controls", 1, BLACK)

    # Button
    Z_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 200, 240, 50)
    Q_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 120, 240, 50)
    S_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 240, 50)
    D_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 240, 50)
    E_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    SPACE_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50)

    # Descriptions
    Z_DESC = font.render("UP", 1, BLACK)
    Q_DESC = font.render("LEFT", 1, BLACK)
    S_DESC = font.render("DOWN", 1, BLACK)
    D_DESC = font.render("RIGHT", 1, BLACK)
    E_DESC = font.render("ACTION", 1, BLACK)
    SPACE_DESC = font.render("SELECT", 1, BLACK)

    # Buttons list
    button_list = [ Z_BUTTON, Q_BUTTON, S_BUTTON, D_BUTTON, E_BUTTON, SPACE_BUTTON, BACK_BUTTON ]

    # List of buttons objects
    Z_KEY_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-z-not-pressed.png")))
    Z_KEY_PRESSED_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-z-pressed.png")))
    Q_KEY_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-q-not-pressed.png")))
    Q_KEY_PRESSED_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-q-pressed.png")))
    S_KEY_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-s-not-pressed.png")))
    S_KEY_PRESSED_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-s-pressed.png")))
    D_KEY_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-d-not-pressed.png")))
    D_KEY_PRESSED_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-d-pressed.png")))
    E_KEY_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-e-not-pressed.png")))
    E_KEY_PRESSED_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "letter-e-pressed.png")))
    SPACE_KEY_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "space-bar.png")))
    SPACE_KEY_PRESSED_IMG = pygame.image.load(os.path.join("assets", os.path.join("keys", "space-pressed.png")))

    index = 0

    def draw_window(self):
        screen.blit(BG_GAME_UI, (0,0))
        
        screen.blit(self.title_text, (WIDTH//2 - self.title_text.get_width()//2, HEIGHT//2 - 320 - self.title_text.get_height()//2))
        screen.blit(self.Z_DESC, (WIDTH//2 - self.Z_BUTTON.x//2, self.Z_BUTTON.y))   
        screen.blit(self.Q_DESC, (WIDTH//2 - self.Q_BUTTON.x//2, self.Q_BUTTON.y))    
        screen.blit(self.S_DESC, (WIDTH//2 - self.S_BUTTON.x//2, self.S_BUTTON.y))   
        screen.blit(self.D_DESC, (WIDTH//2 - self.D_BUTTON.x//2, self.D_BUTTON.y))  
        screen.blit(self.E_DESC, (WIDTH//2 - self.E_BUTTON.x//2, self.E_BUTTON.y))  
        screen.blit(self.SPACE_DESC, (WIDTH//2 - self.SPACE_BUTTON.x//2, self.SPACE_BUTTON.y))  

        if self.index == 0:
            screen.blit(self.Z_KEY_PRESSED_IMG, (self.Z_BUTTON.x, self.Z_BUTTON.y))
        else:
            screen.blit(self.Z_KEY_IMG, (self.Z_BUTTON.x, self.Z_BUTTON.y))     

        if self.index == 1:
            screen.blit(self.Q_KEY_PRESSED_IMG, (self.Q_BUTTON.x, self.Q_BUTTON.y))
        else:
            screen.blit(self.Q_KEY_IMG, (self.Q_BUTTON.x, self.Q_BUTTON.y))
            
        if self.index == 2:
            screen.blit(self.S_KEY_PRESSED_IMG, (self.S_BUTTON.x, self.S_BUTTON.y))
        else:
            screen.blit(self.S_KEY_IMG, (self.S_BUTTON.x, self.S_BUTTON.y)) 
            
        if self.index == 3:
            screen.blit(self.D_KEY_PRESSED_IMG, (self.D_BUTTON.x, self.D_BUTTON.y))
        else:
            screen.blit(self.D_KEY_IMG, (self.D_BUTTON.x, self.D_BUTTON.y))
            
        if self.index == 4:
            screen.blit(self.E_KEY_PRESSED_IMG, (self.E_BUTTON.x, self.E_BUTTON.y))
        else:
            screen.blit(self.E_KEY_IMG, (self.E_BUTTON.x, self.E_BUTTON.y))
            
        if self.index == 5:
            screen.blit(self.SPACE_KEY_PRESSED_IMG, (self.SPACE_BUTTON.x, self.SPACE_BUTTON.y))
        else:
            screen.blit(self.SPACE_KEY_IMG, (self.SPACE_BUTTON.x, self.SPACE_BUTTON.y))

        if self.index == 6:
            screen.blit(BACK_BUTTON_HOVER_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))
        else:
            screen.blit(BACK_BUTTON_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))

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

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            if (up or left) and self.index > 0:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index -= 1
            if (down or right) and self.index < len(self.button_list) - 1:
                music.play_sound(music.BUTTON_SWITCH, 0.15)
                self.index += 1

            if click or interact:
                music.play_sound(music.BUTTON)
                if self.index == 0:
                    print('UP')
                elif self.index == 1:
                    print('LEFT')
                elif self.index == 2:
                    print('DOWN')   
                elif self.index == 3:
                    print('RIGHT')
                elif self.index == 4:
                    print('ACTION')
                elif self.index == 5:
                    print('SELECT')
                else:
                    run = False
                    print('RETURN')
                    # Reset navigation index
                    self.index = 0            

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
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON_CANCEL, 0.2)
                        run = False
                    if event.key == K_SPACE:
                        interact = True
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

    # Ctor
    def __init__(self):        
        # People list
        self.people = [ 'Fatality67', 'RedMorgane', 'Molalix', 'Nyaek', 'Noraxya', 'TotleEclipse' ]
        self.index = 0

    def draw_window(self):
        screen.blit(BG_GAME_UI, (0,0))
        
        title_text = big_font.render("Crédits", 1, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 320 - title_text.get_height()//2))

        for listIndex in range(0, len(self.people)):
            creditMemberText = font.render(self.people[listIndex], 1, BLACK)
            screen.blit(creditMemberText, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100 + 50 * listIndex - title_text.get_height()//2))        

        if self.index == 0:
            screen.blit(BACK_BUTTON_HOVER_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))
        else:
            screen.blit(BACK_BUTTON_IMG, (BACK_BUTTON.x, BACK_BUTTON.y))

        pygame.display.update()

    def main_loop(self):
        run = True
        interact = False
        click = False
        while run:
            clock.tick(60)

            if not pygame.mixer.music.get_busy():
                music.play_music(music.MAIN_THEME)

            if click or interact:
                music.play_sound(music.BUTTON_CANCEL, 0.2)
                run = False
                print('RETURN')
                # Reset navigation index
                self.index = 0
                        
            
            interact = False
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    general_use.close_the_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        music.play_sound(music.BUTTON_CANCEL, 0.2)
                        run = False
                    if event.key == K_SPACE:
                        click = True
                    if event.key == K_e:
                        interact = True
            self.draw_window()

# Property designed to quit the game
exitedGameProperty = False

# baseSettings() # Create the controls configuration file
general_use = general_use_class()
game_variable = game_variable_class()
music = music_class()
super_chaiyan = super_chaiyan_class()
camera = camera_class()
player = player_class()
owner = owner_class()
obstacle = obstacle_class()
behind = behind_wall_class()
grid = grid_class()
interactible = interactible_class()
animation = animation_class()
end_game = end_game_class()
game_over = game_over_class()
button_smash = button_smash_class()
main = main_game_class()
cat_selection = cat_selection_class()
owner_selection = owner_selection_class()
menu = menu_class(exitedGameProperty)
credits = credits_class()
settings = settings_class()
before_game = settings_before_play_class()
grid.maze = redefineMaze(grid.maze)
pathfinder = Pathfinder(grid.maze)
game_ui = game_ui_class()

# for x in grid.maze:
#     print(x)

# main.main_loop()

menu.main_loop()



if exitedGameProperty:
    general_use.close_the_game()