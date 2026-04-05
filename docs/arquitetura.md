# Arquitetura do Projeto — Jogos de Tabuleiro

## Diagrama de Classes (resumo textual)

```
JogoTabuleiro (ABC)
│  + inicializar_tabuleiro()   [abstract]
│  + validar_jogada()          [abstract]
│  + aplicar_jogada()          [abstract]
│  + verificar_fim_de_jogo()   [abstract]
│  + exibir_tabuleiro()        [abstract]
│  + iniciar_partida()         [Template Method]
│  + realizar_jogada()         [Template Method]
│  ─ agrega: Jogador (0..*)
│  ─ compõe: Tabuleiro (1)
│  ─ compõe: Turno (1)
│  ─ compõe: Resultado (1)
│
├─► JogoDamas
│     + listar_jogadas_validas()
│     ─ compõe: PecaDamas (24)
│
└─► JogoLudo
      + rolar_dado()
      + jogadas_possiveis()
      ─ compõe: Dado (1)
      ─ compõe: PecaLudo (4 * nJogadores)

Peca
├─► PecaDamas
│     + e_dama: bool
│     + promover_a_dama()
│
└─► PecaLudo
      + estado: EstadoPeca (NA_BASE | NO_PERCURSO | NA_CHEGADA)
      + passos: int
      + entrar_no_percurso()
      + avancar()
      + voltar_para_base()

Jogada
  + jogador: Jogador
  + origem: tuple | None
  + destino: tuple | None
  + dados_extras: Any

Turno
  + jogador_atual: Jogador
  + avancar()

Resultado
  + tipo: TipoResultado (VITORIA | DERROTA | EMPATE | EM_ANDAMENTO)
  + vencedor: Jogador | None
```

## Padrões OO utilizados

| Princípio       | Onde aparece                                                                 |
|-----------------|------------------------------------------------------------------------------|
| Abstração       | `JogoTabuleiro` (ABC) define contrato sem implementar regras específicas     |
| Herança         | `JogoDamas`, `JogoLudo` ← `JogoTabuleiro`; `PecaDamas`, `PecaLudo` ← `Peca` |
| Polimorfismo    | `realizar_jogada()` chama `validar_jogada()` / `aplicar_jogada()` polimórficos |
| Encapsulamento  | Todos os atributos são `_privados`, expostos via `@property`                 |
| Template Method | `JogoTabuleiro.realizar_jogada()` define o fluxo; subclasses implementam etapas |
| Composição      | `JogoTabuleiro` compõe `Tabuleiro`, `Turno`, `Resultado`                    |
| Agregação       | `JogoTabuleiro` agrega `Jogador` (existem independentemente)                 |

## Como executar

```bash
# Menu interativo
python main.py

# Apenas Damas
python -m src.jogos.damas.terminal

# Apenas Ludo
python -m src.jogos.ludo.terminal

# Testes
python -m pytest tests/ -v
```

## Como adicionar um novo jogo

1. Crie `src/jogos/meujogo/` com `peca_meujogo.py` (herda `Peca`) e `jogo_meujogo.py` (herda `JogoTabuleiro`).
2. Implemente os 5 métodos abstratos: `inicializar_tabuleiro`, `validar_jogada`, `aplicar_jogada`, `verificar_fim_de_jogo`, `exibir_tabuleiro`.
3. Adicione a interface em `terminal.py`.
4. Registre no `main.py`.

Nenhuma classe do `core` precisa ser alterada.
