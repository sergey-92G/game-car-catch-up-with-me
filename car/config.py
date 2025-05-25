# car/config.py

class GameConfig:
    def __init__(self):
        self.use_obstacles = True
        self.ai_speed = 2.0
        self.timer_enabled = False
        self.timer_seconds = 60
        self.player_color = (0, 120, 255)  # Синий по умолчанию

config = GameConfig()
