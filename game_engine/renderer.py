"""Renderer module to render the game."""

import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import EntityManager
from game_engine.helpers import Colors, Config, IConfigListener, Singleton


class RendererInstance(IConfigListener):
    """
    Renderer object. Used to render the game.
    """

    def __init__(self):
        """Renderer object. Used to render the game."""
        self.config = Config.instance()
        self.window = pygame.display.set_mode(
            self.config.screen_dimension, pygame.HWSURFACE | pygame.DOUBLEBUF)  # | pygame.RESIZABLE)
        self.entity_manager = EntityManager.instance()
        self._camera = pygame.Vector2(0, 0)
        self.config.add_listener(self)

    def on_screen_change(self):
        self.window = pygame.display.set_mode(self.config.screen_dimension)

    def config_change_events(self):
        return {
            IConfigListener.SCREEN_DIMENSION: self.on_screen_change
        }

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value
        self.entity_manager.camera_position = value

    def draw(self):
        """Draw the current frame"""
        self.window.fill(Colors.WHITE)

        focus_position = self.entity_manager.position
        heading = focus_position - self.camera

        if isinstance(self.entity_manager.focused_entity, MovableEntity):
            velocity: pygame.Vector2 = self.entity_manager.focused_entity.velocity
            heading += pygame.Vector2(velocity.x*75, velocity.y*25)

        # Calculate the camera position
        self.camera += heading * 0.05

        # View offset
        offset = -self.camera + \
            (pygame.Vector2(self.config.screen_dimension)//2)

        # Print the background entities
        bg_on_screen = self.entity_manager.get_on_screen_bg()
        for entity in bg_on_screen:
            self.window.blit(entity.sprite, (entity.position + offset))

        on_screen = self.entity_manager.get_on_screen()
        on_screen.reverse()

        # Print the foreground entities
        for entity in on_screen:
            self.window.blit(entity.sprite, entity.position+offset)

        # Debug hitbox visualization
        colors = [
            Colors.RED,
            Colors.GREEN,
            Colors.BLUE,
            Colors.YELLOW,
            Colors.CYAN,
            Colors.BLACK
        ]
        # # Uncomment to visualize the hitboxes
        # for entity in on_screen:
        #     pygame.draw.circle(self.window, colors[(id(entity)//16)%len(colors)], pygame.Vector2(entity.rect.bottomleft)+offset, 3)
        #     pygame.draw.rect(self.window, colors[(id(entity)//16)%len(colors)], entity.sprite.get_rect(topleft=entity.position+offset), 1)  # The rect.

        # Print UI entities
        for ui in self.entity_manager.get_ui():
            self.window.blit(ui.sprite, ui.position)
        pygame.display.update()


@Singleton[RendererInstance]
class Renderer(RendererInstance):
    pass
