"""
Módulo: peca.py
Responsabilidade: Representar uma peça genérica de jogo de tabuleiro.
"""
from __future__ import annotations
from typing import Optional, Tuple


class Peca:
    """
    Representa uma peça genérica em um jogo de tabuleiro.

    Atributos encapsulados:
        _simbolo (str): Símbolo visual da peça.
        _dono (Jogador | None): Referência ao jogador dono da peça.
        _posicao (tuple | None): Posição atual da peça no tabuleiro.
        _ativa (bool): Indica se a peça está em jogo.
    """

    def __init__(self, simbolo: str, dono=None):
        self._simbolo = simbolo
        self._dono = dono
        self._posicao: Optional[Tuple] = None
        self._ativa: bool = True

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @property
    def dono(self):
        return self._dono

    @property
    def posicao(self) -> Optional[Tuple]:
        return self._posicao

    @posicao.setter
    def posicao(self, nova_posicao: Optional[Tuple]) -> None:
        self._posicao = nova_posicao

    @property
    def ativa(self) -> bool:
        return self._ativa

    def desativar(self) -> None:
        """Remove a peça de jogo (capturada, eliminada, etc.)."""
        self._ativa = False
        self._posicao = None

    def reativar(self) -> None:
        """Reativa a peça."""
        self._ativa = True

    def __repr__(self) -> str:
        dono_nome = self._dono.nome if self._dono else "Nenhum"
        return f"Peca(simbolo='{self._simbolo}', dono='{dono_nome}', posicao={self._posicao})"
