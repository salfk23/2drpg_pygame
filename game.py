import pygame


class Entity:
  def __init__(self, x:int, y:int, width:int, height:int, image:pygame.Surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.image = image

