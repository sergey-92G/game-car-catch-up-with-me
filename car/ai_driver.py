# car/ai_driver.py

import pygame

def chase_player(ai_pos, player_pos, speed, obstacles, cell_size):
    """
    Примитивная логика движения ИИ к игроку с учётом препятствий.
    Не заходит в клетки, занятые препятствиями.
    """
    direction = player_pos - ai_pos
    if direction.length() == 0:
        return ai_pos

    direction = direction.normalize() * speed
    next_pos = ai_pos + direction

    grid_x = int(next_pos.x) // cell_size
    grid_y = int(next_pos.y) // cell_size
    if (grid_x, grid_y) not in obstacles:
        return next_pos

    # Пробуем обойти — вбок или назад
    alt_dirs = [
        pygame.Vector2(direction.y, -direction.x),
        pygame.Vector2(-direction.y, direction.x),
        pygame.Vector2(-direction.x, -direction.y)
    ]
    for alt in alt_dirs:
        alt_pos = ai_pos + alt.normalize() * speed
        gx = int(alt_pos.x) // cell_size
        gy = int(alt_pos.y) // cell_size
        if (gx, gy) not in obstacles:
            return alt_pos

    return ai_pos
