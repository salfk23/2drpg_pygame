
from game_engine.entities.entity import EntityManager, UIEntity
from ui.main_menu import *
from ui.player import *
from ui.level_selector import *


def register_ui():
    """
    Register the user interface
    """
    uis:list[UIEntity] = [
        MainMenu.instance(),
        HelpMenu.instance(),
        LevelSelector.instance(),
        PlayerHUD.instance(),
        GameOver.instance(),
        GameWin.instance()
    ]
    entity_manager = EntityManager.instance()
    for ui in uis:
        entity_manager.add(ui)
    entity_manager.commit()
    entity_manager.hide_all()