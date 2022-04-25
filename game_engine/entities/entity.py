import abc
import pygame
from game_engine.entities.event import EventListener

from game_engine.helpers import Colors, Config, IManager, Singleton, Size2D


NORMAL_SIZE_ENTITY = (32, 52)
class Entity:
  def __init__(self, position:pygame.Vector2, size: Size2D):
    self._position = position
    self.size = size
    # Remove from the entity manager
    self._remove = False
    self.name = "Entity"
    # Rectangle for collision detection
    self.coll_square:pygame.Rect = pygame.Rect(self.position, self.size)
    # Give color to Rect

    self.additional_objects = []

    # Make a rectangle with color green
    self.sprite = pygame.Surface(size)
    self._color = Colors.GREEN
    self.sprite.fill(self._color)
    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.sprite, self.size), 0)

  @property
  def color(self):
    return self._color

  @color.setter
  def color(self, color:tuple[int, int, int]):
    self._color = color
    self.sprite.fill(color)
    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.sprite, self.size), 0)

  @property
  def position(self):
    return self._position
  @position.setter
  def position(self, value:pygame.Vector2):
    self._position = value
    self.coll_square.topleft = value


  # Remove property
  @property
  def remove(self):
    return self._remove

  @remove.setter
  def remove(self, value):
    self._remove = value
    if value:
      EventListener.instance().remove(self)
      EntityManager.instance().remove(self)

  def update(self):
    pass

  def on_screen(self, screen_dimension:Size2D):
    '''
    Check if entity is within screen_dimension
    '''
    return (self._position.x+self.size[0] >= 0 and self._position.x <= screen_dimension[0] and self._position.y+self.size[1] >= 0 and self._position.y <= screen_dimension[1])
  def distance_to(self, other:'Entity'):
    pos = (self.position - other.position).length()
    print(pos)
    return pos

  def on_collision(self, other:'Entity', collision_type:tuple[bool, bool, bool, bool]):
    pass

  def collision(self, near_entity:'Entity'):
    '''
    Check if entity is colliding with other, and if so, where
    did it collide.
    '''
    if self.coll_square.colliderect(near_entity.coll_square):
      print(self.coll_square.center, near_entity.coll_square.center)
      # self.on_collision(near_entity, (
      #   self.coll_square.left < near_entity.coll_square.right,
      #   self.coll_square.right > near_entity.coll_square.left,
      #   self.coll_square.top < near_entity.coll_square.bottom,
      #   self.coll_square.bottom > near_entity.coll_square.top,
      # ))




class EntityManagerInstance(IManager[Entity]):
    def __init__(self):
        """Create a new EntityManager instance.
        Args:
            screen_size (tuple[int, int]): A tuple of the screen width and height.
        """
        self.entities: dict[int, Entity] = {}
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

    def get_near(self, entity: Entity, radius: int):
        return [
            item
            for item in self.entities.values()
            if item != entity
            # and item.distance_to(entity) <= radius
        ]

    def get_all(self):
        values: list[Entity] = self.entities.values()
        return values

    def add(self, item: Entity):
        self.entities[id(item)] = item


    def remove(self, item: Entity):
        return self.entities.pop(id(item))

@Singleton[EntityManagerInstance]
class EntityManager(EntityManagerInstance):
    pass
