
from typing import Sequence
import pygame
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity

from game_engine.entities.entity import NORMAL_SIZE_ENTITY, Entity
from game_engine.entities.state import Hurtable, Solid
from game_engine.helpers import Colors, Size2D



class Healthbar(Entity):
  def __init__(self, size: pygame.Vector2):
      super().__init__((0,0), size)
      self.object = pygame.Surface(size)
      self.object.fill(Colors.RED)
      self._health = 0
      self.max_health = 100
      self.size = size
      self.on_health_change()
      # Create a rectangle with color green
      # rect = pygame.Rect(0, 0, size.x, size.y)
      # rect.center = self.object.get_rect().center
      # rect.width = self.health * size.x / self.max_health

      # pygame.Surface.fill(self.object, Colors.GREEN, rect)
  @property
  def health(self):
    return self._health

  @health.setter
  def health(self, health: int):
    if health != self._health:
      self._health = health
      self.on_health_change()

  def on_health_change(self):
    pygame.draw.rect(self.object, Colors.YELLOW, (0, 0, self.size.x, self.size.y))
    rect = pygame.Rect(0, 0, self.size.x* self.health / self.max_health, self.size.y)
    pygame.draw.rect(self.object, Colors.GREEN, rect)



class Character(ControllableEntity, Hurtable, AffectedByGravity, Solid):
  def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      ControllableEntity.__init__(self, position, size, speed, jump_power)
      Hurtable.__init__(self, 100, 150)

  @property
  def health(self):
      return self._health
  @health.setter
  def health(self, health: int):
      Hurtable.health.fset(self, health)

  def update(self):
    AffectedByGravity.update(self)
    ControllableEntity.update(self)

class Enemy(Character):
  def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      Character.__init__(self, position, size, speed, jump_power)
      self.health_bar = Healthbar(pygame.Vector2(50, 10))
      self.linked.append(self.health_bar)
      self.on_position_change()
      self.on_health_change()
  def on_position_change(self):
      super().on_position_change()
      health_bar_rect = self.health_bar.rect
      health_bar_rect.center = self.rect.center
      health_bar_rect.top = self.rect.top - health_bar_rect.height - 10
      self.health_bar.position = health_bar_rect.topleft
  def on_health_change(self):
      super().on_health_change()
      self.health_bar.max_health = self.max_health
      self.health_bar.health = self.health

