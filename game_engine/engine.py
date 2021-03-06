"""Game Engine module."""
import pygame
from game_engine.entities.event import EventListener
from game_engine.entities.entity import EntityManager
from game_engine.helpers import Singleton
from game_engine.renderer import Renderer


GAME_FPS = 60


class GameEngineInstance:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2D RPG Game")
        self.entity_manager = EntityManager.instance()
        self.renderer = Renderer.instance()
        self.running = False
        # Event listener, int and function dictionary
        self.event_listener = EventListener.instance()
        self.event_listener.update(
            pygame.QUIT, id(self), lambda e: self.stop(e))

    def stop(self, event: pygame.event.Event):
        """Stop the game engine

        Args:
            event (pygame.event.Event): Event that triggered the stop
        """
        print('Stopping Game engine')
        self.running = False

    def run(self):
        """Run the game engine"""
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.event_listener.commit()
            for event in pygame.event.get():
                for _, callback in self.event_listener.get(event.type).items():
                    callback(event)
            for entity in self.entity_manager.get_all():
                entity.update()
            self.renderer.draw()
            self.entity_manager.commit()
            clock.tick(GAME_FPS)


@Singleton[GameEngineInstance]
class GameEngine(GameEngineInstance):
    pass
