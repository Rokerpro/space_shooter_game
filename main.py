import pygame, random
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet, Laser
from powerup import PowerUp
from utils import collide, spawn_wave
from sounds import enemy_hit_sound, player_hit_sound, game_over_sound
import os

os.system("clear")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Defender")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 50)

#load images
player_img = pygame.image.load("assets/png/player.png").convert_alpha()
enemy_img = pygame.image.load("assets/png/enemy.png").convert_alpha()
power_imgs = {
    "life": pygame.image.load("assets/png/power_life.png").convert_alpha(),
    "shield": pygame.image.load("assets/png/power_shield.png").convert_alpha(),
    "double_laser": pygame.image.load("assets/png/power_double.png").convert_alpha()
}

#game objects
player = Player(WIDTH//2 - 25, HEIGHT - 60)
bullets = []
lasers = []
enemies = []
powerups = []
enemy_dir = 1
level = 1
game_over = False

spawn_wave(level, enemies)

#main loop
running = True
while running:
    now = pygame.time.get_ticks()
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and player.can_shoot(now):
                bullets.append(player.shoot(now))

    if game_over:
        screen.fill(BLACK)
        t = big_font.render("GAME OVER", True, RED)
        s = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 40))
        screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 + 10))
        pygame.display.flip()
        continue

    #input
    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    player.move(dx)

    #laser shooting
    if keys[pygame.K_SPACE] and now - player.laser_timer >= player.laser_cooldown:
        lasers.append(player.shoot_laser())
        if player.double_laser > 0:
            lasers.append(player.shoot_laser())  # extra laser
        player.laser_timer = now

    #update bullets
    for b in bullets[:]:
        b.update()
        if b.y < -50 or b.y > HEIGHT + 50:
            bullets.remove(b)

    #update lasers
    for l in lasers[:]:
        l.update()
        if l.y < -50:
            lasers.remove(l)
        for e in enemies[:]:
            if collide(l, e):
                lasers.remove(l)
                enemies.remove(e)
                player.score += 100
                enemy_hit_sound.play()
                if random.random() < 0.2:
                    powerups.append(PowerUp(e.x + e.w//2, e.y + e.h))
                break

    #update power-ups
    for p in powerups[:]:
        p.update()
        if p.y > HEIGHT:
            powerups.remove(p)
        elif collide(p, player):
            if p.type == "life":
                player.lives += 1
            elif p.type == "double_laser":
                player.double_laser = 300
            elif p.type == "shield":
                player.shield = 300
            powerups.remove(p)

    #enemy movement
    if enemies:
        left = min(e.x for e in enemies)
        right = max(e.x + e.w for e in enemies)
        if right > WIDTH-20:
            enemy_dir = -1
            for e in enemies: e.y += ENEMY_DROP
        if left < 20:
            enemy_dir = 1
            for e in enemies: e.y += ENEMY_DROP

    for e in enemies[:]:
        e.update(enemy_dir * (ENEMY_SPEED + level*0.2))
        if random.random() < ENEMY_FIRE_RATE:
            bullets.append(Bullet(e.x+e.w//2, e.y+e.h, BULLET_SPEED, "enemy"))

    #bullet collisions
    for b in bullets[:]:
        if b.owner == "player":
            for e in enemies[:]:
                if collide(b, e):
                    bullets.remove(b)
                    enemies.remove(e)
                    player.score += 100
                    enemy_hit_sound.play()
                    if random.random() < 0.2:
                        powerups.append(PowerUp(e.x + e.w//2, e.y + e.h))
                    break
        elif b.owner == "enemy" and collide(b, player):
            if player.shield > 0:
                player.shield -= 1
                bullets.remove(b)
            else:
                bullets.remove(b)
                player.lives -= 1
                player_hit_sound.play()
                if player.lives <= 0:
                    game_over = True
                    game_over_sound.play()

    #next wave
    if not enemies:
        level += 1
        player.score += 500
        spawn_wave(level, enemies)

    #draw
    bg_color = BG_COLORS[(level-1) % len(BG_COLORS)]
    screen.fill(bg_color)

    #draw player
    pygame.draw.polygon(screen, BLUE, [
    (player.x, player.y + player.h),
    (player.x + player.w, player.y + player.h),
    (player.x + player.w//2, player.y)
])

    player.draw_shield(screen)

    #draw enemies
    for e in enemies:
        img = pygame.transform.scale(enemy_img, (60, 40))  # smaller size: 30x20 pixels
        screen.blit(img, (e.x, e.y))


    #draw bullets
    for b in bullets:
        pygame.draw.rect(screen, YELLOW if b.owner=="player" else GREEN, b.rect())

    #draw lasers
    for l in lasers:
        pygame.draw.rect(screen, CYAN, l.rect())

    #draw power-ups
    for p in powerups:
        img = pygame.transform.scale(power_imgs[p.type], (30, 30))  # scale to 20x20 pixels
        screen.blit(img, (p.x, p.y))


    #hub
    hud = font.render(f"Score: {player.score}  Lives: {player.lives}  Level: {level}", True, WHITE)
    screen.blit(hud, (10,10))

    #decrease timer
    if player.double_laser > 0:
        player.double_laser -= 1
    if player.shield > 0:
        player.shield -= 1

    pygame.display.flip()

pygame.quit()   