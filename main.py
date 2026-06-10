import os
from pathlib import Path

os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")

from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from app.controllers.game_controller import GameController
from app.views.menu_screen import MenuScreen
from app.views.config_screen import ConfigScreen
from app.views.settings_screen import SettingsScreen
from app.views.board_screen import BoardScreen
from app.views.result_screen import ResultScreen


class DamasApp(MDApp):
    """
    Aplicativo principal do Jogo de Damas com interface KivyMD.

    Configura tema Material Design e gerencia as telas via ScreenManager.
    O GameController é único e compartilhado entre as telas que precisam dele.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sounds_enabled = True
        self.theme_style = "Dark"
        self.theme_palette = "DeepOrange"
        self.font_cartoon = None
        self.font_emoji = None
        self._registrar_fontes()

    def _registrar_fontes(self) -> None:
        """Registra fontes úteis quando disponíveis no Windows."""
        font_path = Path("C:/Windows/Fonts/comic.ttf")
        if font_path.exists():
            LabelBase.register(name="Cartoon", fn_regular=str(font_path))
            self.font_cartoon = "Cartoon"

        emoji_path = Path("C:/Windows/Fonts/seguiemj.ttf")
        if not emoji_path.exists():
            emoji_path = Path("C:/Windows/Fonts/SegoeUIEmoji.ttf")
        if emoji_path.exists():
            LabelBase.register(name="Emoji", fn_regular=str(emoji_path))
            self.font_emoji = "Emoji"

    def build(self):
        # Tema Material Design 3
        self.theme_cls.primary_palette = self.theme_palette
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = self.theme_style
        self.title = "Jogo de Damas — POO"

        # Controller único compartilhado
        controller = GameController()

        # ScreenManager com transição suave
        sm = ScreenManager(transition=SlideTransition(duration=0.18))

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ConfigScreen(name="config", controller=controller))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(BoardScreen(name="board", controller=controller))
        sm.add_widget(ResultScreen(name="result", controller=controller))

        return sm


if __name__ == "__main__":
    DamasApp().run()
