# main.py

import pygame
import sys
from game_loop import game_loop
from car.config import config

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Машинки: Догоняшки")
font = pygame.font.SysFont("arial", 36)

# Состояния
STATE_MENU = "MENU"
STATE_SETTINGS = "SETTINGS"
STATE_GAME = "GAME"
STATE_EXIT = "EXIT"

# Элементы интерфейса
menu_items = ["Старт", "Настройки", "Рекорды (todo)", "Выход"]
color_options = [(255, 0, 0), (0, 120, 255), (0, 255, 0), (255, 255, 0)]

def draw_menu(selected_idx):
    screen.fill(BLACK)
    for idx, item in enumerate(menu_items):
        color = BLUE if idx == selected_idx else WHITE
        text = font.render(item, True, color)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + idx * 50))
        screen.blit(text, rect)

def draw_settings(selected_idx):
    options = [
        f"Препятствия: {'да' if config.use_obstacles else 'нет'}",
        f"Таймер: {'да' if config.timer_enabled else 'нет'}",
        f"Скорость ИИ: {config.ai_speed}",
        "Цвет игрока",
        "Назад"
    ]
    screen.fill(BLACK)
    for idx, item in enumerate(options):
        color = GREEN if idx == selected_idx else WHITE
        text = font.render(item, True, color)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + idx * 50))
        screen.blit(text, rect)

    if selected_idx == 3:
        for i, col in enumerate(color_options):
            rect = pygame.Rect(WIDTH // 2 - 90 + i * 60, HEIGHT // 2 + 150, 40, 40)
            pygame.draw.rect(screen, col, rect)
            if config.player_color == col:
                pygame.draw.rect(screen, WHITE, rect, 3)

def handle_settings_input(event, selected_idx):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if selected_idx == 0:
                config.use_obstacles = not config.use_obstacles
            elif selected_idx == 1:
                config.timer_enabled = not config.timer_enabled
            elif selected_idx == 2:
                config.ai_speed = round(config.ai_speed + 0.5, 1) if config.ai_speed < 5 else 1.0
            elif selected_idx == 4:
                return STATE_MENU
        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and selected_idx == 3:
            idx = color_options.index(config.player_color)
            delta = -1 if event.key == pygame.K_LEFT else 1
            config.player_color = color_options[(idx + delta) % len(color_options)]
    return STATE_SETTINGS

def main():
    state = STATE_MENU
    selected_menu = 0
    selected_settings = 0

    while state != STATE_EXIT:
        if state == STATE_MENU:
            draw_menu(selected_menu)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = STATE_EXIT
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_menu = (selected_menu - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_menu = (selected_menu + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if selected_menu == 0:
                            state = game_loop()
                        elif selected_menu == 1:
                            state = STATE_SETTINGS
                        elif selected_menu == 3:
                            state = STATE_EXIT

        elif state == STATE_SETTINGS:
            draw_settings(selected_settings)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = STATE_EXIT
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_settings = (selected_settings - 1) % 5
                    elif event.key == pygame.K_DOWN:
                        selected_settings = (selected_settings + 1) % 5
                    else:
                        state = handle_settings_input(event, selected_settings)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
