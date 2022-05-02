import pygame
from game_engine.entities.weapon import Melee
from game_engine.helpers import Colors
from assets.images import battleaxe_image, mace_image,silversword_image, trident_image, warhammer_image

SampleWeaponSprite = pygame.Surface((20, 50), pygame.SRCALPHA)
SampleWeaponSprite.fill(Colors.CYAN)
pygame.draw.polygon(SampleWeaponSprite, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))

sample_weapon = Melee(pygame.Vector2(0,0),SampleWeaponSprite, 30, 10)

battleaxe = Melee(
  pygame.Vector2(0,0),
  pygame.transform.scale(battleaxe_image, (50, 75)),
  75, 7)
mace = Melee(
  pygame.Vector2(0,0),
  pygame.transform.scale(mace_image, (40, 52)),
  30, 8)

silversword = Melee(
  pygame.Vector2(0,0),
  pygame.transform.scale(silversword_image, (45, 62)),
  40, 9)


trident = Melee(
  pygame.Vector2(0,0),
  pygame.transform.scale(trident_image, (50, 75)),
  95, 5)


warhammer = Melee(
  pygame.Vector2(0,0),
  pygame.transform.scale(warhammer_image, (60, 90)),
  120, 3)