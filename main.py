import pygame
from game_engine.entities.entity import Entity
from game_engine.entities.event import EmptyCallback, EventListener
from game_engine.helpers import Config, Size2D

from game_engine.engine import EntityManager, GameEngine
class Movable(Entity):
    def __init__(self, position: pygame.Vector2, size:Size2D, speed:int, jump_power:int):
        super().__init__(position, size)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = speed
        self.jump_power = jump_power
        self.event_listener = EventListener.instance()
        self.key_down_actions = {
            pygame.K_d: self.move_right,
            pygame.K_a: self.move_left,
            pygame.K_w: self.move_jump,
        }
        self.key_up_actions = {
            pygame.K_d: self.stop_right,
            pygame.K_a: self.stop_left,
        }
        EventListener.instance().update(
            pygame.KEYUP, self,
            lambda e: self.key_up_actions.get(e.key, lambda : None)()
        )
        EventListener.instance().update(
            pygame.KEYDOWN, self,
            lambda e: self.key_down_actions.get(e.key, lambda : None)()
        )

    def move_left(self):
        self.velocity.x = -self.speed
    def move_right(self):
        self.velocity.x = self.speed
    def stop_right(self):
        self.velocity.x = 0 if self.velocity.x > 0 else self.velocity.x
    def stop_left(self):
        self.velocity.x = 0 if self.velocity.x < 0 else self.velocity.x
    def move_jump(self):
        self.velocity.y = -self.jump_power



class MovableBox(Movable):
    def __init__(self, position:pygame.Vector2, size:pygame.Vector2, speed:int, jump_power:int):
        super().__init__(position, size, speed, jump_power)
        self.input = True
    def update(self):
        self.position += self.velocity
        # Get velocity y closer to 0 each frame
        if self.velocity.y < 0:
            self.velocity.y *= 0.9
            if self.velocity.y < 0 and self.velocity.y > -0.1:
                self.velocity.y = 0

        if self.velocity.y > 0:
            self.velocity.y *= 0.9
            if self.velocity.y > 0 and self.velocity.y < 0.1:
                self.velocity.y = 0





def main():
    print("Running!")
    game = GameEngine.instance()
    em = EntityManager.instance()
    em.add(
        MovableBox(pygame.Vector2(40, 300), (40, 40), 5, 10)
    )
    game.run()



if __name__ == '__main__':
    main()
