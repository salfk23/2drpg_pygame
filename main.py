import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.characters import EnemyCharacter, PlayerCharacter
from game_engine.entities.event import EmptyCallback
from game_engine.entities.ui import PlayerHealthBar
from game_engine.entities.world_objects import Tile
from game_engine.helpers import Colors
from levels.level import level_1




def main():
    print("Running!")
    game = GameEngine.instance()
    actions = {
        pygame.KEYDOWN : {
            pygame.K_r : level_1
        },
    }
    for event_type in actions:
        game.event_listener.update(event_type, game, lambda e: actions.get(e.type, {}).get(e.key, EmptyCallback)())


    game.run()


if __name__ == '__main__':
    main()
