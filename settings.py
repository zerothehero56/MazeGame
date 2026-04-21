# settings.py
# Module for settings menu
import sys
import pygame

import config as cfg
import saves

# Function for the settings menu
def settingsmenu():
    # Unpack menu styles
    btn_font = cfg.menu_styles['btn_font']
    sub_font = cfg.menu_styles['sub_font']
    small_font = cfg.menu_styles['key_font']
    bg_col = cfg.menu_styles['bg_col']
    # Pygame clock
    clock    = pygame.time.Clock()
    # Stop music
    pygame.mixer.stop()

    # Slider constants
    MIN_VOL = 0.0
    MAX_VOL = 1.0
    # Current volumes
    bg_vol  = saves.bg_volume
    sfx_vol = saves.sfx_volume
    # Slider positions - centered
    slider_w = 300
    slider_x = (cfg.WINDOW_W - slider_w) // 2
    slider_y_bg = 200
    slider_y_sfx = 280
    slider_h = 8
    handle_r = 12

    # Toggle buttons - centered
    button_w = 180
    gap = 20
    total_w = button_w * 2 + gap
    start_x = (cfg.WINDOW_W - total_w) // 2
    step_btn = pygame.Rect(start_x, 360, button_w, 50)
    color_btn = pygame.Rect(start_x + button_w + gap, 360, button_w, 50)
    back_btn_w = 150
    back_btn = pygame.Rect((cfg.WINDOW_W - back_btn_w) // 2, 440, back_btn_w, 50)

    # Function to convert vol to slider x
    def vol_to_x(val):
        t = (val - MIN_VOL) / (MAX_VOL - MIN_VOL)
        return int(slider_x + t * slider_w)

    # Function to convert slider x to vol
    def x_to_vol(x):
        t = (x - slider_x) / slider_w
        return round(MIN_VOL + t * (MAX_VOL - MIN_VOL), 2)

    # Dragging flags
    dragging_bg = False
    dragging_sfx = False
    running = True
    while running:
        clock.tick(cfg.FPS)
        mouse = pygame.mouse.get_pos()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    saves.save_settings()
                    from menu import mainmenu
                    mainmenu(); return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check sliders
                handle_bg_x = vol_to_x(bg_vol)
                if abs(mouse[0] - handle_bg_x) <= handle_r + 4 and abs(mouse[1] - slider_y_bg) <= handle_r + 4:
                    dragging_bg = True
                handle_sfx_x = vol_to_x(sfx_vol)
                if abs(mouse[0] - handle_sfx_x) <= handle_r + 4 and abs(mouse[1] - slider_y_sfx) <= handle_r + 4:
                    dragging_sfx = True
                # Check buttons
                if step_btn.collidepoint(mouse):
                    saves.step_sounds_enabled = not saves.step_sounds_enabled
                if color_btn.collidepoint(mouse):
                    saves.color_change_enabled = not saves.color_change_enabled
                if back_btn.collidepoint(mouse):
                    saves.save_settings()
                    from menu import mainmenu
                    mainmenu(); return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_bg = False
                dragging_sfx = False
            if event.type == pygame.MOUSEMOTION:
                if dragging_bg:
                    bg_vol = x_to_vol(max(slider_x, min(slider_x + slider_w, mouse[0])))
                    saves.bg_volume = bg_vol
                if dragging_sfx:
                    sfx_vol = x_to_vol(max(slider_x, min(slider_x + slider_w, mouse[0])))
                    saves.sfx_volume = sfx_vol

        # Fill screen
        cfg.screen.fill(bg_col)

        # Render title
        title = btn_font.render("SETTINGS", True, (210, 210, 255))
        cfg.screen.blit(title, title.get_rect(center=(cfg.WINDOW_W // 2, 80)))

        # BG Volume slider
        label_bg = sub_font.render(f"BG Volume: {int(bg_vol * 100)}%", True, (255, 255, 255))
        cfg.screen.blit(label_bg, (slider_x, slider_y_bg - 40))
        pygame.draw.rect(cfg.screen, (60, 60, 80), (slider_x, slider_y_bg - slider_h // 2, slider_w, slider_h), border_radius=4)
        filled_w = vol_to_x(bg_vol) - slider_x
        pygame.draw.rect(cfg.screen, (85, 85, 118), (slider_x, slider_y_bg - slider_h // 2, filled_w, slider_h), border_radius=4)
        handle_bg_x = vol_to_x(bg_vol)
        pygame.draw.circle(cfg.screen, (210, 210, 255), (handle_bg_x, slider_y_bg), handle_r)
        pygame.draw.circle(cfg.screen, (85, 85, 118), (handle_bg_x, slider_y_bg), handle_r - 3)

        # SFX Volume slider
        label_sfx = sub_font.render(f"SFX Volume: {int(sfx_vol * 100)}%", True, (255, 255, 255))
        cfg.screen.blit(label_sfx, (slider_x, slider_y_sfx - 40))
        pygame.draw.rect(cfg.screen, (60, 60, 80), (slider_x, slider_y_sfx - slider_h // 2, slider_w, slider_h), border_radius=4)
        filled_w = vol_to_x(sfx_vol) - slider_x
        pygame.draw.rect(cfg.screen, (85, 85, 118), (slider_x, slider_y_sfx - slider_h // 2, filled_w, slider_h), border_radius=4)
        handle_sfx_x = vol_to_x(sfx_vol)
        pygame.draw.circle(cfg.screen, (210, 210, 255), (handle_sfx_x, slider_y_sfx), handle_r)
        pygame.draw.circle(cfg.screen, (85, 85, 118), (handle_sfx_x, slider_y_sfx), handle_r - 3)

        # Toggle buttons
        hover_step = step_btn.collidepoint(mouse)
        pygame.draw.rect(cfg.screen, (85, 85, 118) if hover_step else (55, 55, 78), step_btn, border_radius=10)
        step_text = sub_font.render(f"200&300 SFX: {'On' if saves.step_sounds_enabled else 'Off'}", True, (255, 255, 255))
        cfg.screen.blit(step_text, step_text.get_rect(center=step_btn.center))

        hover_color = color_btn.collidepoint(mouse)
        pygame.draw.rect(cfg.screen, (85, 85, 118) if hover_color else (55, 55, 78), color_btn, border_radius=10)
        color_text = sub_font.render(f"Color Change: {'On' if saves.color_change_enabled else 'Off'}", True, (255, 255, 255))
        cfg.screen.blit(color_text, color_text.get_rect(center=color_btn.center))

        # Back button
        hover_back = back_btn.collidepoint(mouse)
        pygame.draw.rect(cfg.screen, (85, 85, 118) if hover_back else (55, 55, 78), back_btn, border_radius=10)
        back_text = sub_font.render("Back", True, (255, 255, 255))
        cfg.screen.blit(back_text, back_text.get_rect(center=back_btn.center))

        # Update display
        pygame.display.flip()
