import pygame
from game_engine.entities.event import EventListener
from game_engine.entities.state import Solid
from game_engine.helpers import Colors, Config, IManager, Singleton, Size2D



NORMAL_SIZE_ENTITY = (32, 52)

class ColoredEntity:
  def __init__(self):
      self._color = Colors.BLUE

  def on_color_change(self):
    raise NotImplementedError()

  @property
  def color(self):
    return self._color

  @color.setter
  def color(self, color:tuple[int, int, int]):
    self._color = color
    self.on_color_change()



class Entity:
  def __init__(self, position:pygame.Vector2, size: Size2D):
    self._position = position
    self.size = size
    # Remove from the entity manager
    self._remove = False
    self.name = "Entity"
    # Make a rectangle with color green
    sprite = pygame.Surface(size)
    self.object = pygame.transform.rotate(
      pygame.transform.scale(sprite, self.size), 0)

    self.linked: list[Entity] = []

  def calculate_position(self, old_position:pygame.Vector2, new_position:pygame.Vector2):
    '''
    Calculate the new position of the entity
    '''
    nears = EntityManager.instance().get_near(self, 50)
    up, down, left, right = False, False, False, False
    for near in nears:
      t_up, t_down, t_left, t_right, bias_x, bias_y = self.collision(near)
      if (((t_up or t_down) and t_right and new_position.x > old_position.x) or
          ((t_up or t_down) and t_left and new_position.x < old_position.x)):
        if (t_up and (near.rect.bottom - new_position.y) > 2) or (t_down and (new_position.y - near.rect.top) > 2):
          new_position.x = old_position.x
          if t_right:
            right = True

          if t_left:
            left = True
      if (((t_left or t_right) and t_up and new_position.y < old_position.y) or
          ((t_left or t_right) and t_down and new_position.y > old_position.y)):
        new_position.y = old_position.y
        # if near.coll_square.top < new_position.y:
        if t_down:
          down = True
        if t_up:
          up = True
        if self.rect.bottom - near.rect.top > 2:
          new_position.y = near.rect.top - self.size[1] +1
    return new_position, (up, down, left, right)

  def on_position_change(self):
    pass
  @property
  def rect(self):
    return pygame.Rect(self.position, self.size)
  @property
  def position(self):
    return self._position
  @position.setter
  def position(self, value:pygame.Vector2):
    self._position = value
    self.on_position_change()


  # Remove property
  @property
  def remove(self):
    return self._remove

  @remove.setter
  def remove(self, value):
    self._remove = value
    if value:
      EventListener.instance().remove(self)
      em = EntityManager.instance()
      if em.focused_entity == self:
        em.focused_entity = None
      em.remove(self)
      for linked in self.linked:
        linked.remove = True

  def update(self):
    pass

  def on_screen(self, position:pygame.Vector2, screen_dimension:Size2D):
    '''
    Check if entity is within screen
    '''
    # return (position.x < self.coll_square.right and position.x < screen_dimension.width and
    #         position.y > 0 and position.y < screen_dimension.height)
    return True
  def distance_to(self, other:'Entity'):
    pos = (self.position - other.position).length()
    print(pos)
    return pos

  def collision(self, other:'Entity'):
    '''
    Check if entity is colliding with other, and if so, where
    did it collide.
    '''
    if not isinstance(other, Solid):
      return False, False, False, False, 0, 0
    is_within_left = self.rect.left > other.rect.left and self.rect.left < other.rect.right
    is_within_right = self.rect.right > other.rect.left and self.rect.right < other.rect.right
    is_within_top = self.rect.top > other.rect.top and self.rect.top < other.rect.bottom
    is_within_bottom = self.rect.bottom > other.rect.top and self.rect.bottom < other.rect.bottom
    bias_x = other.rect.centerx - self.rect.centerx
    bias_y = other.rect.centery - self.rect.centery

    return is_within_top, is_within_bottom, is_within_left, is_within_right, bias_x, bias_y










      # self.on_collision(other, direction)




class EntityManagerInstance(IManager[Entity]):
    def __init__(self):
        """Create a new EntityManager instance.
        Args:
            screen_size (tuple[int, int]): A tuple of the screen width and height.
        """
        self.entities: dict[int, Entity] = {}
        self.config = Config.instance()
        self.focused_entity:Entity = None

    @property
    def position(self):
        if self.focused_entity is not None:
            return pygame.Vector2(self.focused_entity.rect.center)
        return pygame.Vector2(self.config.screen_dimension)//2


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
            if entity.on_screen(self.position, self.config.screen_dimension)
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
        for linked in item.linked:
            self.add(linked)


    def remove(self, item: Entity):
        return self.entities.pop(id(item))

@Singleton[EntityManagerInstance]
class EntityManager(EntityManagerInstance):
    pass
