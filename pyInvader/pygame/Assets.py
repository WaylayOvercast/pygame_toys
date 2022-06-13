import pygame
import os


pygame.font.init()
WINDOW_SIZE = [1500,1000]


def LoadImage(file, route, width = None, height = None):
    if width == None and height == None:
        return pygame.image.load(os.path.join(file, route))
    else:
        return pygame.transform.scale(pygame.image.load(os.path.join(file, route)), (width, height))

#   texture Dir        
LOCAL = "C:/Users/Waylay/Desktop/PythonTesting/pygame/textures"

#   load textures
RED_SPACE_SHIP = LoadImage(LOCAL, "pixel_ship_red_small.png" )
GREEN_SPACE_SHIP = LoadImage(LOCAL, "pixel_ship_green_small.png")
BLUE_SPACE_SHIP = LoadImage(LOCAL, "pixel_ship_blue_small.png")

#   load item textures
HEALTH_CANISTER = LoadImage(LOCAL, "pixel_health_small.png", 100, 100)

# player textures
YELLOW_SPACE_SHIP = LoadImage(LOCAL, "pixel_ship_yellow.png")
YELLOW_SPACE_SHIP_KNOCKOUT = LoadImage(LOCAL, "player_ship_white.png")

# projectile textures
RED_LASER = LoadImage(LOCAL, "pixel_laser_red.png")
GREEN_LASER = LoadImage(LOCAL, "pixel_laser_green.png")
BLUE_LASER = LoadImage(LOCAL, "pixel_laser_blue.png")
YELLOW_LASER = LoadImage(LOCAL, "pixel_laser_yellow.png")

# map textures
MAP = LoadImage(LOCAL, "background-black.png", 1500, 1000)

# fonts
main_font = pygame.font.SysFont('comicsans', 25)
lost_font = pygame.font.SysFont('comicsans', 45)