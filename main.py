from cProfile import run
import pygame


WIDTH, HEIGHT = 800, 600

class GameUI:
  def __init__(self):
      self.entities = []
      pygame.display.set_mode((WIDTH, HEIGHT))

  def draw(self, screen):
      for entity in self.entities:
          entity.draw(screen)




def main():
  print("Running!")
  ui = GameUI()
  # ui.run()
  loop = True

  while loop:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        loop = False

  pygame.quit()

if __name__ == '__main__':
    main()
