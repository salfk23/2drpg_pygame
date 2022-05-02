

import pygame
from game_engine.entities.characters import EnemyCharacter, PlayerCharacter
from game_engine.entities.entity import EntityManager, UIEntity
from game_engine.entities.ui import PlayerHealthBar
from game_engine.entities.world_objects import Tile
from game_engine.helpers import Colors
from assets.images import dirt_image

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
    phb = PlayerHealthBar((25, 15), (300, 15))
    phb.watch_hurtable(player)
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
    # em.add(en)
    em.add(phb)
    em.focused_entity = player