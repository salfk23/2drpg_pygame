import pygame
from game_engine.entities.dynamic import MouseControllable
from game_engine.entities.entity import UIEntity
from game_engine.helpers import Colors, Size2D

class UIButton(UIEntity, MouseControllable):
  """UIButton, can be clicked"""
  def __init__(self, name:str, sprite:pygame.Surface, position: pygame.Vector2, size: Size2D):
      super().__init__(position, size)
      MouseControllable.__init__(self)
      self.sprite = pygame.transform.scale(sprite, size)
      self.name = name
  @staticmethod
  def center_button_sprite(
    text:str,
    font_type:str="monospace", font_size:int=30,
    color:pygame.Color=Colors.BLACK,
    bg_color:pygame.Color=Colors.BUTTON,
    padding:int=0,
    button_size:Size2D=(-1,-1)
  ):
    """Center text in button sprite

    Args:
        text (str): Text to center
        font_type (str, optional): Font type. Defaults to "monospace".
        font_size (int, optional): Font size. Defaults to 30.
        color (pygame.Color, optional): Text color. Defaults to Colors.BLACK.
        bg_color (pygame.Color, optional): Background color. Defaults to Colors.BUTTON.
        padding (int, optional): Padding between text and button. Defaults to 0.
        button_size (Size2D, optional): Size of button. Defaults to (-1,-1).

    Returns:
        pygame.Surface: Button sprite
        pygame.Vector2: Button size
    """
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