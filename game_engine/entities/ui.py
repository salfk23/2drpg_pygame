
from turtle import width
import pygame
from game_engine.entities.characters import Statusbar
from game_engine.entities.dynamic import Controllable, JumpableEntity, MouseControllable
from game_engine.entities.entity import UIEntity
from game_engine.entities.state import Hurtable
from game_engine.helpers import Colors, Config, IConfigListener, Size2D


class PlayerHealthBar(UIEntity):
  def __init__(self, position: pygame.Vector2, size: Size2D):
      super().__init__(position, size)
      self.name = "PLAYER_HEALTHBAR"
      self.watched = Hurtable(10, 100)
      self.healthbar = Statusbar((size[0]-5, size[1]-5))
      self.sprite.fill(Colors.BLACK)
      self.sprite.blit(self.healthbar.sprite, (2, 2))

  def watch_hurtable(self, hurtable: Hurtable):
    self.watched = hurtable


  def update(self):
    self.healthbar.current = self.watched.health
    self.healthbar.max = self.watched.max_health
    self.sprite.fill(Colors.BLACK)
    self.sprite.blit(self.healthbar.sprite, (2, 2))

class UIButton(UIEntity, MouseControllable):
  def __init__(self, name:str, sprite:pygame.Surface, position: pygame.Vector2, size: Size2D):
      super().__init__(position, size)
      MouseControllable.__init__(self)
      self.sprite = pygame.transform.scale(sprite, size)
      self.name = name
      random_sprite = pygame.Surface((10, 10))
      random_sprite.fill(Colors.RED)
      center = (self.rect.centerx, self.rect.centery)
      rect = random_sprite.get_rect(center=center)
      # # Get center of sprite
      childUIEntity = UIEntity(pygame.Vector2(rect.topleft), (10, 10))
      childUIEntity.name = "CHILD"
      childUIEntity.sprite = random_sprite
      self.linked.append(childUIEntity)
class MainMenu(UIEntity, IConfigListener):
  def __init__(self):
      self.config = Config.instance()
      screen_w, screen_h = self.config.screen_dimension
      width = 500
      height = 400
      super().__init__(pygame.Vector2((screen_w-width)/2, (screen_h-height)/2), (width, height))

      self.color = Colors.YELLOW
      self.config.add_listener(self)

      midtop = pygame.Vector2(self.rect.midtop)

      # Type text to the center top of surface as Title
      font = pygame.font.SysFont("monospace",48)
      text = font.render("-------------", True, Colors.BLACK)
      self.sprite.blit(text, ((width-text.get_width())/2,10))


      font = pygame.font.SysFont("monospace",30)
      text = font.render("Play Game", True, Colors.BLACK)

      def center_button_sprite(
        text:str,
        font_type:str="monospace", font_size:int=30,
        color:pygame.Color=Colors.BLACK,
        bg_color:pygame.Color=Colors.YELLOW,
        idstr:str=None,
        padding:int=0,
        button_size:Size2D=(-1,-1)
      ):
        text_surface = pygame.font.SysFont(
          font_type, font_size
          ).render(text, True, color)
        text_width, text_height = text_surface.get_size()
        button_width, button_height = button_size

        if button_height == -1:
          button_height = text_height + padding*2
        if button_width == -1:
          button_width = text_width + padding*2

        text_pos = (
          (button_width-text_width)/2,
          (button_height-text_height)/2
        )

        bg_surface = pygame.Surface((button_width, button_height))
        bg_surface.fill(bg_color)
        bg_surface.blit(text_surface, text_pos)

        return bg_surface, pygame.Vector2(bg_surface.get_size())



      button_sprite, button_size = center_button_sprite("Something", "monospace", 30, Colors.BLACK, Colors.PURPLE, padding=5)


      button_1 = UIButton("BUTTON_1", button_sprite, midtop+pygame.Vector2(-button_size.x/2, 150), button_size)
      button_1.on_pressed = self.button_1_click
      self.linked.append(button_1)

      button_sprite, button_size = center_button_sprite("Something", "monospace", 30, Colors.BLACK, Colors.PURPLE, padding=5, button_size=(300, -1))

      button_2 = UIButton("BUTTON_2", button_sprite, midtop+pygame.Vector2(-button_size.x/2, 225), button_size)
      button_2.on_pressed = self.button_2_click
      self.linked.append(button_2)

  def button_1_click(self):
      print("Button 1 clicked")
  def button_2_click(self):
      print("Button 2 clicked")

  def update(self):
      pass






  def on_screen_change(self):
      width, height = self.config.screen_dimension
      self.center = (width/2, height/2)

  def config_change_events(self):
      return {
          IConfigListener.SCREEN_DIMENSION:self.on_screen_change
      }
