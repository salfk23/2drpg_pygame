
from typing import Sequence
import pygame
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity

from game_engine.entities.entity import NORMAL_SIZE_ENTITY, BiDirectionalEntity, Entity
from game_engine.entities.particles import ExplosionParticle
from game_engine.entities.state import Hurtable, Solid
from game_engine.entities.weapon import Weapon
from game_engine.helpers import Colors, Size2D, load_image



class Healthbar(Entity):
  def __init__(self, size: pygame.Vector2):
      super().__init__((0,0), size)
      self.sprite = pygame.Surface(size)
      self.sprite.fill(Colors.RED)
      self._health = 0
      self.max_health = 100
      self.size = size
      self.on_health_change()
  @property
  def health(self):
    return self._health

  @health.setter
  def health(self, health: int):
    if health != self._health:
      self._health = health
      self.on_health_change()

  def on_health_change(self):
    pygame.draw.rect(self.sprite, Colors.YELLOW, (0, 0, self.size.x, self.size.y))
    rect = pygame.Rect(0, 0, self.size.x* self.health / self.max_health, self.size.y)
    pygame.draw.rect(self.sprite, Colors.GREEN, rect)



class Character(ControllableEntity, BiDirectionalEntity, Hurtable, AffectedByGravity, Solid):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      ControllableEntity.__init__(self, position, size, speed, jump_power)
      Hurtable.__init__(self, 100, 150)
      image = pygame.transform.scale(image, size)
      BiDirectionalEntity.__init__(self, image)
      self.on_direction_change()

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
    ControllableEntity.update(self)
    if self.velocity.x > 0:
      self.direction = True
    elif self.velocity.x < 0:
      self.direction = False
stick_image = load_image("assets/stick.png")
class Enemy(Character):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      Character.__init__(self, image, position, size, speed, jump_power)
      self.health_bar = Healthbar(pygame.Vector2(50, 10))
      # stick = Weapon(stick_image, (10, 50), 1, 1)
      # stick.fill(Colors.RED)
      # stick = pygame.transform.rotate(stick_image, -10)
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.YELLOW)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (0, 0), (20, 0),(6, 50)))
      IMAGE = pygame.transform.rotate(IMAGE, 180)
      self.weapon = Weapon(pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 10, 1)
      self.linked.append(self.health_bar)
      self.linked.append(self.weapon)
      self.on_position_change()
      self.on_health_change()
  def on_position_change(self):
      super().on_position_change()
      health_bar_rect = self.health_bar.rect
      health_bar_rect.center = self.rect.center
      health_bar_rect.top = self.rect.top - health_bar_rect.height - 10
      weapon_rect = self.weapon.rect
      weapon_rect.bottom = self.rect.centery
      if self.direction:
        weapon_rect.right = self.rect.right
        self.weapon.anchor = pygame.Vector2(weapon_rect.right, weapon_rect.centery)
      else:
        weapon_rect.left = self.rect.left - weapon_rect.width
        self.weapon.anchor = pygame.Vector2(weapon_rect.left, weapon_rect.centery)

      self.health_bar.position = health_bar_rect.topleft
      self.weapon.position = weapon_rect.topleft
  def on_health_change(self):
      super().on_health_change()
      self.health_bar.max_health = self.max_health
      self.health_bar.health = self.health
  def die(self):
        center = self.rect.center
        ExplosionParticle.create_particles(pygame.Vector2(center), 100, Colors.RED, (2, 10), (0.1, 3))
        self.remove = True


class Player(Character):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      Character.__init__(self, image, position, size, speed, jump_power)
      # stick = Weapon(stick_image, (10, 50), 1, 1)
      # stick.fill(Colors.RED)
      # stick = pygame.transform.rotate(stick_image, -10)
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.YELLOW)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (0, 0), (20, 0),(6, 50)))
      IMAGE = pygame.transform.rotate(IMAGE, 180)
      self.weapon = Weapon(pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 50, 10)
      self.linked.append(self.weapon)
      self.on_position_change()
      self.on_health_change()
  def on_position_change(self):
      super().on_position_change()
      weapon_rect = self.weapon.rect
      weapon_rect.bottom = self.rect.centery
      if self.direction:
        weapon_rect.right = self.rect.right
        self.weapon.anchor = pygame.Vector2(weapon_rect.right, weapon_rect.centery)
      else:
        weapon_rect.left = self.rect.left - weapon_rect.width
        self.weapon.anchor = pygame.Vector2(weapon_rect.left, weapon_rect.centery)
      self.weapon.position = weapon_rect.topleft
  def die(self):
        center = self.rect.center
        ExplosionParticle.create_particles(pygame.Vector2(center), 100, Colors.RED, (2, 10), (0.1, 3))
        self.remove = True
