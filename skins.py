# skins.py
# Module for handling player skins, loading images, and skin menu
import os
import sys
import pygame
import saves
from config import (
    screen,
    WINDOW_W,
    WINDOW_H,
    FPS,
    SKIN_COST,
    THEME,
    draw_vertical_gradient,
    draw_panel,
    draw_button,
)

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
    font = pygame.font.Font(None, 26)
    title_font = pygame.font.Font(None, 44)
    sub_font = pygame.font.Font(None, 22)

    def fit_text(surface, max_w):
        w, h = surface.get_size()
        if w <= max_w:
            return surface
        scale = max_w / max(1, w)
        return pygame.transform.smoothscale(surface, (max(1, int(w * scale)), max(1, int(h * scale))))

    # List to hold available skins
    skin_list = []

    def get_skin_cost(skin_name):
        key = skin_name.lower()
        costs = {
            "0_default.png": 0,
            "norm.png": 5,
            "wilbut.png": 8,
            "imattheclub.png": 12,
            "bart.png": 16,
            "dingle.png": 22,
            "elonicagartha.png": 30,
            "hillo.png": 45,
            "tuff.png": 65,
            "lebron.png": 2003,
        }
        return costs.get(key, SKIN_COST)

    if os.path.exists(SKIN_DIR):
        for fname in sorted(os.listdir(SKIN_DIR)):
            if not fname.endswith(".png"):
                continue

            img = pygame.image.load(os.path.join(SKIN_DIR, fname)).convert_alpha()
            img = pygame.transform.scale(img, (88, 88))
            skin_list.append({
                "name": fname,
                "display": os.path.splitext(fname)[0],
                "img": img,
            })

    # Layout constants for the menu
    COLS = 2
    CARD_W = 206
    CARD_H = 186
    GAP_X = 16
    GAP_Y = 16
    HEADER_BOTTOM = 78
    CONTENT_TOP = 88
    START_Y = CONTENT_TOP + 8
    grid_w = COLS * CARD_W + (COLS - 1) * GAP_X
    START_X = (WINDOW_W - grid_w) // 2
    content_rect = pygame.Rect(0, CONTENT_TOP, WINDOW_W, WINDOW_H - CONTENT_TOP)

    back_btn = pygame.Rect(14, 12, 116, 34)
    SCROLL_SPEED = 30
    scroll_y = 0

    total_rows = (len(skin_list) + COLS - 1) // COLS
    content_h = total_rows * CARD_H + max(0, total_rows - 1) * GAP_Y
    view_h = WINDOW_H - START_Y - 14
    max_scroll = max(0, content_h - view_h)

    clock = pygame.time.Clock()
    just_clicked = False
    running = True

    while running:
        clock.tick(FPS)
        just_clicked = False

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
                scroll_y = max(0, min(max_scroll, scroll_y))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                just_clicked = True
                if back_btn.collidepoint(event.pos):
                    running = False

        mouse_pos = pygame.mouse.get_pos()
        draw_vertical_gradient(screen, THEME['bg_top'], THEME['bg_bottom'])

        title = title_font.render("SKINS", True, THEME['title'])
        screen.blit(title, title.get_rect(center=(WINDOW_W // 2, 28)))
        subtitle = sub_font.render(f"Wins: {saves.wins}  |  Scroll to browse", True, THEME['muted_text'])
        screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_W // 2, 58)))
        pygame.draw.line(screen, THEME['panel_border'], (12, HEADER_BOTTOM), (WINDOW_W - 12, HEADER_BOTTOM), 1)

        draw_button(screen, back_btn, "Back", "Esc", back_btn.collidepoint(mouse_pos), font, font)

        prev_clip = screen.get_clip()
        screen.set_clip(content_rect)

        for idx, skin in enumerate(skin_list):
            row_num = idx // COLS
            col_num = idx % COLS
            sx = START_X + col_num * (CARD_W + GAP_X)
            sy = START_Y + row_num * (CARD_H + GAP_Y) - scroll_y
            if sy + CARD_H < CONTENT_TOP or sy > WINDOW_H:
                continue

            is_default = skin["name"] == "0_Default.png"
            is_owned = skin["name"] in saves.owned_skins or is_default
            is_equipped = skin["name"] == saves.equipped_skin

            card = pygame.Rect(sx, sy, CARD_W, CARD_H)
            card_col = THEME['panel_alt'] if is_equipped else THEME['panel']
            border_col = THEME['accent'] if is_equipped else THEME['panel_border']
            draw_panel(screen, card, fill_color=card_col, border_color=border_col, radius=12)

            name_surface = fit_text(font.render(skin["display"], True, THEME['title']), CARD_W - 16)
            screen.blit(name_surface, name_surface.get_rect(center=(card.centerx, card.y + 20)))

            img_rect = skin["img"].get_rect(center=(card.centerx, card.y + 78))
            screen.blit(skin["img"], img_rect)

            btn = pygame.Rect(card.x + 14, card.bottom - 44, CARD_W - 28, 30)
            cost = get_skin_cost(skin["name"])
            if is_equipped:
                btn_col, label = (70, 116, 80), "Equipped"
            elif is_owned:
                btn_col, label = THEME['button'], "Equip"
            elif saves.wins >= cost:
                btn_col, label = THEME['button_hover'], f"Buy ({cost}W)"
            else:
                btn_col, label = THEME['panel_alt'], f"Need {cost}W"

            btn_hovered = btn.collidepoint(mouse_pos) and content_rect.collidepoint(mouse_pos)
            draw_button(
                screen,
                btn,
                label,
                "",
                btn_hovered,
                font,
                font,
                base_color=btn_col,
                hover_color=tuple(max(0, c - 10) for c in btn_col),
                text_color=THEME['button_text'],
            )

            if just_clicked and btn.collidepoint(mouse_pos) and content_rect.collidepoint(mouse_pos):
                if is_owned and not is_equipped:
                    saves.equipped_skin = skin["name"]
                    saves.save_skin_state()
                elif not is_owned and saves.wins >= cost:
                    saves.wins -= cost
                    saves.owned_skins.append(skin["name"])
                    saves.equipped_skin = skin["name"]
                    saves.save_wins()
                    saves.save_skin_state()

        screen.set_clip(prev_clip)

        pygame.display.flip()

    return
