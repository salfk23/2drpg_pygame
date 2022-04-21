import pygame
from engine.entities.entity import Entity, Hurtable, IMoveable


class Weapon(Entity):
  def __init__(self, x:int, y:int, width:int, height:int, sprite:pygame.Surface):
    super().__init__(x, y, width, height, sprite)
    self.name = "Weapon"
    self.remove = False

class Projectile(Entity, Hurtable, IMoveable):
  def __init__(self, x:int, y:int, width:int, height:int, sprite:pygame.Surface):
    super().__init__(x, y, width, height, sprite)
    Hurtable.__init__(self, 100, 100)
    self.name = "Projectile"
    self.remove = False


