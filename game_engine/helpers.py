"""Helper module for the game."""
import abc
import random
import pygame

from typing import Generic, TypeVar, Union


Size2D = tuple[int, int]
"""Screen size tuple
Have 2 ints: width and height
"""

ObjectIdCallable = dict[int, callable]
"""ObjectId Callable
The key is an object's id, and the value is said object's method (as callable)
"""

# Enum of directions


class Direction:
    """Direction enum"""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Colors:
    """Colors enum"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)
    BUTTON = (150, 150, 150)
    UI = (222, 222, 222)


T = TypeVar('T')
"""Template type"""


class IManager(Generic[T], metaclass=abc.ABCMeta):
    """ManagerInterface
    This is the interface for all managers.
    """
    @classmethod
    def __subclasshook__(cls, sub):
        return (
            hasattr(sub, 'load_data_source') and callable(sub.load_data_source)
            and hasattr(sub, 'extract_text') and callable(sub.extract_text)
            or NotImplemented)

    @abc.abstractmethod
    def get_all(self):
        """Return a list of all items.

        Returns:
            list[T]: A list of all T items.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, item: T):
        """Add an item to the manager."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, item: T):
        """Remove an entity from the manager."""
        raise NotImplementedError


class Singleton(Generic[T]):
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated: T):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance: T = self._decorated()
            return self._instance

    def __call__(self) -> T:
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


class IConfigListener(metaclass=abc.ABCMeta):
    """ConfigListenerInterface
        Used to listen to config changes (e.g. window size) [intended]
    """
    SCREEN_DIMENSION = 1

    @abc.abstractmethod
    def config_change_events(self):
        """Run this method on config part changed

        Raises:
            NotImplementedError: You didn't implement this
        Returns dict[int, callable]
        """
        raise NotImplementedError


class ConfigInstance:
    """
    Config object
    """

    def __init__(self):
        self._classes: list[IConfigListener] = []
        self._screen_dimension: Size2D = (800, 600)

    def add_listener(self, object: IConfigListener):
        self._classes.append(object)

    def property_changed(self, changed):
        for obj in self._classes:
            fn = obj.config_change_events().get(changed)
            if fn is not None:
                fn()

    @property
    def screen_dimension(self):
        return self._screen_dimension

    @screen_dimension.setter
    def screen_dimension(self, screen_dimension: Size2D):
        self._screen_dimension = screen_dimension
        self.property_changed(IConfigListener.SCREEN_DIMENSION)


@Singleton[ConfigInstance]
class Config(ConfigInstance):
    pass


def tile_texture(texture: Union[pygame.Surface, list[pygame.Surface]], size: Size2D):
    """
    Generate a tile texture from a list of surfaces
    Args:
        texture (Union[pygame.Surface, list[pygame.Surface]]): The texture to tile
        size (Size2D): The size of the tile
    Returns:
        pygame.Surface: The generated tile texture
    """
    result = pygame.Surface(size, pygame.SRCALPHA, depth=32)
    if isinstance(texture, pygame.Surface):
        for x in range(0, size[0], texture.get_width()):
            for y in range(0, size[1], texture.get_height()):
                result.blit(texture, (x, y))
    elif isinstance(texture, list):
        texture_width = texture[0].get_width()
        texture_height = texture[0].get_height()
        for x in range(0, size[0], texture_width):
            for y in range(0, size[1], texture_height):
                result.blit(random.choice(texture), (x, y))
    return result


def gradient_rect(left_colour, right_colour, target_rect: pygame.Rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect>
    Args:
        left_colour (tuple[int, int, int]): The left colour
        right_colour (tuple[int, int, int]): The right colour
        target_rect (pygame.Rect): The rectangle to fill

    Returns:
        pygame.Surface: The generated surface
    """
    colour_rect = pygame.Surface((2, 2))                        # 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour,  (0, 0),(0, 1))  # left line
    pygame.draw.line(colour_rect, right_colour, (1, 0),(1, 1))  # right line
    # stretch!
    return pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
