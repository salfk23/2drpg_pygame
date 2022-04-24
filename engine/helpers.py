import abc
from typing import Generic, TypeVar


Size2D = tuple[int, int]
"""Screen size tuple
Have 2 ints: width and height
"""

ObjectIdCallable = dict[int, callable]
"""ObjectId Callable
The key is an object's id, and the value is said object's method (as callable)
"""


class Singleton:
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

    def __init__(self, decorated):
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
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)

T = TypeVar('T')

# ManagerInterface
class IManager(Generic[T],metaclass=abc.ABCMeta):
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
