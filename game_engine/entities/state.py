
class Hurtable:
  def __init__(self, health: int, max_health: int):
    self._health = health
    self.max_health = max_health

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