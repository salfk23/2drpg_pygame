import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity
from game_engine.entities.entity import ColoredEntity, Entity
from game_engine.entities.state import Solid
from game_engine.helpers import Colors, Direction, Size2D
import game_engine.helpers as helpers


class MovableBox(ControllableEntity, AffectedByGravity, ColoredEntity, Solid):

    def on_color_change(self):
        self.sprite.fill(self.color)
        self.object = pygame.transform.scale(self.sprite, self.size)

    def update(self):
        AffectedByGravity.update(self)
        new_position = self.position + self.velocity
        old_y = self.position.y
        new_position, (up, down, left, right) = self.calculate_position(self.position, new_position)

        if down:
            self.velocity.y = 0
        self.position = new_position
        print(self.position.y, old_y)
        # Get velocity y closer to 0 each frame
        # if self.velocity.y < 0:
        #     self.velocity.y *= 0.9
        #     if self.velocity.y < 0 and self.velocity.y > -0.1:
        #         self.velocity.y = 0

        # if self.velocity.y > 0:
        #     self.velocity.y *= 0.9
        #     if self.velocity.y > 0 and self.velocity.y < 0.1:
        #         self.velocity.y = 0


    def on_collision(self, other: Entity, collision_direction: int):
        # If entity is instance of AffectedByGravity
        if (self.name == "Entity" and other.name == "FollowingMouse"):
            print("Tile")
            print("UP" if collision_direction == Direction.UP else "DOWN" if collision_direction == Direction.DOWN else "LEFT" if collision_direction == Direction.LEFT else "RIGHT")
        if isinstance(other, Solid):
            if collision_direction == Direction.DOWN and self.velocity.y > 0:
                self.velocity.y = 0
                self.position.y = other.position.y - self.size[1]+1
                # Change this entity color to red
                self.color = Colors.RED
            if collision_direction == Direction.UP and self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = other.position.y + other.size[1]
                self.color = Colors.GREEN
            if collision_direction == Direction.LEFT and self.velocity.x < 0:
                self.velocity.x = 0
                self.color = Colors.BLUE
            if collision_direction == Direction.RIGHT and self.velocity.x > 0:
                self.velocity.x = 0
                self.color = Colors.YELLOW








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
    mb.color = Colors.BLUE
    wall.name = "Tile 2"
    em.add(ground)
    em.add(wall)
    em.add(mb)
    em.focused_entity = mb
    fm = FollowingMouse(pygame.Vector2(50, 50), (10, 10))
    fm.name = "FollowingMouse"
    # em.add(fm)
    game.run()



if __name__ == '__main__':
    main()
