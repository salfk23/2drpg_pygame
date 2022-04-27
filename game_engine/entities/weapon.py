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
    self.frame = 0
    self.anchor = anchor
    self.attacked_entities: list[Hurtable] = []

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


  def update(self):
    if self.attacking:
      self.frame += self.speed
      if self.frame <= 90:
        if self.direction:
          # Rotate the sprite 90 degrees to the right incrementally
          self.sprite = pygame.transform.rotozoom(self.image, self.frame, 1)
        else:
          # Rotate the sprite 90 degrees to the left incrementally
          self.sprite = pygame.transform.rotozoom(self.image, -self.frame, 1)
      else:
        if self.direction:
          self.sprite = pygame.transform.rotozoom(self.image, 90-self.frame%91, 1)
        else:
          self.sprite = pygame.transform.rotozoom(self.image, 90+self.frame%91, 1)
      if self.frame > 180:
        self.attacking = False
        self.frame = 0

      _, directions = self.calculate_position(pygame.Vector2(self.rect.center), pygame.Vector2(self.rect.topright))
      print(directions, self.attacked_entities)
      for direction in directions:
        for entity in directions[direction]:
          if entity not in self.attacked_entities:
            print(entity.name)
            entity.health -= self.damage
            self.attacked_entities.append(entity)

    else:
      self.frame = 0





