import pygame
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity

from game_engine.entities.entity import BiDirectionalEntity, Entity
from game_engine.entities.particles import ExplosionParticle
from game_engine.entities.state import Hurtable, Solid
from game_engine.entities.weapon import Weapon
from game_engine.helpers import Colors, Size2D, load_image



class Healthbar(Entity):
  def __init__(self, size: Size2D):
      super().__init__((0,0), size)
      self.name = "Healthbar"
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
    self._health = health
    self.on_health_change()

  def on_health_change(self):
    pygame.draw.rect(self.sprite, Colors.RED, (0, 0, self.size[0], self.size[1]))
    rect = pygame.Rect(0, 0, self.size[0]* self._health / self.max_health, self.size[1])
    pygame.draw.rect(self.sprite, Colors.GREEN, rect)



class Character(ControllableEntity, BiDirectionalEntity, Hurtable, AffectedByGravity, Solid):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      ControllableEntity.__init__(self, position, size, speed, jump_power)
      Hurtable.__init__(self, 150, 150)
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
      self.weapon = None
      Character.__init__(self, image, position, size, speed, jump_power)
      self.health_bar = Healthbar((50, 10))
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.CYAN)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))
      self.weapon = Weapon(pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 30, 10)
      self.weapon.owner = self
      self.weapon = Weapon(pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 10, 1)
      self.weapon.owner = self
      self.linked.append(self.health_bar)
      self.linked.append(self.weapon)
      self.on_position_change()
      self.on_health_change()
  def on_name_change(self):
      self.health_bar.name = self.name+"_Healthbar"
      self.weapon.name = f"{self.name}_Weapon_{self.weapon.name}"

  def on_direction_change(self):
      super().on_direction_change()
      if self.weapon is not None:
        self.weapon.direction = self.direction
  def on_position_change(self):
      super().on_position_change()
      health_bar_rect = self.health_bar.rect
      health_bar_rect.center = self.rect.center
      health_bar_rect.top = self.rect.top - health_bar_rect.height - 10
      if self.direction:
        self.weapon.anchor = pygame.Vector2(self.rect.right, self.rect.centery)
      else:
        self.weapon.anchor = pygame.Vector2(self.rect.left, self.rect.centery)
      self.health_bar.position = pygame.Vector2(health_bar_rect.topleft)
  def on_health_change(self):
      super().on_health_change()
      self.health_bar.max_health = self.max_health
      self.health_bar.health = self.health
      self.health_bar.on_health_change()
  def die(self):
        center = self.rect.center
        ExplosionParticle.create_particles(pygame.Vector2(center), 100, Colors.RED, (2, 10), (0.1, 3))
        self.remove = True
  def update(self):
      super().update()
      # Get distance to player


class Player(Character):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      self.weapon = None
      Character.__init__(self, image, position, size, speed, jump_power)
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.CYAN)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))
      self.weapon = Weapon(pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 30, 10)
      self.weapon.owner = self
      self.linked.append(self.weapon)
      self.on_position_change()
      self.on_health_change()
  def on_position_change(self):
      super().on_position_change()
      if self.direction:
        self.weapon.anchor = pygame.Vector2(self.rect.right, self.rect.centery)
      else:
        self.weapon.anchor = pygame.Vector2(self.rect.left, self.rect.centery)
  def on_direction_change(self):
      super().on_direction_change()
      if self.weapon is not None:
        self.weapon.direction = self.direction
  def die(self):
        center = self.rect.center
        ExplosionParticle.create_particles(pygame.Vector2(center), 100, Colors.RED, (2, 10), (0.1, 3))
        self.remove = True
