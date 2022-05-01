from typing import Callable
import pygame
from game_engine.entities.entity import Entity, EntityManager
from game_engine.entities.event import EmptyCallback, EventListener
from game_engine.helpers import Direction, Size2D


class MovableEntity(Entity):
    def __init__(self, position: pygame.Vector2, size: Size2D):
        super().__init__(position, size)
        self.new_position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
    def update(self):
        self.new_position = self.position + self.velocity

    def calculate_position(self, old_position: pygame.Vector2, new_position: pygame.Vector2):
        '''
        Calculate the new position of the entity
        '''
        nears = EntityManager.instance().get_near(self, 50)
        collided: dict[int, list[Entity]] = {
            Direction.UP: [],
            Direction.DOWN: [],
            Direction.LEFT: [],
            Direction.RIGHT: []
        }
        for near in nears:
            has_collided, direction = self.collision(near)

            if has_collided:
                collided[direction].append(near)
                if direction == Direction.UP:
                    new_position.y = old_position.y
                    for entity in collided[direction]:
                        if not isinstance(entity, MovableEntity):
                            new_position.y = entity.rect.bottom if entity.rect.bottom >= new_position.y else new_position.y
                if direction == Direction.DOWN:
                    # new_position.y = old_position.y
                    for entity in collided[direction]:
                        new_position.y = entity.rect.top-self.rect.height+1 if entity.rect.top <= (new_position.y+self.rect.height) else new_position.y
                if direction == Direction.RIGHT:
                    new_position.x = old_position.x
                    for entity in collided[direction]:
                        new_position.x = entity.rect.right if entity.rect.right >= new_position.x else new_position.x
                if direction == Direction.LEFT:
                    new_position.x = old_position.x
                    for entity in collided[direction]:
                        new_position.x = entity.rect.left.x+self.rect.width if entity.rect.left >= (new_position.x+self.rect.width) else new_position.x
        return new_position, collided

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

