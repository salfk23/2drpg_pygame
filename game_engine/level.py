from typing import Callable
from game_engine.helpers import Singleton


class LevelManagerInstance:
  def __init__(self):
      self.levels = {}
      self._current:str = None

  @property
  def current(self):
      return self._current

  @current.setter
  def current(self, level_name:str):
    if level_name in self.levels:
      self._current = level_name

  @property
  def level(self):
      return self.levels.get(self.current, None)

  def add(self, level_name:str, level:Callable):
      self.levels[level_name] = level







class LevelManager(Singleton[LevelManagerInstance]):
  pass