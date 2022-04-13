# Interface
import abc

class IMoveable(metaclass=abc.ABCMeta):
  @classmethod
  def __subclasshook__(cls, subclass):
    return (hasattr(subclass, 'move') and
            callable(subclass.move))
