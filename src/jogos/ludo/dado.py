"""
Módulo: dado.py
Responsabilidade: Simular um dado de N faces.
"""
import random


class Dado:
    """
    Representa um dado de N faces.

    Atributos encapsulados:
        _faces (int): Número de faces do dado.
        _ultimo_resultado (int | None): Último valor lançado.
    """

    def __init__(self, faces: int = 6):
        if faces < 2:
            raise ValueError("Um dado deve ter ao menos 2 faces.")
        self._faces = faces
        self._ultimo_resultado: int | None = None

    @property
    def faces(self) -> int:
        return self._faces

    @property
    def ultimo_resultado(self) -> int | None:
        return self._ultimo_resultado

    def rolar(self) -> int:
        """Rola o dado e retorna o resultado."""
        self._ultimo_resultado = random.randint(1, self._faces)
        return self._ultimo_resultado

    def rolar_fixo(self, valor: int) -> int:
        """Define resultado manualmente (útil para testes)."""
        if not (1 <= valor <= self._faces):
            raise ValueError(f"Valor {valor} fora do intervalo [1, {self._faces}].")
        self._ultimo_resultado = valor
        return self._ultimo_resultado

    def __repr__(self) -> str:
        return f"Dado(faces={self._faces}, ultimo={self._ultimo_resultado})"
