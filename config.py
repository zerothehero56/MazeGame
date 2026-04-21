# config.py
# Configuration file for game constants and settings
import os
import pygame

# Get base directory for relative paths
BASE_DIR = os.path.dirname(__file__)
# Directory for skin images
SKIN_DIR = os.path.join(BASE_DIR, "skins")
# Directory for sound files
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

# Initialize Pygame mixer and display
pygame.mixer.init()
pygame.init()

# Window dimensions and layout
winz = 0
WINDOW_W = 500
WINDOW_H = 535
HUD_H = 35
VIEW_H = WINDOW_H - HUD_H
player_color = (255, 255, 0)

# Maze cell size calculation
vis = 4
CELL_SIZE = 500 / vis

# Maze dimensions
MAZE_COLS = 20
MAZE_ROWS = MAZE_COLS

# Color definitions
WALL_COLOR = (40, 40, 40)
BG_COLOR = (220, 220, 220)
GOAL_COLOR = (30, 160, 30)

# Game performance settings
FPS = 240
SKIN_COST = 10

# Animation lerp factors
LERP_CAM = 0.12
LERP_PLAYER = 0.18

# Create Pygame display surface
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Maze Game")

# Button rectangles for main menu
btn_play    = pygame.Rect(125, 115, 250, 78)
btn_skins   = pygame.Rect(125, 222, 250, 78)
btn_quit    = pygame.Rect(125, 329, 250, 78)
btn_seceret = pygame.Rect(0, 0, 50, 50)
btn_settings = pygame.Rect(125, 436, 250, 78)

# Menu styles
menu_styles = {
    'btn_font': pygame.font.Font(None, 44),
    'sub_font': pygame.font.Font(None, 28),
    'key_font': pygame.font.Font(None, 22),
    'bg_col': (22, 22, 30),
    'btn_col': (55, 55, 78),
    'btn_sec': (23, 23, 31),
    'btn_sec_hov': (23, 23, 31),
    'btn_hov': (85, 85, 118)
}

# Default settings
DEFAULT_BG_VOLUME = 0.25
DEFAULT_SFX_VOLUME = 0.75
DEFAULT_STEP_SOUNDS_ENABLED = False
DEFAULT_COLOR_CHANGE_ENABLED = True
