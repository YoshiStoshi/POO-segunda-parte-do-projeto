"""
Módulo: resultado.py
Responsabilidade: Encapsular o resultado de uma partida ou jogada.
"""
from enum import Enum, auto
from typing import Optional


class TipoResultado(Enum):
    VITORIA = auto()
    DERROTA = auto()
    EMPATE = auto()
    EM_ANDAMENTO = auto()


class Resultado:
    """
    Encapsula o resultado de uma partida.

    Atributos:
        _tipo (TipoResultado): Tipo do resultado.
        _vencedor: Jogador vencedor, se houver.
        _mensagem (str): Descrição textual do resultado.
    """

    def __init__(self, tipo: TipoResultado, vencedor=None, mensagem: str = ""):
        self._tipo = tipo
        self._vencedor = vencedor
        self._mensagem = mensagem

    @property
    def tipo(self) -> TipoResultado:
        return self._tipo

    @property
    def vencedor(self):
        return self._vencedor

    @property
    def mensagem(self) -> str:
        return self._mensagem

    @property
    def em_andamento(self) -> bool:
        return self._tipo == TipoResultado.EM_ANDAMENTO

    def __repr__(self) -> str:
        return f"Resultado(tipo={self._tipo.name}, vencedor={self._vencedor})"
