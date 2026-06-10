"""
Módulo: game_controller.py
Responsabilidade: Intermediar comunicação entre a interface (View) e a lógica do jogo (Model).
Padrão MVC — Controller.
"""
from typing import Optional, Callable, List, Tuple
from src.core.jogador import Jogador
from src.core.jogada import Jogada
from src.jogos.damas.jogo_damas import JogoDamas


class GameController:
    """
    Controlador do jogo de Damas para a interface KivyMD.

    Atua como intermediário entre as telas (View) e o modelo do jogo (Model).
    Nunca expõe atributos internos do modelo diretamente à View.
    """

    def __init__(self):
        self._jogo: Optional[JogoDamas] = None
        self._jogadores: List[Jogador] = []
        self._peca_selecionada: Optional[Tuple[int, int]] = None

        # Callbacks registrados pelas Views
        self.on_board_update: Optional[Callable] = None
        self.on_game_over: Optional[Callable] = None
        self.on_invalid_move: Optional[Callable] = None
        self.on_piece_selected: Optional[Callable] = None

    # ─────────────────────────────────────────────
    # Configuração e início de partida
    # ─────────────────────────────────────────────

    def iniciar_partida(self, nomes: List[str]) -> None:
        """Cria jogadores, instancia o jogo e inicia a partida."""
        self._jogadores = [Jogador(nome, i) for i, nome in enumerate(nomes)]
        self._jogo = JogoDamas(self._jogadores)
        self._jogo.iniciar_partida()
        self._peca_selecionada = None
        self._notificar_tabuleiro()

    def reiniciar_partida(self) -> None:
        """Reinicia com os mesmos jogadores."""
        if self._jogo:
            self._jogo.iniciar_partida()
            self._peca_selecionada = None
            self._notificar_tabuleiro()

    # ─────────────────────────────────────────────
    # Interação com o tabuleiro
    # ─────────────────────────────────────────────

    def selecionar_celula(self, linha: int, coluna: int) -> None:
        """
        Processa o clique em uma célula do tabuleiro.
        Fluxo: seleciona peça → seleciona destino → executa jogada.
        """
        if not self._jogo or not self._jogo.em_andamento:
            return

        jogador_atual = self._jogo.turno.jogador_atual
        peca_na_celula = self._jogo.tabuleiro.obter(linha, coluna)

        captura_em_andamento = getattr(self._jogo, "captura_em_andamento", None)

        if self._peca_selecionada is None:
            if captura_em_andamento is not None:
                self._peca_selecionada = captura_em_andamento.posicao

            # Primeira seleção: deve ser uma peça do jogador atual
            if peca_na_celula and peca_na_celula.dono == jogador_atual:
                if captura_em_andamento is not None and peca_na_celula != captura_em_andamento:
                    return
                self._peca_selecionada = (linha, coluna)
                if self.on_piece_selected:
                    self.on_piece_selected((linha, coluna), self.get_jogadas_validas_da_peca(linha, coluna))
        else:
            origem = self._peca_selecionada

            # Clicou na mesma peça → deseleciona, exceto se há sequência de captura em andamento
            if (linha, coluna) == origem:
                if captura_em_andamento is not None:
                    return
                self._peca_selecionada = None
                if self.on_piece_selected:
                    self.on_piece_selected(None, [])
                return

            # Clicou em outra peça própria → troca seleção, exceto em sequência de captura
            if peca_na_celula and peca_na_celula.dono == jogador_atual:
                if captura_em_andamento is not None:
                    return
                self._peca_selecionada = (linha, coluna)
                if self.on_piece_selected:
                    self.on_piece_selected((linha, coluna), self.get_jogadas_validas_da_peca(linha, coluna))
                return

            # Tenta executar jogada
            jogada = Jogada(jogador_atual, origem=origem, destino=(linha, coluna))
            sucesso = self._jogo.realizar_jogada(jogada)

            if sucesso:
                if getattr(self._jogo, "captura_em_andamento", None) is not None:
                    self._peca_selecionada = jogada.destino
                    if self.on_piece_selected:
                        self.on_piece_selected(
                            self._peca_selecionada,
                            self.get_jogadas_validas_da_peca(*self._peca_selecionada)
                        )
                else:
                    self._peca_selecionada = None
                    if self.on_piece_selected:
                        self.on_piece_selected(None, [])

                self._notificar_tabuleiro()
                if not self._jogo.em_andamento:
                    resultado = self._jogo.resultado
                    if self.on_game_over:
                        self.on_game_over(resultado.vencedor, resultado.mensagem)
            else:
                if self.on_invalid_move:
                    self.on_invalid_move()
                if captura_em_andamento is not None and self._peca_selecionada is not None:
                    if self.on_piece_selected:
                        self.on_piece_selected(
                            self._peca_selecionada,
                            self.get_jogadas_validas_da_peca(*self._peca_selecionada)
                        )
                else:
                    if self.on_piece_selected:
                        self.on_piece_selected(None, [])

    # ─────────────────────────────────────────────
    # Consultas ao estado do jogo (nunca expõe internals)
    # ─────────────────────────────────────────────

    def get_estado_tabuleiro(self) -> List[List]:
        """Retorna grade com símbolo display de cada peça (ou None)."""
        if not self._jogo:
            return []
        tab = self._jogo.tabuleiro
        estado = []
        for l in range(tab.linhas):
            linha = []
            for c in range(tab.colunas):
                peca = tab.obter(l, c)
                if peca is None:
                    linha.append(None)
                else:
                    linha.append({
                        "simbolo": peca.simbolo_display(),
                        "dono_id": peca.dono.id,
                        "e_dama": peca.e_dama,
                    })
            estado.append(linha)
        return estado

    def get_jogador_atual(self) -> Optional[Jogador]:
        """Retorna o jogador cujo turno é agora."""
        if not self._jogo:
            return None
        return self._jogo.turno.jogador_atual

    def get_jogadores(self) -> List[Jogador]:
        return list(self._jogadores)

    def get_peca_selecionada(self) -> Optional[Tuple[int, int]]:
        return self._peca_selecionada

    def get_jogadas_validas_da_peca(self, linha: int, coluna: int) -> List[Tuple]:
        """Retorna destinos válidos para a peça na posição dada."""
        if not self._jogo:
            return []
        todas = self._jogo.listar_jogadas_validas(self._jogo.turno.jogador_atual)
        return [dest for orig, dest in todas if orig == (linha, coluna)]

    def get_contagem_pecas(self) -> dict:
        """Retorna quantas peças ativas cada jogador possui."""
        if not self._jogo:
            return {}
        resultado = {}
        for j in self._jogadores:
            pecas_ativas = [p for p in self._jogo._pecas[j] if p.ativa]
            resultado[j.id] = len(pecas_ativas)
        return resultado

    def jogo_em_andamento(self) -> bool:
        return bool(self._jogo and self._jogo.em_andamento)

    # ─────────────────────────────────────────────
    # Notificação interna
    # ─────────────────────────────────────────────

    def _notificar_tabuleiro(self) -> None:
        if self.on_board_update:
            self.on_board_update(self.get_estado_tabuleiro())
