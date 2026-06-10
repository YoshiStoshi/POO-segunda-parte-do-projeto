from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class ConfigScreen(MDScreen):
    """
    Tela de configuração de partida: apenas nomes dos jogadores.
    """

    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self._controller = controller
        self._campo_j1 = None
        self._campo_j2 = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
        )

        layout.add_widget(Widget(size_hint_y=0.08))

        card = MDCard(
            orientation="vertical",
            padding=dp(28),
            spacing=dp(18),
            size_hint=(0.85, None),
            height=dp(380),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(16)],
        )

        app = MDApp.get_running_app()
        fonte_divertida = getattr(app, "font_cartoon", None)

        titulo = MDLabel(
            text="Nomes dos Jogadores",
            halign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Primary",
            font_name=fonte_divertida,
        )

        subtitulo = MDLabel(
            text="Digite os nomes para começar a partida",
            halign="center",
            font_style="Body2",
            theme_text_color="Secondary",
            font_name=fonte_divertida,
        )

        self._campo_j1 = MDTextField(
            hint_text="Nome do Jogador 1 (Brancas ●)",
            text="Jogador 1",
            mode="rectangle",
            size_hint_x=1,
        )

        self._campo_j2 = MDTextField(
            hint_text="Nome do Jogador 2 (Pretas ●)",
            text="Jogador 2",
            mode="rectangle",
            size_hint_x=1,
        )

        btn_jogar = MDRaisedButton(
            text="INICIAR PARTIDA",
            size_hint=(1, None),
            height=dp(52),
            font_size="16sp",
            on_release=self._iniciar_partida,
        )

        btn_voltar = MDFlatButton(
            text="VOLTAR",
            size_hint=(1, None),
            height=dp(44),
            on_release=self._voltar,
        )

        card.add_widget(titulo)
        card.add_widget(subtitulo)
        card.add_widget(self._campo_j1)
        card.add_widget(self._campo_j2)
        card.add_widget(btn_jogar)
        card.add_widget(btn_voltar)

        layout.add_widget(card)
        layout.add_widget(Widget(size_hint_y=0.08))

        self.add_widget(layout)

    def _iniciar_partida(self, *args) -> None:
        nome1 = self._campo_j1.text.strip() or "Jogador 1"
        nome2 = self._campo_j2.text.strip() or "Jogador 2"

        if nome1 == nome2:
            Snackbar(text="Os jogadores precisam ter nomes diferentes.").open()
            return

        self._controller.iniciar_partida([nome1, nome2])
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "board"), 0)

    def _voltar(self, *args) -> None:
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "menu"), 0)
