import pygame
from game_engine.engine import EntityManager, GameEngine
from game_engine.entities.characters import Character, Enemy, Player
from game_engine.entities.dynamic import AffectedByGravity, ControllableEntity, MovableEntity
from game_engine.entities.entity import ColoredEntity, Entity
from game_engine.entities.particles import ExplosionParticle
from game_engine.entities.state import Solid
from game_engine.entities.ui import PlayerHealthBar
from game_engine.helpers import Colors, Direction, Size2D
import game_engine.helpers as helpers

player_image = helpers.load_image("assets\player.png")
death_sound = helpers.load_sound("assets\death.ogg")


class MovableBox(Player, ColoredEntity):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(player_image, position, size, speed, jump_power)
        self.jump_limit = 3
        self.actions = {
            pygame.KEYDOWN: {
                pygame.K_d: self.move_right,
                pygame.K_a: self.move_left,
                pygame.K_w: self.move_jump,
                pygame.K_s: self.action_hurt,
                pygame.K_f: self.attack,
            },
            pygame.KEYUP:  {
                pygame.K_d: self.stop_right,
                pygame.K_a: self.stop_left,
            }
        }

    def move_jump(self):
        print("jump")

        _, dirs = self.calculate_position(
            self.position, self.position+pygame.Vector2(0, 5))
        for entity in dirs[Direction.DOWN]:
            self.jump_number = 0
            print("Jumped on " + entity.name)
            if isinstance(entity, Enemy):
                entity.hurt(20)
        super().move_jump()

    def attack(self):
        self.weapon.attacking = True

    def action_hurt(self):
        self.hurt(100)

    def on_color_change(self):
        sprite = pygame.Surface(self.size)
        sprite.fill(self.color)
        self.object = pygame.transform.scale(sprite, self.size)

    def update(self):
        super().update()
        new_position, dirs = self.calculate_position(
            self.position, self.new_position)

        if len(dirs[Direction.DOWN]) > 0:
            self.velocity.y = 0 if self.velocity.y > 0 else self.velocity.y
            self.color = Colors.GREEN
        if len(dirs[Direction.UP]) > 0:
            self.velocity.y = 0
            self.color = Colors.PURPLE
        if len(dirs[Direction.LEFT]) > 0:
            self.color = Colors.RED
        if len(dirs[Direction.RIGHT]) > 0:
            self.color = Colors.YELLOW
        self.position = new_position
        if self.position.y > 5000:
            self.die()

    def die(self):
        center = self.rect.center
        particles = []
        particles.extend(ExplosionParticle.create_particles(
            pygame.Vector2(center), 35, color=Colors.RED, size=(5, 15)))
        particles.extend(ExplosionParticle.create_particles(
            pygame.Vector2(center), 35, color=Colors.YELLOW, size=(5, 15)))
        particles.extend(ExplosionParticle.create_particles(
            pygame.Vector2(center), 35, color=Colors.GREEN, size=(5, 15)))
        particles.extend(ExplosionParticle.create_particles(
            pygame.Vector2(center), 35, color=Colors.BLACK, size=(5, 15)))
        ExplosionParticle.register_particles(particles)
        death_sound.play()
        self.health = 0
        self.remove = True


class MovableBox2(Enemy, ColoredEntity):
    def __init__(self, position: pygame.Vector2, size: Size2D, speed: int, jump_power: int):
        super().__init__(player_image, position, size, speed, jump_power)

        self.actions = {
            pygame.KEYDOWN: {
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
        new_position, dirs = self.calculate_position(
            self.position, self.new_position)

        if len(dirs[Direction.DOWN]) > 0:
            self.velocity.y = 0 if self.velocity.y > 0 else self.velocity.y
            self.color = Colors.BLACK
            for entity in dirs[Direction.DOWN]:
                if isinstance(entity, StepableBlock):
                    entity.color = Colors.RED
                    self.health -= 1
        if len(dirs[Direction.UP]) > 0:
            self.velocity.y = 0
            self.color = Colors.BLACK
        if len(dirs[Direction.LEFT]) > 0:
            self.color = Colors.BLACK
        if len(dirs[Direction.RIGHT]) > 0:
            self.color = Colors.BLACK
        self.position = new_position


class FollowingMouse(Entity, Solid):
    def update(self):
        # Get mouse position
        point = pygame.Vector2(pygame.mouse.get_pos())

        self.position = point


class Tile(Entity, Solid):
    pass


class StepableBlock(Tile, ColoredEntity):
    def on_color_change(self):
        sprite = pygame.Surface(self.size)
        sprite.fill(self.color)
        self.sprite = pygame.transform.scale(sprite, self.size)


def tile_texture(texture, size):
    result = pygame.Surface(size, depth=32)
    for x in range(0, size[0], texture.get_width()):
        for y in range(0, size[1], texture.get_height()):
            result.blit(texture, (x, y))
    return result


def main():
    print("Running!")
    game = GameEngine.instance()
    em = EntityManager.instance()
    ground = Tile(pygame.Vector2(20, 450), (600, 300))
    ground.name = "Ground"

    ground.sprite = pygame.transform.scale(
        pygame.image.load("assets\dirt_1.png"), ground.size)

    wall = Tile(pygame.Vector2(20, 400), (20, 70))

    mb = MovableBox(pygame.Vector2(220, 300), (40, 40), 5, 10)
    en = MovableBox2(pygame.Vector2(300, 300), (40, 60), 5, 10)
    mb.name = "Player"
    en.name = "Enemy"
    en.direction = False
    mb.color = Colors.BLUE
    phb = PlayerHealthBar((25, 15), (300, 15))
    phb.watch_hurtable(mb)
    wall.name = "Wall"
    em.add(ground)
    em.add(wall)
    em.add(mb)
    em.add(en)
    em.add(phb)
    em.focused_entity = mb
    fm = FollowingMouse(pygame.Vector2(50, 50), (10, 10))
    fm.name = "FollowingMouse"
    # em.add(fm)
    game.run()


if __name__ == '__main__':
    main()
