from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar


class SettingsScreen(MDScreen):
    """Tela de configurações separada para tema e som."""

    PALETAS = ["DeepOrange", "Blue", "Green", "Purple"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._label_som = None
        self._label_tema = None
        self._btn_paleta = None
        self._build_ui()

    def _build_ui(self) -> None:
        app = MDApp.get_running_app()
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

        titulo = MDLabel(
            text="Configurações",
            halign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Primary",
        )

        subtitulo = MDLabel(
            text="Ajuste som e tema instantaneamente.",
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
        )

        self._label_som = MDLabel(
            text=f"Som: {'Ativado' if app.sounds_enabled else 'Desativado'}",
            halign="left",
            font_style="Subtitle1",
        )

        switch_som = MDSwitch(active=getattr(app, "sounds_enabled", True))
        switch_som.bind(active=self._on_toggle_som)

        self._label_tema = MDLabel(
            text=f"Tema: {app.theme_style}",
            halign="left",
            font_style="Subtitle1",
        )

        switch_tema = MDSwitch(active=(getattr(app, "theme_style", "Dark") == "Dark"))
        switch_tema.bind(active=self._on_toggle_tema)

        self._btn_paleta = MDRaisedButton(
            text=f"Paleta: {getattr(app, 'theme_palette', 'DeepOrange')}",
            size_hint=(1, None),
            height=dp(48),
            on_release=self._alterar_paleta,
        )

        row_som = MDBoxLayout(spacing=dp(12), size_hint_y=None, height=dp(56))
        row_som.add_widget(self._label_som)
        row_som.add_widget(switch_som)

        row_tema = MDBoxLayout(spacing=dp(12), size_hint_y=None, height=dp(56))
        row_tema.add_widget(self._label_tema)
        row_tema.add_widget(switch_tema)

        btn_voltar = MDFlatButton(
            text="VOLTAR",
            size_hint=(1, None),
            height=dp(44),
            on_release=self._voltar,
        )

        card.add_widget(titulo)
        card.add_widget(subtitulo)
        card.add_widget(row_som)
        card.add_widget(row_tema)
        card.add_widget(self._btn_paleta)
        card.add_widget(btn_voltar)

        layout.add_widget(card)
        layout.add_widget(Widget(size_hint_y=0.08))
        self.add_widget(layout)

    def _on_toggle_som(self, switch, ativa: bool) -> None:
        app = MDApp.get_running_app()
        app.sounds_enabled = ativa
        self._label_som.text = f"Som: {'Ativado' if ativa else 'Desativado'}"
        Snackbar(text=f"Som {'ativado' if ativa else 'desativado'}.").open()

    def _on_toggle_tema(self, switch, ativa: bool) -> None:
        app = MDApp.get_running_app()
        estilo = "Dark" if ativa else "Light"
        app.theme_cls.theme_style = estilo
        app.theme_style = estilo
        app.theme_cls.primary_palette = getattr(app, "theme_palette", "DeepOrange")
        self._label_tema.text = f"Tema: {estilo}"
        Snackbar(text=f"Tema alterado para {estilo}.").open()

    def _alterar_paleta(self, *args) -> None:
        app = MDApp.get_running_app()
        paleta_atual = getattr(app, "theme_palette", "DeepOrange")
        indice = self.PALETAS.index(paleta_atual) if paleta_atual in self.PALETAS else 0
        indice = (indice + 1) % len(self.PALETAS)
        nova_paleta = self.PALETAS[indice]
        app.theme_cls.primary_palette = nova_paleta
        app.theme_palette = nova_paleta
        self._btn_paleta.text = f"Paleta: {nova_paleta}"
        Snackbar(text=f"Paleta de cores alterada para {nova_paleta}.").open()

    def _voltar(self, *args) -> None:
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "menu"), 0)
