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
- no notebook resolvido, a fonte conterá a solução, as 17 células serão
  executadas na ordem em que aparecem e não conservarão saídas de erro.

Essa correspondência permitirá verificar automaticamente que a solução não
introduziu uma etapa ausente no material entregue ao estudante.

Em todos os ciclos, cada operação com saída independente ocupará sua própria
célula. Resultados diferentes não serão reunidos artificialmente em uma
`Series`, tabela ou outra estrutura apenas para reduzir a quantidade de células.

## 4. Topologia das células

Cada notebook terá exatamente 24 células:

1. Markdown — cabeçalho institucional, idêntico à primeira célula de
   `notebooks/u1_a01.ipynb`;
2. Markdown — `# Aula 2 — Fundamentos estatísticos e investigação com dados`;
3. Markdown — `## Carregamento do conjunto de dados`;
4. código — carregamento;
5. Markdown — `## Ciclo 1 — reconhecer a variabilidade`;
6. código — quantidade de valores válidos de massa corporal;
7. código — menor massa corporal;
8. código — maior massa corporal;
9. código — quantidade de valores distintos de massa corporal;
10. Markdown — `## Ciclo 2 — comparar descrição amostral e populacional`;
11. código — seleção da amostra aleatória;
12. código — média da massa corporal no conjunto disponível;
13. código — média da massa corporal na amostra;
14. Markdown — `## Ciclo 3 — delimitar população, amostra e unidades`;
15. código — tamanho do conjunto disponível;
16. código — tamanho da amostra;
17. código — quantidade de unidades distintas pelo par identificador;
18. código — unidade de análise;
19. código — unidade de observação;
20. Markdown — `## Ciclo 4 — comparar amostragem aleatória e por conveniência`;
21. código — seleção da amostra aleatória;
22. código — seleção da amostra por conveniência;
23. código — contagens de espécies na amostra aleatória;
24. código — contagens de espécies na amostra por conveniência.

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

O ciclo terá quatro células de código independentes, na seguinte ordem:

- quantidade de valores válidos de massa corporal;
- menor massa corporal;
- maior massa corporal;
- quantidade de valores distintos.

Cada célula produzirá somente seu próprio resultado. Essa granularidade segue o
padrão operacional de `notebooks/u1_a01.ipynb`, no qual cada operação discente
corresponde a uma célula própria.

Não serão antecipados desvio-padrão, quartis, variância ou gráficos.

### 6.3 Ciclo 2 — descrição amostral e populacional

O ciclo terá três células de código independentes:

1. selecionar aleatoriamente 30 observações, com semente fixa para
   reprodutibilidade, e exibir a amostra;
2. calcular a média da massa corporal no conjunto disponível;
3. calcular a média da massa corporal na amostra.

As médias serão apresentadas em células distintas para que seus alcances sejam
comparados sem uma saída conjunta. O resultado não será apresentado como
inferência probabilística formal.

### 6.4 Ciclo 3 — população, amostra e unidades

O ciclo terá cinco células de código independentes:

- tamanho do conjunto disponível;
- tamanho da amostra;
- quantidade de unidades distintas pelo par identificador;
- unidade de análise: pinguim;
- unidade de observação: registro de um pinguim.

Cada célula exibirá somente um desses resultados. As decisões do exercício serão
explicitadas sem afirmar que uma linha define universalmente a unidade de
análise.

### 6.5 Ciclo 4 — mecanismos de seleção

O ciclo terá quatro células de código independentes:

1. selecionar aleatoriamente 30 observações da população de referência;
2. formar uma amostra por conveniência com as primeiras 30 observações da ilha
   Biscoe;
3. contar as espécies na amostra aleatória;
4. contar as espécies na amostra por conveniência.

As duas contagens permanecerão em células distintas. Como os tamanhos são
iguais, as saídas permitirão comparar diretamente a composição observada e
reconhecer o risco de viés introduzido pelo recorte de conveniência.

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
contagens sequenciais de 1 a 17 e não conterão saídas de erro. O notebook discente
não terá contagens de execução nem saídas.

## 9. Validação

Um teste específico verificará:

- validade do JSON e leitura por `nbformat`;
- existência dos dois arquivos;
- total de 24 células em cada notebook;
- igualdade do cabeçalho com a primeira célula de `u1_a01.ipynb`;
- igualdade da topologia, dos IDs e das células Markdown entre as versões;
- 17 células de código vazias e sem saídas no notebook discente;
- 17 células de código preenchidas, executadas sequencialmente e sem erros no
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
