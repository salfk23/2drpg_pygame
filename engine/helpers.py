import abc

from engine.entities.entity import Entity


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)


# ManagerInterface
class IEntityManager(metaclass=abc.ABCMeta):
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
        """Return a list of all entities.

        Returns:
            list[Entity]: A list of all entities.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, entity: Entity):
        """Add an entity to the manager."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, entity: Entity):
        """Remove an entity from the manager."""
        raise NotImplementedError
