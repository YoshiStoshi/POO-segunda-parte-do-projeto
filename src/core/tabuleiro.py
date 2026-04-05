"""
Módulo: tabuleiro.py
Responsabilidade: Representar o tabuleiro genérico de um jogo,
mantendo o estado das casas/posições.
"""
from __future__ import annotations
from typing import Any, Optional, Tuple, List


class Tabuleiro:
    """
    Representa um tabuleiro genérico de grade (linhas x colunas).

    Composição: o tabuleiro contém (compõe) uma grade de células.

    Atributos encapsulados:
        _linhas (int): Número de linhas do tabuleiro.
        _colunas (int): Número de colunas do tabuleiro.
        _grade (list[list]): Grade bidimensional de células.
    """

    def __init__(self, linhas: int, colunas: int, valor_vazio: Any = None):
        if linhas <= 0 or colunas <= 0:
            raise ValueError("Dimensões do tabuleiro devem ser positivas.")
        self._linhas = linhas
        self._colunas = colunas
        self._valor_vazio = valor_vazio
        self._grade: List[List[Any]] = [
            [valor_vazio for _ in range(colunas)] for _ in range(linhas)
        ]

    @property
    def linhas(self) -> int:
        return self._linhas

    @property
    def colunas(self) -> int:
        return self._colunas

    def posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição existe no tabuleiro."""
        return 0 <= linha < self._linhas and 0 <= coluna < self._colunas

    def obter(self, linha: int, coluna: int) -> Any:
        """Retorna o conteúdo de uma posição."""
        if not self.posicao_valida(linha, coluna):
            raise IndexError(f"Posição ({linha}, {coluna}) inválida.")
        return self._grade[linha][coluna]

    def definir(self, linha: int, coluna: int, valor: Any) -> None:
        """Define o conteúdo de uma posição."""
        if not self.posicao_valida(linha, coluna):
            raise IndexError(f"Posição ({linha}, {coluna}) inválida.")
        self._grade[linha][coluna] = valor

    def limpar(self, linha: int, coluna: int) -> None:
        """Remove o conteúdo de uma posição (volta ao valor vazio)."""
        self.definir(linha, coluna, self._valor_vazio)

    def esta_vazia(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está vazia."""
        return self.obter(linha, coluna) == self._valor_vazio

    def resetar(self) -> None:
        """Limpa todo o tabuleiro."""
        for l in range(self._linhas):
            for c in range(self._colunas):
                self._grade[l][c] = self._valor_vazio

    def grade_copia(self) -> List[List[Any]]:
        """Retorna uma cópia rasa da grade."""
        return [linha[:] for linha in self._grade]

    def __repr__(self) -> str:
        return f"Tabuleiro({self._linhas}x{self._colunas})"
