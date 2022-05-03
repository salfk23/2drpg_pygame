

import random
import pygame
from assets.objects.characters import Demon, Enemy, Goblin, Minotaur, Player, Zombie
from game_engine.entities.entity import BackgroundEntity, Entity, EntityManager
from game_engine.entities.world_objects import Tile

from ui.player import GameWin, PlayerHUD
from assets.images import dirt_image, grass_images, tree_images, foliage_images
from assets.objects.weapons import *
from game_engine.helpers import gradient_rect, tile_texture


def run():
    print("Level 1")
    em = EntityManager.instance()
    # World Objects declaration
    GROUND_LEVEL = 500
    WORLD_LENGTH = 10000

    sky = BackgroundEntity( pygame.Vector2(-1000, -500),
                            (WORLD_LENGTH, GROUND_LEVEL+505))
    sky.sprite = pygame.transform.rotate(
        gradient_rect(
            pygame.color.Color("#cdf9ff"),
            pygame.color.Color("#75d5e3"),
            pygame.Rect(0, 0, GROUND_LEVEL+505, WORLD_LENGTH)
        ), 90)

    grass = Entity(pygame.Vector2(-1000, GROUND_LEVEL-11), (WORLD_LENGTH, 40))
    invisible_ground = Tile(
        pygame.Vector2(-1000, GROUND_LEVEL), (WORLD_LENGTH, 50))
    ground = Tile(pygame.Vector2(-1000, 525), (WORLD_LENGTH, 300))
    invisible_walls = [
        Tile(pygame.Vector2(0, 0), (20, 500)),
        Tile(pygame.Vector2(WORLD_LENGTH-2000, 0), (20, 500))
    ]

    background: list[Entity] = []

    tree_size = pygame.Vector2(60, 90)
    for x in range(-500, WORLD_LENGTH-1200, 100):
        # Increase tree tree_size by multiplying by random number
        size = tree_size * random.uniform(0.8, 3)
        # Randomize tree position
        tree = BackgroundEntity(
            pygame.Vector2(x + random.randint(-300, 300),
            GROUND_LEVEL-size.y+5),
            size
        )
        tree.sprite = pygame.transform.scale(random.choice(tree_images), size)
        background.append(tree)

        int_decoration = random.randint(0, 3)

        for i in range(int_decoration):
            foilage_image = random.choice(foliage_images)
            # Decrease foilage size by multiplying by random number
            size = pygame.Vector2(15, 15) * random.uniform(1, 2)
            decoration = Entity(
                pygame.Vector2(x + random.randint(-100, 100),
                GROUND_LEVEL-size.y+5),
                pygame.Vector2(0, 0)
            )
            decoration.sprite = pygame.transform.scale(foilage_image, size)
            background.append(decoration)



    # Player and other entities declaration
    player = Player(pygame.Vector2(220, 300), 5, 10)

    en = Enemy(pygame.Vector2(300, 300), (40, 60), 5, 10)
    en_2 = Zombie(pygame.Vector2(500, 300))
    en_3 = Goblin(pygame.Vector2(600, 300))
    en_4 = Minotaur(pygame.Vector2(700, 300))
    en_5 = Demon(pygame.Vector2(800, 300))

    enemies = [en, en_2, en_3, en_4, en_5]
    # Tweaks



    ground.sprite = tile_texture(dirt_image, ground.size)
    grass.sprite = tile_texture(grass_images, grass.size)

    player.weapon = silversword.copy()

    en.name = "Enemy"
    en.direction = False
    en.weapon = sample_weapon.copy()

    player_healthbar = PlayerHUD.instance()
    player_healthbar.watch_hurtable(player)
    player_healthbar.show = True

    # Add world objects first
    em.add(ground)
    em.add(invisible_ground)
    em.add(grass)
    em.add(invisible_walls)
    # Then other entities
    em.add(player)
    em.add(enemies)
    # Then background objects
    em.add(sky)
    em.add(background)
    # Focus on player
    em.focused_entity = player
