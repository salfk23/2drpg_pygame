
from threading import Timer
import pygame
from game_engine.entities.character import Enemy as EnemyConstruct , Player as PlayerConstruct
from game_engine.entities.particles import ExplosionParticle

from game_engine.helpers import Colors, Direction, Size2D

from assets.images import *
from assets.sounds import *
from assets.objects.weapons import *
from ui.player import GameWin

class Player(PlayerConstruct):
    def __init__(self, position: pygame.Vector2, speed: int, jump_power: int):
        super().__init__(knight_image, position, (50, 70) , speed, jump_power)
        self.name = "Player"
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

    @property
    def anchor(self):
        return (pygame.Vector2(self.rect.midright) + pygame.Vector2(-10, 15)
                if self.direction else
                pygame.Vector2(self.rect.midleft) + pygame.Vector2(10, 15))

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
        if self.health > 0:
            death_sound.play()

    def die(self):
        center = self.rect.center
        particles = []
        for color in [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.BLACK]:
            particles.extend(ExplosionParticle.create_particles(
            pygame.Vector2(center), 35, color=color, size=(5, 15)))
        explode_sound.play()
        ExplosionParticle.register_particles(particles)
        death_sound.play()
        self.health = 0
        self.remove = True
        self.on_death()


class Enemy(EnemyConstruct):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int, image=player_image):
        super().__init__(image, position, size, speed, jump_power)
        self.flip_interval = 235
        self.direction = False
        self.actions = {
            # pygame.KEYDOWN: {
            #     pygame.K_j: self.move_right,
            #     pygame.K_l: self.move_left,
            #     pygame.K_i: self.move_jump,
            # },
            # pygame.KEYUP:  {
            #     pygame.K_j: self.stop_right,
            #     pygame.K_l: self.stop_left,
            # }
        }
        self.name = "Enemy"

    def on_attack(self):
        super().on_attack()

    def update(self):
        super().update()
        new_position, dirs = self.calculate_position(
            self.position, self.new_position)
        self.position = new_position

        if len(dirs[Direction.DOWN]) > 0:
            self.velocity.y = 0 if self.velocity.y > 0 else self.velocity.y
        if len(dirs[Direction.UP]) > 0:
            self.velocity.y = 0

        if self.position.y > 5000:
            self.die()

    def die(self):
        super().die()
        explode_sound.play()


class Zombie(Enemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, (50, 70), 3, 5, image=zombie_image)
        self.name = "Zombie"
        self.weapon = claws.copy()
        self.max_health = 50

    @property
    def anchor(self):
        return (pygame.Vector2(self.rect.midright) + pygame.Vector2(-10, 15)
                if self.direction else
                pygame.Vector2(self.rect.midleft) + pygame.Vector2(10, 15))

    def on_attack(self):
        super().on_attack()
        zombie_grunt_sound.play()

    def hurt(self, damage: int):
        super().hurt(damage)
        if self.health > 0:
            zombie_hurt_sound.play()

    def die(self):
        super().die()
        zombie_death_sound.play()



class Goblin(Enemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, (50, 70), 3, 5, image=goblin_image)
        self.name = "Goblin"
        self.weapon = mace.copy()
        self.health = self.max_health = 125

    @property
    def anchor(self):
        return (pygame.Vector2(self.rect.midright) + pygame.Vector2(-10, 17)
                if self.direction else
                pygame.Vector2(self.rect.midleft) + pygame.Vector2(10, 17))

    def on_attack(self):
        super().on_attack()
        goblin_grunt_sound.play()

    def hurt(self, damage: int):
        super().hurt(damage)
        if self.health > 0:
            goblin_hurt_sound.play()

    def die(self):
        super().die()
        goblin_death_sound.play()


class Minotaur(Enemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, (75, 105), 3, 5, image=minotaur_image)
        self.name = "Minotaur"
        self.weapon = battleaxe.copy()
        self.max_health = self.health = 250
        # self.weapon.sprite = pygame.transform.scale(self.weapon.sprite, (75, 75))

    @property
    def anchor(self):
        return (pygame.Vector2(self.rect.midright) + pygame.Vector2(-10, 15)
                if self.direction else
                pygame.Vector2(self.rect.midleft) + pygame.Vector2(10, 15))

    def on_attack(self):
        super().on_attack()
        demon_grunt_sound.play()

    def hurt(self, damage: int):
        super().hurt(damage)
        if self.health > 0:
            demon_hurt_sound.play()

    def die(self):
        super().die()
        demon_death_sound.play()


class Demon(Enemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, (125, 175), 3, 5, image=devil_image)
        self.name = "Demon"
        self.weapon = Melee(
            pygame.Vector2(0,0),
            pygame.transform.scale(trident_image, (100, 150)),
        95, 5)
        self.weapon.on_hit_sounds = hit_sharp_sounds
        self.attack_distance = self.weapon.size[1] + 200
        self.max_health = self.health = 666

    @property
    def anchor(self):
        return (pygame.Vector2(self.rect.midright) + pygame.Vector2(-10, 50)
                if self.direction else
                pygame.Vector2(self.rect.midleft) + pygame.Vector2(10, 50))

    def on_attack(self):
        super().on_attack()
        demon_grunt_sound.play()

    def hurt(self, damage: int):
        super().hurt(damage)
        if self.health > 0:
            demon_hurt_sound.play()

    def die(self):
        super().die()
        demon_death_sound.play()
        self.on_death()

    def on_death(self):
        super().on_death()
        # wait for 5 seconds
        def on_death():
            GameWin.instance().show = True
            print("You win!")
        on_wait = Timer(3,on_death)
        on_wait.start()

