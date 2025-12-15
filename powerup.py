from game_object import GameObject
import random
from config import CYAN, GREEN, YELLOW
import pygame

class PowerUp(GameObject):
    TYPES = ["life", "double_laser", "shield"]

    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.type = random.choice(self.TYPES)
        self.vy = 3  #falling speed

    def update(self):
        self.y += self.vy

    def draw(self, screen):
        color = CYAN if self.type == "double_laser" else GREEN if self.type == "shield" else YELLOW
        pygame.draw.rect(screen, color, self.rect())
