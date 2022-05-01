import pygame
from game_engine.entities.dynamic import MovableEntity
from game_engine.entities.entity import BiDirectionalEntity
from game_engine.entities.state import Hurtable
from game_engine.helpers import Size2D


class Weapon(MovableEntity, BiDirectionalEntity):
  def __init__(self, anchor:pygame.Vector2, sprite:pygame.Surface, size:Size2D, damage:int, speed:int):
    super().__init__((0,0), size)
    BiDirectionalEntity.__init__(self, sprite)
    self.name = "Weapon"
    self.image = sprite
    self.sprite = sprite
    self.speed = speed
    self.damage = damage
    self._attacking = False
    self.offset = pygame.Vector2(-self.rect.height//2,0)
    self.frame = 0
    self._anchor = anchor
    self.attacked_entities: set[Hurtable] = set()
    self.owner = None

  @property
  def anchor(self):
    return self._anchor

  @anchor.setter
  def anchor(self, anchor:pygame.Vector2):
    self._anchor = anchor
    rect = None
    if self.direction:
      rect = self.sprite.get_rect(bottomleft=self.anchor)
    else:
      rect = self.sprite.get_rect(bottomright=self.anchor)
    self.position = pygame.Vector2(rect.topleft)


  @property
  def attacking(self):
    return self._attacking

  @attacking.setter
  def attacking(self, attacking:bool):
    if attacking != self._attacking:
      self._attacking = attacking
      if attacking:
        self.frame = 0
        self.attacked_entities.clear()
        self.attacked_entities.add(self.owner)

  def on_direction_change(self):
    self.sprite = self.sprites[self.direction]

  def update(self):
    if self.attacking:
      self.frame += self.speed
      if self.frame < 270:
        frame = self.frame if self.frame < 180 else 180 - (self.frame - 180)*2

        if self.direction:
          self.sprite = pygame.transform.rotozoom(self.sprites[self.direction], -frame, 1)
          offset_rect = self.offset.rotate(frame)
          self.position = pygame.Vector2(
            self.sprite.get_rect(center=self.anchor+offset_rect).topleft
          )
        else:
          self.sprite = pygame.transform.rotozoom(self.sprites[self.direction], frame, 1)
          offset_rect = pygame.Vector2(-self.offset.x, self.offset.y).rotate(-frame)
          self.position = pygame.Vector2(
            self.sprite.get_rect(center=self.anchor+offset_rect).topleft
          )
      else:
        self.sprite = self.sprites[self.direction]
        self.attacking = False
        self.frame = 0

      _, directions = self.calculate_position(
        pygame.Vector2(self.rect.center),
        pygame.Vector2(self.rect.topright if self.direction else self.rect.topleft)
      )

      entity_hit: list[Hurtable] = [entity for key in directions for entity in directions[key] if isinstance(entity, Hurtable)]

      for entity in entity_hit:
        if entity not in self.attacked_entities:
          self.attacked_entities.add(entity)
          entity.hurt(self.damage)





