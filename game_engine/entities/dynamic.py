"""Dynamic module, used to declare dynamic or non-static entities."""
from typing import Callable
import pygame
from game_engine.entities.entity import Entity, EntityManager, Hitbox
from game_engine.entities.event import EmptyCallback, EventListener
from game_engine.helpers import Direction, Size2D


class MovableEntity(Entity):
    """Entity that can move"""
    def __init__(self, position: pygame.Vector2, size: Size2D):
        super().__init__(position, size)
        self.new_position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)

    def update(self):
        self.new_position = self.position + self.velocity

    def calculate_position(self, old_position: pygame.Vector2, new_position: pygame.Vector2):
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
                            new_position.y = (entity.rect.bottom if entity.rect.bottom >= new_position.y else new_position.y)
                if direction == Direction.DOWN:
                    # new_position.y = old_position.y
                    for entity in collided[direction]:
                        new_position.y = entity.rect.top-self.rect.height + 1 if entity.rect.top <= (new_position.y+self.rect.height) else new_position.y
                if direction == Direction.RIGHT:
                    new_position.x = old_position.x
                    for entity in collided[direction]:
                        new_position.x = entity.rect.right if entity.rect.right >= new_position.x else new_position.x
                if direction == Direction.LEFT:
                    new_position.x = old_position.x
                    for entity in collided[direction]:
                        new_position.x = entity.rect.left.x + self.rect.width if entity.rect.left >= (new_position.x+self.rect.width) else new_position.x
        return new_position, collided


class AffectedByGravity(MovableEntity):
    """Entity that can move and affected by gravity"""
    GRAVITY_MODIFIER = 0.5

    def update(self):
        self.velocity.y += self.GRAVITY_MODIFIER


class Controllable:
    """Entity that can be controlled by input"""
    def __init__(self):
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
            if event_type == pygame.KEYDOWN or event_type == pygame.KEYUP:
                eventListener.update(event_type, self, lambda e: self.actions.get(
                    e.type, {}).get(e.key, EmptyCallback)(e))
            elif event_type == pygame.MOUSEBUTTONUP or event_type == pygame.MOUSEBUTTONDOWN:
                eventListener.update(event_type, self, lambda e: self.actions.get(
                    e.type, {}).get(e.button, EmptyCallback)(e))
            else:
                print("Unknown event type:", event_type, "for", self)


class MouseControllable(Controllable, Hitbox):
    """Entity that can be controlled by mouse"""
    def __init__(self):
        super().__init__()
        self.button_down = False
        self.actions = {
            pygame.MOUSEBUTTONUP: {
                pygame.BUTTON_LEFT: self.on_up_event
            },
            pygame.MOUSEBUTTONDOWN: {
                pygame.BUTTON_LEFT: self.on_down_event
            }
        }

    def on_up_event(self, event: pygame.event.Event):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.show:
            self.on_mouse_up()
            if self.button_down:
                self.on_pressed()
        self.button_down = False

    def on_down_event(self, event: pygame.event.Event):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.show:
            self.button_down = True
            self.on_mouse_down()

    def on_mouse_down(self):
        pass

    def on_mouse_up(self):
        pass

    def on_pressed(self):
        pass


class JumpableEntity(MovableEntity, Controllable):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        MovableEntity.__init__(self, position, size)
        Controllable.__init__(self)
        self.speed = speed
        self.jump_power = jump_power
        self.jump_number = 0
        self.jump_limit = 2
        self._actions: dict[id, dict[id, Callable]] = {}

    def move_left(self, event: pygame.event.Event):
        self.velocity.x = -self.speed

    def move_right(self, event: pygame.event.Event):
        self.velocity.x = self.speed

    def stop_right(self, event: pygame.event.Event):
        self.velocity.x = 0 if self.velocity.x > 0 else self.velocity.x

    def stop_left(self, event: pygame.event.Event):
        self.velocity.x = 0 if self.velocity.x < 0 else self.velocity.x

    def move_jump(self, event: pygame.event.Event):
        self.jump_number += 1
        if self.jump_number < self.jump_limit:
            self.velocity.y = -self.jump_power
