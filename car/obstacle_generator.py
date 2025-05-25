# car/obstacle_generator.py

import random

def generate_obstacles(grid_w, grid_h, path, count=30):
    """
    Генерирует препятствия вне трассы (path). Возвращает список (x, y).
    """
    occupied = set(path)
    obstacles = set()
    attempts = 0

    while len(obstacles) < count and attempts < count * 10:
        x = random.randint(0, grid_w - 1)
        y = random.randint(0, grid_h - 1)
        if (x, y) not in occupied and (x, y) not in obstacles:
            obstacles.add((x, y))
        attempts += 1

    return list(obstacles)
