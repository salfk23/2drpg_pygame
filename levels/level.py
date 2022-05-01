

import pygame
from game_engine.entities.characters import EnemyCharacter, PlayerCharacter
from game_engine.entities.entity import EntityManager
from game_engine.entities.ui import PlayerHealthBar
from game_engine.entities.world_objects import Tile
from game_engine.helpers import Colors
from assets.images import dirt_image

def level_1():
    """Level 1"""

    em = EntityManager.instance()
    em.clear()
    ground = Tile(pygame.Vector2(20, 450), (600, 300))
    ground.name = "Ground"

    ground.sprite = pygame.transform.scale(dirt_image, ground.size)

    wall = Tile(pygame.Vector2(20, 400), (20, 70))

    mb = PlayerCharacter(pygame.Vector2(220, 300), (40, 40), 5, 10)
    # en = EnemyCharacter(pygame.Vector2(300, 300), (40, 60), 5, 10)
    mb.name = "Player"
    # en.name = "Enemy"
    # en.direction = False
    mb.color = Colors.BLUE
    phb = PlayerHealthBar((25, 15), (300, 15))
    phb.watch_hurtable(mb)
    wall.name = "Wall"
    em.add(ground)
    em.add(wall)
    em.add(mb)
    # em.add(en)
    em.add(phb)
    em.focused_entity = mb