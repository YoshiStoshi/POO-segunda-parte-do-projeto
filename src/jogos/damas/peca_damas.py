"""
Módulo: peca_damas.py
Responsabilidade: Representa uma peça de Damas, com suporte a promoção a dama.
"""
from src.core.peca import Peca
from src.core.jogador import Jogador


class PecaDamas(Peca):
    """
    Herda de Peca e adiciona comportamento específico de Damas:
    - Peça simples (move em diagonal para frente)
    - Dama (move em diagonal para qualquer direção)

    Atributos extras:
        _e_dama (bool): True se a peça foi promovida a dama.
    """

    def __init__(self, simbolo: str, dono: Jogador):
        super().__init__(simbolo, dono)
        self._e_dama: bool = False

    @property
    def e_dama(self) -> bool:
        return self._e_dama

    def promover_a_dama(self) -> None:
        """Promove a peça a dama."""
        self._e_dama = True

    def simbolo_display(self) -> str:
        """Retorna o símbolo visual, diferenciando dama de peça normal."""
        return self._simbolo.upper() if self._e_dama else self._simbolo.lower()

    def __repr__(self) -> str:
        tipo = "Dama" if self._e_dama else "Peça"
        return f"PecaDamas({tipo}, dono='{self._dono.nome}', pos={self._posicao})"
