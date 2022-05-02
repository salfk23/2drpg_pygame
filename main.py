import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.characters import EnemyCharacter, PlayerCharacter
from game_engine.entities.event import EmptyCallback
from game_engine.entities.ui import MainMenu, PlayerHealthBar, UIButton
from game_engine.entities.world_objects import Tile
from game_engine.helpers import Colors
from levels.level import level_1



def main():
    print("Running!")
    game = GameEngine.instance()
    em = EntityManager.instance()

    surface = pygame.Surface((100, 100))
    surface.fill(Colors.GREEN)
    # Add text to the center of surface
    font = pygame.font.SysFont("monospace",20)
    text = font.render("Hello World!", True, Colors.BLACK)
    text_rect = text.get_rect()
    text_rect.center = surface.get_rect().center
    surface.blit(text, text_rect)

    button = UIButton("BTN_START", surface, pygame.Vector2(0, 0), (100, 100))
    # Modify button.on_click() to run level_1 and set visible to False
    def on_click():
        level_1()
        button.show = False
    button.on_pressed = on_click
    def on_click():
        print("Clicked!")
    em.add(button)

    mainMenu = MainMenu()
    em.add(mainMenu)

    game.event_listener.update(pygame.KEYDOWN, game, lambda e: {
        pygame.KEYDOWN: {
            pygame.K_r: lambda e: level_1()
        }
    }.get(e.type, {}).get(e.key, EmptyCallback)(e))

    game.run()


if __name__ == '__main__':
    main()
