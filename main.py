import pygame
from game_engine.entities.entity import Entity
from game_engine.entities.event import EventListener
from game_engine.helpers import Config

from game_engine.engine import EntityManager, GameEngine

# from engine.entities.characters import Enemy, Player
# from engine.entities.entity import Entity, Hurtable
# from engine.ui import GameEngine


# WIDTH, HEIGHT = 800, 400


# def do_nothing(*args, **kwargs):
#     pass

# debug_print = print
# # debug_print = do_nothing

# class GameUI:
#     entities: list[Entity] = []
#     def __init__(self):
#         self.window = pygame.display.set_mode((WIDTH, HEIGHT))
#         pygame.display.set_caption("2D RPG Game")

#         player = Player(100, 100)
#         enemy = Enemy(100, 200)

#         ground = Entity(0, HEIGHT-32, WIDTH, 32, pygame.Surface((WIDTH, 32)))
#         ground.name = "Ground"



#         GameUI.entities.append(player)
#         player.health = 40
#         GameUI.entities.append(enemy)
#         GameUI.entities.append(ground)

#     def draw(self):

#         self.window.fill(Colors.WHITE)
#         for entity in GameUI.entities:
#             if (entity.x <= WIDTH and entity.y <= HEIGHT and
#                 entity.x >= 0-entity.width and entity.y >= 0-entity.height):
#                 # If entity is within the screen
#                 self.window.blit(entity.object, (entity.x, entity.y))
#                 debug_print("[IB]", entity.name, entity.x, entity.y, end='\t')
#             else:
#                 # If entity is completely outside the screen
#                 debug_print("[OB]", entity.name, entity.x, entity.y, end='\t')
#                 if entity.remove:
#                     self.entities.remove(entity)

#             self.window.blit(entity.object, (entity.x, entity.y))
#             # If entity extends Hurtable class
#             if isinstance(entity, Hurtable):
#                 debug_print("[H]", entity.health, entity.max_health, end='\t')
#                 # Add red bar
#                 self.window.fill(Colors.RED, (entity.x, entity.y-10, entity.width, 5))
#                 # Add health bar
#                 self.window.fill(Colors.GREEN, (entity.x, entity.y-10, (entity.width*entity.health)//entity.max_health, 5))
#         debug_print()
#         pygame.display.update()

#     def run(self):
#         loop = True
#         clock = pygame.time.Clock()

#         while loop:
#             clock.tick(60)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     loop = False
#             key_pressed = pygame.key.get_pressed()
#             for entity in GameUI.entities:
#                 # Check if method move exists
#                 if hasattr(entity, 'move'):
#                     entity.move(key_pressed, GameUI.entities)

#             self.draw()


class MovableBox(Entity):
    def __init__(self, position:pygame.Vector2, size:pygame.Vector2):
        super().__init__(position, size)
        self.input = True
        EventListener.instance().update(pygame.KEYDOWN, id(self), self.on_key_up)
        EventListener.instance().update(pygame.KEYUP, id(self), self.on_key_down)

    def on_key_down(self, event:pygame.event.Event):
        if event.key == pygame.K_LEFT:
            self.velocity.x = -10
        elif event.key == pygame.K_RIGHT:
            self.velocity.x = 10
        elif event.key == pygame.K_UP:
            self.velocity.y = -10
        elif event.key == pygame.K_DOWN:
            self.velocity.y = 10

    def on_key_up(self, event:pygame.event.Event):
        if event.key == pygame.K_LEFT:
            self.velocity.x = 0
        elif event.key == pygame.K_RIGHT:
            self.velocity.x = 0
        elif event.key == pygame.K_UP:
            self.velocity.y = 0
        elif event.key == pygame.K_DOWN:
            self.velocity.y = 0

    def update(self):
        self.position += self.velocity







def main_old():
    print("Running!")
    ui = GameUI()
    ui.run()
    pygame.quit()

def main():
    game = GameEngine.instance()
    em = EntityManager.instance()
    em.add(
        MovableBox(pygame.Vector2(40, 40), (40, 40))
    )
    game.run()



if __name__ == '__main__':
    main()
