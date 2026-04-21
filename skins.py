# skins.py
# Module for handling player skins, loading images, and skin menu
import os
import sys
import pygame
import saves
from config import screen, WINDOW_W, WINDOW_H, FPS, SKIN_COST

# Get base directory for relative paths
BASE_DIR = os.path.dirname(__file__)
# Directory for skin images
SKIN_DIR = os.path.join(BASE_DIR, "skins")

# Function to load all skin images from the skins directory
def load_all_skin_images():
    # Dictionary to hold loaded images
    imgs   = {}
    # Check if skins directory exists
    if os.path.exists(SKIN_DIR):
        # Loop through sorted filenames in directory
        for fname in sorted(os.listdir(SKIN_DIR)):
            # Only load PNG files
            if fname.endswith(".png"):
                # Load and convert image with alpha
                imgs[fname] = pygame.image.load(os.path.join(SKIN_DIR, fname)).convert_alpha()
    # Return the dictionary of images
    return imgs

# Function to create a circular player surface from skin image
def make_player_surf(skin_name, all_imgs, radius):
    # Calculate diameter from radius
    diam = radius * 2
    # Check if skin exists in loaded images
    if skin_name not in all_imgs:
        return None
    # Scale the image to fit the diameter
    scaled = pygame.transform.scale(all_imgs[skin_name], (diam, diam))
    # Create a mask surface for circular clipping
    mask   = pygame.Surface((diam, diam), pygame.SRCALPHA)
    # Draw a white circle on the mask
    pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)
    # Apply the mask to the scaled image
    scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    # Return the masked surface
    return scaled

# Function for the skin selection menu
def skinmenu():
    # Define fonts for text rendering
    font     = pygame.font.Font(None, 26)
    big_font = pygame.font.Font(None, 44)
    # List to hold available skins
    skin_list   = []
    # Check if skins directory exists
    if os.path.exists(SKIN_DIR):
        # Loop through sorted filenames
        for fname in sorted(os.listdir(SKIN_DIR)):
            # Skip non-PNG files
            if not fname.endswith(".png"):
                continue
            # Skip locked skins if not unlocked
            if fname == "lebron.png" and not saves.secret_lebron_unlocked and fname not in saves.owned_skins:
                continue
            if fname in ["tuff.png", "hillo.png"] and not saves.secret_lebron_unlocked and fname not in saves.owned_skins:
                continue
            # Load and scale the image
            img = pygame.image.load(os.path.join(SKIN_DIR, fname)).convert_alpha()
            img = pygame.transform.scale(img, (72, 72))
            # Add to skin list
            skin_list.append({"name": fname, "img": img})

    # Layout constants for the menu
    COLS      = 3
    THUMB_W   = 72
    THUMB_H   = 72
    BTN_H     = 26
    SPACING_X = 150
    SPACING_Y = 130
    START_X   = 55
    START_Y   = 100
    # Back button rectangle
    back_btn  = pygame.Rect(10, 8, 112, 32)
    SCROLL_SPEED = 30
    # Scrolling variables
    scroll_y  = 0
    # Calculate total rows and max scroll
    total_rows = (len(skin_list) + COLS - 1) // COLS
    max_scroll = max(0, total_rows * SPACING_Y - (WINDOW_H - START_Y))
    # Pygame clock for frame rate
    clock      = pygame.time.Clock()
    just_clicked = False
    running    = True

    # Main menu loop
    while running:
        # Limit frame rate
        clock.tick(FPS)
        just_clicked = False
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - SCROLL_SPEED)
                elif event.key == pygame.K_DOWN:
                    scroll_y = min(max_scroll, scroll_y + SCROLL_SPEED)
            if event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * SCROLL_SPEED
                scroll_y  = max(0, min(max_scroll, scroll_y))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                just_clicked = True
                if back_btn.collidepoint(event.pos):
                    running = False

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Fill screen with background color
        screen.fill((22, 22, 30))

        # Render wins text
        ws = big_font.render(f"WINS: {saves.wins}", True, (255, 215, 0))
        screen.blit(ws, (WINDOW_W // 2 - ws.get_width() // 2, 10))

        # Draw back button
        pygame.draw.rect(screen, (140, 40, 40), back_btn, border_radius=6)
        screen.blit(font.render("Back (Esc)", True, (255, 255, 255)),
                    (back_btn.x + 8, back_btn.y + 7))

        # Loop through skins to render
        for idx, skin in enumerate(skin_list):
            # Calculate row and column
            row_num = idx // COLS
            col_num = idx  % COLS
            sx = START_X + col_num * SPACING_X
            sy = START_Y + row_num * SPACING_Y - scroll_y
            # Skip if off-screen
            if sy + THUMB_H + BTN_H + 24 < 0 or sy > WINDOW_H:
                continue
            # Check skin status
            is_default  = skin["name"] == "0_Default.png"
            is_owned    = skin["name"] in saves.owned_skins or is_default
            is_equipped = skin["name"] == saves.equipped_skin

            # Draw card background
            card = pygame.Rect(sx - 8, sy - 8, THUMB_W + 16, THUMB_H + BTN_H + 24)
            pygame.draw.rect(screen, (50, 80, 50) if is_equipped else (38, 38, 55),
                             card, border_radius=8)
            # Blit skin image
            screen.blit(skin["img"], (sx, sy))

            # Draw button based on status
            btn = pygame.Rect(sx, sy + THUMB_H + 6, THUMB_W, BTN_H)
            # Set cost for the skin
            cost = 2003 if skin["name"] == "lebron.png" else SKIN_COST
            if is_equipped:
                btn_col, label = (50, 190, 70),  "Equipped"
            elif is_owned:
                btn_col, label = (70, 100, 220), "Equip"
            elif saves.wins >= cost:
                btn_col, label = (200, 150, 40), f"Buy {cost}W"
            else:
                btn_col, label = (65, 65, 65),   f"Need {cost}W"

            # Draw button
            pygame.draw.rect(screen, btn_col, btn, border_radius=5)
            ls = font.render(label, True, (255, 255, 255))
            screen.blit(ls, ls.get_rect(center=btn.center))

            # Handle button clicks
            if just_clicked and btn.collidepoint(mouse_pos):
                if is_owned and not is_equipped:
                    saves.equipped_skin = skin["name"]
                    saves.save_skin_state()
                elif not is_owned and saves.wins >= cost:
                    saves.wins -= cost
                    saves.owned_skins.append(skin["name"])
                    saves.equipped_skin = skin["name"]
                    saves.save_wins()
                    saves.save_skin_state()

        # Update display
        pygame.display.flip()

    # Return from function
    return
