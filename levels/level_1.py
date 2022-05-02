

import random
import pygame
from assets.objects.characters import Enemy, Player
from game_engine.entities.entity import BackgroundEntity, Entity, EntityManager
from game_engine.entities.world_objects import Tile

from ui.player import PlayerHUD
from assets.images.library import dirt_image,grass_image, tree_1_image, tree_2_image, tree_3_image, tree_4_image
from assets.objects.weapons import sample_weapon
from game_engine.helpers import gradient_rect, tile_texture




def run():
    print("Level 1")
    em = EntityManager.instance()
    ground_level = 500
    # World Objects declaration
    WORLD_LENGTH = 10000
    sky = BackgroundEntity(pygame.Vector2(-1000, -500), (WORLD_LENGTH, ground_level+500))
    sky.sprite = pygame.transform.rotate(
        gradient_rect(
            pygame.color.Color("#cdf9ff"),
            pygame.color.Color("#75d5e3"),
            pygame.Rect(0, 0, ground_level+500, WORLD_LENGTH)
        )
    , 90)
    grass = Tile(pygame.Vector2(-1000, ground_level), (WORLD_LENGTH, 40))
    ground = Tile(pygame.Vector2(-1000, 525), (WORLD_LENGTH, 300))
    invisible_wall = Tile(pygame.Vector2(0, 0), (20, 500))
    trees: list[Entity] = []
    for x in range(-500, 8500, 100):
        # Randomize tree position
        x += random.randint(-300, 300)
        size = pygame.Vector2(60, 90)
        # Increase tree size by multiplying by random number bewtween 1 and 1.5
        size *= random.uniform(1, 3)
        tree = BackgroundEntity(pygame.Vector2(x, ground_level-size.y+5), size)
        tree_image = random.choice([tree_1_image, tree_2_image, tree_3_image, tree_4_image])
        tree.sprite = pygame.transform.scale(tree_image, tree.size)
        trees.append(tree)

    # Player and other entities declaration
    player = Player(pygame.Vector2(220, 300), (40, 40), 5, 10)
    en = Enemy(pygame.Vector2(300, 300), (40, 60), 5, 10)

    # Tweaks
    ground.name = "Ground"
    ground.sprite = tile_texture(dirt_image, ground.size)
    grass.name = "Grass"
    grass.sprite = tile_texture(grass_image, grass.size)

    invisible_wall.name = "Invisible Wall"

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
    em.add(grass)
    em.add(invisible_wall)
    # Then other entities
    em.add(player)
    em.add(en)
    # Then background objects
    em.add(sky)
    em.add(trees)
    # Focus on player
    em.focused_entity = player