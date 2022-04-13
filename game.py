from typing import Sequence
import pygame

from movable import IMoveable


class Entity:
  def __init__(self, x:int, y:int, width:int, height:int, image:pygame.Surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.image = image

    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.image, (self.width, self.height)), 0)

class Player(Entity, IMoveable):
  def __init__(self, x:int, y:int):
    super().__init__(x, y, 32, 32, pygame.image.load("assets/test_player.png"))

  def move(self, key_pressed:Sequence[bool]):
    if key_pressed[pygame.K_w]:
      self.y -= 1
    if key_pressed[pygame.K_s]:
      self.y += 1
    if key_pressed[pygame.K_a]:
      self.x -= 1
    if key_pressed[pygame.K_d]:
      self.x += 1

