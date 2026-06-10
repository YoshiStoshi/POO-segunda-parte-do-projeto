"""
Módulo: jogo_damas.py
Responsabilidade: Implementação concreta do jogo de Damas (versão brasileira simplificada).

Regras implementadas:
  - Tabuleiro 8x8, peças nas casas escuras das três primeiras fileiras de cada lado.
  - Movimento diagonal simples para frente (peça normal) ou qualquer direção (dama).
  - Captura obrigatória (salto sobre peça adversária).
  - Promoção a dama ao atingir a última fileira.
  - Vitória: adversário sem peças ou sem jogadas válidas.
"""
from typing import List, Tuple, Optional
from src.core.jogo_tabuleiro import JogoTabuleiro
from src.core.jogador import Jogador
from src.core.tabuleiro import Tabuleiro
from src.core.jogada import Jogada
from src.core.resultado import Resultado, TipoResultado
from .peca_damas import PecaDamas


class JogoDamas(JogoTabuleiro):
    """
    Jogo de Damas brasileiro simplificado.

    Herda de JogoTabuleiro e implementa todos os métodos abstratos.
    Polimorfismo: sobrescreve inicializar_tabuleiro, validar_jogada,
    aplicar_jogada, verificar_fim_de_jogo e exibir_tabuleiro.
    """

    LINHAS = 8
    COLUNAS = 8

    def __init__(self, jogadores: List[Jogador]):
        super().__init__(jogadores)
        # jogador 0 → peças 'b' (brancas), começa de baixo (linhas 5-7)
        # jogador 1 → peças 'p' (pretas), começa de cima (linhas 0-2)
        self._simbolos = {
            self._jogadores[0]: 'b',
            self._jogadores[1]: 'p',
        }
        # Direção de avanço: brancas sobem (linha decresce), pretas descem
        self._direcao_avanco = {
            self._jogadores[0]: -1,
            self._jogadores[1]: +1,
        }
        self._captura_em_andamento = None

    # ─────────────────────────────────────────────
    # Implementação dos métodos abstratos
    # ─────────────────────────────────────────────

    def inicializar_tabuleiro(self) -> None:
        """Posiciona as 12 peças de cada jogador nas casas escuras iniciais."""
        self._tabuleiro = Tabuleiro(self.LINHAS, self.COLUNAS, valor_vazio=None)
        self._pecas: dict = {j: [] for j in self._jogadores}

        # Brancas: linhas 5, 6, 7
        for linha in range(5, 8):
            for col in range(self.COLUNAS):
                if (linha + col) % 2 == 1:
                    peca = PecaDamas(self._simbolos[self._jogadores[0]], self._jogadores[0])
                    peca.posicao = (linha, col)
                    self._tabuleiro.definir(linha, col, peca)
                    self._pecas[self._jogadores[0]].append(peca)

        # Pretas: linhas 0, 1, 2
        for linha in range(0, 3):
            for col in range(self.COLUNAS):
                if (linha + col) % 2 == 1:
                    peca = PecaDamas(self._simbolos[self._jogadores[1]], self._jogadores[1])
                    peca.posicao = (linha, col)
                    self._tabuleiro.definir(linha, col, peca)
                    self._pecas[self._jogadores[1]].append(peca)

    def validar_jogada(self, jogada: Jogada) -> bool:
        """Valida movimento ou captura segundo as regras de Damas."""
        origem = jogada.origem
        destino = jogada.destino
        jogador = jogada.jogador

        if origem is None or destino is None:
            return False

        li, ci = origem
        lf, cf = destino

        # Posições devem estar no tabuleiro
        if not self._tabuleiro.posicao_valida(li, ci):
            return False
        if not self._tabuleiro.posicao_valida(lf, cf):
            return False

        # Deve existir peça na origem pertencente ao jogador
        peca = self._tabuleiro.obter(li, ci)
        if peca is None or peca.dono != jogador:
            return False

        # Destino deve estar vazio
        if not self._tabuleiro.esta_vazia(lf, cf):
            return False

        # Destino deve ser casa escura
        if (lf + cf) % 2 != 1:
            return False

        dl = lf - li
        dc = cf - ci

        # Verifica capturas obrigatórias primeiro
        capturas = self._listar_capturas_do_jogador(jogador)
        if capturas:
            # Se há capturas disponíveis, só aceita jogadas de captura
            return (origem, destino) in [(c[0], c[1]) for c in capturas]

        # Movimento simples (sem captura)
        if abs(dl) == 1 and abs(dc) == 1:
            if peca.e_dama:
                return True  # Dama move em qualquer diagonal
            # Peça normal: só avança
            dir_avanco = self._direcao_avanco[jogador]
            return dl == dir_avanco

        return False

    def aplicar_jogada(self, jogada: Jogada) -> None:
        """Move a peça, realiza captura se necessário e verifica promoção."""
        li, ci = jogada.origem
        lf, cf = jogada.destino

        peca = self._tabuleiro.obter(li, ci)
        dl = lf - li
        dc = cf - ci

        # Move peça
        self._tabuleiro.limpar(li, ci)
        peca.posicao = (lf, cf)
        self._tabuleiro.definir(lf, cf, peca)

        # Captura: pula 2 casas → remove peça do meio
        if abs(dl) == 2:
            lm = li + dl // 2
            cm = ci + dc // 2
            capturada = self._tabuleiro.obter(lm, cm)
            if capturada:
                capturada.desativar()
                self._tabuleiro.limpar(lm, cm)
                self._pecas[capturada.dono].remove(capturada)

        # Promoção a dama
        if not peca.e_dama:
            if peca.dono == self._jogadores[0] and lf == 0:
                peca.promover_a_dama()
            elif peca.dono == self._jogadores[1] and lf == self.LINHAS - 1:
                peca.promover_a_dama()

        # Se houve captura, mantenha o estado de sequência de captura.
        if abs(dl) == 2:
            self._captura_em_andamento = peca
        else:
            self._captura_em_andamento = None

    def _eh_captura(self, origem: Tuple[int, int], destino: Tuple[int, int]) -> bool:
        li, ci = origem
        lf, cf = destino
        return abs(lf - li) == 2 and abs(cf - ci) == 2

    def _capturas_para_peca(self, peca: Optional[PecaDamas]) -> List[Tuple]:
        if peca is None or not peca.ativa:
            return []

        capturas = []
        li, ci = peca.posicao
        for dl, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            lf, cf = li + dl, ci + dc
            lm, cm = li + dl // 2, ci + dc // 2
            if not self._tabuleiro.posicao_valida(lf, cf):
                continue
            if not self._tabuleiro.esta_vazia(lf, cf):
                continue
            meio = self._tabuleiro.obter(lm, cm)
            if meio and meio.dono != peca.dono:
                capturas.append(((li, ci), (lf, cf), (lm, cm)))
        return capturas

    def realizar_jogada(self, jogada: Jogada) -> bool:
        if not self.em_andamento:
            raise RuntimeError("O jogo já terminou.")

        if not self._turno.e_turno_de(jogada.jogador):
            raise PermissionError(
                f"Não é o turno de {jogada.jogador.nome}. "
                f"É o turno de {self._turno.jogador_atual.nome}."
            )

        if not self.validar_jogada(jogada):
            return False

        self.aplicar_jogada(jogada)
        self._historico_jogadas.append(jogada)
        self._resultado = self.verificar_fim_de_jogo()

        if self.em_andamento and self._eh_captura(jogada.origem, jogada.destino):
            peca = self._tabuleiro.obter(*jogada.destino)
            if peca and self._capturas_para_peca(peca):
                self._captura_em_andamento = peca
                return True

        self._captura_em_andamento = None
        if self.em_andamento:
            self._turno.avancar()

        return True

    @property
    def captura_em_andamento(self) -> Optional[PecaDamas]:
        return self._captura_em_andamento

    def verificar_fim_de_jogo(self) -> Resultado:
        """Verifica se algum jogador perdeu todas as peças ou ficou sem movimentos."""
        for jogador in self._jogadores:
            pecas_ativas = [p for p in self._pecas[jogador] if p.ativa]
            if not pecas_ativas:
                adversario = self._outro_jogador(jogador)
                return Resultado(
                    TipoResultado.VITORIA, adversario,
                    f"{adversario.nome} venceu! {jogador.nome} ficou sem peças."
                )

        # Verifica se o jogador atual tem algum movimento válido
        jogador_atual = self._turno.jogador_atual
        if not self._tem_movimentos_validos(jogador_atual):
            adversario = self._outro_jogador(jogador_atual)
            return Resultado(
                TipoResultado.VITORIA, adversario,
                f"{adversario.nome} venceu! {jogador_atual.nome} ficou sem movimentos."
            )

        return Resultado(TipoResultado.EM_ANDAMENTO)

    def exibir_tabuleiro(self) -> None:
        """Imprime o tabuleiro no terminal com coordenadas."""
        print("\n  " + "  ".join(str(c) for c in range(self.COLUNAS)))
        for l in range(self.LINHAS):
            linha_str = f"{l} "
            for c in range(self.COLUNAS):
                peca = self._tabuleiro.obter(l, c)
                if peca is None:
                    casa = "·" if (l + c) % 2 == 0 else "░"
                else:
                    casa = peca.simbolo_display()
                linha_str += f" {casa} "
            print(linha_str)
        print()

    # ─────────────────────────────────────────────
    # Métodos auxiliares (privados)
    # ─────────────────────────────────────────────

    def _outro_jogador(self, jogador: Jogador) -> Jogador:
        return self._jogadores[1] if jogador == self._jogadores[0] else self._jogadores[0]

    def _listar_capturas_do_jogador(self, jogador: Jogador) -> List[Tuple]:
        """Retorna lista de (origem, destino, meio) de todas as capturas disponíveis."""
        capturas = []
        for peca in self._pecas[jogador]:
            if not peca.ativa:
                continue
            li, ci = peca.posicao
            for dl, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                lf, cf = li + dl, ci + dc
                lm, cm = li + dl // 2, ci + dc // 2
                if not self._tabuleiro.posicao_valida(lf, cf):
                    continue
                if not self._tabuleiro.esta_vazia(lf, cf):
                    continue
                meio = self._tabuleiro.obter(lm, cm)
                if meio and meio.dono != jogador:
                    if not peca.e_dama:
                        capturas.append(((li, ci), (lf, cf), (lm, cm)))
                    else:
                        capturas.append(((li, ci), (lf, cf), (lm, cm)))
        return capturas

    def _tem_movimentos_validos(self, jogador: Jogador) -> bool:
        """Verifica se um jogador tem ao menos um movimento válido."""
        # Verifica capturas
        if self._listar_capturas_do_jogador(jogador):
            return True

        dir_avanco = self._direcao_avanco[jogador]
        for peca in self._pecas[jogador]:
            if not peca.ativa:
                continue
            li, ci = peca.posicao
            diags = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if peca.e_dama else [
                (dir_avanco, -1), (dir_avanco, 1)
            ]
            for dl, dc in diags:
                lf, cf = li + dl, ci + dc
                if self._tabuleiro.posicao_valida(lf, cf) and self._tabuleiro.esta_vazia(lf, cf):
                    return True
        return False

    def listar_jogadas_validas(self, jogador: Jogador) -> List[Tuple]:
        """Retorna lista de (origem, destino) de jogadas válidas para um jogador."""
        if self._captura_em_andamento is not None:
            capturas = self._capturas_para_peca(self._captura_em_andamento)
            return [((c[0][0], c[0][1]), (c[1][0], c[1][1])) for c in capturas]

        capturas = self._listar_capturas_do_jogador(jogador)
        if capturas:
            return [(c[0], c[1]) for c in capturas]

        movimentos = []
        dir_avanco = self._direcao_avanco[jogador]
        for peca in self._pecas[jogador]:
            if not peca.ativa:
                continue
            li, ci = peca.posicao
            diags = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if peca.e_dama else [
                (dir_avanco, -1), (dir_avanco, 1)
            ]
            for dl, dc in diags:
                lf, cf = li + dl, ci + dc
                if self._tabuleiro.posicao_valida(lf, cf) and self._tabuleiro.esta_vazia(lf, cf):
                    movimentos.append(((li, ci), (lf, cf)))
        return movimentos
