import abc
import pygame

from game_engine.helpers import Colors, Config, IManager, Singleton, Size2D


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
    return (self.position.x >= 0 and self.position.x <= screen_dimension[0] and self.position.y >= 0 and self.position.y <= screen_dimension[1])
  def distance_to(self, other:'Entity'):
    return (self.position - other.position).length()
  def collision(self, near_entity):
    pass


class EntityManagerInstance(IManager[Entity]):
    def __init__(self):
        """Create a new EntityManager instance.
        Args:
            screen_size (tuple[int, int]): A tuple of the screen width and height.
        """
        self.entities: dict[int, Entity] = {}
        self.i_entities: dict[int, Entity] = {}
        self.config = Config.instance()

    def get_on_screen(self):
        """Return a list of entities that are on screen.
        Args:
            screen_size (tuple[int, int]): A tuple of the screen width and height.
        Returns:
            list[Entity]: A list of entities that are on screen.
        """
        return [
            entity
            for entity in self.entities.values()
            if entity.on_screen(self.config.screen_dimension)
        ]

    def get_input_entities(self):
        values: list[Entity] = self.i_entities.values()
        return values

    def get_near(self, entity: Entity, radius: int):
        return [
            item
            for item in self.entities.values()
            if item.distance_to(entity) < radius
        ]

    def get_all(self):
        values: list[Entity] = self.entities.values()
        return values

    def add(self, item: Entity):
        self.entities[id(item)] = item
        if item.input:
            self.i_entities[id(item)] = item


    def remove(self, item: Entity):
        if item in self.i_entities.values():
            del self.i_entities[id(item)]
        return self.entities.pop(id(item))

@Singleton[EntityManagerInstance]
class EntityManager(EntityManagerInstance):
    pass


class IMoveable(metaclass=abc.ABCMeta):
  @classmethod
  def __subclasshook__(cls, subclass):
    return (hasattr(subclass, 'move') and
            callable(subclass.move))
