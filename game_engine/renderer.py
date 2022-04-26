import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import EntityManager
from game_engine.helpers import Colors, Config, IConfigListener, Singleton





class RendererInstance(IConfigListener):
    def __init__(self):
        self.config = Config.instance()
        self.window = pygame.display.set_mode(self.config.screen_dimension)
        self.entity_manager = EntityManager.instance()
        self.config.add_listener(self)
        self.camera = pygame.Vector2(0, 0)
    def on_screen_change(self):
        self.window = pygame.display.set_mode(self.config.screen_dimension)
    def config_change_events(self):
        return {
            IConfigListener.SCREEN_DIMENSION:self.on_screen_change
        }

    def draw(self):
        self.window.fill(Colors.WHITE)
        focus_position  = self.entity_manager.position
        heading = focus_position - self.camera
        if isinstance(self.entity_manager.focused_entity, MovableEntity):
            velocity:pygame.Vector2 = self.entity_manager.focused_entity.velocity
            heading +=  pygame.Vector2(velocity.x*75, velocity.y*25)
        self.camera += heading * 0.05
        offset = -self.camera + (pygame.Vector2(self.config.screen_dimension)//2)
        for entity in self.entity_manager.get_on_screen():
            self.window.blit(entity.object, entity.position+offset)
        pygame.display.update()


@Singleton[RendererInstance]
class Renderer(RendererInstance):
    pass
