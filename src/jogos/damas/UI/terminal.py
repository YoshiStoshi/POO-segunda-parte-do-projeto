"""
Interface de terminal para jogar Damas.
Uso: python -m src.jogos.damas.terminal
"""
from src.core.jogador import Jogador
from src.core.jogada import Jogada
from ..jogo_damas import JogoDamas


def _parse_posicao(texto: str):
    """Converte '3 4' ou '3,4' para (3, 4)."""
    texto = texto.strip().replace(',', ' ')
    partes = texto.split()
    if len(partes) != 2:
        return None
    try:
        return (int(partes[0]), int(partes[1]))
    except ValueError:
        return None


def jogar_damas():
    print("\n" + "=" * 50)
    print("         ♟  JOGO DE DAMAS  ♟")
    print("=" * 50)

    nome1 = input("Nome do Jogador 1 (Brancas): ").strip() or "Jogador 1"
    nome2 = input("Nome do Jogador 2 (Pretas):  ").strip() or "Jogador 2"

    j1 = Jogador(nome1, 0)
    j2 = Jogador(nome2, 1)
    jogo = JogoDamas([j1, j2])
    jogo.iniciar_partida()

    print("\nLegenda: b/B = Brancas (normal/dama) | p/P = Pretas (normal/dama)")
    print("Coordenadas: linha coluna (ex: 5 1)")
    print("=" * 50)

    while jogo.em_andamento:
        jogo.exibir_tabuleiro()
        jogador_atual = jogo.turno.jogador_atual

        # Mostra jogadas válidas
        validas = jogo.listar_jogadas_validas(jogador_atual)
        if validas:
            print(f"🎯 Turno de {jogador_atual.nome}")
            print("   Jogadas disponíveis:")
            for orig, dest in validas:
                print(f"     {orig} → {dest}")

        # Lê a jogada
        while True:
            try:
                ori_str = input(f"\n[{jogador_atual.nome}] Origem (linha col): ")
                dest_str = input(f"[{jogador_atual.nome}] Destino (linha col): ")
                origem = _parse_posicao(ori_str)
                destino = _parse_posicao(dest_str)

                if origem is None or destino is None:
                    print("⚠  Formato inválido. Use: linha coluna (ex: 5 2)")
                    continue

                jogada = Jogada(jogador_atual, origem=origem, destino=destino)

                try:
                    aceita = jogo.realizar_jogada(jogada)
                except PermissionError as e:
                    print(f"⛔ {e}")
                    continue

                if not aceita:
                    print("❌ Jogada inválida. Tente novamente.")
                else:
                    break
            except KeyboardInterrupt:
                print("\nJogo encerrado pelo usuário.")
                return

    jogo.exibir_tabuleiro()
    print("\n" + "=" * 50)
    print(f"  {jogo.resultado.mensagem}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    jogar_damas()
