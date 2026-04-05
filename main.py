"""
Ponto de entrada principal do sistema de jogos de tabuleiro.
Uso: python main.py
"""
from src.jogos.damas.UI.terminal import jogar_damas
from src.jogos.ludo.terminal import jogar_ludo


def menu():
    print("\n" + "=" * 50)
    print("    🎲  JOGOS DE TABULEIRO  🎲")
    print("=" * 50)
    print("  [1] Damas")
    print("  [2] Ludo Simplificado")
    print("  [0] Sair")
    print("=" * 50)


def main():
    while True:
        menu()
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            jogar_damas()
        elif opcao == "2":
            jogar_ludo()
        elif opcao == "0":
            print("Até logo!\n")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
