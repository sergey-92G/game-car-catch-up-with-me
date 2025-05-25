# car/track_generator.py

import random

def generate_track(grid_w, grid_h):
    """Генерирует проходимую трассу от левого до правого края."""
    path = []
    x, y = 0, random.randint(0, grid_h - 1)
    path.append((x, y))

    while x < grid_w - 1:
        direction = random.choice(["right", "up", "down"])
        if direction == "right":
            x += 1
        elif direction == "up" and y > 0:
            y -= 1
        elif direction == "down" and y < grid_h - 1:
            y += 1
        path.append((x, y))

    return path
