import pygame
from engine.entities.entity import Entity
from engine.helpers import Colors, IEntityManager, Singleton

ScreenDimension = tuple[int, int]
"""Screen size tuple
Have 2 ints: width and height
"""


class EntityManager(IEntityManager, metaclass=Singleton):
  def __init__(self, screen_dimensions: ScreenDimension):
    """Create a new EntityManager.
    Args:
        screen_size (tuple[int, int]): A tuple of the screen width and height.
    """
    self.screen_dimensions = screen_dimensions
    self.entities: dict[int, Entity] = {}

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
      if entity.on_screen(self.screen_dimensions)
    ]

  def change_screen_size(self, screen_dimensions: ScreenDimension):
    self.screen_dimensions = screen_dimensions

  def get_all(self):
    values:list[Entity] = self.entities.values()
    return values

  def add(self, entity: Entity):
    self.entities[id(entity)] = entity

  def remove(self, entity: Entity):
    return self.entities.pop(id(entity))


class KeyInputManager(IEntityManager, metaclass=Singleton):
  def __init__(self):
    """Create a new KeyInputManager."""
    self.entities: dict[int, Entity] = {}

  def get_all(self):
    values:list[Entity] = self.entities.values()
    return values

  def add(self, entity: Entity):
    self.entities[id(entity)] = entity

  def remove(self, entity: Entity):
    return self.entities.pop(id(entity))

# class  Camera(metaclass=Singleton):
#   def __init__(self):


class Renderer(metaclass=Singleton):
  def __init__(self, screen_dimensions: ScreenDimension):
    self.screen_dimensions = screen_dimensions
    pygame.init()
    self.window = pygame.display.set_mode(screen_dimensions)
    pygame.display.set_caption("2D RPG Game")
    self.entity_manager = EntityManager(screen_dimensions)

  def change_screen_size(self, screen_dimensions: ScreenDimension):
    self.screen_dimensions = screen_dimensions
    self.window = pygame.display.set_mode(screen_dimensions)
    self.entity_manager.change_screen_size(screen_dimensions)

  def draw(self):
    self.window.fill(Colors.WHITE)
    for entity in self.entity_manager.get_on_screen():
      self.window.blit(entity.object, (entity.x, entity.y))
    pygame.display.update()





class GameUI:
    entities: list[Entity] = []
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D RPG Game")

        player = Player(100, 100)
        enemy = Enemy(100, 200)

        ground = Entity(0, HEIGHT-32, WIDTH, 32, pygame.Surface((WIDTH, 32)))
        ground.name = "Ground"



        GameUI.entities.append(player)
        player.health = 40
        GameUI.entities.append(enemy)
        GameUI.entities.append(ground)

    def draw(self):

        self.window.fill(Colors.WHITE)
        for entity in GameUI.entities:
            if (entity.x <= WIDTH and entity.y <= HEIGHT and
                entity.x >= 0-entity.width and entity.y >= 0-entity.height):
                # If entity is within the screen
                self.window.blit(entity.object, (entity.x, entity.y))
                debug_print("[IB]", entity.name, entity.x, entity.y, end='\t')
            else:
                # If entity is completely outside the screen
                debug_print("[OB]", entity.name, entity.x, entity.y, end='\t')
                if entity.remove:
                    self.entities.remove(entity)

            self.window.blit(entity.object, (entity.x, entity.y))
            # If entity extends Hurtable class
            if isinstance(entity, Hurtable):
                debug_print("[H]", entity.health, entity.max_health, end='\t')
                # Add red bar
                self.window.fill(Colors.RED, (entity.x, entity.y-10, entity.width, 5))
                # Add health bar
                self.window.fill(Colors.GREEN, (entity.x, entity.y-10, (entity.width*entity.health)//entity.max_health, 5))
        debug_print()
        pygame.display.update()

    def run(self):
        loop = True
        clock = pygame.time.Clock()

        while loop:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
            key_pressed = pygame.key.get_pressed()
            for entity in GameUI.entities:
                # Check if method move exists
                if hasattr(entity, 'move'):
                    entity.move(key_pressed, GameUI.entities)

            self.draw()






