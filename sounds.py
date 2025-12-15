import pygame

pygame.mixer.init()

#background music
pygame.mixer.music.load("assets/sound/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # loop forever

#sound effects
shoot_sound = pygame.mixer.Sound("assets/sound/shoot.mp3")
laser_sound = pygame.mixer.Sound("assets/sound/laser.mp3")
enemy_hit_sound = pygame.mixer.Sound("assets/sound/enemy_hit.wav")
player_hit_sound = pygame.mixer.Sound("assets/sound/player_hit.wav")
game_over_sound = pygame.mixer.Sound("assets/sound/game_over.wav")