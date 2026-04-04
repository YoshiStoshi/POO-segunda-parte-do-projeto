[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/V9HS9CV8)
# Desafio OO – Jogos de Tabuleiro

## Visão geral
Este repositório é o **template inicial** da atividade **Jogos de Tabuleiro**, proposta na disciplina de Programação Orientada a Objetos com Python.

O objetivo do desafio é projetar e implementar uma **arquitetura orientada a objetos extensível**, capaz de servir como base para diferentes tipos de jogos de tabuleiro.

O foco principal da atividade **não é apenas fazer um jogo funcionar**, mas sim construir uma solução reutilizável, organizada e de fácil manutenção, que permita adicionar novos jogos com o menor impacto possível no código existente.

---

## Objetivo do projeto
Cada grupo deverá desenvolver, em Python, um conjunto de classes orientadas a objetos para representar os principais elementos de jogos de tabuleiro, como por exemplo:

- jogo;
- tabuleiro;
- jogador;
- peça;
- jogada;
- turno;
- regras.

A arquitetura deve ser planejada para que seja possível implementar diferentes jogos sobre a mesma base, como por exemplo:

- Jogo da Velha;
- Lig-4;
- Damas;
- Xadrez simplificado;
- Trilha;
- Ludo simplificado;
- outros jogos semelhantes.

---

## Desafio
Seu grupo deverá criar uma solução orientada a objetos que atenda aos seguintes princípios:

- **extensibilidade**: a base deve permitir a criação de novos jogos;
- **reuso**: classes e componentes devem poder ser reaproveitados;
- **organização**: código separado em módulos e pastas coerentes;
- **clareza de responsabilidades**: cada classe deve ter uma função bem definida;
- **boa modelagem OO**: uso adequado de abstração, encapsulamento, herança, polimorfismo e relações entre objetos.

Além da arquitetura genérica, o grupo deverá implementar **pelo menos 1 jogo funcional** usando a estrutura criada.

---

## Requisitos obrigatórios

### 1. Estrutura orientada a objetos
A solução deve conter classes bem definidas para os conceitos centrais do domínio.

Conceitos esperados na modelagem:

- `JogoTabuleiro`
- `Tabuleiro`
- `Jogador`
- `Peca`
- `Jogada`
- `Regra` ou mecanismo equivalente de validação

Os nomes podem variar, mas os papéis devem existir claramente no projeto.

### 2. Arquitetura extensível
A solução deve permitir implementar jogos diferentes reaproveitando a base.

Exemplo de ideia:

- uma classe base `JogoTabuleiro`;
- subclasses como `JogoDaVelha`, `Lig4`, `Damas`.

### 3. Uso de abstração
O projeto deve ter ao menos uma classe-base, classe abstrata ou interface conceitual para representar comportamentos comuns.

Exemplos de métodos que podem existir em uma classe base:

- `inicializar_tabuleiro()`
- `validar_jogada()`
- `aplicar_jogada()`
- `verificar_fim_de_jogo()`

### 4. Uso de herança e polimorfismo
A solução deve demonstrar:

- herança entre classes;
- sobrescrita de métodos;
- comportamento polimórfico.

### 5. Encapsulamento
Os atributos das classes devem ser manipulados de forma adequada, evitando exposição desnecessária do estado interno.

### 6. Relações entre objetos
A modelagem deve deixar claro o uso de relações como:

- associação;
- agregação;
- composição;
- herança.

### 7. Pelo menos um jogo funcional
Deve existir ao menos um jogo funcionando com:

- início da partida;
- alternância de turnos;
- validação de jogadas;
- atualização do estado do tabuleiro;
- verificação de vitória, derrota, empate ou fim de jogo.

### 8. Interface mínima
A interação pode ser feita em:

- terminal;
- menu textual;
- interface gráfica simples.

Para esta atividade, uma versão em terminal já é suficiente.

### 9. Testes
O projeto deve conter testes simples para validar partes importantes da lógica.

Exemplos:

- impedir jogadas inválidas;
- impedir jogadas fora do turno;
- verificar se o sistema detecta vitória corretamente.

---

## Restrições

- Não vale fazer um código totalmente específico para apenas um jogo.
- O foco principal da atividade é a **arquitetura reutilizável**.
- Não é obrigatório usar interface gráfica.
- A implementação deve ser feita em **Python**.

---

## Estrutura inicial do repositório
Este template contém apenas a **organização inicial de pastas**. Cabe ao grupo criar os arquivos necessários e implementar a solução.

```text
jogos-de-tabuleiro-template/
├── README.md
├── docs/
├── src/
│   ├── core/
│   └── jogos/
└── tests/
```

### Sugestão de uso das pastas

- `src/core/`: classes mais genéricas e reutilizáveis da arquitetura.
- `src/jogos/`: implementações concretas dos jogos.
- `tests/`: testes automatizados.
- `docs/`: diagramas, relatórios curtos, rascunhos de modelagem ou documentação complementar.

---

## Entregáveis
O grupo deverá entregar:

### 1. Código-fonte
Projeto organizado em módulos e pastas.

### 2. README atualizado
Este README deve ser complementado pelo grupo com:

- nomes dos integrantes;
- descrição da arquitetura criada;
- explicação das classes principais;
- instruções para execução;
- jogos implementados;
- decisões de projeto;
- limitações e melhorias futuras.

### 3. Modelagem/documentação
Pode estar no próprio README ou em arquivos na pasta `docs/`, contendo:

- principais classes;
- responsabilidades;
- relações entre objetos;
- pontos de extensibilidade.

### 4. Testes
Testes simples, mas relevantes, cobrindo regras importantes da solução.

### 5. Apresentação/demonstração
O grupo deverá demonstrar:

- a arquitetura criada;
- pelo menos um jogo funcionando;
- como seria possível adicionar outro jogo à base.

---

## Critérios de avaliação

### Modelagem orientada a objetos
- classes bem definidas;
- responsabilidades claras;
- boa decomposição do problema.

### Uso de conceitos de POO
- abstração;
- encapsulamento;
- herança;
- polimorfismo;
- composição/agregação/associação.

### Extensibilidade
- facilidade de adicionar novos jogos;
- reaproveitamento de código;
- baixo acoplamento.

### Funcionamento
- jogo implementado funciona corretamente;
- regras básicas foram respeitadas;
- turnos e estados são tratados adequadamente.

### Organização e documentação
- estrutura do projeto clara;
- README bem escrito;
- testes presentes.

---

## Perguntas-guia para a modelagem
Antes de começar a codificar, o grupo deve discutir:

- O que todo jogo de tabuleiro tem em comum?
- O que muda de um jogo para outro?
- O que deve ficar na classe base?
- O que deve ser sobrescrito pelas subclasses?
- O tabuleiro conhece regras ou apenas o estado do jogo?
- Como adicionar um novo jogo sem modificar os jogos já existentes?

---

## Sugestão de desenvolvimento
1. Modelar as classes e as relações.
2. Definir o núcleo reutilizável da arquitetura.
3. Implementar um primeiro jogo funcional.
4. Criar testes para as regras principais.
5. Refatorar a arquitetura para facilitar expansão.
6. Documentar as decisões do grupo.

---

## Integrantes
Preencher pelo grupo.

- Integrante 1:
- Integrante 2:

---

## Jogo(s) implementado(s)
Preencher pelo grupo.

- Jogo 1:
- Jogo 2 (opcional):

---

## Como executar
Preencher pelo grupo.

Exemplo:

```bash
python src/main.py
```

---

## Observação final
Neste projeto, a qualidade da **modelagem orientada a objetos** é tão importante quanto o funcionamento do jogo. Uma solução simples, mas bem projetada e extensível, vale mais do que uma implementação grande e difícil de manter.
