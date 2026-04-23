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
    key_font = cfg.menu_styles['key_font']
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
        cfg.draw_vertical_gradient(cfg.screen, cfg.THEME['bg_top'], cfg.THEME['bg_bottom'])

        # Render title
        title = btn_font.render("SETTINGS", True, cfg.THEME['title'])
        cfg.screen.blit(title, title.get_rect(center=(cfg.WINDOW_W // 2, 80)))

        # BG Volume slider
        label_bg = sub_font.render(f"BG Volume: {int(bg_vol * 100)}%", True, cfg.THEME['button_text'])
        cfg.screen.blit(label_bg, (slider_x, slider_y_bg - 40))
        pygame.draw.rect(cfg.screen, cfg.THEME['panel_alt'], (slider_x, slider_y_bg - slider_h // 2, slider_w, slider_h), border_radius=4)
        filled_w = vol_to_x(bg_vol) - slider_x
        pygame.draw.rect(cfg.screen, cfg.THEME['button_hover'], (slider_x, slider_y_bg - slider_h // 2, filled_w, slider_h), border_radius=4)
        handle_bg_x = vol_to_x(bg_vol)
        pygame.draw.circle(cfg.screen, cfg.THEME['title'], (handle_bg_x, slider_y_bg), handle_r)
        pygame.draw.circle(cfg.screen, cfg.THEME['button'], (handle_bg_x, slider_y_bg), handle_r - 3)

        # SFX Volume slider
        label_sfx = sub_font.render(f"SFX Volume: {int(sfx_vol * 100)}%", True, cfg.THEME['button_text'])
        cfg.screen.blit(label_sfx, (slider_x, slider_y_sfx - 40))
        pygame.draw.rect(cfg.screen, cfg.THEME['panel_alt'], (slider_x, slider_y_sfx - slider_h // 2, slider_w, slider_h), border_radius=4)
        filled_w = vol_to_x(sfx_vol) - slider_x
        pygame.draw.rect(cfg.screen, cfg.THEME['button_hover'], (slider_x, slider_y_sfx - slider_h // 2, filled_w, slider_h), border_radius=4)
        handle_sfx_x = vol_to_x(sfx_vol)
        pygame.draw.circle(cfg.screen, cfg.THEME['title'], (handle_sfx_x, slider_y_sfx), handle_r)
        pygame.draw.circle(cfg.screen, cfg.THEME['button'], (handle_sfx_x, slider_y_sfx), handle_r - 3)

        # Toggle buttons
        hover_step = step_btn.collidepoint(mouse)
        cfg.draw_button(
            cfg.screen,
            step_btn,
            f"200&300 SFX: {'On' if saves.step_sounds_enabled else 'Off'}",
            "",
            hover_step,
            sub_font,
            key_font,
        )

        hover_color = color_btn.collidepoint(mouse)
        cfg.draw_button(
            cfg.screen,
            color_btn,
            f"Color Change: {'On' if saves.color_change_enabled else 'Off'}",
            "",
            hover_color,
            sub_font,
            key_font,
        )

        # Back button
        hover_back = back_btn.collidepoint(mouse)
        cfg.draw_button(cfg.screen, back_btn, "Back", "Esc", hover_back, sub_font, key_font)

        # Update display
        pygame.display.flip()
