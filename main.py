from cProfile import run
import pygame


WIDTH, HEIGHT = 800, 600


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)


class GameUI:
    def __init__(self):
        self.entities = []
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D RPG Game")

    def draw(self):
        self.window.fill(Colors.WHITE)
        pygame.display.update()

    def run(self):
        loop = True
        clock = pygame.time.Clock()

        while loop:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
            self.draw()


def main():
    print("Running!")
    ui = GameUI()
    ui.run()
    pygame.quit()


if __name__ == '__main__':
    main()
