# Jogos de Tabuleiro — OO com Python

Projeto desenvolvido na disciplina de Programação Orientada a Objetos.  
Implementa uma **arquitetura extensível** para jogos de tabuleiro, com dois jogos funcionais: **Damas** e **Ludo Simplificado**.

Alunos : Rodrigo de Azevedo Junior 2840482421044
Davi Sousa Cirilo 2840482421006

---

## Como executar

```bash
# Menu interativo (escolha o jogo)
python main.py

# Apenas Damas
python -m src.jogos.damas.terminal

# Apenas Ludo
python -m src.jogos.ludo.terminal

# Rodar todos os testes
python -m pytest tests/ -v
```

---

## Estrutura do projeto

```
jogos-tabuleiro/
├── main.py                         ← ponto de entrada (menu)
├── src/
│   ├── core/                       ← arquitetura genérica reutilizável
│   │   ├── jogo_tabuleiro.py       ← classe base abstrata (ABC)
│   │   ├── tabuleiro.py            ← grade genérica NxM
│   │   ├── jogador.py              ← jogador genérico
│   │   ├── peca.py                 ← peça genérica
│   │   ├── jogada.py               ← encapsula uma jogada
│   │   ├── turno.py                ← gerencia alternância de turnos
│   │   └── resultado.py            ← resultado de partida
│   └── jogos/
│       ├── damas/
│       │   ├── jogo_damas.py       ← regras do jogo de Damas
│       │   ├── peca_damas.py       ← peça com promoção a dama
│       │   └── terminal.py         ← interface de terminal para Damas
│       └── ludo/
│           ├── jogo_ludo.py        ← regras do Ludo simplificado
│           ├── peca_ludo.py        ← peça com estado (base/percurso/chegada)
│           ├── dado.py             ← dado de N faces
│           └── terminal.py         ← interface de terminal para Ludo
├── tests/
│   ├── test_core.py                ← testes das classes do core
│   ├── test_damas.py               ← testes do jogo de Damas
│   └── test_ludo.py                ← testes do Ludo
└── docs/
    └── arquitetura.md              ← documentação da arquitetura OO
```

---

## Arquitetura OO

### Classe base abstrata — `JogoTabuleiro`

Define o **contrato** que todo jogo deve implementar, via métodos abstratos:

| Método                    | Responsabilidade                         |
| ------------------------- | ---------------------------------------- |
| `inicializar_tabuleiro()` | Configura estado inicial das peças       |
| `validar_jogada(jogada)`  | Verifica se a jogada respeita as regras  |
| `aplicar_jogada(jogada)`  | Aplica os efeitos da jogada no tabuleiro |
| `verificar_fim_de_jogo()` | Detecta vitória, derrota ou empate       |
| `exibir_tabuleiro()`      | Renderiza o estado atual                 |

O método `realizar_jogada()` implementa o **padrão Template Method**: define o fluxo (validar → aplicar → verificar → avançar turno) e delega cada etapa à subclasse.

### Relações entre objetos

| Relação    | Entre                                               | Tipo       |
| ---------- | --------------------------------------------------- | ---------- |
| Herança    | `JogoDamas`, `JogoLudo` ← `JogoTabuleiro`           | Herança    |
| Herança    | `PecaDamas`, `PecaLudo` ← `Peca`                    | Herança    |
| Composição | `JogoTabuleiro` → `Tabuleiro`, `Turno`, `Resultado` | Composição |
| Agregação  | `JogoTabuleiro` → `Jogador` (lista)                 | Agregação  |
| Composição | `JogoLudo` → `Dado`                                 | Composição |

### Princípios aplicados

- **Abstração**: `JogoTabuleiro` (ABC) e `Peca` definem comportamentos comuns sem implementar regras específicas de nenhum jogo.
- **Herança**: `JogoDamas` e `JogoLudo` herdam de `JogoTabuleiro`; `PecaDamas` e `PecaLudo` herdam de `Peca`.
- **Polimorfismo**: `realizar_jogada()` chama `validar_jogada()` e `aplicar_jogada()` polimorficamente — o comportamento correto é determinado em tempo de execução conforme o jogo instanciado.
- **Encapsulamento**: todos os atributos são `_privados`, expostos apenas via `@property`. Nenhum estado interno é acessível diretamente de fora da classe.
- **Template Method**: o fluxo geral da jogada está definido uma única vez em `JogoTabuleiro.realizar_jogada()`.

---

## Jogos implementados

### Damas (versão brasileira simplificada)

- Tabuleiro 8×8, peças nas casas escuras das três primeiras fileiras de cada lado.
- Movimento diagonal simples para frente (peça normal) ou qualquer diagonal (dama).
- **Captura obrigatória**: se houver captura disponível, o jogador é obrigado a realizá-la.
- **Promoção a dama**: peça que chega à última fileira adversária vira dama.
- **Vitória**: adversário sem peças ou sem movimentos disponíveis.

### Ludo Simplificado (2 a 4 jogadores)

- Cada jogador tem 4 peças; dado de 6 faces.
- Dado = 6 para tirar peça da base.
- **Captura**: cair na mesma posição de uma peça adversária manda-a de volta à base.
- **Casas seguras**: posições 0, 13, 26 e 39 do percurso (relativas à saída).
- **Vitória**: primeiro jogador a colocar todas as 4 peças no centro (57 passos).

---

## Decisões de Projeto

- Uso de classe abstrata JogoTabuleiro para permitir extensibilidade
- Separação entre core e jogos concretos
- Uso de Template Method para fluxo de jogada
- Interface via terminal para simplificação
- Testes unitários com pytest

---

## Limitações

- Interface apenas via terminal
- Ludo simplificado sem regras completas
- Damas sem múltiplas capturas encadeadas
- Sem interface gráfica

## Melhorias Futuras

- Interface gráfica (Tkinter / Pygame)
- Novos jogos (xadrez, dominó)
- Multiplayer online
- IA para jogar contra computador
- Persistência de partidas

---

## Testes

**64 testes** cobrindo:

- Criação e validação de `Jogador`, `Peca`, `Tabuleiro`, `Turno`, `Resultado`
- Inicialização do tabuleiro de Damas e Ludo
- Movimentos válidos e inválidos
- Captura obrigatória (Damas) e captura por colisão (Ludo)
- Promoção a dama
- Controle de turnos e permissões
- Detecção de vitória
- Rejeição de jogadas após fim de jogo

```bash
python -m pytest tests/ -v
# 64 passed in 0.22s
```
