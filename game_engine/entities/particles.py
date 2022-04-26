


import math
import random
import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import EntityManager
from game_engine.helpers import Size2D


class DeathParticle(MovableEntity):
  '''
  Particle object that last for 360 frame, and have random direction
  '''
  def __init__(self, position: pygame.Vector2):
      super().__init__(position, (2, 2))
      angle = random.uniform(0, 2.0*math.pi)
      speed = random.uniform(7, 15)
      # Set velocity to random direction that is not mroe than 15 point speed
      self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
      self.lifetime = 360
      self.remove = False
      self._lifetime = 60
  def update(self):
      super().update()
      self.position = self.new_position
      self.lifetime -= 1
  @property
  def lifetime(self):
      return self._lifetime

  @lifetime.setter
  def lifetime(self, lifetime: int):
      self._lifetime = lifetime
      if self._lifetime <= 0:
          self.remove = True

  @classmethod
  def create_particles(cls, position: pygame.Vector2, amount: int):
      entity_manager = EntityManager.instance()
      for i in range(amount):
          entity_manager.add(cls(position))




