

import pygame
from assets.objects.characters import EnemyCharacter, PlayerCharacter
from game_engine.entities.entity import EntityManager
from game_engine.entities.world_objects import Tile
from game_engine.helpers import Colors

from ui.player import PlayerHUD
from assets.images.library import dirt_image
from assets.objects.weapon import sample_weapon

def level_1():
    """Level 1"""

    em = EntityManager.instance()
    ground = Tile(pygame.Vector2(20, 450), (600, 300))
    ground.name = "Ground"

    ground.sprite = pygame.transform.scale(dirt_image, ground.size)

    wall = Tile(pygame.Vector2(20, 400), (20, 70))

    player = PlayerCharacter(pygame.Vector2(220, 300), (40, 40), 5, 10)
    en = EnemyCharacter(pygame.Vector2(300, 300), (40, 60), 5, 10)
    player.name = "Player"
    en.name = "Enemy"
    en.direction = False
    en.weapon = sample_weapon
    wall.name = "Wall"
    em.add(ground)
    em.add(wall)
    em.add(player)
    em.add(en)

    player_healthbar = PlayerHUD.instance()
    player_healthbar.watch_hurtable(player)
    player_healthbar.show = True

    em.focused_entity = player