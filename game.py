from typing import Sequence
import pygame

from movable import IMoveable

NORMAL_SIZE_ENTITY = (32, 52)
class Hurtable:
  def __init__(self, health: int, max_health: int):
    self.health = health
    self.max_health = max_health

class HurtBox:
  def __init__(self, x1: int, y1: int, x2: int, y2: int):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

  def conflict(self, other:'HurtBox'):
    # If the two hurtboxes are overlapping, return true
    return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

class Entity:
  def __init__(self, x:int, y:int, width:int, height:int, sprite:pygame.Surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.sprite = sprite
    self.remove = False
    self.name = "Entity"
    self.hurtbox = HurtBox(x, y, x+width, y+height)

    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.sprite, (self.width, self.height)), 0)

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

class Weapon(Entity):
  def __init__(self, x:int, y:int, width:int, height:int, sprite:pygame.Surface):
    super().__init__(x, y, width, height, sprite)
    self.name = "Weapon"
    self.remove = False
