from typing import Callable
import pygame
from game_engine.entities.entity import Entity
from game_engine.entities.event import EmptyCallback, EventListener
from game_engine.helpers import Size2D


class MovableEntity(Entity):
    def __init__(self, position: pygame.Vector2, size: Size2D):
        super().__init__(position, size)
        self.new_position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
    def update(self):
        self.new_position = self.position + self.velocity

class AffectedByGravity(MovableEntity):
    GRAVITY_MODIFIER = 0.5
    def update(self):
        self.velocity.y += self.GRAVITY_MODIFIER

class ControllableEntity(MovableEntity):
    def __init__(self, position: pygame.Vector2, size:Size2D, speed:int, jump_power:int):
        MovableEntity.__init__(self, position, size)
        self.speed = speed
        self.jump_power = jump_power
        self._actions: dict[id, dict[id, Callable]] = {}
    @property
    def actions(self):
        return self._actions
    @actions.setter
    def actions(self, actions: dict[id, dict[id, Callable]]):
        self._actions = actions
        eventListener = EventListener.instance()
        eventListener.remove(self)
        for event_type in self.actions:
            eventListener.update(event_type, self, lambda e: self.actions.get(e.type, {}).get(e.key, EmptyCallback)())


    def move_left(self):
        self.velocity.x = -self.speed
    def move_right(self):
        self.velocity.x = self.speed
    def stop_right(self):
        self.velocity.x = 0 if self.velocity.x > 0 else self.velocity.x
    def stop_left(self):
        self.velocity.x = 0 if self.velocity.x < 0 else self.velocity.x
    def move_jump(self):
        self.velocity.y = -self.jump_power

