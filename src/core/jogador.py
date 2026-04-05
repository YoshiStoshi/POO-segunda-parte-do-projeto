"""
Módulo: jogador.py
Responsabilidade: Representar um jogador genérico no sistema de jogos de tabuleiro.
"""


class Jogador:
    """
    Representa um jogador participante de um jogo de tabuleiro.

    Atributos encapsulados:
        _nome (str): Nome do jogador.
        _id (int): Identificador único do jogador na partida.
        _pontuacao (int): Pontuação acumulada (usada em jogos com pontuação).
    """

    def __init__(self, nome: str, id_jogador: int):
        if not nome or not isinstance(nome, str):
            raise ValueError("O nome do jogador deve ser uma string não vazia.")
        if not isinstance(id_jogador, int) or id_jogador < 0:
            raise ValueError("O id do jogador deve ser um inteiro não negativo.")

        self._nome = nome
        self._id = id_jogador
        self._pontuacao = 0

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def id(self) -> int:
        return self._id

    @property
    def pontuacao(self) -> int:
        return self._pontuacao

    def adicionar_pontos(self, pontos: int) -> None:
        """Adiciona pontos à pontuação do jogador."""
        if pontos < 0:
            raise ValueError("Não é possível adicionar pontuação negativa.")
        self._pontuacao += pontos

    def resetar_pontuacao(self) -> None:
        """Zera a pontuação do jogador."""
        self._pontuacao = 0

    def __repr__(self) -> str:
        return f"Jogador(id={self._id}, nome='{self._nome}', pontuacao={self._pontuacao})"

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Jogador):
            return False
        return self._id == outro._id

    def __hash__(self) -> int:
        return hash(self._id)
