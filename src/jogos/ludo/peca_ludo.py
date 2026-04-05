"""
Módulo: peca_ludo.py
Responsabilidade: Representa uma peça do Ludo com estado de progresso no percurso.
"""
from src.core.peca import Peca
from src.core.jogador import Jogador


class EstadoPeca:
    """Estados possíveis de uma peça de Ludo."""
    NA_BASE = "NA_BASE"          # Aguardando sair (precisa de 6 para entrar)
    NO_PERCURSO = "NO_PERCURSO"  # Está circulando no tabuleiro
    NA_CHEGADA = "NA_CHEGADA"    # Completou o percurso — chegou ao centro


class PecaLudo(Peca):
    """
    Herda de Peca e adiciona comportamento específico do Ludo:
    - Estado: na base, no percurso, chegou ao centro.
    - Posição no percurso (0 a 56 steps totais no Ludo simplificado).

    Atributos extras:
        _estado (str): Estado atual da peça.
        _passos (int): Quantos passos já percorreu desde a saída (0 = em casa).
        _id_peca (int): Identificador da peça dentro do conjunto do jogador.
    """

    TOTAL_PASSOS = 57  # 52 do percurso externo + 5 da reta final

    def __init__(self, simbolo: str, dono: Jogador, id_peca: int):
        super().__init__(simbolo, dono)
        self._estado: str = EstadoPeca.NA_BASE
        self._passos: int = 0
        self._id_peca: int = id_peca

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def passos(self) -> int:
        return self._passos

    @property
    def id_peca(self) -> int:
        return self._id_peca

    @property
    def na_base(self) -> bool:
        return self._estado == EstadoPeca.NA_BASE

    @property
    def no_percurso(self) -> bool:
        return self._estado == EstadoPeca.NO_PERCURSO

    @property
    def chegou(self) -> bool:
        return self._estado == EstadoPeca.NA_CHEGADA

    def entrar_no_percurso(self) -> None:
        """Sai da base e entra no percurso (requer dado = 6)."""
        if self._estado != EstadoPeca.NA_BASE:
            raise RuntimeError("Peça não está na base.")
        self._estado = EstadoPeca.NO_PERCURSO
        self._passos = 0

    def avancar(self, quantidade: int) -> None:
        """Avança a peça no percurso."""
        if self._estado != EstadoPeca.NO_PERCURSO:
            raise RuntimeError("Peça não está no percurso.")
        novos_passos = self._passos + quantidade
        if novos_passos >= self.TOTAL_PASSOS:
            self._passos = self.TOTAL_PASSOS
            self._estado = EstadoPeca.NA_CHEGADA
        else:
            self._passos = novos_passos

    def voltar_para_base(self) -> None:
        """Envia a peça de volta para a base (foi comida)."""
        self._estado = EstadoPeca.NA_BASE
        self._passos = 0
        self._posicao = None

    def __repr__(self) -> str:
        return (f"PecaLudo(id={self._id_peca}, dono='{self._dono.nome}', "
                f"estado={self._estado}, passos={self._passos})")
