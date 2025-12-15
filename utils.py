import random
from enemy import Enemy

def collide(a, b):
    return a.rect().colliderect(b.rect())

def spawn_wave(level, enemies_list):
    enemies_list.clear()
    cols = 6 + level
    rows = 3 + level//2
    spacing = 60
    for r in range(rows):
        for c in range(cols):
            x = 60 + c*spacing
            y = 60 + r*40
            enemies_list.append(Enemy(x, y))
