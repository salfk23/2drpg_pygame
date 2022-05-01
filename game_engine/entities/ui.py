
import pygame
from game_engine.entities.characters import Statusbar
from game_engine.entities.entity import UIEntity
from game_engine.entities.state import Hurtable
from game_engine.helpers import Colors, Size2D


class PlayerHealthBar(UIEntity):
  def __init__(self, position: pygame.Vector2, size: Size2D):
      super().__init__(position, size)
      self.watched = Hurtable(10, 100)
      self.healthbar = Statusbar((size[0]-5, size[1]-5))
      self.sprite.fill(Colors.BLACK)
      self.sprite.blit(self.healthbar.sprite, (2, 2))

  def watch_hurtable(self, hurtable: Hurtable):
    self.watched = hurtable


  def update(self):
    self.healthbar.current = self.watched.health
    self.healthbar.max = self.watched.max_health
    self.sprite.fill(Colors.BLACK)
    self.sprite.blit(self.healthbar.sprite, (2, 2))

