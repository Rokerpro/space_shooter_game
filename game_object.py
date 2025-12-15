from dataclasses import dataclass
import pygame

@dataclass
class GameObject:
    x: float
    y: float
    w: int
    h: int

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
