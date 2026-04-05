"""
Módulo: jogo_ludo.py
Responsabilidade: Implementação do Ludo simplificado para 2-4 jogadores.

Simplificações em relação ao Ludo clássico:
  - Percurso modelado como trilha linear de passos (não uma grade 2D completa).
  - Cada jogador tem 4 peças, saída com dado = 6.
  - Captura: landing na mesma posição do adversário manda de volta à base.
  - Casas seguras: posição 0 (saída) e múltiplos de 13.
  - Vitória: primeiro a colocar todas as 4 peças no centro (57 passos).
"""
from typing import List, Optional, Dict
from src.core.jogo_tabuleiro import JogoTabuleiro
from src.core.jogador import Jogador
from src.core.tabuleiro import Tabuleiro
from src.core.jogada import Jogada
from src.core.resultado import Resultado, TipoResultado
from .peca_ludo import PecaLudo, EstadoPeca
from .dado import Dado


class JogoLudo(JogoTabuleiro):
    """
    Ludo simplificado para 2 a 4 jogadores.

    Herda de JogoTabuleiro e implementa todos os métodos abstratos.
    Polimorfismo: sobrescreve inicializar_tabuleiro, validar_jogada,
    aplicar_jogada, verificar_fim_de_jogo e exibir_tabuleiro.

    O percurso é modelado como uma trilha de 52 casas compartilhadas + 5 de reta
    final exclusiva por jogador (total 57 passos desde a saída).
    """

    PECAS_POR_JOGADOR = 4
    PASSOS_PERCURSO = 52   # volta completa ao tabuleiro
    PASSOS_TOTAL = 57      # inclui 5 casas da reta final
    CASAS_SEGURAS_RELATIVAS = {0, 13, 26, 39}  # relativas ao offset de saída

    SIMBOLOS = ['A', 'V', 'X', 'Z']  # um por jogador

    def __init__(self, jogadores: List[Jogador]):
        if not (2 <= len(jogadores) <= 4):
            raise ValueError("Ludo requer entre 2 e 4 jogadores.")
        super().__init__(jogadores)
        self._dado = Dado(6)
        self._valor_dado: int = 0
        # Offset de saída de cada jogador no percurso compartilhado (0, 13, 26, 39)
        self._offset: Dict[Jogador, int] = {
            j: i * (self.PASSOS_PERCURSO // len(jogadores))
            for i, j in enumerate(jogadores)
        }
        self._pecas_por_jogador: Dict[Jogador, List[PecaLudo]] = {}

    # ─────────────────────────────────────────────
    # Implementação dos métodos abstratos
    # ─────────────────────────────────────────────

    def inicializar_tabuleiro(self) -> None:
        """Cria um tabuleiro simbólico linear e inicializa as peças na base."""
        # Para Ludo, usamos o tabuleiro como registro auxiliar — o estado
        # real das peças fica em PecaLudo (padrão orientado a objetos).
        self._tabuleiro = Tabuleiro(1, self.PASSOS_PERCURSO, valor_vazio=None)
        self._pecas_por_jogador = {}

        for i, jogador in enumerate(self._jogadores):
            pecas = []
            for j in range(self.PECAS_POR_JOGADOR):
                simbolo = self.SIMBOLOS[i % len(self.SIMBOLOS)]
                peca = PecaLudo(simbolo, jogador, j)
                pecas.append(peca)
            self._pecas_por_jogador[jogador] = pecas

    def validar_jogada(self, jogada: Jogada) -> bool:
        """
        Valida uma jogada de Ludo.

        dados_extras da Jogada deve ser:
            {'acao': 'sair', 'id_peca': N}   → sair da base (requer dado=6)
            {'acao': 'mover', 'id_peca': N}  → mover peça N pelo dado atual
        """
        dados = jogada.dados_extras
        jogador = jogada.jogador

        if not dados or 'acao' not in dados or 'id_peca' not in dados:
            return False

        id_peca = dados['id_peca']
        if not (0 <= id_peca < self.PECAS_POR_JOGADOR):
            return False

        peca = self._pecas_por_jogador[jogador][id_peca]
        acao = dados['acao']

        if acao == 'sair':
            return peca.na_base and self._valor_dado == 6

        if acao == 'mover':
            if not peca.no_percurso:
                return False
            # Não pode ultrapassar o centro
            return peca.passos + self._valor_dado <= self.PASSOS_TOTAL

        return False

    def aplicar_jogada(self, jogada: Jogada) -> None:
        """Move a peça conforme a jogada, realiza capturas e verifica chegada."""
        dados = jogada.dados_extras
        jogador = jogada.jogador
        id_peca = dados['id_peca']
        acao = dados['acao']

        peca = self._pecas_por_jogador[jogador][id_peca]

        if acao == 'sair':
            peca.entrar_no_percurso()
        elif acao == 'mover':
            peca.avancar(self._valor_dado)
            if peca.chegou:
                return  # Chegou ao centro, sem captura possível

            # Verifica captura
            pos_absoluta = self._posicao_absoluta(peca, jogador)
            if not self._e_casa_segura(peca.passos):
                self._verificar_captura(jogador, peca, pos_absoluta)

    def verificar_fim_de_jogo(self) -> Resultado:
        """Verifica se algum jogador colocou todas as 4 peças no centro."""
        for jogador in self._jogadores:
            pecas = self._pecas_por_jogador[jogador]
            if all(p.chegou for p in pecas):
                return Resultado(
                    TipoResultado.VITORIA, jogador,
                    f"🏆 {jogador.nome} venceu o Ludo!"
                )
        return Resultado(TipoResultado.EM_ANDAMENTO)

    def exibir_tabuleiro(self) -> None:
        """Exibe o estado das peças de cada jogador."""
        print("\n" + "=" * 50)
        print(f"🎲 Turno {self._turno.numero_turno} — {self._turno.jogador_atual.nome}")
        if self._valor_dado:
            print(f"   Dado: {self._valor_dado}")
        print("=" * 50)

        for jogador in self._jogadores:
            pecas = self._pecas_por_jogador[jogador]
            print(f"\n  {jogador.nome} ({self.SIMBOLOS[self._jogadores.index(jogador)]}):")
            for peca in pecas:
                if peca.na_base:
                    status = "🏠 Na base"
                elif peca.chegou:
                    status = "🏆 Chegou!"
                else:
                    status = f"🏃 Passos: {peca.passos}/{self.PASSOS_TOTAL}"
                print(f"    Peça {peca.id_peca}: {status}")
        print()

    # ─────────────────────────────────────────────
    # Métodos específicos do Ludo
    # ─────────────────────────────────────────────

    def rolar_dado(self) -> int:
        """Rola o dado e armazena o valor para a jogada atual."""
        self._valor_dado = self._dado.rolar()
        return self._valor_dado

    def rolar_dado_fixo(self, valor: int) -> int:
        """Define o dado manualmente (para testes)."""
        self._valor_dado = self._dado.rolar_fixo(valor)
        return self._valor_dado

    @property
    def valor_dado(self) -> int:
        return self._valor_dado

    def pecas_do_jogador(self, jogador: Jogador) -> List[PecaLudo]:
        return list(self._pecas_por_jogador[jogador])

    def jogadas_possiveis(self, jogador: Jogador) -> List[dict]:
        """Lista todas as ações possíveis para o jogador atual com o dado rolado."""
        possiveis = []
        pecas = self._pecas_por_jogador[jogador]

        for peca in pecas:
            if peca.na_base and self._valor_dado == 6:
                possiveis.append({'acao': 'sair', 'id_peca': peca.id_peca})
            elif peca.no_percurso and peca.passos + self._valor_dado <= self.PASSOS_TOTAL:
                possiveis.append({'acao': 'mover', 'id_peca': peca.id_peca})

        return possiveis

    # ─────────────────────────────────────────────
    # Auxiliares privados
    # ─────────────────────────────────────────────

    def _posicao_absoluta(self, peca: PecaLudo, dono: Jogador) -> int:
        """Converte passos relativos em posição absoluta no percurso compartilhado."""
        return (self._offset[dono] + peca.passos) % self.PASSOS_PERCURSO

    def _e_casa_segura(self, passos_relativos: int) -> bool:
        """Verifica se a posição relativa é uma casa segura."""
        return passos_relativos in self.CASAS_SEGURAS_RELATIVAS

    def _verificar_captura(self, atacante: Jogador, peca_atacante: PecaLudo,
                            pos_abs: int) -> None:
        """Verifica se a peça aterrisou sobre uma peça adversária e a captura."""
        for outro_jogador in self._jogadores:
            if outro_jogador == atacante:
                continue
            for peca_adv in self._pecas_por_jogador[outro_jogador]:
                if not peca_adv.no_percurso:
                    continue
                pos_adv = self._posicao_absoluta(peca_adv, outro_jogador)
                if pos_abs == pos_adv:
                    # Captura!
                    peca_adv.voltar_para_base()
