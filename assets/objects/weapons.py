import pygame
from game_engine.entities.weapon import Melee, Weapon
from game_engine.helpers import Colors

SampleWeaponSprite = pygame.Surface((20, 50), pygame.SRCALPHA)
SampleWeaponSprite.fill(Colors.CYAN)
pygame.draw.polygon(SampleWeaponSprite, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))

sample_weapon = Melee(pygame.Vector2(0,0),SampleWeaponSprite, (10, 50), 30, 10)


SampleWeaponSprite = pygame.Surface((20, 50), pygame.SRCALPHA)
SampleWeaponSprite.fill(Colors.YELLOW)
pygame.draw.polygon(SampleWeaponSprite, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))

sample_weapon2 = Melee(pygame.Vector2(0,0),SampleWeaponSprite, (10, 50), 30, 10)
