import sys
import random
import time
import pygame
import os

# Import configuration module for game settings
import config as cfg
# Import saves module for handling game save data
import saves
# Import skins module for player skin management
import skins
# Import sounds module for audio loading and effects
import sounds
# Import state module for global game state variables
import state
# Import maze generation and drawing functions
from maze import generate_maze, draw_maze, grid_index
# Import specific constants from config for screen and game parameters
from config import (screen, WINDOW_W, WINDOW_H, HUD_H, VIEW_H,
                    FPS, LERP_CAM, LERP_PLAYER, GOAL_COLOR)
# Import slider function for difficulty selection
from slider import slider
# Import mainmenu function for the main menu
from menu import mainmenu


# Function to get the player surface based on equipped skin
def get_player_surf(all_imgs, radius):
    # Call skins.make_player_surf to create the player image surface
    return skins.make_player_surf(saves.equipped_skin, all_imgs, radius)


# Function to initialize a new game with given columns and rows
def new_game(cols, rows):
    # Generate the maze grid using the maze module
    grid   = generate_maze(cols, rows)
    # Set initial player position at top-left
    player = [0, 0]
    # Set goal position at bottom-right
    goal   = [cols - 1, rows - 1]
    # Record start time for timing the game
    start_t = time.time()
    # Calculate initial smooth player x position
    spx = float(0 * cfg.CELL_SIZE + cfg.CELL_SIZE // 2)
    # Calculate initial smooth player y position
    spy = float(0 * cfg.CELL_SIZE + cfg.CELL_SIZE // 2)
    # Calculate initial camera x offset
    csx = float(max(0, spx - cfg.WINDOW_W // 2))
    # Calculate initial camera y offset
    csy = float(max(0, spy - cfg.VIEW_H  // 2))
    # Return all initial game state variables
    return grid, player, goal, start_t, False, 0, False, False, spx, spy, csx, csy


# Main game loop function
def main():
    # Initialize sunshine variable (possibly unused or for future features)
    sunshine = True
    # Get maze dimensions from config
    cols, rows = cfg.MAZE_COLS, cfg.MAZE_ROWS
    # Create Pygame clock for frame rate control
    clock      = pygame.time.Clock()
    # Create font for HUD text
    font       = pygame.font.SysFont(None, 23)
    # Create small font (possibly unused)
    small_font = pygame.font.Font(None, 22)
    # Calculate player radius based on cell size
    radius     = cfg.CELL_SIZE // 3
    # Load all skin images for player customization
    all_imgs   = skins.load_all_skin_images()
    pygame.mixer.stop()
    pygame.mixer.init()

    # Ensure sounds are loaded
    sounds.load_all_sounds()

    # Start background music based on equipped skin
    def get_soundtrack(skin):
        # Return soundtrack file based on skin name
        if skin == "lebron.png":
            return "LebronShine.wav"
        elif skin == "dingle.png":
            return "rizzy.mp3"
        else:
            return "default.mp3"

    # Get the soundtrack file for the current equipped skin
    soundtrack_file = get_soundtrack(saves.equipped_skin)
    # Construct full path to the soundtrack file
    music_path = os.path.join(cfg.SOUNDS_DIR, soundtrack_file)
    # Check if the music file exists and load/play it in a loop
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(saves.bg_volume)

    # Reinitialize sunshine (redundant?)
    sunshine = True
    # Initialize new game state
    (grid, player, goal, start_t, won, steps,
     played_200, played_300, smooth_px, smooth_py, cam_sx, cam_sy) = new_game(cols, rows)

    # Flag to allow winning once per game
    canwin   = True
    # Flag for win sound playback
    winplay  = True
    # Time taken to win
    win_time = 0.0
    # Get player surface for rendering
    player_surf = get_player_surf(all_imgs, radius)

    # Main game loop flag
    running = True
    # Start the main game loop
    while running:
        # Calculate delta time for smooth animations
        dt = clock.tick(FPS) / 1000.0

        # Event handling loop
        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.stop()
            # Handle key down events
            elif event.type == pygame.KEYDOWN:
                # Regenerate maze on R key
                if event.key == pygame.K_r:
                    (grid, player, goal, start_t, won, steps,
                     played_200, played_300, smooth_px, smooth_py,
                     cam_sx, cam_sy) = new_game(cols, rows)
                    canwin   = True
                    sunshine = True
                    win_time = 0.0
                    player_surf = get_player_surf(all_imgs, radius)
                    continue
                # Return to menu on Escape
                if event.key == pygame.K_ESCAPE:
                    running = False
                    mainmenu()
                    
                    return
                # Go to slider (difficulty) on Q
                if event.key == pygame.K_q:
                    running = False
                    slider()
                    
                    return
                # Handle movement if game not won
                if not won:
                    # Get current player position
                    col_p, row_p = player
                    # Flag for whether player moved
                    moved = False
                    # Get current cell index
                    idx = grid_index(col_p, row_p, cols, rows)
                    # Get current cell if in bounds
                    cur = grid[idx] if idx is not None else None
                    # Check noclip state for movement rules
                    if state.noclip == 0:
                        # Normal movement with bounds and wall checks
                        if event.key in (pygame.K_UP, pygame.K_w):
                            if row_p > 0 and (cur is None or not cur.walls[0]):
                                player[1] -= 1; moved = True
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            if row_p < rows - 1 and (cur is None or not cur.walls[2]):
                                player[1] += 1; moved = True
                        elif event.key in (pygame.K_LEFT, pygame.K_a):
                            if col_p > 0 and (cur is None or not cur.walls[3]):
                                player[0] -= 1; moved = True
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            if col_p < cols - 1 and (cur is None or not cur.walls[1]):
                                player[0] += 1; moved = True
                    else:
                        # Noclip movement: ignores internal walls but respects map boundaries
                        if event.key in (pygame.K_UP, pygame.K_w):
                            if row_p > 0:
                                player[1] -= 1; moved = True
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            if row_p < rows - 1:
                                player[1] += 1; moved = True
                        elif event.key in (pygame.K_LEFT, pygame.K_a):
                            if col_p > 0:
                                player[0] -= 1; moved = True
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            if col_p < cols - 1:
                                player[0] += 1; moved = True
                    # If player moved, handle step logic
                    if moved:
                        steps += 1
                        if saves.step_sounds_enabled and steps == 200 and not played_200:
                            played_200 = True
                            if sounds.sound_200:
                                sounds.sound_200.set_volume(saves.sfx_volume)
                                sounds.sound_200.play()
                        if saves.step_sounds_enabled and steps == 300 and not played_300:
                            played_300 = True
                            if sounds.sound_300:
                                sounds.sound_300.set_volume(saves.sfx_volume)
                                sounds.sound_300.play()
                        # Play sound effects based on skin and noclip
                        if state.noclip == 0:
                            # Normal mode sound effects
                            if saves.equipped_skin == "Hillo.png" and steps != 200 and steps != 300:
                                if sounds.sound_fah:
                                    sounds.sound_fah.play()
                            if saves.equipped_skin == "imattheclub.png" and steps != 200 and steps != 300:
                                if sounds.sound_idk:
                                    sounds.sound_idk.play()
                            if saves.equipped_skin == "bart.png" and steps != 200 and steps != 300:
                                if sounds.sound_aycaramba:
                                    sounds.sound_aycaramba.play()
                            if saves.equipped_skin == "lebron.png":
                                if sounds.sound_flight:
                                    sounds.sound_flight.play()
                            if saves.equipped_skin == "dingle.png":
                                if sounds.sound_rizz:
                                    sounds.sound_rizz.play()
                        else:
                            # Noclip random sound effects
                            rando = random.randint(1, 85)
                            if rando in range(55, 85):
                                if sounds.sound_ankle:
                                    sounds.sound_ankle.play()
                            elif rando in range(1, 3):
                                if sounds.sound_talary:
                                    sounds.sound_talary.play()
                            elif rando in range(6,9):
                                if sounds.sound_sike:
                                    sounds.sound_sike.play()
                            elif rando in range(11, 12):
                                if sounds.sound_siren:
                                    sounds.sound_siren.play()
                            elif rando in range(16, 23):
                                if sounds.sound_weave:
                                    sounds.sound_weave.play()
                    # Check if player reached goal
                    if player == goal:
                        won      = True
                        win_time = time.time() - start_t
                        if canwin:
                            saves.wins += 1
                            canwin = False
                            saves.save_wins()

        # Smooth player position interpolation
        target_px = float(player[0] * cfg.CELL_SIZE + cfg.CELL_SIZE // 2)
        target_py = float(player[1] * cfg.CELL_SIZE + cfg.CELL_SIZE // 2)
        tp         = min(1.0, LERP_PLAYER * 60 * dt)
        smooth_px += (target_px - smooth_px) * tp
        smooth_py += (target_py - smooth_py) * tp

        # Calculate maze dimensions in pixels
        maze_pw = cols * cfg.CELL_SIZE
        maze_ph = rows * cfg.CELL_SIZE
        # Calculate target camera position
        tcx     = max(0, min(smooth_px - WINDOW_W // 2, maze_pw - WINDOW_W))
        tcy     = max(0, min(smooth_py - VIEW_H  // 2,  maze_ph - VIEW_H))
        tc      = min(1.0, LERP_CAM * 60 * dt)
        # Interpolate camera position
        cam_sx += (tcx - cam_sx) * tc
        cam_sy += (tcy - cam_sy) * tc

        # Fill screen with background color
        screen.fill((125, 115, 105))
        # Draw the maze
        draw_maze(screen, grid, cfg.CELL_SIZE, cam_sx, cam_sy)

        # Draw goal rectangle
        gsx = goal[0] * cfg.CELL_SIZE - int(cam_sx)
        gsy = goal[1] * cfg.CELL_SIZE - int(cam_sy)
        pygame.draw.rect(screen, GOAL_COLOR,
                         (gsx + 4, gsy + 4, cfg.CELL_SIZE - 8, cfg.CELL_SIZE - 8))

        # Draw player
        draw_px = int(smooth_px - cam_sx)
        draw_py = int(smooth_py - cam_sy)
        if saves.color_change_enabled:
            if steps >= 300:
                player_color = (255, 0, 0)  # red
            elif steps >= 200:
                player_color = (255, 165, 0)  # orange
            else:
                player_color = (255, 255, 0)  # yellow
        else:
            player_color = (255, 255, 0)
        pygame.draw.circle(screen, player_color, (draw_px, draw_py), radius)
        if player_surf:
            screen.blit(player_surf, (draw_px - radius, draw_py - radius))

        # Draw HUD
        elapsed = time.time() - start_t
        pygame.draw.rect(screen, (255, 255, 255), (0, VIEW_H, WINDOW_W, HUD_H))
        hud = font.render(f"Time:{int(elapsed)}s Steps: {steps}", True, (10, 10, 10))
        screen.blit(hud, (8, VIEW_H + 9))

        # Handle win screen
        if won:
            # Play win sound once
            if winplay:
                if saves.equipped_skin == "lebron.png":
                    if sounds.sound_cmonman:
                        sounds.canel.play(sounds.sound_cmonman)
                elif saves.equipped_skin == "bart.png":
                    if sounds.sound_eatmyshorts:
                        sounds.sound_eatmyshorts.play()
                else:
                    if sounds.sound_win:
                        sounds.sound_win.play()
                winplay = False

            # Draw win overlay
            overlay = pygame.Surface((WINDOW_W, VIEW_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            # Define win card dimensions
            card_w, card_h = 420, 220
            card_x = (WINDOW_W - card_w) // 2
            card_y = (VIEW_H - card_h) // 2
            card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            card.fill((30, 30, 50, 230))
            screen.blit(card, (card_x, card_y))
            pygame.draw.rect(screen, (120, 120, 200), (card_x, card_y, card_w, card_h), 2, border_radius=12)

            # Create fonts for win screen
            title_font = pygame.font.Font(None, 56)
            stat_font  = pygame.font.Font(None, 30)
            btn_font   = pygame.font.Font(None, 26)
            key_font   = pygame.font.Font(None, 20)

            # Render win title
            t = title_font.render("YOU WIN!", True, (255, 215, 0))
            screen.blit(t, t.get_rect(center=(WINDOW_W // 2, card_y + 44)))

            # Render stats
            s1 = stat_font.render(f"Steps: {steps}", True, (200, 200, 255))
            s2 = stat_font.render(f"Time:  {int(win_time)}s", True, (200, 200, 255))
            screen.blit(s1, s1.get_rect(center=(WINDOW_W // 2, card_y + 90)))
            screen.blit(s2, s2.get_rect(center=(WINDOW_W // 2, card_y + 118)))

            # Get mouse position for button hover
            mouse = pygame.mouse.get_pos()
            btn_w, btn_h = 118, 44
            gap = 10
            total_w = 3 * btn_w + 2 * gap
            bx = (WINDOW_W - total_w) // 2
            by = card_y + 152

            # Define win buttons
            win_btn_labels = [("Regenerate", "R"), ("Menu", "Esc"), ("Resize", "Q")]
            win_btn_rects = []
            for i, (label, hotkey) in enumerate(win_btn_labels):
                r = pygame.Rect(bx + i * (btn_w + gap), by, btn_w, btn_h)
                win_btn_rects.append(r)
                hov = r.collidepoint(mouse)
                pygame.draw.rect(screen, (85, 85, 118) if hov else (55, 55, 78), r, border_radius=8)
                pygame.draw.rect(screen, (120, 120, 200), r, 1, border_radius=8)
                lt = btn_font.render(label, True, (255, 255, 255))
                kt = key_font.render(hotkey, True, (150, 150, 200))
                screen.blit(lt, lt.get_rect(center=(r.centerx, r.y + 16)))
                screen.blit(kt, kt.get_rect(center=(r.centerx, r.y + 32)))

            # Handle win button clicks
            for event_w in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                if event_w.button == 1:
                    if win_btn_rects[0].collidepoint(event_w.pos):
                        (grid, player, goal, start_t, won, steps,
                         played_200, played_300, smooth_px, smooth_py,
                         cam_sx, cam_sy) = new_game(cols, rows)
                        canwin = True; sunshine = True; win_time = 0.0; winplay = True
                        player_surf = get_player_surf(all_imgs, radius)
                    elif win_btn_rects[1].collidepoint(event_w.pos):
                        pygame.mixer.stop(); mainmenu(); return
                    elif win_btn_rects[2].collidepoint(event_w.pos):
                        pygame.mixer.stop(); slider(); return

        # Update display
        pygame.display.flip()

    # Quit Pygame and exit
    pygame.quit()
    sys.exit()
