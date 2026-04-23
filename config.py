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
WINDOW_W = 500
WINDOW_H = 535
HUD_H = 35
VIEW_H = WINDOW_H - HUD_H

# Maze cell size calculation
vis = 4
CELL_SIZE = 500 / vis

# Maze dimensions
MAZE_COLS = 20
MAZE_ROWS = MAZE_COLS

# Color definitions
WALL_COLOR = (24, 28, 34)
BG_COLOR = (46, 52, 61)
GOAL_COLOR = (46, 170, 80)
GOAL_BORDER_COLOR = (170, 240, 180)

THEME = {
    "bg_top": (26, 30, 36),
    "bg_bottom": (20, 24, 30),
    "panel": (34, 39, 47),
    "panel_alt": (44, 50, 60),
    "panel_border": (82, 90, 103),
    "button": (62, 70, 83),
    "button_hover": (78, 88, 103),
    "button_text": (232, 236, 242),
    "muted_text": (172, 181, 194),
    "title": (244, 247, 252),
    "accent": (116, 214, 146),
    "danger": (139, 83, 83),
}

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
btn_quit    = pygame.Rect(125, 436, 250, 78)
btn_secret = pygame.Rect(0, 0, 50, 50)
btn_settings = pygame.Rect(125, 329, 250, 78)

# Menu styles
menu_styles = {
    'btn_font': pygame.font.Font(None, 44),
    'sub_font': pygame.font.Font(None, 28),
    'key_font': pygame.font.Font(None, 22),
    'bg_col': THEME['bg_top'],
    'btn_col': THEME['button'],
    'btn_sec': THEME['panel'],
    'btn_sec_hov': THEME['panel_alt'],
    'btn_hov': THEME['button_hover']
}


def draw_vertical_gradient(surface, top_color, bottom_color):
    height = surface.get_height()
    width = surface.get_width()
    if height <= 1:
        surface.fill(top_color)
        return

    for y in range(height):
        t = y / (height - 1)
        color = (
            int(top_color[0] + (bottom_color[0] - top_color[0]) * t),
            int(top_color[1] + (bottom_color[1] - top_color[1]) * t),
            int(top_color[2] + (bottom_color[2] - top_color[2]) * t),
        )
        pygame.draw.line(surface, color, (0, y), (width, y))


def _fit_surface(surface, max_width, max_height):
    max_width = max(1, int(max_width))
    max_height = max(1, int(max_height))
    width, height = surface.get_size()
    if width <= max_width and height <= max_height:
        return surface

    scale = min(max_width / width, max_height / height)
    new_w = max(1, int(width * scale))
    new_h = max(1, int(height * scale))
    return pygame.transform.smoothscale(surface, (new_w, new_h))


def draw_panel(surface, rect, fill_color=None, border_color=None, radius=14, alpha=235):
    fill_color = fill_color or THEME['panel']
    border_color = border_color or THEME['panel_border']
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 60), shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.x, rect.y + 2))

    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*fill_color, alpha), panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)
    pygame.draw.rect(surface, border_color, rect, 1, border_radius=radius)


def draw_button(surface, rect, label, hotkey, hovered, btn_font, key_font,
                base_color=None, hover_color=None, text_color=None, key_color=None):
    base_color = base_color or THEME['button']
    hover_color = hover_color or THEME['button_hover']
    text_color = text_color or THEME['button_text']
    key_color = key_color or THEME['muted_text']
    color = hover_color if hovered else base_color
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 70), shadow.get_rect(), border_radius=10)
    surface.blit(shadow, (rect.x, rect.y + 2))

    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, THEME['panel_border'], rect, 1, border_radius=10)

    if label:
        label_surface = btn_font.render(label, True, text_color)
        if hotkey:
            key_surface = key_font.render(hotkey, True, key_color)

            label_surface = _fit_surface(label_surface, rect.width - 10, rect.height // 2)
            key_surface = _fit_surface(key_surface, rect.width - 10, rect.height // 2)

            gap = 2
            total_h = label_surface.get_height() + key_surface.get_height() + gap
            available_h = max(1, rect.height - 8)
            if total_h > available_h:
                scale = available_h / total_h
                label_surface = _fit_surface(
                    label_surface,
                    int(label_surface.get_width() * scale),
                    int(label_surface.get_height() * scale),
                )
                key_surface = _fit_surface(
                    key_surface,
                    int(key_surface.get_width() * scale),
                    int(key_surface.get_height() * scale),
                )
                total_h = label_surface.get_height() + key_surface.get_height() + gap

            top = rect.y + (rect.height - total_h) // 2
            surface.blit(label_surface, label_surface.get_rect(center=(rect.centerx, top + label_surface.get_height() // 2)))
            key_y = top + label_surface.get_height() + gap
            surface.blit(key_surface, key_surface.get_rect(center=(rect.centerx, key_y + key_surface.get_height() // 2)))
        else:
            label_surface = _fit_surface(label_surface, rect.width - 10, rect.height - 8)
            surface.blit(label_surface, label_surface.get_rect(center=rect.center))

# Default settings
DEFAULT_BG_VOLUME = 0.25
DEFAULT_SFX_VOLUME = 0.75
DEFAULT_STEP_SOUNDS_ENABLED = False
DEFAULT_COLOR_CHANGE_ENABLED = True
