"""
Módulo: turno.py
Responsabilidade: Gerenciar a alternância de turnos entre os jogadores.
"""
from typing import List


class Turno:
    """
    Gerencia a ordem e alternância de turnos numa partida.

    Atributos encapsulados:
        _jogadores (list): Lista de jogadores na ordem de turno.
        _indice_atual (int): Índice do jogador atual.
        _numero_turno (int): Contador de turnos realizados.
    """

    def __init__(self, jogadores: List):
        if not jogadores:
            raise ValueError("Deve haver ao menos um jogador.")
        self._jogadores = list(jogadores)
        self._indice_atual = 0
        self._numero_turno = 1

    @property
    def jogador_atual(self):
        return self._jogadores[self._indice_atual]

    @property
    def numero_turno(self) -> int:
        return self._numero_turno

    @property
    def indice_atual(self) -> int:
        return self._indice_atual

    def avancar(self) -> None:
        """Passa para o próximo jogador."""
        self._indice_atual = (self._indice_atual + 1) % len(self._jogadores)
        self._numero_turno += 1

    def resetar(self) -> None:
        """Volta ao início da ordem de turnos."""
        self._indice_atual = 0
        self._numero_turno = 1

    def e_turno_de(self, jogador) -> bool:
        """Verifica se é o turno de um jogador específico."""
        return self.jogador_atual == jogador

    def __repr__(self) -> str:
        return (f"Turno(numero={self._numero_turno}, "
                f"jogador_atual='{self.jogador_atual.nome}')")
