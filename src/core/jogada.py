"""
Módulo: jogada.py
Responsabilidade: Encapsular os dados de uma jogada realizada por um jogador.
"""
from __future__ import annotations
from typing import Optional, Tuple, Any


class Jogada:
    """
    Representa uma jogada genérica em um jogo de tabuleiro.

    Atributos encapsulados:
        _jogador: O jogador que realizou a jogada.
        _origem (tuple | None): Posição de origem da peça (se aplicável).
        _destino (tuple | None): Posição de destino da peça (se aplicável).
        _dados_extras (Any): Informações adicionais específicas do jogo.
    """

    def __init__(self, jogador, origem: Optional[Tuple] = None,
                 destino: Optional[Tuple] = None, dados_extras: Any = None):
        self._jogador = jogador
        self._origem = origem
        self._destino = destino
        self._dados_extras = dados_extras

    @property
    def jogador(self):
        return self._jogador

    @property
    def origem(self) -> Optional[Tuple]:
        return self._origem

    @property
    def destino(self) -> Optional[Tuple]:
        return self._destino

    @property
    def dados_extras(self) -> Any:
        return self._dados_extras

    def __repr__(self) -> str:
        return (f"Jogada(jogador='{self._jogador.nome}', "
                f"origem={self._origem}, destino={self._destino})")
