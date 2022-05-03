from game_engine.engine import GameEngine

from ui import ui
from ui.main_menu import MainMenu



def main():
    print("Running!")
    game = GameEngine.instance()
    ui.register_ui()
    # game.event_listener.update(pygame.KEYDOWN, game, lambda e: {
    #     pygame.KEYDOWN: {
    #         pygame.K_r: lambda e: load_level("1"),
    #     }
    # }.get(e.type, {}).get(e.key, EmptyCallback)(e))
    MainMenu.instance().show = True
    game.run()


if __name__ == '__main__':
    main()
