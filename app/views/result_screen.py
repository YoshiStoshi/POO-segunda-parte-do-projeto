from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.screen import MDScreen


class ResultScreen(MDScreen):
    """
    Tela de resultado final da partida.
    Exibe o vencedor, a mensagem e opções de nova partida ou voltar ao menu.
    """

    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self._controller = controller
        self._label_resultado = None
        self._label_mensagem = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
        )

        layout.add_widget(Widget(size_hint_y=0.15))

        card = MDCard(
            orientation="vertical",
            padding=dp(32),
            spacing=dp(20),
            size_hint=(0.85, None),
            height=dp(380),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(16)],
        )

        app = MDApp.get_running_app()
        fonte_divertida = getattr(app, "font_cartoon", None)

        icone = MDIcon(
            icon="trophy",
            halign="center",
            font_size="64sp",
            size_hint_y=None,
            height=dp(64),
            theme_text_color="Primary",
        )

        self._label_resultado = MDLabel(
            text="Fim de Jogo!",
            halign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Primary",
            font_name=fonte_divertida,
        )

        self._label_mensagem = MDLabel(
            text="",
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
        )

        sep = Widget(size_hint_y=None, height=dp(16))

        btn_nova = MDRaisedButton(
            text="NOVA PARTIDA",
            size_hint=(1, None),
            height=dp(52),
            font_size="16sp",
            on_release=self._nova_partida,
        )

        btn_menu = MDFlatButton(
            text="MENU PRINCIPAL",
            size_hint=(1, None),
            height=dp(44),
            on_release=self._ir_menu,
        )

        card.add_widget(icone)
        card.add_widget(self._label_resultado)
        card.add_widget(self._label_mensagem)
        card.add_widget(sep)
        card.add_widget(btn_nova)
        card.add_widget(btn_menu)

        layout.add_widget(card)
        layout.add_widget(Widget(size_hint_y=0.15))

        self.add_widget(layout)

    def mostrar_resultado(self, vencedor, mensagem: str) -> None:
        """Atualiza a tela com os dados do resultado da partida."""
        if vencedor:
            self._label_resultado.text = f"{vencedor.nome} venceu!"
        else:
            self._label_resultado.text = "Empate!"
        self._label_mensagem.text = mensagem

    def _nova_partida(self, *args) -> None:
        self._controller.reiniciar_partida()
        self.manager.current = "board"

    def _ir_menu(self, *args) -> None:
        self.manager.current = "menu"
