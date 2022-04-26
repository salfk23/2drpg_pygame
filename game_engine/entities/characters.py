
from typing import Sequence
import pygame
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity

from game_engine.entities.entity import NORMAL_SIZE_ENTITY, Entity
from game_engine.entities.state import Hurtable, Solid
from game_engine.helpers import Colors, Size2D



class Healthbar(Entity, Hurtable):
  def __init__(self, size: Size2D):
      super().__init__(0,0, size)
      Hurtable.__init__(self)
      self.object = pygame.Surface(size)
      self.object.fill(Colors.RED)
      # Create a rectangle with color green
      rect = pygame.Rect(0, 0, size.x, size.y)
      rect.center = self.object.get_rect().center
      rect.width = self.health * size.x / self.max_health

      pygame.Surface.fill(self.object, Colors.GREEN, rect)



  def on_health_change(self):
    pass

  def die(self):
    # Do nothing
    pass


class Character(ControllableEntity, Hurtable, AffectedByGravity, Solid):
  def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      super().__init__(position, size, speed, jump_power)
      Hurtable.__init__(self, 100, 100)

  @property
  def health(self):
      return self._health
  @health.setter
  def health(self, health: int):
      Hurtable.health.fset(self, health)

  def update(self):
    AffectedByGravity.update(self)
    ControllableEntity.update(self)