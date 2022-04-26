import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import BiDirectionalEntity
from game_engine.helpers import Size2D


class Weapon(MovableEntity, BiDirectionalEntity):
  def __init__(self, sprite:pygame.Surface, size:Size2D, damage:int, speed:int):
    super().__init__((0,0), size)
    BiDirectionalEntity.__init__(self, sprite)
    self.sprite = sprite
    self.speed = speed
    self.damage = damage
    self.attacking = False
    self.frame = 0

  def update(self):
    if self.attacking:
      self.frame += self.speed
      if self.frame <= 90:
        if self.direction:
          # Rotate the sprite 90 degrees to the right incrementally
          self.sprite = pygame.transform.rotate(self.sprite, 3)
        else:
          # Rotate the sprite 90 degrees to the left incrementally
          self.sprite = pygame.transform.rotate(self.sprite, -3)
      if self.frame > 180:
        self.attacking = False
        self.frame = 0
    else:
      self.frame = 0





