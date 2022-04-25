import pygame
from game_engine.entities.entity import Entity
from game_engine.helpers import Size2D


class Tile(Entity):
  def __init__(self, position: pygame.Vector2, size: Size2D):
      super().__init__(position, size)

  def collision(self, near_entity):
      return super().collision(near_entity)