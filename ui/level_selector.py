"""Level Select UI Module"""
import pygame

from game_engine.entities.entity import EntityManager, UIEntity
from game_engine.entities.ui import UIButton
from game_engine.helpers import Colors, Config, IConfigListener, Singleton

from levels.manager import get_levels, load_level


class LevelSelectorInstance(UIEntity, IConfigListener):
    """Level Select UI
    """

    def __init__(self):
        """Level select UI
        """
        self.config = Config.instance()
        screen_w, screen_h = self.config.screen_dimension
        width = 500
        height = 400
        super().__init__(
            pygame.Vector2((screen_w-width)/2, (screen_h-height)/2),
            (width, height)
        )
        self.color = Colors.UI
        self.config.add_listener(self)
        self.selected_level = None

        topright = pygame.Vector2(self.rect.topright)
        topleft = pygame.Vector2(self.rect.topleft)

        # Type text to the center top of surface as Title
        font = pygame.font.SysFont("monospace", 48)
        text = font.render("Level Select", True, Colors.BLACK)
        self.sprite.blit(text, ((width-text.get_width())/2, 10))

        button_bgcolor = Colors.BUTTON
        button_font_color = Colors.WHITE


        button_sprite, button_size = UIButton.center_button_sprite(
            "X", pygame.font.get_default_font(), 18,
            button_font_color, button_bgcolor,
            padding=10, button_size=(-1, -1)
        )
        button_exit = UIButton(
            "BUTTON_EXIT", button_sprite,
            topright+pygame.Vector2(-button_size.y,0),
            (button_size.y, button_size.y)
        )
        button_exit.on_pressed = self.button_exit_click
        self.linked.append(button_exit)

        # Columns and rows initalized to 0
        x, y = 0, 0

        # Print all levels in the game
        for level_id in get_levels():
            def on_level_click(level_id: str = level_id):
                self.selected_level = level_id
                self.load_last_level()
            button_sprite, button_size = UIButton.center_button_sprite(
                level_id, pygame.font.get_default_font(), 40,
                button_font_color, button_bgcolor,
                padding=10, button_size=(80, 80)
            )
            button = UIButton(
                "BUTTON_LEVEL_{}".format(level_id), button_sprite,
                topleft+pygame.Vector2(60+x*100, 100 +y*100),
                (button_size.x, button_size.y)
            )
            # Column and row wrap
            x += 1
            if x % 4 == 0:
                x = 0
                y += 1
            button.on_pressed = on_level_click
            self.linked.append(button)

    def load_last_level(self):
        """Load last level"""
        load_level(self.selected_level)

    def button_exit_click(self):
        EntityManager.instance().clear()
        EntityManager.instance().hide_all()
        from ui.main_menu import MainMenu  # Circular import hack
        MainMenu.instance().show = True

    def on_screen_change(self):
        width, height = self.config.screen_dimension
        self.center = (width/2, height/2)

    def config_change_events(self):
        return {
            IConfigListener.SCREEN_DIMENSION: self.on_screen_change
        }


@Singleton[LevelSelectorInstance]
class LevelSelector(LevelSelectorInstance):
    pass
