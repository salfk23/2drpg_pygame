import pygame

from game import Enemy, Entity, Hurtable, Player


WIDTH, HEIGHT = 800, 400


def do_nothing(*args, **kwargs):
    pass

debug_print = print
# debug_print = do_nothing
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
    entities: list[Entity] = []
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D RPG Game")

        player = Player(100, 100)
        enemy = Enemy(100, 200)

        ground = Entity(0, HEIGHT-32, WIDTH, 32, pygame.Surface((WIDTH, 32)))
        ground.name = "Ground"



        GameUI.entities.append(player)
        player.health = 40
        GameUI.entities.append(enemy)
        GameUI.entities.append(ground)

    def draw(self):

        self.window.fill(Colors.WHITE)
        for entity in GameUI.entities:
            if (entity.x <= WIDTH and entity.y <= HEIGHT and
                entity.x >= 0-entity.width and entity.y >= 0-entity.height):
                # If entity is within the screen
                self.window.blit(entity.object, (entity.x, entity.y))
                debug_print("[IB]", entity.name, entity.x, entity.y, end='\t')
            else:
                # If entity is completely outside the screen
                debug_print("[OB]", entity.name, entity.x, entity.y, end='\t')
                if entity.remove:
                    self.entities.remove(entity)

            self.window.blit(entity.object, (entity.x, entity.y))
            # If entity extends Hurtable class
            if isinstance(entity, Hurtable):
                debug_print("[H]", entity.health, entity.max_health, end='\t')
                # Add red bar
                self.window.fill(Colors.RED, (entity.x, entity.y-10, entity.width, 5))
                # Add health bar
                self.window.fill(Colors.GREEN, (entity.x, entity.y-10, (entity.width*entity.health)//entity.max_health, 5))
        debug_print()
        pygame.display.update()

    def run(self):
        loop = True
        clock = pygame.time.Clock()

        while loop:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
            key_pressed = pygame.key.get_pressed()
            for entity in GameUI.entities:
                # Check if method move exists
                if hasattr(entity, 'move'):
                    entity.move(key_pressed, GameUI.entities)

            self.draw()


def main():
    print("Running!")
    ui = GameUI()
    ui.run()
    pygame.quit()


if __name__ == '__main__':
    main()
