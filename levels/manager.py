

from game_engine.entities.entity import EntityManager
from levels.level_1 import level_1


_levels = {
  "1": level_1,
  "2": level_1,
  "3": level_1,
  "4": level_1,
  "5": level_1,
  "6": level_1,
  "7": level_1,
  "8": level_1,
  "9": level_1,
  "10": level_1,
}

def get_levels():
  return list(_levels.keys())

def load_level(level_id:str):
  em = EntityManager.instance()
  em.clear()
  em.hide_all()
  level = _levels.get(level_id)
  level()