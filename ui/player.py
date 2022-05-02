import pygame
from game_engine.entities.characters import Statusbar
from game_engine.entities.entity import EntityManager, UIEntity
from game_engine.entities.state import Hurtable
from game_engine.entities.ui import UIButton
from game_engine.helpers import Colors, Config, IConfigListener, Singleton, Size2D


class PlayerHUDInstance(UIEntity):
  def __init__(self):
      size = (300, 15)
      super().__init__(pygame.Vector2(25, 15), size)
      self.name = "PLAYER_HEALTHBAR"
      self.watched = Hurtable(10, 100)
      self.healthbar = Statusbar((size[0]-5, size[1]-5))
      self.sprite.fill(Colors.BLACK)
      self.sprite.blit(self.healthbar.sprite, (2, 2))

  def watch_hurtable(self, hurtable: Hurtable):
    self.watched = hurtable
    self.watched.on_health_change = self.on_hud_change
    self.watched.on_death = self.on_death
    self.on_hud_change()

  def on_hud_change(self):
    self.healthbar.current = self.watched.health
    self.healthbar.max = self.watched.max_health
    self.sprite.fill(Colors.BLACK)
    self.sprite.blit(self.healthbar.sprite, (2, 2))
    if self.watched.health <= 0:
      self.watched.on_death()

  def on_death(self):
    GameOver.instance().show = True


@Singleton[PlayerHUDInstance]
class PlayerHUD(PlayerHUDInstance):
  pass



class GameOverInstance(UIEntity, IConfigListener):
  def __init__(self):
      self.config = Config.instance()
      screen_w, screen_h = self.config.screen_dimension
      width = 500
      height = 200
      super().__init__(
        pygame.Vector2((screen_w-width)/2,(screen_h-height)/2),
        (width, height)
      )
      self.config.add_listener(self)
      self.color = Colors.UI

      self.name = "GAME_OVER"


      midtop = pygame.Vector2(self.rect.midtop)
      topright = pygame.Vector2(self.rect.topright)
      # Type text to the center top of surface as Title
      font = pygame.font.SysFont("monospace", 48)
      text = font.render("Game Over", True, Colors.BLACK)
      self.sprite.blit(text, ((width-text.get_width())/2, 10))

      text = font.render("You died!", True, Colors.BLACK)
      self.sprite.blit(text, ((width-text.get_width())/2, 75))


      button_bgcolor = Colors.BUTTON
      button_font_color = Colors.WHITE
      button_sprite, button_size = UIButton.center_button_sprite(
          "X", pygame.font.get_default_font(), 18, button_font_color, button_bgcolor,
          padding=10, button_size=(-1, -1)
      )
      button_exit = UIButton(
          "BUTTON_EXIT", button_sprite,
          topright+pygame.Vector2(-button_size.y, 0), (button_size.y, button_size.y)
      )
      button_exit.on_pressed = self.button_exit_click
      self.linked.append(button_exit)


      button_sprite, button_size = UIButton.center_button_sprite(
          "Retry!", "monospace", 30, button_font_color, button_bgcolor,
          padding=5, button_size=(300, -1))
      button_exit = UIButton(
        "BUTTON_RETRY", button_sprite,
        midtop+pygame.Vector2(-button_size.x/2, 140), button_size)
      button_exit.on_pressed = self.retry_level
      self.linked.append(button_exit)

  def button_exit_click(self):
    em = EntityManager.instance()
    em.hide_all()
    em.clear()
    from ui.main_menu import MainMenu
    MainMenu.instance().show = True
    self.show = False
  def retry_level(self):
    self.show = False
    from ui.level_selector import LevelSelector
    LevelSelector.instance().load_last_level()


  def on_screen_change(self):
      width, height = self.config.screen_dimension
      self.center = (width/2, height/2)

  def config_change_events(self):
      return {
          IConfigListener.SCREEN_DIMENSION: self.on_screen_change
      }
@Singleton[GameOverInstance]
class GameOver(GameOverInstance):
  pass

