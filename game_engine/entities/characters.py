import pygame
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity

from game_engine.entities.entity import BiDirectionalEntity, Entity, EntityManager
from game_engine.entities.particles import ExplosionParticle
from game_engine.entities.state import Hurtable, Solid
from game_engine.entities.weapon import Melee
from game_engine.helpers import Colors, Size2D, load_image



class Statusbar(Entity):
  def __init__(self, size: Size2D):
      super().__init__((0,0), size)
      self.name = "Healthbar"
      self.sprite = pygame.Surface(size)
      self.sprite.fill(Colors.RED)
      self._current = 0
      self.max = 100
      self.size = size
      self.background_color = Colors.RED
      self.fill_color = Colors.GREEN
      self.on_health_change()
  @property
  def current(self):
    return self._current

  @current.setter
  def current(self, health: int):
    self._current = health
    self.on_health_change()

  def on_health_change(self):
    pygame.draw.rect(self.sprite, self.background_color, (0, 0, self.size[0], self.size[1]))
    rect = pygame.Rect(0, 0, self.size[0]* self._current / self.max, self.size[1])
    pygame.draw.rect(self.sprite, self.fill_color, rect)



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
      self.health_bar = Statusbar((50, 10))
      self.strike_bar = Statusbar((50, 5))
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.CYAN)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))
      self.weapon = Melee(self, pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 10, 10)
      self.linked.append(self.health_bar)
      self.linked.append(self.strike_bar)
      self.linked.append(self.weapon)
      self.on_position_change()
      self.on_health_change()
      self.frame = 0
      self.strike_interval = 500
      self.flip_interval = 250
      self.strike_bar.max = self.strike_interval
      self.strike_bar.background_color = Colors.BLACK
      self.strike_bar.fill_color = Colors.YELLOW

  def on_name_change(self):
      self.health_bar.name = self.name+"_Healthbar"
      self.strike_bar.name = self.name+"_Strikebar"
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
      strike_bar_rect = self.strike_bar.rect
      strike_bar_rect.center = self.rect.center
      strike_bar_rect.top = self.rect.top - strike_bar_rect.height - 5
      if self.direction:
        self.weapon.anchor = pygame.Vector2(self.rect.right, self.rect.centery)
      else:
        self.weapon.anchor = pygame.Vector2(self.rect.left, self.rect.centery)
      self.health_bar.position = pygame.Vector2(health_bar_rect.topleft)
      self.strike_bar.position = pygame.Vector2(strike_bar_rect.topleft)
  def on_health_change(self):
      super().on_health_change()
      self.health_bar.max = self.max_health
      self.health_bar.current = self.health
      self.health_bar.on_health_change()
  def die(self):
        center = self.rect.center
        ExplosionParticle.create_particles(pygame.Vector2(center), 100)
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
        current_distance =  self.distance_to(player)
        if current_distance < distance:
          distance = current_distance
          # Get whether the player is on left or right side
          if player.rect.centerx < self.rect.centerx :
            direction = False
          else:
            direction = True
      if self.frame % self.flip_interval == 0:
        self.direction = direction
      if distance < 200 and self.weapon.attacking == False and self.frame > self.strike_interval:
        self.weapon.attacking = True
        self.frame = 0
      self.frame += 1
      self.strike_bar.current = self.frame



class Player(Character):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      self.weapon = None
      Character.__init__(self, image, position, size, speed, jump_power)
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.CYAN)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))
      self.weapon = Melee(self, pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 30, 10)
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
        ExplosionParticle.create_particles(pygame.Vector2(center), 100)
        self.remove = True
