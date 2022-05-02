

import pygame
from assets.objects.characters import Enemy, Player
from game_engine.entities.entity import EntityManager
from game_engine.entities.world_objects import Tile

from ui.player import PlayerHUD
from assets.images import dirt_image
from assets.objects.weapons import sample_weapon

def run():
    print("Level 2")
    em = EntityManager.instance()

    # World Objects declaration
    ground = Tile(pygame.Vector2(20, 450), (600, 300))
    wall = Tile(pygame.Vector2(20, 400), (20, 70))

    # Player and other entities declaration
    player = Player(pygame.Vector2(220, 300), (40, 40), 5, 10)
    en = Enemy(pygame.Vector2(300, 300), (40, 60), 5, 10)

    # Tweaks
    ground.name = "Ground"
    ground.sprite = pygame.transform.scale(dirt_image, ground.size)

    wall.name = "Wall"

    player.name = "Player"
    player.weapon = sample_weapon.copy()

    en.name = "Enemy"
    en.direction = False
    en.weapon = sample_weapon.copy()


    player_healthbar = PlayerHUD.instance()
    player_healthbar.watch_hurtable(player)
    player_healthbar.show = True


    # Add world objects first
    em.add(ground)
    em.add(wall)
    # Then other entities
    em.add(player)
    em.add(en)

    # Focus on player
    em.focused_entity = player