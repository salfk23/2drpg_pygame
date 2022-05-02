import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.event import EmptyCallback
from game_engine.entities.ui import UIButton
from game_engine.helpers import Colors
from levels.level_1 import level_1
from ui import ui
from ui.main_menu import MainMenu
from levels.manager import load_level



def main():
    print("Running!")
    game = GameEngine.instance()
    ui.register_ui()
    game.event_listener.update(pygame.KEYDOWN, game, lambda e: {
        pygame.KEYDOWN: {
            pygame.K_r: lambda e: load_level("1"),
        }
    }.get(e.type, {}).get(e.key, EmptyCallback)(e))
    MainMenu.instance().show = True
    game.run()


if __name__ == '__main__':
    main()
