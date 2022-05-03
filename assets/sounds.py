import pygame
import game_engine.helpers as helpers

pygame.mixer.init()

game_music = pygame.mixer.Sound("assets/sounds/game_run.ogg")
main_menu_music = pygame.mixer.Sound("assets/sounds/main_menu.wav")

game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.ogg")

explode_sound = pygame.mixer.Sound("assets/sounds/explode.wav")
death_sound = pygame.mixer.Sound("assets\sounds\death.ogg")

demon_death_sound = pygame.mixer.Sound("assets\sounds\demon_death.wav")
demon_grunt_sound = pygame.mixer.Sound("assets\sounds\demon_grunt.wav")
demon_hurt_sound = pygame.mixer.Sound("assets\sounds\demon_hurt.wav")

goblin_death_sound = pygame.mixer.Sound("assets\sounds\goblin_death.wav")
goblin_grunt_sound = pygame.mixer.Sound("assets\sounds\goblin_grunt.wav")
goblin_hurt_sound = pygame.mixer.Sound("assets\sounds\goblin_hurt.wav")

minotaur_death_sound = pygame.mixer.Sound("assets\sounds\minotaur_death.ogg")
minotaur_grunt_sound = pygame.mixer.Sound("assets\sounds\minotaur_grunt.wav")
minotaur_hurt_sound = pygame.mixer.Sound("assets\sounds\minotaur_hurt.ogg")

zombie_death_sound = pygame.mixer.Sound("assets\sounds\zombie_death.wav")
zombie_grunt_sound = pygame.mixer.Sound("assets\sounds\zombie_grunt.wav")
zombie_hurt_sound = pygame.mixer.Sound("assets\sounds\zombie_hurt.wav")


hit_blunt_1_sound = pygame.mixer.Sound("assets\sounds\hit_blunt_1.wav")
hit_blunt_2_sound = pygame.mixer.Sound("assets\sounds\hit_blunt_2.wav")
hit_blunt_3_sound = pygame.mixer.Sound("assets\sounds\hit_blunt_3.wav")

hit_sharp_1_sound = pygame.mixer.Sound("assets\sounds\hit_sharp_1.wav")
hit_sharp_2_sound = pygame.mixer.Sound("assets\sounds\hit_sharp_2.wav")
hit_sharp_3_sound = pygame.mixer.Sound("assets\sounds\hit_sharp_3.wav")

hit_blunt_sounds = [hit_blunt_1_sound, hit_blunt_2_sound, hit_blunt_3_sound]
hit_sharp_sounds = [hit_sharp_1_sound, hit_sharp_2_sound, hit_sharp_3_sound]