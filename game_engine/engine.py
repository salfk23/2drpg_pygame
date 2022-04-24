import pygame
from game_engine.entities.event import EventListener
from game_engine.entities.entity import EntityManager
from game_engine.helpers import Singleton
from game_engine.renderer import Renderer





class GameEngineInstance:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2D RPG Game")
        self.entity_manager = EntityManager.instance()
        self.renderer = Renderer.instance()
        self.running = False
        # Event listener, int and function dictionary
        self.event_listener = EventListener.instance()
        self.event_listener.update(pygame.QUIT, id(self), self.stop)

    def stop(self, event:pygame.event.Event):
        self.running = False

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                for _, callback in self.event_listener.get(event.type).items():
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