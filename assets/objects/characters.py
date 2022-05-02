
import pygame
from game_engine.entities.character import Enemy as EnemyConstruct , Player as PlayerConstruct
from game_engine.entities.particles import ExplosionParticle

from game_engine.helpers import Colors, Direction, Size2D

from assets.images.library import player_image
from assets.sounds.library import death_sound

class Player(PlayerConstruct):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(player_image, position, size, speed, jump_power)
        self.jump_limit = 3
        self.stomp_damage = 40
        self.actions = {
            pygame.KEYDOWN: {
                pygame.K_d: self.move_right,
                pygame.K_a: self.move_left,
                pygame.K_w: self.move_jump,
                pygame.K_s: self.action_hurt,
                pygame.K_SPACE: self.attack,
            },
            pygame.KEYUP:  {
                pygame.K_d: self.stop_right,
                pygame.K_a: self.stop_left,
            },
            pygame.MOUSEBUTTONDOWN:{
                pygame.BUTTON_LEFT: self.attack,
            }
        }

    def move_jump(self, event: pygame.event.Event):
        _, dirs = self.calculate_position(
            self.position, self.position+pygame.Vector2(0, 5))
        for entity in dirs[Direction.DOWN]:
            self.jump_number = 0
            if isinstance(entity, Enemy):
                entity.hurt(self.stomp_damage)
        super().move_jump(event)

    def attack(self, event: pygame.event.Event):
        if self.weapon is not None:
            self.weapon.attacking = True

    def action_hurt(self, event: pygame.event.Event):
        self.hurt(100)

    def update(self):
        super().update()
        new_position, dirs = self.calculate_position(
            self.position, self.new_position)

        if len(dirs[Direction.DOWN]) > 0:
            self.velocity.y = 0 if self.velocity.y > 0 else self.velocity.y
        if len(dirs[Direction.UP]) > 0:
            self.velocity.y = 0
        self.position = new_position
        if self.position.y > 5000:
            self.die()

    def hurt(self, damage: int):
        super().hurt(damage)
        death_sound.play()

    def die(self):
        center = self.rect.center
        particles = []
        for color in [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.BLACK]:
            particles.extend(ExplosionParticle.create_particles(
            pygame.Vector2(center), 35, color=color, size=(5, 15)))
        ExplosionParticle.register_particles(particles)
        death_sound.play()
        self.health = 0
        self.remove = True
        self.on_death()


class Enemy(EnemyConstruct):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(player_image, position, size, speed, jump_power)
        self.flip_interval = 235
        self.actions = {
            pygame.KEYDOWN: {
                pygame.K_j: self.move_right,
                pygame.K_l: self.move_left,
                pygame.K_i: self.move_jump,
            },
            pygame.KEYUP:  {
                pygame.K_j: self.stop_right,
                pygame.K_l: self.stop_left,
            }
        }

    def update(self):
        super().update()
        new_position, dirs = self.calculate_position(
            self.position, self.new_position)
        self.position = new_position

        if self.position.y > 5000:
            self.die()


