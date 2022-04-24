import pygame
from game_engine.entities.entity import EntityManager
from game_engine.helpers import Colors, Config, IConfigListener, Singleton





class RendererInstance(IConfigListener):
    def __init__(self):
        self.config = Config.instance()
        self.window = pygame.display.set_mode(self.config.screen_dimension)
        self.entity_manager = EntityManager.instance()
        self.config.add_listener(self)
    def on_screen_change(self):
        self.window = pygame.display.set_mode(self.config.screen_dimension)
    def config_change_events(self):
        return {
            IConfigListener.SCREEN_DIMENSION:self.on_screen_change
        }

    def draw(self):
        self.window.fill(Colors.WHITE)
        for entity in self.entity_manager.get_on_screen():
            self.window.blit(entity.object, (entity.position.x, entity.position.y))
            for extensive in entity.additional_objects:
                self.window.blit(extensive, (extensive.x, extensive.y))
        pygame.display.update()


@Singleton[RendererInstance]
class Renderer(RendererInstance):
    pass
