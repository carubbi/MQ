# Notebook mínimo da Aula 2 — desenho

**Data:** 27 de agosto de 2026

**Disciplina:** T199 — Métodos Quantitativos em Computação

**Estado:** desenho aprovado; aguardando revisão da especificação escrita

## 1. Objetivo

Criar um par de notebooks para `u1_a02` que permita ao estudante construir o
código do zero sem perder a correspondência com os quatro ciclos conceituais da
aula. O notebook discente fornecerá somente o cabeçalho institucional, o título
da aula, os títulos das seções e células de código vazias. O notebook resolvido
preservará o mesmo esqueleto de seções, mas acrescentará todas as células
necessárias a uma solução mínima, executada e verificável.

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

Os dois notebooks compartilharão o cabeçalho, o título, os cinco títulos de
seção e a ordem dessas sete células Markdown. Os IDs e conteúdos dessas células
serão idênticos.

O notebook discente terá apenas uma célula de código vazia imediatamente depois
de cada seção operacional. Essas cinco células serão pontos iniciais de trabalho;
o estudante será responsável por criar novas células quando uma seção exigir
mais de uma operação.

O notebook resolvido não ficará limitado a uma célula por seção. Ele conterá as
18 células de código necessárias para separar operações e saídas conforme o
contrato. Os IDs e a quantidade das células de código não precisarão coincidir
entre as duas versões.

Em todos os ciclos, cada operação com saída independente ocupará sua própria
célula. Resultados diferentes não serão reunidos artificialmente em uma
`Series`, tabela ou outra estrutura apenas para reduzir a quantidade de células.
As saídas serão escalares ou textos simples por padrão. `DataFrame`, `Series`,
listas ou outras coleções só serão exibidos quando a estrutura conjunta for o
próprio objeto da análise e não puder ser substituída por uma saída simples sem
perda conceitual.

## 4. Topologia das células

### 4.1 Notebook discente

O notebook discente terá exatamente 12 células:

1. Markdown — cabeçalho institucional, idêntico à primeira célula de
   `notebooks/u1_a01.ipynb`;
2. Markdown — `# Aula 2 — Fundamentos estatísticos e investigação com dados`;
3. Markdown — `## Carregamento do conjunto de dados`;
4. código — célula inicial vazia;
5. Markdown — `## Ciclo 1 — reconhecer a variabilidade`;
6. código — célula inicial vazia;
7. Markdown — `## Ciclo 2 — comparar descrição amostral e populacional`;
8. código — célula inicial vazia;
9. Markdown — `## Ciclo 3 — delimitar população, amostra e unidades`;
10. código — célula inicial vazia;
11. Markdown — `## Ciclo 4 — comparar amostragem aleatória e por conveniência`;
12. código — célula inicial vazia.

As cinco células de código terão fonte vazia, `execution_count` nulo e
`outputs` vazio. O arquivo não antecipará quantas células adicionais o estudante
deverá criar em cada seção.

### 4.2 Notebook resolvido

O notebook resolvido terá exatamente 25 células:

1. Markdown — cabeçalho institucional, idêntico à primeira célula de
   `notebooks/u1_a01.ipynb`;
2. Markdown — `# Aula 2 — Fundamentos estatísticos e investigação com dados`;
3. Markdown — `## Carregamento do conjunto de dados`;
4. código — carregamento;
5. código — informações básicas do conjunto de dados com `dados.info()`;
6. Markdown — `## Ciclo 1 — reconhecer a variabilidade`;
7. código — quantidade de valores válidos de massa corporal;
8. código — menor massa corporal;
9. código — maior massa corporal;
10. código — quantidade de valores distintos de massa corporal;
11. Markdown — `## Ciclo 2 — comparar descrição amostral e populacional`;
12. código — seleção da amostra aleatória;
13. código — média da massa corporal no conjunto disponível;
14. código — média da massa corporal na amostra;
15. Markdown — `## Ciclo 3 — delimitar população, amostra e unidades`;
16. código — tamanho do conjunto disponível;
17. código — tamanho da amostra;
18. código — quantidade de unidades distintas pelo par identificador;
19. código — unidade de análise;
20. código — exemplo de um registro de pinguim;
21. Markdown — `## Ciclo 4 — comparar amostragem aleatória e por conveniência`;
22. código — seleção da amostra aleatória;
23. código — seleção da amostra por conveniência;
24. código — contagens de espécies na amostra aleatória;
25. código — contagens de espécies na amostra por conveniência.

Não haverá resumo, objetivos, texto instrucional, comentários-guia, perguntas,
respostas, síntese ou referências no notebook discente. O notebook resolvido
também não acrescentará células Markdown além das sete compartilhadas.

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

A primeira célula de código importará `pandas`, carregará o CSV público e
selecionará as cinco colunas necessárias. Ela apenas criará `dados` e não
produzirá saída. A segunda célula executará `dados.info()` para apresentar, em
formato textual, o índice, as colunas, as quantidades de valores não nulos, os
tipos de dados e o uso de memória. A remoção das linhas sem massa corporal será
realizada somente nas operações que dependerem dessa medida.

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
   reprodutibilidade, sem exibir o `DataFrame`;
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
- registro de um pinguim apresentado como linha do conjunto de dados.

Cada célula exibirá somente um desses resultados. A última usará
`dados.iloc[[0], :]` para manter a estrutura tabular de uma linha e explicitar a
seleção posicional de linhas e colunas. O registro exemplificará os dados obtidos
de uma unidade observada, sem afirmar que uma linha define universalmente a
unidade de análise ou a unidade de observação.

### 6.5 Ciclo 4 — mecanismos de seleção

O ciclo terá quatro células de código independentes:

1. selecionar aleatoriamente 30 observações da população de referência;
2. formar uma amostra por conveniência com as primeiras 30 observações da ilha
   Biscoe;
3. contar as espécies na amostra aleatória;
4. contar as espécies na amostra por conveniência.

As duas células de seleção apenas criarão os `DataFrame` e não os exibirão. As
contagens permanecerão em células distintas e serão as únicas saídas em
`Series`, pois a distribuição conjunta das categorias é o objeto necessário à
comparação. Como os tamanhos são iguais, essas saídas permitirão comparar
diretamente a composição observada e reconhecer o risco de viés introduzido
pelo recorte de conveniência.

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

Cada célula de código da versão resolvida começará com um único comentário curto
em português, formulado com verbo no infinitivo e destinado a indicar a
finalidade da célula. O comentário não explicará sintaxe evidente nem repetirá
os nomes das instruções. Não haverá comentários adicionais na mesma célula.

Os nomes das variáveis serão curtos, significativos e, sempre que possível, em
português, como `dados`, `massa`, `amostra` e `media`. A clareza prevalecerá
sobre a brevidade: nomes como `amostra_aleatoria` serão preferidos a abreviações
ambíguas como `aa`. Nomes genéricos ou sem significado no contexto, como `df`,
`x` e `tmp`, não serão usados.

Cada linha realizará uma operação principal. Não haverá encadeamento de métodos;
quando forem necessárias duas ou mais transformações, os resultados
intermediários serão atribuídos a variáveis. O acesso direto a uma coluna, como
`dados["Body Mass (g)"]`, não será considerado encadeamento. Por exemplo, o
cálculo de uma média seguirá esta forma:

```python
massa = dados["Body Mass (g)"]
massa = massa.dropna()
media = massa.mean()
media
```

Serão priorizados os métodos mais simples e diretos do `pandas`. Expressões
compactas, funções auxiliares e construções avançadas não serão empregadas
quando uma sequência curta de instruções básicas comunicar melhor cada etapa.
Cada célula continuará dedicada a um único resultado, ainda que contenha linhas
intermediárias necessárias para produzi-lo.

As células de criação do conjunto de dados e de seleção poderão não produzir
saída. Nas demais, cada saída será um único número ou texto. A inspeção com
`dados.info()` produzirá uma saída textual estrutural. O exemplo de registro do
Ciclo 3 produzirá o único `DataFrame`, com uma linha e as cinco colunas
selecionadas. As duas contagens por espécie do Ciclo 4 produzirão uma `Series`
cada. Nenhuma célula produzirá lista nem outro `DataFrame` como saída.

## 8. Metadados e execução

Os metadados de kernel e linguagem serão derivados de
`notebooks/u1_a01.ipynb`. Metadados de execução específicos do ambiente local
que não sejam necessários à portabilidade poderão ser normalizados.

O notebook resolvido será executado do início ao fim. As células de código terão
contagens sequenciais de 1 a 18 e não conterão saídas de erro. O notebook discente
terá cinco células de código vazias, sem contagens de execução nem saídas.

Quatro células resolvidas — criação de `dados`, seleção amostral do Ciclo 2 e as
duas seleções do Ciclo 4 — não produzirão saída. As outras 14 produzirão uma saída
por célula: onze escalares ou textos simples, um `DataFrame` de uma linha e as
duas `Series` categóricas justificadas no Ciclo 4.

## 9. Validação

Um teste específico verificará:

- validade do JSON e leitura por `nbformat`;
- existência dos dois arquivos;
- total de 12 células no notebook discente e 25 no resolvido;
- igualdade do cabeçalho com a primeira célula de `u1_a01.ipynb`;
- igualdade dos conteúdos, IDs e ordem das sete células Markdown entre as
  versões;
- presença de uma única célula de código imediatamente depois de cada seção no
  notebook discente;
- cinco células de código vazias e sem saídas no notebook discente;
- 18 células de código preenchidas, executadas sequencialmente e sem erros no
  notebook resolvido;
- distribuição das células resolvidas por seção em `2`, `4`, `3`, `5` e `4`;
- ausência de células Markdown além das sete previstas;
- ausência de funções próprias, gráficos e bibliotecas adicionais;
- presença de um único comentário inicial, curto e orientado à finalidade, em
  cada célula de código resolvida;
- uso de nomes de variáveis curtos e significativos, sem abreviações ambíguas;
- ausência de encadeamento de métodos e presença de uma única operação principal
  por linha;
- uso de variáveis intermediárias quando uma operação exigir mais de uma
  transformação;
- ausência de listas e presença de somente um `DataFrame`, correspondente ao
  registro de um pinguim no Ciclo 3;
- presença de somente duas saídas em `Series`, ambas correspondentes às
  contagens por espécie do Ciclo 4;
- presença da saída textual de `dados.info()` com as cinco colunas selecionadas;
- presença de quatro células operacionais sem saída e 14 células com uma única
  saída;
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
