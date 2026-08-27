# Notebook mínimo da Aula 2 — desenho

**Data:** 27 de agosto de 2026

**Disciplina:** T199 — Métodos Quantitativos em Computação

**Estado:** desenho aprovado; aguardando revisão da especificação escrita

## 1. Objetivo

Criar um par de notebooks para `u1_a02` que permita ao estudante construir o
código do zero sem perder a correspondência com os quatro ciclos conceituais da
aula. O notebook discente fornecerá somente o cabeçalho institucional, o título
da aula, os títulos das seções e células de código vazias. O notebook resolvido
preservará a mesma topologia e preencherá as células com uma solução mínima,
executada e verificável.

O novo desenho substitui, para a Aula 2, o padrão mais guiado observado em
`notebooks/u1_a01.ipynb`. O cabeçalho da Aula 1 será reutilizado, mas seus
resumos, objetivos, explicações, comentários-guia e exercícios orientados não
serão transferidos.

## 2. Artefatos

Serão criados:

```text
notebooks/u1_a02.ipynb
notebooks/resolvidos/u1_a02.ipynb
```

`notebooks/u1_a01.ipynb` será apenas fonte do cabeçalho e dos metadados básicos;
não será modificado. Nenhum notebook removido no worktree será restaurado.

## 3. Relação entre as versões

Os dois notebooks terão a mesma sequência, tipos e IDs de células. As células
Markdown serão idênticas. A única diferença de conteúdo estará nas células de
código:

- no notebook discente, a fonte será vazia, `execution_count` será nulo e
  `outputs` será uma lista vazia;
- no notebook resolvido, a fonte conterá a solução, as cinco células serão
  executadas na ordem em que aparecem e não conservarão saídas de erro.

Essa correspondência permitirá verificar automaticamente que a solução não
introduziu uma etapa ausente no material entregue ao estudante.

## 4. Topologia das células

Cada notebook terá exatamente 12 células:

1. Markdown — cabeçalho institucional, idêntico à primeira célula de
   `notebooks/u1_a01.ipynb`;
2. Markdown — `# Aula 2 — Fundamentos estatísticos e investigação com dados`;
3. Markdown — `## Carregamento do conjunto de dados`;
4. código — carregamento;
5. Markdown — `## Ciclo 1 — reconhecer a variabilidade`;
6. código — variabilidade;
7. Markdown — `## Ciclo 2 — comparar descrição amostral e populacional`;
8. código — descrição e comparação;
9. Markdown — `## Ciclo 3 — delimitar população, amostra e unidades`;
10. código — delimitação das unidades e dos conjuntos;
11. Markdown — `## Ciclo 4 — comparar amostragem aleatória e por conveniência`;
12. código — mecanismos de seleção e comparação de composição.

Não haverá resumo, objetivos, texto instrucional, comentários-guia, perguntas,
respostas, síntese ou referências no notebook discente. Para manter a topologia
idêntica, o notebook resolvido também não acrescentará células Markdown.

## 5. Conjunto de dados

Será utilizada a versão bruta do Palmer Penguins, já apresentada na Aula 1. O
notebook carregará o CSV pela URL pública do repositório da disciplina para
funcionar no Google Colab sem upload manual. Durante a validação local, o
arquivo equivalente em `data/raw/penguins_raw.csv` poderá ser usado para
confirmar a lógica sem alterar o código final.

Somente estas colunas serão conservadas:

- `studyName`;
- `Individual ID`;
- `Species`;
- `Island`;
- `Body Mass (g)`.

As análises que dependem de massa corporal usarão observações com valor válido
nessa variável. O par `studyName` e `Individual ID` será usado para conferir a
identidade das unidades registradas.

O arquivo será tratado como conjunto de dados disponível e, quando a atividade
assim o declarar, como população finita de referência. O notebook não afirmará
que ele representa todos os pinguins nem confundirá automaticamente conjunto de
dados e população-alvo.

## 6. Código da versão resolvida

### 6.1 Carregamento do conjunto de dados

A primeira célula de código importará `pandas`, carregará o CSV público,
selecionará as cinco colunas necessárias e removerá somente as linhas sem massa
corporal quando essa medida for necessária. A célula exibirá as primeiras linhas
do conjunto selecionado.

### 6.2 Ciclo 1 — variabilidade

A célula produzirá uma série pequena com:

- quantidade de valores válidos de massa corporal;
- menor massa corporal;
- maior massa corporal;
- quantidade de valores distintos.

Não serão antecipados desvio-padrão, quartis, variância ou gráficos.

### 6.3 Ciclo 2 — descrição amostral e populacional

A célula selecionará aleatoriamente 30 observações, com semente fixa para
reprodutibilidade, e comparará a média da massa corporal na amostra com a média
do conjunto disponível. As duas medidas serão apresentadas com rótulos que
distinguem seus alcances. O resultado não será apresentado como inferência
probabilística formal.

### 6.4 Ciclo 3 — população, amostra e unidades

A célula apresentará uma estrutura simples com:

- tamanho do conjunto disponível;
- tamanho da amostra;
- quantidade de unidades distintas pelo par identificador;
- unidade de análise: pinguim;
- unidade de observação: registro de um pinguim.

Essa estrutura explicitará as decisões do exercício sem afirmar que uma linha
define universalmente a unidade de análise.

### 6.5 Ciclo 4 — mecanismos de seleção

A célula construirá duas amostras com 30 observações e a mesma população de
referência:

- uma amostra selecionada aleatoriamente;
- uma amostra por conveniência formada pelas primeiras 30 observações da ilha
  Biscoe.

As contagens de espécies das duas amostras serão reunidas em uma tabela. Como os
tamanhos são iguais, as contagens permitirão comparar diretamente a composição
observada e reconhecer o risco de viés introduzido pelo recorte de conveniência.

## 7. Restrições de simplicidade

O notebook resolvido não incluirá:

- funções definidas pelo usuário;
- classes;
- gráficos;
- simulações;
- bibliotecas além de `pandas`;
- comentários didáticos extensos;
- procedimentos inferenciais formais;
- medidas estatísticas ainda não ensinadas;
- código ou células que não contribuam diretamente para um dos cinco blocos
  operacionais.

Comentários de código também serão omitidos para que a versão resolvida seja
formada apenas pelas instruções necessárias. Nomes de objetos e rótulos de saída
serão suficientes para tornar o código legível.

## 8. Metadados e execução

Os metadados de kernel e linguagem serão derivados de
`notebooks/u1_a01.ipynb`. Metadados de execução específicos do ambiente local
que não sejam necessários à portabilidade poderão ser normalizados.

O notebook resolvido será executado do início ao fim. As células de código terão
contagens sequenciais de 1 a 5 e não conterão saídas de erro. O notebook discente
não terá contagens de execução nem saídas.

## 9. Validação

Um teste específico verificará:

- validade do JSON e leitura por `nbformat`;
- existência dos dois arquivos;
- total de 12 células em cada notebook;
- igualdade do cabeçalho com a primeira célula de `u1_a01.ipynb`;
- igualdade da topologia, dos IDs e das células Markdown entre as versões;
- cinco células de código vazias e sem saídas no notebook discente;
- cinco células de código preenchidas, executadas sequencialmente e sem erros no
  notebook resolvido;
- ausência de células Markdown além das sete previstas;
- ausência de funções próprias, gráficos e bibliotecas adicionais;
- execução integral do código resolvido com o conjunto de dados esperado.

A verificação de conteúdo examinará os objetos e resultados produzidos, não
apenas a presença de palavras no JSON. `git diff --check` será executado sobre os
arquivos relacionados antes da entrega.

## 10. Limites

Este incremento não:

- altera `notebooks/u1_a01.ipynb`;
- restaura os notebooks antigos removidos;
- reformula outros notebooks da Unidade I;
- cria uma skill de geração de notebooks;
- modifica o conteúdo teórico de `aulas/u1_a02.md`;
- substitui a revisão docente da adequação das atividades aos quatro ciclos.
