import pygame
from game_engine.entities.characters import Statusbar
from game_engine.entities.entity import UIEntity
from game_engine.entities.state import Hurtable
from game_engine.helpers import Colors, Singleton, Size2D

class PlayerHealthBarInstance(UIEntity):
  def __init__(self):
      size = (300, 15)
      super().__init__(pygame.Vector2(25, 15), size)
      self.name = "PLAYER_HEALTHBAR"
      self.watched = Hurtable(10, 100)
      self.healthbar = Statusbar((size[0]-5, size[1]-5))
      self.sprite.fill(Colors.BLACK)
      self.sprite.blit(self.healthbar.sprite, (2, 2))

  def watch_hurtable(self, hurtable: Hurtable):
    self.watched = hurtable
    self.watched.on_health_change = self.on_health_change
    self.on_health_change()

  def on_health_change(self):
    self.healthbar.current = self.watched.health
    self.healthbar.max = self.watched.max_health
    self.sprite.fill(Colors.BLACK)
    self.sprite.blit(self.healthbar.sprite, (2, 2))
    if self.watched.health <= 0:
      self.watched.on_death()


@Singleton[PlayerHealthBarInstance]
class PlayerHealthBar(PlayerHealthBarInstance):
  pass