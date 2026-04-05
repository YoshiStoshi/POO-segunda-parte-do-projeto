"""
Testes para o jogo de Ludo simplificado.
Valida: saída da base, movimentação, captura, chegada e vitória.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.core.jogador import Jogador
from src.core.jogada import Jogada
from src.core.resultado import TipoResultado
from src.jogos.ludo.jogo_ludo import JogoLudo
from src.jogos.ludo.peca_ludo import EstadoPeca


@pytest.fixture
def jogo():
    j1 = Jogador("Alice", 0)
    j2 = Jogador("Bob", 1)
    g = JogoLudo([j1, j2])
    g.iniciar_partida()
    return g


@pytest.fixture
def jogadores(jogo):
    return jogo.jogadores


class TestInicializacaoLudo:
    def test_pecas_criadas(self, jogo):
        j1, j2 = jogo.jogadores
        assert len(jogo.pecas_do_jogador(j1)) == 4
        assert len(jogo.pecas_do_jogador(j2)) == 4

    def test_todas_pecas_na_base(self, jogo):
        for j in jogo.jogadores:
            for p in jogo.pecas_do_jogador(j):
                assert p.na_base is True

    def test_numero_jogadores_invalido(self):
        with pytest.raises(ValueError):
            JogoLudo([Jogador("X", 0)])

    def test_turno_inicial(self, jogo):
        assert jogo.turno.jogador_atual == jogo.jogadores[0]


class TestSaidaDaBaseLudo:
    def test_sair_com_dado_6(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(6)
        jogada = Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0})
        aceita = jogo.realizar_jogada(jogada)
        assert aceita is True
        peca = jogo.pecas_do_jogador(j1)[0]
        assert peca.no_percurso is True

    def test_nao_sair_sem_dado_6(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(5)
        jogada = Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0})
        assert jogo.validar_jogada(jogada) is False

    def test_nao_sair_com_dado_1(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(1)
        jogada = Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0})
        assert jogo.validar_jogada(jogada) is False

    def test_nao_e_turno_invalido(self, jogo):
        j2 = jogo.jogadores[1]  # Turno é de J1
        jogo.rolar_dado_fixo(6)
        jogada = Jogada(j2, dados_extras={'acao': 'sair', 'id_peca': 0})
        with pytest.raises(PermissionError):
            jogo.realizar_jogada(jogada)


class TestMovimentoLudo:
    def _colocar_peca_no_percurso(self, jogo, jogador, id_peca=0):
        """Coloca uma peça no percurso via dado 6."""
        jogo.rolar_dado_fixo(6)
        jogada = Jogada(jogador, dados_extras={'acao': 'sair', 'id_peca': id_peca})
        jogo.realizar_jogada(jogada)
        # Avança o turno de volta para J1 se necessário
        while jogo.turno.jogador_atual != jogador:
            jogo.turno.avancar()

    def test_mover_peca_no_percurso(self, jogo):
        j1 = jogo.jogadores[0]
        self._colocar_peca_no_percurso(jogo, j1)
        jogo.rolar_dado_fixo(3)
        jogada = Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0})
        aceita = jogo.realizar_jogada(jogada)
        assert aceita is True
        peca = jogo.pecas_do_jogador(j1)[0]
        assert peca.passos == 3

    def test_nao_pode_mover_peca_na_base(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(3)
        jogada = Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0})
        assert jogo.validar_jogada(jogada) is False

    def test_passos_acumulam(self, jogo):
        j1, j2 = jogo.jogadores

        # Coloca J1 no percurso
        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0}))

        # J2 passa a vez (sem peça para mover)
        jogo.turno.avancar()

        # J1 avança 4
        jogo.rolar_dado_fixo(4)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0}))

        # J2 passa a vez
        jogo.turno.avancar()

        # J1 avança mais 2
        jogo.rolar_dado_fixo(2)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0}))

        peca = jogo.pecas_do_jogador(j1)[0]
        assert peca.passos == 6

    def test_id_peca_invalido(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(3)
        jogada = Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 99})
        assert jogo.validar_jogada(jogada) is False

    def test_dados_extras_nulos_invalidos(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(3)
        jogada = Jogada(j1, dados_extras=None)
        assert jogo.validar_jogada(jogada) is False


class TestChegadaLudo:
    def test_peca_chega_ao_centro(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0}))
        jogo.turno.avancar()  # simula turno de J2

        peca = jogo.pecas_do_jogador(j1)[0]
        # Leva a peça até 51 passos — com dado=6 chega exatamente em 57
        peca._passos = 51

        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0}))
        assert peca.chegou is True

    def test_nao_pode_ultrapassar_o_centro(self, jogo):
        j1 = jogo.jogadores[0]
        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0}))
        jogo.turno.avancar()

        peca = jogo.pecas_do_jogador(j1)[0]
        peca._passos = 55  # faltam 2 para chegar

        jogo.rolar_dado_fixo(6)  # 55 + 6 > 57 → inválido
        jogada = Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0})
        assert jogo.validar_jogada(jogada) is False


class TestVitoriaLudo:
    def test_vitoria_quando_todas_pecas_chegam(self, jogo):
        j1, j2 = jogo.jogadores

        # Coloca todas as 4 peças de J1 com 56 passos já dados
        for i in range(4):
            jogo.rolar_dado_fixo(6)
            jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': i}))
            jogo.turno.avancar()  # pula J2
            peca = jogo.pecas_do_jogador(j1)[i]
            peca._passos = 51  # faltam 6

        # Move as primeiras 3 até 57
        for i in range(3):
            jogo.rolar_dado_fixo(6)
            jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': i}))
            jogo.turno.avancar()

        # Antes da última: ainda em andamento
        assert jogo.em_andamento is True

        # Última peça chega
        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 3}))

        assert jogo.resultado.tipo == TipoResultado.VITORIA
        assert jogo.resultado.vencedor == j1


class TestCapturLudo:
    def test_captura_manda_peca_de_volta(self, jogo):
        j1, j2 = jogo.jogadores

        # Coloca J1 peça 0 no percurso
        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'sair', 'id_peca': 0}))

        # Coloca J2 peça 0 no percurso
        jogo.rolar_dado_fixo(6)
        jogo.realizar_jogada(Jogada(j2, dados_extras={'acao': 'sair', 'id_peca': 0}))

        # Posiciona J2 peça 0 exatamente onde J1 vai chegar
        peca_j1 = jogo.pecas_do_jogador(j1)[0]
        peca_j2 = jogo.pecas_do_jogador(j2)[0]

        # Offset J1 = 0, offset J2 = 26 (com 2 jogadores: 52//2 = 26)
        # Para captura: pos_abs_j1 == pos_abs_j2
        # pos_abs_j1 = (0 + passos_j1) % 52
        # pos_abs_j2 = (26 + passos_j2) % 52
        # Para serem iguais com passos_j1 = 5: pos_abs = 5
        # 26 + passos_j2 ≡ 5 (mod 52) → passos_j2 = 31
        peca_j1._passos = 4
        peca_j2._passos = 31

        jogo.rolar_dado_fixo(1)  # J1 vai para passos=5, pos_abs=5
        jogo.realizar_jogada(Jogada(j1, dados_extras={'acao': 'mover', 'id_peca': 0}))

        assert peca_j2.na_base is True, "J2 deveria ter voltado para a base"
        assert peca_j1.passos == 5
