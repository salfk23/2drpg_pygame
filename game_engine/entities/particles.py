"""Particle module, used to create particles entities."""


import math
import random
import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import ColoredEntity, EntityManager
from game_engine.helpers import Colors


class ExplosionParticle(MovableEntity, ColoredEntity):
  '''
  Particle object that last for frames, and have random direction
  '''
  def __init__(self, position: pygame.Vector2, color: tuple[int, int, int], size:tuple[int, int], angle:tuple[int, int], speed:tuple[float, float]):
      """Create particle

      Args:
          position (pygame.Vector2): Starting position
          color (tuple[int, int, int]): Color of particle
          size (tuple[int, int]): Size of particle (x, y)
          angle (tuple[int, int, int]): Range of angle (start, end) and delta
          speed (tuple[float, float]): Range of speed (min, max)
      """
      size = random.randint(size[0], size[1])
      super().__init__(position, (size, size))
      self.color = color
      start, end = angle
      if start < 0:
        start += 360
        end += 360
        angle_rand = random.randint(start, end)
        angle_rand = angle_rand % 360
      else:
        angle_rand = random.randint(start, end)
      angle_m = math.radians(angle_rand)
      # angle_m = random.uniform(1.9*math.pi, 2.1*math.pi)
      speed = random.uniform(speed[0], speed[1])

      self.velocity = pygame.Vector2(math.cos(angle_m), math.sin(angle_m)) * speed
      # Set velocity to random direction that is not mroe than 15 point speed
      # self.velocity = pygame.Vector2(math.cos(angle_m), math.sin(angle_m)) * speed
      self.lifetime = 0
  def on_color_change(self):
      sprite = pygame.Surface(self.size)
      sprite.fill(self.color)
      self.sprite = pygame.transform.scale(sprite, self.size)

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
  def create_particles(cls, position: pygame.Vector2, amount: int, size:tuple[int, int]=(2, 10), color: tuple[int, int, int]=Colors.RED, speed:tuple[float, float]=(0.1, 3), angle:tuple[int, int]=(0, 360)):
      particles: list[ExplosionParticle] = []
      for i in range(amount):
          particles.append(cls(position, color, size, angle, speed))
      return particles
  @staticmethod
  def register_particles(particles: list['ExplosionParticle']):
      # Shuffle particles
      random.shuffle(particles)
      em = EntityManager.instance()
      for particle in particles:
          em.add(particle)





