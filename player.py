import pygame
from game_object import GameObject
from bullet import Bullet, Laser
from sounds import shoot_sound, laser_sound
from config import PLAYER_SPEED, BULLET_SPEED

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 30)
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.last_shot = 0
        self.shoot_delay = 300
        self.score = 0
        self.laser_timer = 0
        self.laser_cooldown = 200
        self.double_laser = 0    #duration in frames
        self.shield = 0  

    def move(self, dx):
        self.x += dx * self.speed
        from config import WIDTH
        self.x = max(0, min(WIDTH - self.w, self.x))

    def can_shoot(self, now):
        return now - self.last_shot >= self.shoot_delay

    def shoot(self, now):
        self.last_shot = now
        shoot_sound.play()
        return Bullet(self.x + self.w//2, self.y, -BULLET_SPEED, "player")

    def shoot_laser(self):
        laser_sound.play()
        return Laser(self.x + self.w//2, self.y)
    def draw_shield(self, screen):
        if self.shield > 0:
            pygame.draw.ellipse(screen, (0, 200, 255), (self.x-5, self.y-5, self.w+10, self.h+10), 3)
