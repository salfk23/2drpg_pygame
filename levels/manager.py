

from game_engine.entities.entity import EntityManager
from levels.level_1 import run as level_1
from levels.level_2 import run as level_2
from levels.level_3 import run as level_3
from levels.level_4 import run as level_4
from levels.level_5 import run as level_5
from levels.level_6 import run as level_6



_levels = {
  "1": level_1,
  "2": level_2,
  "3": level_3,
  "4": level_4,
  "5": level_5,
  "6": level_6,
}

def get_levels():
  return list(_levels.keys())

def load_level(level_id:str):
  em = EntityManager.instance()
  em.clear()
  em.hide_all()
  level = _levels.get(level_id)
  level()