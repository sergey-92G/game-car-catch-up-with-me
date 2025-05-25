# game_loop.py

import pygame
# Инициализируем модуль шрифтов до создания font
pygame.font.init()

from car.config import config
from car.track_generator import generate_track
from car.obstacle_generator import generate_obstacles
from car.ai_driver import chase_player

# Константы экрана и сетки
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
STATE_MENU = "MENU"
STATE_EXIT = "EXIT"

# Экран создаётся в main, но если вызываем отдельно, инициализируем дисплей
if not pygame.display.get_init():
    pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Создаём font после инициализации шрифтов
font = pygame.font.SysFont("arial", 36)

# Проверка на столкновение с препятствием
def is_colliding(pos, obstacles, radius):
    grid_x = int(pos.x) // CELL_SIZE
    grid_y = int(pos.y) // CELL_SIZE
    return (grid_x, grid_y) in obstacles


def game_loop():
    clock = pygame.time.Clock()

    player_pos = pygame.Vector2(WIDTH // 4, HEIGHT // 2)
    ai_pos = pygame.Vector2(3 * WIDTH // 4, HEIGHT // 2)
    speed = 4
    ai_speed = config.ai_speed
    radius = 20
    start_time = pygame.time.get_ticks()

    # Генерация мира
    path = generate_track(GRID_WIDTH, GRID_HEIGHT)
    obstacles = set()
    if config.use_obstacles:
        obstacles = set(generate_obstacles(GRID_WIDTH, GRID_HEIGHT, path, count=30))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return STATE_MENU

        # Таймер
        if config.timer_enabled:
            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed > config.timer_seconds:
                return STATE_MENU

        # Управление игроком
        keys = pygame.key.get_pressed()
        move_vector = pygame.Vector2(0, 0)
        if keys[pygame.K_UP]:
            move_vector.y -= speed
        if keys[pygame.K_DOWN]:
            move_vector.y += speed
        if keys[pygame.K_LEFT]:
            move_vector.x -= speed
        if keys[pygame.K_RIGHT]:
            move_vector.x += speed

        new_pos = player_pos + move_vector
        if not is_colliding(new_pos, obstacles, radius):
            player_pos = new_pos

        # AI преследует игрока
        ai_next = chase_player(ai_pos, player_pos, ai_speed, obstacles, CELL_SIZE)
        ai_pos = ai_next

        # Столкновение с ИИ
        if player_pos.distance_to(ai_pos) < radius * 2:
            return STATE_MENU

        # Отрисовка
        screen.fill(GRAY)

        # Препятствия
        for (x, y) in obstacles:
            pygame.draw.rect(screen, (100, 100, 100), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Машинки
        pygame.draw.circle(screen, config.player_color, player_pos, radius)
        pygame.draw.circle(screen, (255, 0, 0), ai_pos, radius)

        # Таймер
        if config.timer_enabled:
            time_left = max(0, config.timer_seconds - int(elapsed))
            time_text = font.render(f"Время: {time_left}", True, WHITE)
            screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
