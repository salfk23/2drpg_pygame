import abc
import pygame


NORMAL_SIZE_ENTITY = (32, 52)
class Hurtable:
  def __init__(self, health: int, max_health: int):
    self.health = health
    self.max_health = max_health

class HurtBox:
  def __init__(self, x1: int, y1: int, x2: int, y2: int):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

  def conflict(self, other:'HurtBox'):
    # If the two hurtboxes are overlapping, return true
    return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

class Entity:
  def __init__(self, x:int, y:int, width:int, height:int, sprite:pygame.Surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.sprite = sprite
    self.remove = False
    self.name = "Entity"
    self.hurtbox = HurtBox(x, y, x+width, y+height)

    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.sprite, (self.width, self.height)), 0)


class IMoveable(metaclass=abc.ABCMeta):
  @classmethod
  def __subclasshook__(cls, subclass):
    return (hasattr(subclass, 'move') and
            callable(subclass.move))
