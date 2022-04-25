import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity



class MovableBox(ControllableEntity, AffectedByGravity):
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

        AffectedByGravity.update(self)





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
