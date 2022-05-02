# Todo: Create inventory system
from game_engine.helpers import Singleton


class InventoryInstance:
  def __init__(self):
      pass


class Inventory(Singleton[InventoryInstance]):
  pass