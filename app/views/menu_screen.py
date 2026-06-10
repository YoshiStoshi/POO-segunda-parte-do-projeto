from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.screen import MDScreen


class MenuScreen(MDScreen):
    """
    Tela inicial do jogo.
    Exibe o nome do jogo e botões de navegação.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
        )

        # Espaço superior
        layout.add_widget(Widget(size_hint_y=0.1))

        # Card central com título
        card = MDCard(
            orientation="vertical",
            padding=dp(32),
            spacing=dp(20),
            size_hint=(0.85, None),
            height=dp(420),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(16)],
        )

        app = MDApp.get_running_app()
        fonte_divertida = getattr(app, "font_cartoon", None)
        fonte_emoji = getattr(app, "font_emoji", None)

        icone = MDIcon(
            icon="chess-queen",
            halign="center",
            font_size="72sp",
            theme_text_color="Primary",
            size_hint=(1, None),
            height=dp(80),
            pos_hint={"center_x": 0.5},
        )

        titulo = MDLabel(
            text="DAMAS",
            halign="center",
            font_style="H2",
            bold=True,
            theme_text_color="Primary",
            font_name=fonte_divertida,
        )

        subtitulo = MDLabel(
            text="Jogo de Tabuleiro Clássico",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            font_name=fonte_divertida,
        )

        pecas_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, None),
            height=dp(48),
        )
        pecas = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint=(None, None),
            size=(dp(196), dp(48)),
        )

        cores = [(1, 1, 1, 1), (0, 0, 0, 1), (1, 1, 1, 1), (0, 0, 0, 1), (1, 1, 1, 1), (0, 0, 0, 1)]
        for cor in cores:
            pecas.add_widget(
                MDIcon(
                    icon="chess-pawn",
                    halign="center",
                    font_size="36sp",
                    theme_text_color="Custom",
                    text_color=cor,
                    size_hint=(None, None),
                    size=(dp(40), dp(40)),
                )
            )
        pecas_container.add_widget(pecas)

        separador = Widget(size_hint_y=None, height=dp(8))

        btn_nova_partida = MDRaisedButton(
            text="NOVA PARTIDA",
            size_hint=(1, None),
            height=dp(52),
            font_size="16sp",
            on_release=self._ir_para_config,
        )

        btn_configuracoes = MDRaisedButton(
            text="CONFIGURAÇÕES",
            size_hint=(1, None),
            height=dp(52),
            font_size="16sp",
            on_release=self._ir_para_configuracoes,
        )

        btn_sair = MDFlatButton(
            text="SAIR",
            size_hint=(1, None),
            height=dp(48),
            font_size="14sp",
            on_release=self._sair,
        )

        card.add_widget(icone)
        card.add_widget(titulo)
        card.add_widget(subtitulo)
        card.add_widget(pecas_container)
        card.add_widget(separador)
        card.add_widget(btn_nova_partida)
        card.add_widget(btn_configuracoes)
        card.add_widget(btn_sair)

        layout.add_widget(card)
        layout.add_widget(Widget(size_hint_y=0.1))

        self.add_widget(layout)

    def _ir_para_tela(self, nome: str) -> None:
        self.manager.current = nome

    def _ir_para_config(self, *args) -> None:
        Clock.schedule_once(lambda dt: self._ir_para_tela("config"), 0)

    def _ir_para_configuracoes(self, *args) -> None:
        Clock.schedule_once(lambda dt: self._ir_para_tela("settings"), 0)

    def _sair(self, *args) -> None:
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 0)
