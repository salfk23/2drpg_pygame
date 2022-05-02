import pygame
from game_engine.entities.dynamic import AffectedByGravity, JumpableEntity

from game_engine.entities.entity import BiDirectionalEntity, Entity, EntityManager
from game_engine.entities.particles import ExplosionParticle
from game_engine.entities.state import Hurtable, Solid
from game_engine.entities.weapon import Melee, Weapon
from game_engine.helpers import Colors, Direction, Size2D
from assets.images import player_image
from assets.sounds import death_sound

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



class Character(JumpableEntity, BiDirectionalEntity, Hurtable, AffectedByGravity, Solid):
  def __init__(self, image:pygame.Surface, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
      JumpableEntity.__init__(self, position, size, speed, jump_power)
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
    JumpableEntity.update(self)
    if self.velocity.x > 0:
      self.direction = True
    elif self.velocity.x < 0:
      self.direction = False

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
      self._weapon = None
      Character.__init__(self, image, position, size, speed, jump_power)
      IMAGE = pygame.Surface((20, 50), pygame.SRCALPHA)
      IMAGE.fill(Colors.CYAN)
      pygame.draw.polygon(IMAGE, pygame.Color('red'), ( (5, 0), (20, 50),(5, 50)))
      self._weapon = Melee(self, pygame.Vector2(self.rect.right,self.rect.centery),IMAGE, (10, 50), 30, 10)
      self.linked.append(self.weapon)
      self.on_position_change()
      self.on_health_change()

  @property
  def weapon(self):
      return self._weapon

  @weapon.setter
  def weapon(self, weapon: Weapon):
      if self._weapon is not None:
        self.linked.remove(self._weapon)
        self._weapon.remove = True
      self._weapon = weapon
      self.linked.append(weapon)
      self.on_position_change()
      self.on_health_change()
      self.on_name_change()

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
        ExplosionParticle.register_particles(
          ExplosionParticle.create_particles(pygame.Vector2(center), 100)
        )
        self.remove = True
        self.on_death()

class PlayerCharacter(Player):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(player_image, position, size, speed, jump_power)
        self.jump_limit = 3
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
                entity.hurt(20)
        super().move_jump(event)

    def attack(self, event: pygame.event.Event):
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


class EnemyCharacter(Enemy):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(player_image, position, size, speed, jump_power)

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


