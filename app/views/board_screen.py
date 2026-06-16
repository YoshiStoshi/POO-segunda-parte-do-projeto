import math
import random
import struct
import wave

from kivy.core.text import Label as CoreLabel
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from pathlib import Path
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.toolbar import MDTopAppBar
from typing import Optional, List, Tuple


class CelulaWidget(Button):
    """
    Widget de uma célula do tabuleiro de Damas.
    Exibe cor de casa, peça (se houver) e indicadores de seleção/destino válido.
    """

    COR_CASA_CLARA = (0.95, 0.87, 0.70, 1)
    COR_CASA_ESCURA = (0.55, 0.35, 0.15, 1)
    COR_SELECIONADA = (0.2, 0.7, 0.2, 1)
    COR_DESTINO_VALIDO = (0.2, 0.6, 1.0, 0.6)
    COR_PECA_BRANCA = (0.95, 0.95, 0.95, 1)
    COR_PECA_PRETA = (0.1, 0.1, 0.1, 1)
    COR_DAMA_BORDA = (1.0, 0.84, 0.0, 1)

    def __init__(self, linha: int, coluna: int, callback, **kwargs):
        super().__init__(**kwargs)
        self.linha = linha
        self.coluna = coluna
        self._callback = callback
        self._dados_peca = None
        self._selecionada = False
        self._destino_valido = False
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self._redesenhar, size=self._redesenhar)
        self.bind(on_release=self._ao_clicar)

    def atualizar(self, dados_peca, selecionada: bool, destino_valido: bool) -> None:
        self._dados_peca = dados_peca
        self._selecionada = selecionada
        self._destino_valido = destino_valido
        self._redesenhar()

    def _redesenhar(self, *args) -> None:
        self.canvas.before.clear()
        with self.canvas.before:
            # Cor de fundo da casa
            if self._selecionada:
                Color(*self.COR_SELECIONADA)
            elif self._destino_valido:
                cor_base = self.COR_CASA_ESCURA if (self.linha + self.coluna) % 2 == 1 else self.COR_CASA_CLARA
                Color(*cor_base)
            else:
                if (self.linha + self.coluna) % 2 == 0:
                    Color(*self.COR_CASA_CLARA)
                else:
                    Color(*self.COR_CASA_ESCURA)
            Rectangle(pos=self.pos, size=self.size)

            # Indicador de destino válido
            if self._destino_valido and not self._selecionada:
                Color(*self.COR_DESTINO_VALIDO)
                margem = min(self.width, self.height) * 0.3
                Ellipse(
                    pos=(self.x + margem, self.y + margem),
                    size=(self.width - 2 * margem, self.height - 2 * margem)
                )

            # Peça
            if self._dados_peca:
                margem = min(self.width, self.height) * 0.1
                raio = min(self.width, self.height) - 2 * margem

                # Sombra da peça
                Color(0, 0, 0, 0.3)
                Ellipse(
                    pos=(self.x + margem + 2, self.y + margem - 2),
                    size=(raio, raio)
                )

                # Corpo da peça
                if self._dados_peca["dono_id"] == 0:
                    Color(*self.COR_PECA_BRANCA)
                else:
                    Color(*self.COR_PECA_PRETA)
                Ellipse(pos=(self.x + margem, self.y + margem), size=(raio, raio))

                # Borda da peça
                Color(0.5, 0.5, 0.5, 0.8)
                Line(
                    ellipse=(self.x + margem, self.y + margem, raio, raio),
                    width=1.2
                )

                # Coroa para dama
                if self._dados_peca["e_dama"]:
                    Color(*self.COR_DAMA_BORDA)
                    borda = min(self.width, self.height) * 0.06
                    Line(
                        ellipse=(self.x + margem + borda, self.y + margem + borda,
                                 raio - 2 * borda, raio - 2 * borda),
                        width=2.5
                    )

                # Texto da peça para visibilidade em fontes que não suportam emoji
                texto = "D" if self._dados_peca["e_dama"] else "O"
                label = CoreLabel(text=texto, font_size=raio * 0.7, bold=True)
                label.refresh()
                texture = label.texture
                tex_x = self.x + (self.width - texture.width) / 2
                tex_y = self.y + (self.height - texture.height) / 2
                Color(1, 1, 1, 1)
                Rectangle(texture=texture, pos=(tex_x, tex_y), size=texture.size)

    def _ao_clicar(self, *args) -> None:
        self._callback(self.linha, self.coluna)


class BoardScreen(MDScreen):
    """
    Tela principal do tabuleiro de Damas.
    Renderiza o tabuleiro 8x8, painel de status dos jogadores e controles.
    """

    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self._controller = controller
        self._celulas: List[List[Optional[CelulaWidget]]] = []
        self._destinos_validos: List[Tuple[int, int]] = []
        self._label_turno = None
        self._label_pecas_j1 = None
        self._label_pecas_j2 = None
        self._som_movimento = None
        self._som_invalid = None
        self._som_selecao = None
        self._som_start = None
        self._registrar_callbacks()
        self._carregar_efeitos_sonoros()
        self._build_ui()

    def _registrar_callbacks(self) -> None:
        if self._controller:
            self._controller.on_board_update = self._ao_atualizar_tabuleiro
            self._controller.on_game_over = self._ao_fim_de_jogo
            self._controller.on_invalid_move = self._ao_jogada_invalida
            self._controller.on_piece_selected = self._ao_selecionar_peca
            self._controller.on_game_start = self._ao_inicio_de_jogo
            self._controller.on_move = lambda origem, destino: self._tocar_som("move")

    def _carregar_efeitos_sonoros(self) -> None:
        base_dir = Path(__file__).resolve().parents[2]
        som_dir = base_dir / "assets" / "sounds"
        som_dir.mkdir(parents=True, exist_ok=True)

        self._criar_som_padrao(som_dir / "dama_move.wav", "move")
        self._criar_som_padrao(som_dir / "invalid.wav", "invalid")
        # Não gerar nem carregar som de seleção (removido)

        # Carrega som de início caso exista
        self._som_start = SoundLoader.load(str(som_dir / "StartSound.wav"))

        self._som_movimento = SoundLoader.load(str(som_dir / "dama_move.wav"))
        self._som_invalid = SoundLoader.load(str(som_dir / "invalid.wav")) or self._som_movimento
        self._som_selecao = None

    def _criar_som_padrao(self, caminho: Path, tipo: str) -> None:
        if caminho.exists():
            return

        taxa = 44100
        duracao = 0.18 if tipo == "move" else 0.12
        amplitude = 32767
        frames = int(taxa * duracao)

        with wave.open(str(caminho), "w") as arquivo:
            arquivo.setnchannels(1)
            arquivo.setsampwidth(2)
            arquivo.setframerate(taxa)

            for i in range(frames):
                t = i / taxa
                if tipo == "move":
                    # Deslize e pouso de madeira levemente abafado
                    envelope = max(0.0, 1.0 - (t / duracao) ** 2)
                    ruido = (random.random() - 0.5) * 2 * envelope * 0.08
                    thock = 0.0
                    if t > 0.05:
                        thock = 0.28 * math.exp(-120 * (t - 0.05)) * math.sin(2 * math.pi * 200 * (t - 0.05))
                    if t > 0.1:
                        thock += 0.08 * math.exp(-140 * (t - 0.1)) * math.sin(2 * math.pi * 320 * (t - 0.1))
                    valor = int(amplitude * max(-1.0, min(1.0, ruido + thock)))
                elif tipo == "select":
                    envelope = math.exp(-18 * t)
                    valor = int(amplitude * 0.12 * envelope * math.sin(2 * math.pi * 1100 * t))
                else:
                    # Impacto seco em madeira, com ressonância curta
                    envelope = math.exp(-45 * t)
                    golpe = math.sin(2 * math.pi * 700 * t) * (1 if t < 0.03 else 0)
                    rastro = 0.08 * math.exp(-100 * t) * math.sin(2 * math.pi * 260 * t)
                    valor = int(amplitude * (envelope * golpe + rastro))

                arquivo.writeframes(struct.pack("<h", max(-amplitude, min(amplitude, valor))))

    def _build_ui(self) -> None:
        layout_principal = MDBoxLayout(orientation="vertical")

        # Barra superior
        toolbar = MDTopAppBar(
            title="Jogo de Damas",
            left_action_items=[["arrow-left", lambda x: self._voltar_menu()]],
            right_action_items=[["refresh", lambda x: self._reiniciar()]],
        )
        layout_principal.add_widget(toolbar)

        # Conteúdo central
        conteudo = MDBoxLayout(orientation="vertical", padding=dp(8), spacing=dp(8))

        # Label de turno
        self._label_turno = MDLabel(
            text="Vez de: —",
            halign="center",
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(36),
        )
        conteudo.add_widget(self._label_turno)

        # Tabuleiro
        grid = MDGridLayout(
            cols=8,
            size_hint=(None, None),
            pos_hint={"center_x": 0.5},
        )
        self._celulas = []
        for l in range(8):
            linha_celulas = []
            for c in range(8):
                celula = CelulaWidget(l, c, self._ao_clicar_celula)
                grid.add_widget(celula)
                linha_celulas.append(celula)
            self._celulas.append(linha_celulas)

        # Ajuste dinâmico do tamanho do grid
        def _ajustar_grid(dt):
            lado = min(self.width, self.height - dp(200))
            lado = max(lado, dp(200))
            grid.width = lado
            grid.height = lado
            tam_celula = lado / 8
            for l in range(8):
                for c in range(8):
                    self._celulas[l][c].size = (tam_celula, tam_celula)

        Clock.schedule_once(_ajustar_grid, 0.1)
        self.bind(size=lambda *a: Clock.schedule_once(_ajustar_grid, 0))

        conteudo.add_widget(grid)

        # Painel de status dos jogadores
        painel = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(80),
            padding=[dp(4), dp(4)],
        )

        card_j1 = MDCard(
            orientation="vertical",
            padding=dp(8),
            size_hint=(0.5, 1),
            elevation=2,
            radius=[dp(8)],
        )
        self._label_nome_j1 = MDLabel(text="Jogador 1", halign="center", font_style="Subtitle2", bold=True)
        self._label_pecas_j1 = MDLabel(text="Peças: 12", halign="center", font_style="Body2")
        card_j1.add_widget(self._label_nome_j1)
        card_j1.add_widget(self._label_pecas_j1)

        card_j2 = MDCard(
            orientation="vertical",
            padding=dp(8),
            size_hint=(0.5, 1),
            elevation=2,
            radius=[dp(8)],
        )
        self._label_nome_j2 = MDLabel(text="Jogador 2", halign="center", font_style="Subtitle2", bold=True)
        self._label_pecas_j2 = MDLabel(text="Peças: 12", halign="center", font_style="Body2")
        card_j2.add_widget(self._label_nome_j2)
        card_j2.add_widget(self._label_pecas_j2)

        painel.add_widget(card_j1)
        painel.add_widget(card_j2)
        conteudo.add_widget(painel)

        layout_principal.add_widget(conteudo)
        self.add_widget(layout_principal)

    def on_enter(self, *args) -> None:
        """Atualiza a tela ao entrar — garante que estado esteja sincronizado."""
        self._atualizar_tela_completa()

    # ─────────────────────────────────────────────
    # Callbacks do controller
    # ─────────────────────────────────────────────

    def _ao_atualizar_tabuleiro(self, estado) -> None:
        Clock.schedule_once(lambda dt: self._atualizar_tela_completa(), 0)

    def _ao_fim_de_jogo(self, vencedor, mensagem: str) -> None:
        def _abrir(dt):
            self.manager.get_screen("result").mostrar_resultado(vencedor, mensagem)
            self.manager.current = "result"
        Clock.schedule_once(_abrir, 0.3)

    def _ao_jogada_invalida(self) -> None:
        self._tocar_som("invalid")
        Clock.schedule_once(lambda dt: Snackbar(text="Jogada inválida!").open(), 0)

    def _ao_selecionar_peca(self, pos_selecionada, destinos) -> None:
        self._destinos_validos = destinos or []
        Clock.schedule_once(lambda dt: self._redesenhar_tabuleiro(), 0)

    def _ao_inicio_de_jogo(self, *args) -> None:
        self._tocar_som("start")

    # ─────────────────────────────────────────────
    # Interação
    # ─────────────────────────────────────────────

    def _ao_clicar_celula(self, linha: int, coluna: int) -> None:
        self._controller.selecionar_celula(linha, coluna)

    def _voltar_menu(self) -> None:
        self.manager.current = "menu"

    def _reiniciar(self) -> None:
        self._tocar_som("move")
        self._controller.reiniciar_partida()

    def _tocar_som(self, tipo: str) -> None:
        app = MDApp.get_running_app()
        if not getattr(app, "sounds_enabled", False):
            return

        sound = {
            "invalid": self._som_invalid,
            "start": self._som_start,
            "move": self._som_movimento,
        }.get(tipo)

        if not sound:
            return

        sound.stop()
        sound.play()

    # ─────────────────────────────────────────────
    # Renderização
    # ─────────────────────────────────────────────

    def _atualizar_tela_completa(self) -> None:
        self._redesenhar_tabuleiro()
        self._atualizar_painel_status()

    def _redesenhar_tabuleiro(self) -> None:
        if not self._controller.jogo_em_andamento():
            return

        estado = self._controller.get_estado_tabuleiro()
        pos_selecionada = self._controller.get_peca_selecionada()

        for l in range(8):
            for c in range(8):
                peca = estado[l][c] if estado else None
                selecionada = (pos_selecionada == (l, c))
                destino_valido = (l, c) in self._destinos_validos
                self._celulas[l][c].atualizar(peca, selecionada, destino_valido)

    def _atualizar_painel_status(self) -> None:
        jogadores = self._controller.get_jogadores()
        if not jogadores:
            return

        jogador_atual = self._controller.get_jogador_atual()
        contagem = self._controller.get_contagem_pecas()

        # Labels de nomes
        self._label_nome_j1.text = jogadores[0].nome
        self._label_nome_j2.text = jogadores[1].nome

        # Labels de peças
        p1 = contagem.get(0, 12)
        p2 = contagem.get(1, 12)
        self._label_pecas_j1.text = f"Peças: {p1}"
        self._label_pecas_j2.text = f"Peças: {p2}"

        # Label de turno
        if jogador_atual:
            simbolo = "●" if jogador_atual.id == 0 else "●"
            self._label_turno.text = f"Vez de: {jogador_atual.nome} {'(Brancas)' if jogador_atual.id == 0 else '(Pretas)'}"
