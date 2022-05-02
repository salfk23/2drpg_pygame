
class Hurtable:
  def __init__(self, health: int, max_health: int):
    self._health = health
    self._max_health = max_health

  @property
  def max_health(self):
    return self._max_health

  @max_health.setter
  def max_health(self, max_health: int):
    if max_health != self.max_health and max_health > -1:
      self._max_health = max_health
      if self.health > max_health:
        self.health = max_health
      self.on_health_change()

  @property
  def health(self):
    return self._health

  @health.setter
  def health(self, health: int):
    if health != self._health:
      self._health = health
      if self._health > self.max_health:
        self._health = self.max_health
      if self._health < 0:
        self._health = 0
      self.on_health_change()
      if self._health == 0:
        self.die()

  def hurt(self, damage: int):
    self.health -= damage

  def on_health_change(self):
    pass

  def on_death(self):
    pass

  def die(self):
    raise NotImplementedError()


class Solid:
  pass