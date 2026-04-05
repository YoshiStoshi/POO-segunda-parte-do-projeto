"""
Interface de terminal para jogar Ludo simplificado.
Uso: python -m src.jogos.ludo.terminal
"""
from src.core.jogador import Jogador
from src.core.jogada import Jogada
from .jogo_ludo import JogoLudo


def jogar_ludo():
    print("\n" + "=" * 50)
    print("         🎲  LUDO SIMPLIFICADO  🎲")
    print("=" * 50)

    num_jogadores = 0
    while num_jogadores not in [2, 3, 4]:
        try:
            num_jogadores = int(input("Número de jogadores (2-4): "))
        except ValueError:
            pass

    jogadores = []
    for i in range(num_jogadores):
        nome = input(f"Nome do Jogador {i + 1}: ").strip() or f"Jogador {i + 1}"
        jogadores.append(Jogador(nome, i))

    jogo = JogoLudo(jogadores)
    jogo.iniciar_partida()

    print("\nRegras: dado=6 para sair da base | chegue ao passo 57 para vencer")
    print("Captura: caia sobre peça adversária para mandá-la de volta à base")
    print("=" * 50)

    while jogo.em_andamento:
        jogo.exibir_tabuleiro()
        jogador_atual = jogo.turno.jogador_atual

        input(f"[{jogador_atual.nome}] Pressione ENTER para rolar o dado...")
        valor = jogo.rolar_dado()
        print(f"  🎲 Dado: {valor}")

        possiveis = jogo.jogadas_possiveis(jogador_atual)

        if not possiveis:
            print(f"  ⏭  Sem jogadas possíveis. Passando a vez...")
            jogo.turno.avancar()
            # Verifica se o dado foi 6 (ganha outra vez) - não implementado para simplificar
            continue

        # Mostra as opções
        print(f"\n  Escolha uma ação:")
        for i, acao in enumerate(possiveis):
            peca = jogo.pecas_do_jogador(jogador_atual)[acao['id_peca']]
            if acao['acao'] == 'sair':
                desc = f"Peça {acao['id_peca']}: Sair da base"
            else:
                desc = f"Peça {acao['id_peca']}: Avançar {valor} passos ({peca.passos} → {peca.passos + valor})"
            print(f"  [{i}] {desc}")

        # Lê a escolha
        while True:
            try:
                escolha = int(input(f"\n  Escolha (0-{len(possiveis)-1}): "))
                if 0 <= escolha < len(possiveis):
                    break
                print("  ⚠  Opção inválida.")
            except ValueError:
                print("  ⚠  Digite um número.")
            except KeyboardInterrupt:
                print("\nJogo encerrado pelo usuário.")
                return

        acao_escolhida = possiveis[escolha]
        jogada = Jogada(jogador_atual, dados_extras=acao_escolhida)

        try:
            aceita = jogo.realizar_jogada(jogada)
            if not aceita:
                print("  ❌ Jogada inválida (verifique as regras).")
                jogo.turno.avancar()
        except Exception as e:
            print(f"  ⚠  Erro: {e}")
            jogo.turno.avancar()

    jogo.exibir_tabuleiro()
    print("\n" + "=" * 50)
    print(f"  {jogo.resultado.mensagem}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    jogar_ludo()
