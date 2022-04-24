import abc
import pygame

from engine.helpers import Colors, Size2D


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
  def __init__(self, position:pygame.Vector2, size: Size2D):
    self.position = position
    self.velocity = pygame.Vector2(0, 0)
    self.size = size
    # Make a rectangle with color green
    self.sprite = pygame.Surface(size)
    self.sprite.fill(Colors.GREEN)

    # Facing right
    self.front_facing = True

    # Remove from the entity manager
    self.remove = False
    # If the entity has input
    self.input = False

    self.name = "Entity"
    # Rectangle for collision detection
    self.hurtbox = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])

    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.sprite, self.size), 0)
    self.additional_objects = []
  def update(self):
    pass

  def on_screen(self, screen_dimension:Size2D):
    '''
    Check if entity is within screen_dimension
    '''
    return (self.position.x-self.size[0] >= 0 or self.position.x <= screen_dimension[0] and
            self.position.y-self.size[1] >= 0 or self.position.y <= screen_dimension[1])
  def distance_to(self, other:'Entity'):
    return 0
  def collision(self, near_entity):
    pass



class IMoveable(metaclass=abc.ABCMeta):
  @classmethod
  def __subclasshook__(cls, subclass):
    return (hasattr(subclass, 'move') and
            callable(subclass.move))
