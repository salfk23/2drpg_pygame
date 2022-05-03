"""Character module, used to provide character-like behaviour."""

import pygame

from game_engine.entities.dynamic import AffectedByGravity, JumpableEntity
from game_engine.entities.entity import BiDirectionalEntity, Entity, EntityManager
from game_engine.entities.particles import ExplosionParticle
from game_engine.entities.state import Hurtable, Solid
from game_engine.entities.weapon import Weapon
from game_engine.helpers import Colors, Size2D


class Statusbar(Entity):
    """Bar with current and max values"""

    def __init__(self, size: Size2D, max: int = 100, current: int = 100, fill_color: tuple = Colors.GREEN, background_color: tuple = Colors.RED):
        super().__init__((0, 0), size)
        self.name = "Healthbar"
        self.sprite = pygame.Surface(size)
        self.sprite.fill(background_color)
        self._current = current
        self._max = max
        self.size = size
        self.background_color = background_color
        self.fill_color = fill_color
        self.on_health_change()

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value
        self.on_health_change()

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, health: int):
        self._current = health
        self.on_health_change()

    def on_health_change(self):
        size = (0, 0, self.size[0], self.size[1])
        pygame.draw.rect(self.sprite, self.background_color, size)
        rect = pygame.Rect(
            0, 0, self.size[0] * self._current / self.max, self.size[1]
        )
        pygame.draw.rect(self.sprite, self.fill_color, rect)


class Character(
  JumpableEntity, BiDirectionalEntity, Hurtable, AffectedByGravity, Solid
  ):
    """
    Character entity, which is affected by gravity, can be hurt and move, and
    is solid, meaning it can be jumped on.
    """
    def __init__(self, image: pygame.Surface, position: pygame.Vector2,
                 size: Size2D, speed: int, jump_power: int):
        JumpableEntity.__init__(self, position, size, speed, jump_power)
        Hurtable.__init__(self, 150, 150)
        image = pygame.transform.scale(image, size)
        BiDirectionalEntity.__init__(self, image)
        self.on_direction_change()
        self.on_health_change()
        self.on_position_change()

    def on_direction_change(self):
        self.sprite = self.sprites[self.direction]

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health: int):
        Hurtable.health.fset(self, health)

    def update(self):
        AffectedByGravity.update(self)
        JumpableEntity.update(self)
        if self.velocity.x > 0:
            self.direction = True
        elif self.velocity.x < 0:
            self.direction = False


class WeaponizedCharacter(Character):
    def __init__(self, image: pygame.Surface, position: pygame.Vector2,
                 size: Size2D, speed: int, jump_power: int, weapon: Weapon = None):
        self._weapon = weapon
        super().__init__(image, position, size, speed, jump_power)
        self.on_weapon_change()

    def on_attack(self):
        pass

    @property
    def anchor(self):
        return pygame.Vector2(self.rect.midright) if self.direction else pygame.Vector2(self.rect.midleft)

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, weapon: Weapon):
        if self._weapon is not None:
            self._weapon.owner = None
            self.linked.remove(self._weapon)
            self._weapon.remove = True
        self._weapon = weapon
        self.linked.append(self.weapon)
        self.weapon.owner = self
        self.on_direction_change()
        self.on_position_change()
        self.on_weapon_change()

    def on_weapon_change(self):
        pass

    def on_position_change(self):
        super().on_position_change()
        if self.weapon is not None:
            self.weapon.anchor = self.anchor

    def on_direction_change(self):
        super().on_direction_change()
        if self.weapon is not None:
            self.weapon.direction = self.direction


class Enemy(WeaponizedCharacter):
    def __init__(self, image: pygame.Surface, position: pygame.Vector2,
                 size: Size2D, speed: int, jump_power: int, weapon: Weapon = None):
        self.strike_interval = 500
        self.flip_interval = 245
        self.frame = 0
        self.attack_distance = 200

        self.health_bar = Statusbar((size[0], 10))
        self.strike_bar = Statusbar(
            (size[0], 5), max=self.strike_interval, current=self.frame,
            fill_color=Colors.YELLOW, background_color=Colors.BLACK
        )
        super().__init__(image, position, size, speed, jump_power, weapon)
        self.linked.append(self.health_bar)
        self.linked.append(self.strike_bar)
        self.name = "Enemy"

    def on_name_change(self):
        self.health_bar.name = self.name+"_Healthbar"
        self.strike_bar.name = self.name+"_Strikebar"

    def on_position_change(self):
        super().on_position_change()
        health_bar_rect = self.health_bar.rect
        health_bar_rect.midbottom = self.rect.midtop
        health_bar_rect.top -= 10
        strike_bar_rect = self.strike_bar.rect
        strike_bar_rect.midbottom = self.rect.midtop
        strike_bar_rect.top -= 5
        self.health_bar.position = pygame.Vector2(health_bar_rect.topleft)
        self.strike_bar.position = pygame.Vector2(strike_bar_rect.topleft)

    def on_health_change(self):
        super().on_health_change()
        self.health_bar.max = self.max_health
        self.health_bar.current = self.health

    def die(self):
        center = self.rect.center
        ExplosionParticle.register_particles(
            ExplosionParticle.create_particles(pygame.Vector2(center), 100)
        )
        self.remove = True

    def update(self):
        super().update()
        # Get distance to player

        players: list[Player] = EntityManager.instance().get_of_type(Player)
        # Infinite distance
        distance = float("inf")
        direction = self.direction

        for player in players:
            # Get distance to player
            current_distance = self.distance_to(player)
            if current_distance < distance:
                distance = current_distance
                # Get whether the player is on left or right side
                if player.rect.centerx < self.rect.centerx:
                    direction = False
                else:
                    direction = True
        if self.frame % self.flip_interval == 0:
            self.direction = direction
        if self.weapon is not None:
            if (    distance < self.attack_distance
                and self.weapon.attacking == False
                and self.frame > self.strike_interval):
                self.weapon.attacking = True
                self.frame = 0
        if self.frame <= self.strike_interval:
            self.frame += 1
        self.strike_bar.current = self.frame


class Player(WeaponizedCharacter):
    def die(self):
        center = self.rect.center
        ExplosionParticle.register_particles(
            ExplosionParticle.create_particles(pygame.Vector2(center), 100)
        )
        self.remove = True
        self.on_death()
