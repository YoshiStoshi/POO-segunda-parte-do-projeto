"""
Módulo: jogo_tabuleiro.py
Responsabilidade: Classe base abstrata para todos os jogos de tabuleiro.
Define o contrato (interface) que todo jogo deve implementar.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .jogador import Jogador
from .tabuleiro import Tabuleiro
from .jogada import Jogada
from .turno import Turno
from .resultado import Resultado, TipoResultado


class JogoTabuleiro(ABC):
    """
    Classe base abstrata para jogos de tabuleiro.

    Define a estrutura e o contrato que todos os jogos concretos devem seguir.
    Implementa o padrão Template Method para o fluxo geral da partida.

    Relações:
        - Agrega Jogador (jogadores existem independentemente)
        - Compõe Tabuleiro (tabuleiro pertence ao jogo)
        - Compõe Turno (gerenciamento de turno pertence ao jogo)
    """

    def __init__(self, jogadores: List[Jogador]):
        if len(jogadores) < 2:
            raise ValueError("Um jogo de tabuleiro requer ao menos 2 jogadores.")
        self._jogadores: List[Jogador] = jogadores
        self._tabuleiro: Optional[Tabuleiro] = None
        self._turno: Optional[Turno] = None
        self._resultado: Resultado = Resultado(TipoResultado.EM_ANDAMENTO)
        self._historico_jogadas: List[Jogada] = []

    @property
    def jogadores(self) -> List[Jogador]:
        return list(self._jogadores)

    @property
    def tabuleiro(self) -> Optional[Tabuleiro]:
        return self._tabuleiro

    @property
    def turno(self) -> Optional[Turno]:
        return self._turno

    @property
    def resultado(self) -> Resultado:
        return self._resultado

    @property
    def historico_jogadas(self) -> List[Jogada]:
        return list(self._historico_jogadas)

    @property
    def em_andamento(self) -> bool:
        return self._resultado.em_andamento

    # ─────────────────────────────────────────────
    # Métodos abstratos — contrato do jogo concreto
    # ─────────────────────────────────────────────

    @abstractmethod
    def inicializar_tabuleiro(self) -> None:
        """Configura o estado inicial do tabuleiro e das peças."""
        pass

    @abstractmethod
    def validar_jogada(self, jogada: Jogada) -> bool:
        """Verifica se uma jogada é permitida pelas regras do jogo."""
        pass

    @abstractmethod
    def aplicar_jogada(self, jogada: Jogada) -> None:
        """Aplica os efeitos de uma jogada ao estado do tabuleiro."""
        pass

    @abstractmethod
    def verificar_fim_de_jogo(self) -> Resultado:
        """Avalia se o jogo terminou e retorna o resultado."""
        pass

    @abstractmethod
    def exibir_tabuleiro(self) -> None:
        """Renderiza o estado atual do tabuleiro (terminal ou UI)."""
        pass

    # ─────────────────────────────────────────────
    # Template Method — fluxo geral da partida
    # ─────────────────────────────────────────────

    def iniciar_partida(self) -> None:
        """Inicia uma nova partida."""
        self._turno = Turno(self._jogadores)
        self._resultado = Resultado(TipoResultado.EM_ANDAMENTO)
        self._historico_jogadas.clear()
        self.inicializar_tabuleiro()

    def realizar_jogada(self, jogada: Jogada) -> bool:
        """
        Tenta realizar uma jogada. Retorna True se a jogada foi aceita.
        Implementa o fluxo: validar → aplicar → verificar fim → avançar turno.
        """
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

        if self.em_andamento:
            self._turno.avancar()

        return True

    def __repr__(self) -> str:
        nomes = ", ".join(j.nome for j in self._jogadores)
        return f"{self.__class__.__name__}(jogadores=[{nomes}])"
