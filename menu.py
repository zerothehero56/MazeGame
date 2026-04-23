# menu.py
# Module for the main menu interface
import sys
import pygame

import saves
import skins
import sounds
from config import (
    screen,
    WINDOW_W,
    WINDOW_H,
    FPS,
    btn_play,
    btn_skins,
    btn_quit,
    btn_secret,
    btn_settings,
    menu_styles,
    THEME,
    draw_vertical_gradient,
    draw_button,
)
from slider import slider
import state

# Function for the main menu
def mainmenu():
    # Unpack menu styles
    btn_font = menu_styles['btn_font']
    sub_font = menu_styles['sub_font']
    key_font = menu_styles['key_font']
    btn_col = menu_styles['btn_col']
    btn_hov = menu_styles['btn_hov']

    # Pygame clock and running flag
    clock   = pygame.time.Clock()
    running = True
    # Loading screen
    draw_vertical_gradient(screen, THEME['bg_top'], THEME['bg_bottom'])
    loading_font = pygame.font.Font(None, 44)
    loading_text = loading_font.render("Loading...", True, THEME['button_text'])
    screen.blit(loading_text, loading_text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2)))
    pygame.display.flip()

    # Load all sounds
    sounds.load_all_sounds()
    pygame.mixer.music.stop()
    pygame.mixer.stop()


    # Main menu loop
    while running:
        # Limit frame rate
        clock.tick(FPS)
        # Get mouse position
        mouse = pygame.mouse.get_pos()

        # Check button hovers
        hover_play    = btn_play.collidepoint(mouse)
        hover_skins   = btn_skins.collidepoint(mouse)
        hover_quit    = btn_quit.collidepoint(mouse)
        hover_secret = btn_secret.collidepoint(mouse)
        hover_settings = btn_settings.collidepoint(mouse)

        draw_vertical_gradient(screen, THEME['bg_top'], THEME['bg_bottom'])

        # Render title
        title_font = pygame.font.Font(None, 50)
        title = title_font.render("TITLED MAZE GAME", True, THEME['title'])
        screen.blit(title, title.get_rect(center=(WINDOW_W // 2, 52)))

        # Render wins subtitle
        sub = sub_font.render(f"Wins: {saves.wins}", True, THEME['accent'])
        screen.blit(sub, sub.get_rect(center=(WINDOW_W // 2, 84)))

        # Draw buttons
        for btn, hov, label, hotkey, col, hov_col in [
            (btn_play,    hover_play,    "Play",  "E",   btn_col, btn_hov),
            (btn_skins,   hover_skins,   "Skins", "S",   btn_col, btn_hov),
            (btn_quit,    hover_quit,    "Quit",  "Esc", btn_col, btn_hov),
            (btn_settings, hover_settings, "Settings", "T",   btn_col, btn_hov),
        ]:
            draw_button(
                screen,
                btn,
                label,
                hotkey,
                hov,
                btn_font,
                key_font,
                base_color=col,
                hover_color=hov_col,
            )

        # Update display
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle button clicks
                if hover_play:
                    slider(); return
                if hover_skins:
                    skins.skinmenu(); continue
                if hover_settings:
                    import settings
                    settings.settingsmenu(); continue
                if hover_quit:
                    pygame.quit(); sys.exit()
                if hover_secret:
                    # Secret button logic
                    if not saves.secret_lebron_unlocked:
                        saves.secret_lebron_unlocked = True
                        saves.save_skin_state()
                    # Toggle noclip mode
                    if state.noclip == 1:
                        state.noclip = 0
                        if sounds.sound_flight:
                            sounds.sound_flight.set_volume(saves.sfx_volume)
                            sounds.sound_flight.play()
                    elif state.noclip == 0:
                        if sounds.sound_fah:
                            sounds.sound_fah.set_volume(saves.sfx_volume)
                            sounds.sound_fah.play()
                        state.noclip = 1
            elif event.type == pygame.KEYDOWN:
                # Handle key presses
                if event.key == pygame.K_e:
                    slider()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); running = False; sys.exit()
                if event.key == pygame.K_s:
                    skins.skinmenu(); continue          
                if event.key == pygame.K_t: 
                    import settings
                    settings.settingsmenu(); continue
