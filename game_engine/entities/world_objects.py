import pygame
from game_engine.entities.entity import Entity, ColoredEntity

from game_engine.entities.state import Solid


class Tile(Entity, Solid):
    """Tile, can be jumped on"""
    pass


class StepableBlock(Tile, ColoredEntity):
    """Stepable block, can be jumped on and has effects on the player"""
    def on_color_change(self):
        sprite = pygame.Surface(self.size)
        sprite.fill(self.color)
        self.sprite = pygame.transform.scale(sprite, self.size)
