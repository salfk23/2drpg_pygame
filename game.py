import pygame


class Entity:
  def __init__(self, x:int, y:int, width:int, height:int, image:pygame.Surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.image = image

    self.object = pygame.transform.rotate(
      pygame.transform.scale(self.image, (self.width, self.height)), 0)

class Player(Entity):
  def __init__(self, x:int, y:int):
    super().__init__(x, y, 32, 32, pygame.image.load("assets/test_player.png"))

