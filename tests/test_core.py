"""
Testes para as classes do core: Jogador, Peca, Jogada, Tabuleiro, Turno, Resultado.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.core.jogador import Jogador
from src.core.peca import Peca
from src.core.jogada import Jogada
from src.core.tabuleiro import Tabuleiro
from src.core.turno import Turno
from src.core.resultado import Resultado, TipoResultado


# ─── Jogador ───────────────────────────────────────────────────────────────

class TestJogador:
    def test_criacao_valida(self):
        j = Jogador("Ana", 0)
        assert j.nome == "Ana"
        assert j.id == 0
        assert j.pontuacao == 0

    def test_nome_vazio_raise(self):
        with pytest.raises(ValueError):
            Jogador("", 0)

    def test_id_negativo_raise(self):
        with pytest.raises(ValueError):
            Jogador("Bob", -1)

    def test_adicionar_pontos(self):
        j = Jogador("Ana", 0)
        j.adicionar_pontos(10)
        assert j.pontuacao == 10

    def test_adicionar_pontos_negativos_raise(self):
        j = Jogador("Ana", 0)
        with pytest.raises(ValueError):
            j.adicionar_pontos(-5)

    def test_resetar_pontuacao(self):
        j = Jogador("Ana", 0)
        j.adicionar_pontos(50)
        j.resetar_pontuacao()
        assert j.pontuacao == 0

    def test_igualdade_por_id(self):
        j1 = Jogador("Ana", 1)
        j2 = Jogador("Ana", 1)
        j3 = Jogador("Bob", 2)
        assert j1 == j2
        assert j1 != j3


# ─── Peca ──────────────────────────────────────────────────────────────────

class TestPeca:
    def test_criacao(self):
        j = Jogador("Ana", 0)
        p = Peca("X", j)
        assert p.simbolo == "X"
        assert p.dono == j
        assert p.ativa is True
        assert p.posicao is None

    def test_definir_posicao(self):
        p = Peca("X")
        p.posicao = (3, 4)
        assert p.posicao == (3, 4)

    def test_desativar(self):
        p = Peca("X")
        p.posicao = (1, 1)
        p.desativar()
        assert p.ativa is False
        assert p.posicao is None

    def test_reativar(self):
        p = Peca("X")
        p.desativar()
        p.reativar()
        assert p.ativa is True


# ─── Tabuleiro ─────────────────────────────────────────────────────────────

class TestTabuleiro:
    def test_criacao(self):
        t = Tabuleiro(8, 8)
        assert t.linhas == 8
        assert t.colunas == 8

    def test_dimensao_invalida(self):
        with pytest.raises(ValueError):
            Tabuleiro(0, 8)

    def test_posicao_valida(self):
        t = Tabuleiro(3, 3)
        assert t.posicao_valida(0, 0) is True
        assert t.posicao_valida(2, 2) is True
        assert t.posicao_valida(3, 0) is False
        assert t.posicao_valida(-1, 0) is False

    def test_definir_e_obter(self):
        t = Tabuleiro(3, 3)
        t.definir(1, 2, "X")
        assert t.obter(1, 2) == "X"

    def test_limpar(self):
        t = Tabuleiro(3, 3)
        t.definir(0, 0, "X")
        t.limpar(0, 0)
        assert t.esta_vazia(0, 0) is True

    def test_acesso_fora_dos_limites(self):
        t = Tabuleiro(3, 3)
        with pytest.raises(IndexError):
            t.obter(5, 5)

    def test_resetar(self):
        t = Tabuleiro(3, 3)
        t.definir(0, 0, "X")
        t.definir(2, 2, "Y")
        t.resetar()
        assert t.esta_vazia(0, 0) is True
        assert t.esta_vazia(2, 2) is True


# ─── Turno ─────────────────────────────────────────────────────────────────

class TestTurno:
    def setup_method(self):
        self.j1 = Jogador("J1", 0)
        self.j2 = Jogador("J2", 1)
        self.turno = Turno([self.j1, self.j2])

    def test_jogador_inicial(self):
        assert self.turno.jogador_atual == self.j1

    def test_avancar(self):
        self.turno.avancar()
        assert self.turno.jogador_atual == self.j2

    def test_rotacao(self):
        self.turno.avancar()
        self.turno.avancar()
        assert self.turno.jogador_atual == self.j1

    def test_e_turno_de(self):
        assert self.turno.e_turno_de(self.j1) is True
        assert self.turno.e_turno_de(self.j2) is False

    def test_numero_turno_incrementa(self):
        assert self.turno.numero_turno == 1
        self.turno.avancar()
        assert self.turno.numero_turno == 2

    def test_resetar(self):
        self.turno.avancar()
        self.turno.resetar()
        assert self.turno.jogador_atual == self.j1
        assert self.turno.numero_turno == 1

    def test_sem_jogadores_raise(self):
        with pytest.raises(ValueError):
            Turno([])


# ─── Resultado ─────────────────────────────────────────────────────────────

class TestResultado:
    def test_em_andamento(self):
        r = Resultado(TipoResultado.EM_ANDAMENTO)
        assert r.em_andamento is True
        assert r.vencedor is None

    def test_vitoria(self):
        j = Jogador("Ana", 0)
        r = Resultado(TipoResultado.VITORIA, j, "Ana venceu!")
        assert r.em_andamento is False
        assert r.vencedor == j
        assert r.mensagem == "Ana venceu!"

    def test_empate(self):
        r = Resultado(TipoResultado.EMPATE, mensagem="Empate!")
        assert r.tipo == TipoResultado.EMPATE
        assert r.vencedor is None
