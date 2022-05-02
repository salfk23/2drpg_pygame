import pygame
from game_engine.engine import GameEngine
from game_engine.entities.entity import UIEntity
from game_engine.entities.ui import UIButton
from game_engine.helpers import Colors, Config, IConfigListener, Singleton, Size2D


class MainMenuInstance(UIEntity, IConfigListener):
    def __init__(self):
        self.config = Config.instance()
        screen_w, screen_h = self.config.screen_dimension
        width = 500
        height = 400
        super().__init__(
          pygame.Vector2((screen_w-width)/2,(screen_h-height)/2),
          (width, height)
        )
        self.color = Colors.YELLOW
        self.config.add_listener(self)

        midtop = pygame.Vector2(self.rect.midtop)
        # Type text to the center top of surface as Title
        font = pygame.font.SysFont("monospace", 48)
        text = font.render("2D RPG Game", True, Colors.BLACK)
        self.sprite.blit(text, ((width-text.get_width())/2, 10))

        button_bgcolor = Colors.PURPLE
        button_font_color = Colors.WHITE
        button_sprite, button_size = UIButton.center_button_sprite(
            "Play Game", "monospace", 30, button_font_color, button_bgcolor,
            padding=5, button_size=(300, -1)
        )
        button_instruction = UIButton(
            "BUTTON_1", button_sprite,
            midtop+pygame.Vector2(-button_size.x/2, 150), button_size
        )
        button_instruction.on_pressed = self.button_play_click
        self.linked.append(button_instruction)

        button_sprite, button_size = UIButton.center_button_sprite(
            "How to Play", "monospace", 30, button_font_color, button_bgcolor,
            padding=5, button_size=(300, -1)
            )
        button_instruction = UIButton(
            "BUTTON_1", button_sprite,
            midtop+pygame.Vector2(-button_size.x/2, 225), button_size)
        button_instruction.on_pressed = self.button_instruction_click
        self.linked.append(button_instruction)

        button_sprite, button_size = UIButton.center_button_sprite(
            "Exit Game", "monospace", 30, button_font_color, button_bgcolor,
            padding=5, button_size=(300, -1))
        button_exit = UIButton(
          "BUTTON_EXIT_GAME", button_sprite,
          midtop+pygame.Vector2(-button_size.x/2, 300), button_size)
        button_exit.on_pressed = self.button_quit_click
        self.linked.append(button_exit)

    def button_play_click(self):
        print("Button 1 clicked")

    def button_instruction_click(self):
        self.show = False
        print("Button instruction clicked")

    def button_quit_click(self):
        print("Exiting game")
        self.show = False
        GameEngine.instance().running = False

    def on_screen_change(self):
        width, height = self.config.screen_dimension
        self.center = (width/2, height/2)

    def config_change_events(self):
        return {
            IConfigListener.SCREEN_DIMENSION: self.on_screen_change
        }


@Singleton[MainMenuInstance]
class MainMenu(MainMenuInstance):
    pass
