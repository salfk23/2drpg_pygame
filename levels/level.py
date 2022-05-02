

import pygame
from game_engine.entities.characters import EnemyCharacter, PlayerCharacter
from game_engine.entities.entity import EntityManager
from game_engine.entities.world_objects import Tile
from game_engine.helpers import Colors
from assets.images import dirt_image
from ui.player import PlayerHealthBar

def level_1():
    """Level 1"""

    em = EntityManager.instance()
    em.clear()
    em.hide_all()
    ground = Tile(pygame.Vector2(20, 450), (600, 300))
    ground.name = "Ground"

    ground.sprite = pygame.transform.scale(dirt_image, ground.size)

    wall = Tile(pygame.Vector2(20, 400), (20, 70))

    player = PlayerCharacter(pygame.Vector2(220, 300), (40, 40), 5, 10)
    # en = EnemyCharacter(pygame.Vector2(300, 300), (40, 60), 5, 10)
    player.name = "Player"
    # en.name = "Enemy"
    # en.direction = False
    player.color = Colors.BLUE
    player_healthbar = PlayerHealthBar.instance()
    player_healthbar.watch_hurtable(player)
    player_healthbar.show = True
    def on_death():
        print("You died!")
        em.clear()
        em.hide_all()
        for ui in em.get_ui(all_item=True):
            if ui.name == "BTN_START":
                ui.show = True

    player.on_death = on_death
    wall.name = "Wall"
    em.add(ground)
    em.add(wall)
    em.add(player)
    em.focused_entity = player