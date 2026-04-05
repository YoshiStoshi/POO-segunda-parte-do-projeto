"""
Testes para o jogo de Damas.
Valida regras, movimentos, capturas, promoção e condições de vitória.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.core.jogador import Jogador
from src.core.jogada import Jogada
from src.core.resultado import TipoResultado
from src.jogos.damas.jogo_damas import JogoDamas
from src.jogos.damas.peca_damas import PecaDamas


@pytest.fixture
def jogo():
    j1 = Jogador("Brancas", 0)
    j2 = Jogador("Pretas", 1)
    g = JogoDamas([j1, j2])
    g.iniciar_partida()
    return g


@pytest.fixture
def jogadores(jogo):
    return jogo.jogadores


class TestInicializacaoDamas:
    def test_tabuleiro_criado(self, jogo):
        assert jogo.tabuleiro is not None
        assert jogo.tabuleiro.linhas == 8
        assert jogo.tabuleiro.colunas == 8

    def test_numero_pecas_iniciais(self, jogo):
        j1, j2 = jogo.jogadores
        # Cada jogador começa com 12 peças nas casas escuras (3 fileiras x 4 peças)
        pecas_j1 = [p for p in jogo._pecas[j1] if p.ativa]
        pecas_j2 = [p for p in jogo._pecas[j2] if p.ativa]
        assert len(pecas_j1) == 12
        assert len(pecas_j2) == 12

    def test_casas_escuras_ocupadas(self, jogo):
        t = jogo.tabuleiro
        # Linhas 0-2: pretas
        for l in range(0, 3):
            for c in range(8):
                if (l + c) % 2 == 1:
                    assert t.obter(l, c) is not None, f"Deveria haver peça em ({l},{c})"
                else:
                    assert t.obter(l, c) is None
        # Linhas 5-7: brancas
        for l in range(5, 8):
            for c in range(8):
                if (l + c) % 2 == 1:
                    assert t.obter(l, c) is not None

    def test_turno_inicial_brancas(self, jogo):
        j1 = jogo.jogadores[0]
        assert jogo.turno.jogador_atual == j1

    def test_jogo_em_andamento(self, jogo):
        assert jogo.em_andamento is True


class TestMovimentoSimplesDamas:
    def test_movimento_valido_brancas(self, jogo):
        j1 = jogo.jogadores[0]
        # Branca em (5,0) [casa escura: (5+0)%2=1] pode ir para (4,1)
        jogada = Jogada(j1, origem=(5, 0), destino=(4, 1))
        assert jogo.validar_jogada(jogada) is True

    def test_movimento_para_tras_invalido(self, jogo):
        j1 = jogo.jogadores[0]
        # Brancas avançam subindo (direção -1); mover para linha 6 é inválido
        jogada = Jogada(j1, origem=(5, 0), destino=(6, 1))
        assert jogo.validar_jogada(jogada) is False

    def test_movimento_casa_clara_invalido(self, jogo):
        j1 = jogo.jogadores[0]
        # Casa clara: (4, 0) — (4+0)%2 = 0 → inválida
        jogada = Jogada(j1, origem=(5, 0), destino=(4, 0))
        assert jogo.validar_jogada(jogada) is False

    def test_nao_e_turno_do_jogador(self, jogo):
        j2 = jogo.jogadores[1]  # É o turno do J1
        jogada = Jogada(j2, origem=(2, 1), destino=(3, 2))
        with pytest.raises(PermissionError):
            jogo.realizar_jogada(jogada)

    def test_movimento_aceito_e_atualiza_turno(self, jogo):
        j1, j2 = jogo.jogadores
        jogada = Jogada(j1, origem=(5, 0), destino=(4, 1))
        aceita = jogo.realizar_jogada(jogada)
        assert aceita is True
        assert jogo.turno.jogador_atual == j2

    def test_posicao_atualizada_apos_movimento(self, jogo):
        j1 = jogo.jogadores[0]
        jogada = Jogada(j1, origem=(5, 0), destino=(4, 1))
        jogo.realizar_jogada(jogada)
        assert jogo.tabuleiro.obter(4, 1) is not None
        assert jogo.tabuleiro.esta_vazia(5, 0)

    def test_movimento_com_peca_do_adversario_invalido(self, jogo):
        j1 = jogo.jogadores[0]
        # Tenta mover peça preta (em (1,0)) sendo J1
        jogada = Jogada(j1, origem=(1, 0), destino=(2, 1))
        assert jogo.validar_jogada(jogada) is False

    def test_jogada_fora_do_tabuleiro_invalida(self, jogo):
        j1 = jogo.jogadores[0]
        jogada = Jogada(j1, origem=(5, 0), destino=(4, -1))
        assert jogo.validar_jogada(jogada) is False


class TestCapturaDamas:
    def _setup_captura(self, jogo):
        """Prepara cenário de captura: branca em (4,2), preta em (3,3), destino (2,4)."""
        j1, j2 = jogo.jogadores
        t = jogo.tabuleiro

        # Limpa área e posiciona peças manualmente
        t.resetar()
        for pecas in jogo._pecas.values():
            pecas.clear()

        # (4+2)%2=0 → casa clara — vamos usar (4,3) preta, branca em (5,2), destino (3,4)
        # (5+2)%2=1 ✓  (4+3)%2=1 ✓  (3+4)%2=1 ✓
        peca_b = PecaDamas('b', j1)
        peca_b.posicao = (5, 2)
        t.definir(5, 2, peca_b)
        jogo._pecas[j1].append(peca_b)

        peca_p = PecaDamas('p', j2)
        peca_p.posicao = (4, 3)
        t.definir(4, 3, peca_p)
        jogo._pecas[j2].append(peca_p)

        return peca_b, peca_p

    def test_captura_obrigatoria_valida(self, jogo):
        j1 = jogo.jogadores[0]
        peca_b, peca_p = self._setup_captura(jogo)
        # branca em (5,2) captura preta em (4,3) → destino (3,4)
        jogada = Jogada(j1, origem=(5, 2), destino=(3, 4))
        assert jogo.validar_jogada(jogada) is True

    def test_captura_remove_peca_adversaria(self, jogo):
        j1, j2 = jogo.jogadores
        peca_b, peca_p = self._setup_captura(jogo)
        jogada = Jogada(j1, origem=(5, 2), destino=(3, 4))
        jogo.realizar_jogada(jogada)
        assert peca_p.ativa is False
        assert jogo.tabuleiro.esta_vazia(4, 3)

    def test_movimento_simples_proibido_quando_ha_captura(self, jogo):
        j1 = jogo.jogadores[0]
        peca_b, peca_p = self._setup_captura(jogo)
        # Tenta movimento simples em vez de captura obrigatória
        jogada = Jogada(j1, origem=(5, 2), destino=(4, 1))
        assert jogo.validar_jogada(jogada) is False


class TestPromocaoDamas:
    def test_peca_promovida_ao_chegar_na_ultima_fileira(self, jogo):
        j1, j2 = jogo.jogadores
        t = jogo.tabuleiro
        t.resetar()
        for pecas in jogo._pecas.values():
            pecas.clear()

        # Branca na fileira 1 em casa escura (1+0)%2=1 → (1,0), prestes a chegar na 0
        peca_b = PecaDamas('b', j1)
        peca_b.posicao = (1, 0)
        t.definir(1, 0, peca_b)
        jogo._pecas[j1].append(peca_b)

        # Peça preta qualquer em casa escura
        peca_p = PecaDamas('p', j2)
        peca_p.posicao = (7, 6)  # (7+6)%2=1 ✓
        t.definir(7, 6, peca_p)
        jogo._pecas[j2].append(peca_p)

        assert peca_b.e_dama is False
        # move (1,0) → (0,1): (0+1)%2=1 ✓
        jogada = Jogada(j1, origem=(1, 0), destino=(0, 1))
        jogo.realizar_jogada(jogada)
        assert peca_b.e_dama is True


class TestVitoriaDamas:
    def test_vitoria_quando_adversario_sem_pecas(self, jogo):
        j1, j2 = jogo.jogadores
        t = jogo.tabuleiro
        t.resetar()
        for pecas in jogo._pecas.values():
            pecas.clear()

        # branca em (5,2) captura preta em (4,3) → destino (3,4)
        peca_b = PecaDamas('b', j1)
        peca_b.posicao = (5, 2)
        t.definir(5, 2, peca_b)
        jogo._pecas[j1].append(peca_b)

        peca_p = PecaDamas('p', j2)
        peca_p.posicao = (4, 3)
        t.definir(4, 3, peca_p)
        jogo._pecas[j2].append(peca_p)

        jogada = Jogada(j1, origem=(5, 2), destino=(3, 4))
        jogo.realizar_jogada(jogada)

        assert jogo.resultado.tipo == TipoResultado.VITORIA
        assert jogo.resultado.vencedor == j1
        assert jogo.em_andamento is False

    def test_jogo_nao_aceita_jogadas_apos_fim(self, jogo):
        j1, j2 = jogo.jogadores
        t = jogo.tabuleiro
        t.resetar()
        for pecas in jogo._pecas.values():
            pecas.clear()

        peca_b = PecaDamas('b', j1)
        peca_b.posicao = (5, 2)
        t.definir(5, 2, peca_b)
        jogo._pecas[j1].append(peca_b)

        peca_p = PecaDamas('p', j2)
        peca_p.posicao = (4, 3)
        t.definir(4, 3, peca_p)
        jogo._pecas[j2].append(peca_p)

        jogo.realizar_jogada(Jogada(j1, origem=(5, 2), destino=(3, 4)))

        with pytest.raises(RuntimeError):
            jogo.realizar_jogada(Jogada(j2, origem=(3, 4), destino=(4, 3)))
