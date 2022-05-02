from typing import Union
import math
import pygame
from game_engine.entities.event import EventListener
from game_engine.entities.state import Solid
from game_engine.helpers import Colors, Config, Direction, IManager, Singleton, Size2D



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


class Hitbox:
  @property
  def rect(self):
    return pygame.Rect((0,0), (0,0))
class Entity(Hitbox):
  def __init__(self, position:pygame.Vector2, size: Size2D):
    self._position = position
    # Remove from the entity manager
    self._remove = False
    self._name = "Entity"
    # Make a rectangle with color green
    sprite = pygame.Surface(size, pygame.SRCALPHA)
    self._sprite = pygame.transform.scale(sprite, size)

    self.linked: list[Entity] = []

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name:str):
    self._name = name
    self.on_name_change()

  def on_name_change(self):
    pass

  def __str__(self):
    return self.name + ": " + str(self.position) + " " + str(self.size)

  @property
  def sprite(self):
    return self._sprite

  @sprite.setter
  def sprite(self, sprite:pygame.Surface):
    self._sprite = sprite


  @property
  def size(self):
    return self.sprite.get_size()
  @size.setter
  def size(self, size:Size2D):
    self.sprite = pygame.transform.scale(self.sprite, size)
  def calculate_position(self, old_position:pygame.Vector2, new_position:pygame.Vector2):
    pass

  def on_position_change(self):
    pass
  @property
  def rect(self):
    return self.sprite.get_rect(topleft=self.position)
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

  def on_screen(self,position:pygame.Vector2, size:Size2D):
    '''
    Check if entity is within screen
    '''
    rect = pygame.Rect(position, size)
    rect.center = position
    return self.rect.colliderect(rect)
  def distance_to(self, other:'Entity'):
    return (self.position - other.position).length()

  def collision(self, other:'Entity'):
    '''
    Check if entity is colliding with other, and if so, where
    did it collide.
    '''
    if not isinstance(other, Solid):
      return False, None

    collided = False

    collided = self.rect.colliderect(other.rect)
    direction = Direction.DOWN
    if collided:
      x1, y1 = self.rect.center
      x2, y2 = other.rect.center
      x_diff = x1 - x2
      y_diff = y1 - y2


      angle = math.degrees(math.atan2(y_diff, x_diff))
      if angle < 0:  angle += 360

      collided_angle_x = other.rect.height / (other.rect.height + other.rect.width) * 90
      collided_angle_y = other.rect.width / (other.rect.height + other.rect.width) * 90

      if angle < 270 + collided_angle_y and angle >= 270 - collided_angle_y:
        direction = Direction.DOWN
      elif angle < 180 + collided_angle_x and angle >= 180 - collided_angle_x:
        direction = Direction.LEFT
      elif angle < 90 + collided_angle_y and angle >= 90 - collided_angle_y:
        direction = Direction.UP
      elif angle < 0 + collided_angle_x or angle >= 360 - collided_angle_x:
        direction = Direction.RIGHT
    return collided, direction



class BiDirectionalEntity:
  def __init__(self, sprite:pygame.Surface):
    self.sprites = {
      True: sprite,
      False: pygame.transform.flip(sprite, True, False)
    }
    self._direction = True

  def on_direction_change(self):
    raise NotImplementedError()

  @property
  def direction(self):
    return self._direction

  @direction.setter
  def direction(self, value):
    if self._direction != value:
      self._direction = value
      self.on_direction_change()


class UIEntity(Entity, ColoredEntity):
  def __init__(self, position:pygame.Vector2, size:Size2D):
    super().__init__(position, size)
    self.color = Colors.BLUE
    self.name = "UI"
    self._show = True
    self.sprite.fill(self.color)
  def on_color_change(self):
    self.sprite.fill(self.color)
  def update(self):
    pass

  @property
  def show(self):
    return self._show

  @show.setter
  def show(self, value):
    if self._show != value:
      self._show = value
      self.on_show_change()

  def on_show_change(self):
    for linked in self.linked:
      linked.show = self.show
class BackgroundEntity(Entity):
  def __init__(self, position:pygame.Vector2, size:Size2D):
    super().__init__(position, size)
    self.name = "Background"
class EntityManagerInstance(IManager[Entity]):
    def __init__(self):
        """Create a new EntityManager instance.
        Args:
            screen_size (tuple[int, int]): A tuple of the screen width and height.
        """
        self._entities: dict[int, Entity] = {}
        self._ui_components: dict[int, UIEntity] = {}
        self._background: dict[int, BackgroundEntity] = {}
        self._remove_list: list[Entity] = []
        self._add_list: list[Entity] = []
        self.config = Config.instance()
        self.focused_entity:Entity = None
        self.camera_position = pygame.Vector2(0, 0)
    @property
    def entities(self):
        return self._entities

    @property
    def ui_components(self):
        return self._ui_components
    @property
    def background(self):
        return self._background

    @property
    def position(self):
        if self.focused_entity is not None:
            return pygame.Vector2(self.focused_entity.rect.center)
        return pygame.Vector2(self.config.screen_dimension)//2


    def commit(self):
        for entity in self._remove_list:
            self._entities.pop(id(entity), None)
            self._ui_components.pop(id(entity), None)
            self._background.pop(id(entity), None)
        self._remove_list.clear()
        for entity in self._add_list:
            if isinstance(entity, UIEntity):
                self._ui_components[id(entity)] = entity
            elif isinstance(entity, BackgroundEntity):
                self._background[id(entity)] = entity
            else:
              self._entities[id(entity)] = entity
        self._add_list.clear()

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
            if entity.on_screen(self.camera_position, self.config.screen_dimension)
        ]

    def get_on_screen_bg(self):
      return [
        entity
        for entity in self.background.values()
        if entity.on_screen(self.camera_position, self.config.screen_dimension)
      ]

    def get_ui(self, show:bool=True, all_item:bool=False):
        return [
            entity
            for entity in self.ui_components.values()
            if all_item or entity.show == show
        ]
    def get_background(self):
        return [
            entity
            for entity in self.background.values()
        ]

    def get_near(self, entity: Entity, radius: int):
        return [
            item
            for item in self.entities.values()
            if item != entity
            # and item.distance_to(entity) <= radius
        ]

    def get_all(self):
        lists = []
        entities: list[Entity] = self.entities.values()
        uis : list[UIEntity] = self.ui_components.values()
        lists.extend(entities)
        lists.extend(uis)
        return lists

    def get_of_type(self, entity_type: type):
        from_ui = [
            entity
            for entity in self.ui_components.values()
            if isinstance(entity, entity_type)
        ]
        from_entities = [
            entity
            for entity in self.entities.values()
            if isinstance(entity, entity_type)
        ]
        return from_ui + from_entities

    def hide_all(self):
        for entity in self.ui_components.values():
            entity.show = False
    # Add list or Entity
    def add(self, item: Union[Entity, list[Entity]]):
      if isinstance(item, list):
        for entity in item:
          self.add(entity)
      else:
        self._add_list.append(item)
        for linked in item.linked:
            self.add(linked)


    def remove(self, item: Entity):
        # return self.entities.pop(id(item))
        self._remove_list.append(item)

    def clear(self):
        for entity in self.entities.values():
            entity.remove = True
        for entity in self.background.values():
            entity.remove = True

@Singleton[EntityManagerInstance]
class EntityManager(EntityManagerInstance):
    pass
