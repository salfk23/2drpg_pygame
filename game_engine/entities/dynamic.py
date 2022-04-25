import pygame
from game_engine.entities.entity import Entity
from game_engine.entities.event import EventListener, KeyEventRegister
from game_engine.helpers import Size2D


class MovableEntity(Entity):
    def update(self):
        self.position += self.velocity

class AffectedByGravity(Entity):
    GRAVITY_MODIFIER = 0.5
    def update(self):
        self.velocity.y += self.GRAVITY_MODIFIER

class ControllableEntity(MovableEntity, KeyEventRegister):
    def __init__(self, position: pygame.Vector2, size:Size2D, speed:int, jump_power:int):
        super().__init__(position, size)
        KeyEventRegister.__init__(self)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = speed
        self.jump_power = jump_power
        self.event_listener = EventListener.instance()
        self.change_keybind(pygame.K_d, pygame.K_a, pygame.K_w)
    def change_keybind(self, move_right:int, move_left:int, jump:int):
        self.actions[pygame.KEYDOWN] = {
            move_right: self.move_right,
            move_left: self.move_left,
            jump: self.move_jump,
        }
        self.actions[pygame.KEYUP] = {
            move_right: self.stop_right,
            move_left: self.stop_left,
        }
        self.register_actions()
    def action_set(self):
        return self.actions

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

