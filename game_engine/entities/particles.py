


import math
import random
import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import ColoredEntity, EntityManager
from game_engine.helpers import Size2D


class ExplosionParticle(MovableEntity, ColoredEntity):
  '''
  Particle object that last for 360 frame, and have random direction
  '''
  def __init__(self, position: pygame.Vector2, color: tuple[int, int, int], size:tuple[int, int], speed:tuple[float, float]):
      size = random.randint(size[0], size[1])
      super().__init__(position, (size, size))
      self.color = color
      angle = random.uniform(0, 2.0*math.pi)
      speed = random.uniform(speed[0], speed[1])
      # Set velocity to random direction that is not mroe than 15 point speed
      self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
      self.lifetime = 0
  def on_color_change(self):
      sprite = pygame.Surface(self.size)
      sprite.fill(self.color)
      self.object = pygame.transform.scale(sprite, self.size)

  def update(self):
      super().update()
      self.position = self.new_position
      self.lifetime += 1
      if self.lifetime % 5 == 0:
        size = (self.size[0] - 1, self.size[1] - 1)
        if size[0] <= 0 or size[1] <= 0:
          self.remove = True
        else:
          self.size = size
  @classmethod
  def create_particles(cls, position: pygame.Vector2, amount: int, color: tuple[int, int, int], size:tuple[int, int], speed:tuple[float, float]):
      entity_manager = EntityManager.instance()
      for i in range(amount):
          entity_manager.add(cls(position, color, size, speed))




