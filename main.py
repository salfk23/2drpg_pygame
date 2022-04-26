import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.characters import Character, Enemy
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity, MovableEntity
from game_engine.entities.entity import ColoredEntity, Entity
from game_engine.entities.state import Solid
from game_engine.helpers import Colors, Direction, Size2D
import game_engine.helpers as helpers


class MovableBox(Enemy, ColoredEntity):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(position, size, speed, jump_power)

        self.actions = {
            pygame.KEYDOWN : {
                pygame.K_d: self.move_right,
                pygame.K_a: self.move_left,
                pygame.K_w: self.move_jump,
            },
            pygame.KEYUP:  {
                pygame.K_d: self.stop_right,
                pygame.K_a: self.stop_left,
            }
        }


    def on_color_change(self):
        sprite = pygame.Surface(self.size)
        sprite.fill(self.color)
        self.object = pygame.transform.scale(sprite, self.size)

    def update(self):
        super().update()
        new_position, (up, down, left, right) = self.calculate_position(self.position, self.new_position)


        if down:
            self.velocity.y = 0
            self.color = Colors.GREEN
        if up:
            self.velocity.y = 0
            self.color = Colors.PURPLE
        if left:
            self.color = Colors.RED
        if right:
            self.color = Colors.YELLOW
        self.position = new_position


class MovableBox2(Enemy, ColoredEntity):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(position, size, speed, jump_power)

        self.actions = {
            pygame.KEYDOWN : {
                pygame.K_j: self.move_right,
                pygame.K_l: self.move_left,
                pygame.K_i: self.move_jump,
            },
            pygame.KEYUP:  {
                pygame.K_j: self.stop_right,
                pygame.K_l: self.stop_left,
            }
        }

    def on_color_change(self):
        sprite = pygame.Surface(self.size)
        sprite.fill(self.color)
        self.object = pygame.transform.scale(sprite, self.size)

    def update(self):
        super().update()
        new_position, (up, down, left, right) = self.calculate_position(self.position, self.new_position)


        if down:
            self.velocity.y = 0
            self.color = Colors.BLACK
        if up:
            self.velocity.y = 0
            self.color = Colors.BLACK
        if left:
            self.color = Colors.BLACK
        if right:
            self.color = Colors.BLACK
        self.position = new_position









class FollowingMouse(Entity, Solid):
    def update(self):
        # Get mouse position
        point = pygame.Vector2(pygame.mouse.get_pos())

        self.position = point

class Tile(Entity, Solid):
    pass

def main():
    print("Running!")
    game = GameEngine.instance()
    em = EntityManager.instance()
    ground = Tile(pygame.Vector2(20, 450), (600, 300))
    ground.name = "Tile"

    wall = Tile(pygame.Vector2(20, 400), (200, 70))

    mb = MovableBox(pygame.Vector2(220, 390), (40, 40), 5, 10)
    en = MovableBox2(pygame.Vector2(250, 300), (40, 60), 5, 10)
    mb.color = Colors.BLUE
    wall.name = "Tile 2"
    em.add(ground)
    em.add(wall)
    em.add(mb)
    em.add(en)
    em.focused_entity = mb
    fm = FollowingMouse(pygame.Vector2(50, 50), (10, 10))
    fm.name = "FollowingMouse"
    # em.add(fm)
    game.run()



if __name__ == '__main__':
    main()
