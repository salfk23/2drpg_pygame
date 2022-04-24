import pygame
from engine.entities.entity import Entity
from engine.helpers import Colors, Config, IConfigListener, IManager, ObjectIdCallable, Singleton, Size2D



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


class RendererInstance(IConfigListener):
    def __init__(self):
        self.config = Config.instance()
        self.window = pygame.display.set_mode(self.config.screen_dimension)
        self.entity_manager = EntityManager.instance()
        self.config.add_listener(self)
    def on_screen_change(self):
        self.window = pygame.display.set_mode(self.config.screen_dimension)
    def register_entity_manager(self, entity_manager: EntityManagerInstance):
        self.entity_manager = entity_manager

    def config_change_events(self):
        return {
            IConfigListener.SCREEN_DIMENSION:self.on_screen_change
        }

    def draw(self):
        self.window.fill(Colors.WHITE)
        entities: list[Entity] = self.entity_manager.get_on_screen()
        for entity in entities:
            self.window.blit(entity.object, (entity.position.x, entity.position.y))
            for extensive in entity.additional_objects:
                self.window.blit(extensive, (extensive.x, extensive.y))
        pygame.display.update()


@Singleton[RendererInstance]
class Renderer(RendererInstance):
    pass

class GameEngineInstance:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2D RPG Game")
        self.entity_manager = EntityManager.instance()
        self.renderer = Renderer.instance()
        self.running = False
        # Event listener, int and function dictionary
        self.event_listener: dict[int, dict[int, float]] = {
            pygame.QUIT : {
                id(self): self.stop
            }
        }

    def stop(self, event:pygame.event.Event):
        self.running = False

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                for _, callback in self.event_listener.get(event.type, {}).items():
                    callback(event)
            for entity in self.entity_manager.get_all():
                for near_entity in self.entity_manager.get_near(entity, 20):
                    entity.collision(near_entity)
                entity.update()
            self.renderer.draw()
            clock.tick(60)


@Singleton[GameEngineInstance]
class GameEngine(GameEngineInstance):
    pass