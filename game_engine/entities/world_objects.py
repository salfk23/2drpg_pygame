import pygame
from game_engine.entities.entity import Entity, ColoredEntity

from game_engine.entities.state import Solid
from game_engine.helpers import Size2D


class Tile(Entity, Solid):
    pass


class StepableBlock(Tile, ColoredEntity):
    def on_color_change(self):
        sprite = pygame.Surface(self.size)
        sprite.fill(self.color)
        self.sprite = pygame.transform.scale(sprite, self.size)
