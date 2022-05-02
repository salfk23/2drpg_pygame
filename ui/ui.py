
from game_engine.entities.entity import EntityManager, UIEntity
from ui.main_menu import MainMenu
from ui.player import PlayerHealthBar


def register_ui():
    """
    Register the user interface
    """
    uis:list[UIEntity] = [
        MainMenu.instance(),
        PlayerHealthBar.instance()
    ]
    entity_manager = EntityManager.instance()
    for ui in uis:
        entity_manager.add(ui)
    entity_manager.commit()
    entity_manager.hide_all()