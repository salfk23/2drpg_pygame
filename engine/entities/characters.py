
from typing import Sequence
import pygame

from engine.entities.entity import NORMAL_SIZE_ENTITY, Entity, HurtBox, Hurtable
from movable import IMoveable


class Player(Entity, Hurtable, IMoveable):
  def __init__(self, x:int, y:int):
    super().__init__(x, y, NORMAL_SIZE_ENTITY[0], NORMAL_SIZE_ENTITY[1], pygame.image.load("assets/player.png"))
    Hurtable.__init__(self, 100, 100)
    self.name = "Player"

  def move(self, key_pressed:Sequence[bool], entities:list[Entity]):
    y_mod, x_mod = 0, 0
    if key_pressed[pygame.K_w]:
      y_mod -= 1
    if key_pressed[pygame.K_s]:
      y_mod += 1
    if key_pressed[pygame.K_a]:
      x_mod -= 1
    if key_pressed[pygame.K_d]:
      x_mod += 1

    # New hurtbox but for Y
    new_hurtbox = HurtBox(self.x, self.y+y_mod, self.x+self.width, self.y+self.height+y_mod)
    conflict = False
    for entity in entities:
      if entity.hurtbox.conflict(new_hurtbox) and self is not entity:
        conflict = True
        break

    if not conflict:
      self.y += y_mod
      self.hurtbox = new_hurtbox

    new_hurtbox = HurtBox(self.x+x_mod, self.y, self.x+self.width+x_mod, self.y+self.height)
    conflict = False
    for entity in entities:
      if entity.hurtbox.conflict(new_hurtbox) and self is not entity:
        conflict = True
        break
    if not conflict:
      self.x += x_mod
      self.hurtbox = new_hurtbox



class Enemy(Entity, Hurtable, IMoveable):
  def __init__(self, x:int, y:int):
    super().__init__(x, y, NORMAL_SIZE_ENTITY[0], NORMAL_SIZE_ENTITY[1], pygame.image.load("assets/enemy.png"))
    Hurtable.__init__(self, 100, 100)
    self.name = "Enemy"

  def move(self, key_pressed:Sequence[bool], entities:list[Entity]):
    if key_pressed[pygame.K_UP]:
      self.y -= 1
    if key_pressed[pygame.K_DOWN]:
      self.y += 1
    if key_pressed[pygame.K_LEFT]:
      self.x -= 1
    if key_pressed[pygame.K_RIGHT]:
      self.x += 1
