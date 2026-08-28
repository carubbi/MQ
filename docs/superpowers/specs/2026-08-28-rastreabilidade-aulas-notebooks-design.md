# Rastreabilidade entre curadoria, aulas e notebooks

## Objetivo

Eliminar omissões entre os subassuntos aprovados, a aula pública e o notebook,
além de impedir formalizações matemáticas ornamentais e exemplos sem origem
bibliográfica verificável.

O fluxo continuará separado em três autoridades:

- `selecao.yaml` decide escopo, referências, ciclos e exercícios;
- `aulas/<aula-id>.md` apresenta a fundamentação e a resolução manual;
- `notebook.yaml` decide a materialização computacional e gera o par de
  notebooks.

## Decisões arquiteturais

### Cobertura dos subassuntos no notebook

`notebook.yaml` receberá uma matriz explícita de cobertura. Cada subassunto de
todo tópico selecionado no manifesto aparecerá exatamente uma vez, com:

- ID do tópico;
- texto exato do subassunto aprovado;
- tratamento `computacional` ou `teorico`;
- IDs das operações que produzem evidência, quando computacional;
- justificativa, quando o tratamento for exclusivamente teórico.

O validador comparará a matriz com o manifesto. Falhará diante de subassunto
omitido, duplicado, estranho ao manifesto, associado a operação inexistente ou
declarado teórico sem justificativa.

A matriz não obrigará uma célula para cada subassunto. Essa obrigação produziria
código artificial para conteúdos cuja evidência é conceitual.

### Origem do exemplo resolvido

Cada ciclo de `selecao.yaml` receberá a origem da atividade usada em `Exemplo e
resolução`, com:

- ID da referência no grafo;
- item, questão ou seção;
- páginas PDF;
- tipo de origem: `exercicio`, `questao` ou `exemplo_aplicado`;
- forma de uso: `parafraseado` ou `adaptado`;
- conceitos que devem ser aplicados manualmente.

O enunciado público será parafraseado ou adaptado, preservará os dados
necessários e receberá citação próxima. Não haverá reprodução extensa do texto
editorial nem código na resolução.

Quando as referências já selecionadas não contiverem exercício compatível, a
curadoria consultará o grafo e o banco de questões. Se essa busca também não
encontrar exercício ou questão, será permitido converter um exemplo aplicado da
referência em atividade com resolução manual. O manifesto registrará explicitamente
essa exceção e sua origem; a skill não inventará dados ou fenômenos para preencher
a seção.

### Utilidade das fórmulas

Uma fórmula permanecerá na aula somente quando cumprir pelo menos uma função
observável:

- calcular um resultado na resolução manual;
- sustentar uma dedução usada na aula;
- definir uma quantidade retomada posteriormente;
- permitir uma interpretação necessária ao resultado de aprendizagem.

Cada fórmula será auditada quanto a origem, uso posterior, símbolos, domínio e
pressupostos. Formalizações que apenas renomeiem uma frase, listem categorias ou
representem genericamente uma transformação serão substituídas por texto direto.
As fórmulas remanescentes serão renumeradas sequencialmente por aula.

A auditoria inicial abrangerá as duas aulas públicas atuais:

- `aulas/u1_a02.md`;
- `aulas/u1_a05.md`.

Cada aula será revisada em rascunho privado. Nenhuma remoção ou reformulação
matemática será publicada antes da aprovação docente do diff correspondente.

## Aula 5

### Variáveis derivadas aprovadas

A cópia `dados` receberá três variáveis com significado no Palmer Penguins:

1. `postura_completa`: variável lógica obtida pela condição
   `Clutch Completion == "Yes"`;
2. `ano_observacao`: variável quantitativa discreta extraída de `Date Egg`;
3. `faixa_massa`: variável qualitativa ordinal obtida da massa corporal por
   três grupos amostrais.

A discretização da massa ocorrerá em duas operações didáticas:

1. `pd.qcut()` sem rótulos, para exibir os intervalos calculados;
2. `pd.qcut()` com os rótulos ordenados `inferior`, `intermediária` e
   `superior`, adicionando somente `faixa_massa` ao DataFrame.

As faixas serão descritas como relativas à amostra observada, e não como limites
biológicos universais. Os dois valores ausentes de massa continuarão ausentes.

### Suporte bibliográfico

O recorte de `mckinney-2017-sec-7-2` será ampliado das páginas PDF 215–219
para 215–223. As páginas 221–223 apresentam discretização, `cut()` e `qcut()`.
O nó do grafo já cobre integralmente a seção 7.2, nas páginas 215–228; não
será necessário alterar o grafo para essa ampliação.

### Sincronização

Depois de aprovado e validado o `notebook.yaml`, o gerador executará o plano em
diretório temporário, comparará as saídas e promoverá conjuntamente:

- `notebooks/u1_a05.ipynb`;
- `notebooks/resolvidos/u1_a05.ipynb`.

O notebook discente conservará uma única célula vazia por seção operacional. O
resolvido terá uma célula por operação aprovada, comentários concisos, variáveis
curtas e significativas e saídas separadas.

## Skills e validadores

### `curar-aula-formal`

A skill e o contrato do manifesto passarão a exigir a origem da atividade de
cada ciclo. O schema e os testes de `scripts/aulas` validarão a estrutura, a
existência do ID no grafo e a precedência de exercício ou questão sobre exemplo
aplicado.

### `gerar-aula-formal`

O contrato da aula exigirá:

- atividade rastreável por ciclo, priorizando exercício ou questão;
- enunciado parafraseado ou adaptado;
- resolução manual;
- citação próxima;
- teste de utilidade para cada fórmula.

### `gerar-notebooks-aula`

O contrato de `notebook.yaml`, seu schema e o validador passarão a exigir a
matriz de cobertura. A validação cruzada com `selecao.yaml` ocorrerá antes da
geração e novamente antes da promoção pública.

As skills serão alteradas separadamente. Cada mudança seguirá teste de
comportamento RED–GREEN, validação estrutural e os testes automatizados
pertinentes antes de iniciar a skill seguinte.

## Migração e validação

A mudança de contrato será migrada primeiro nos manifestos e planos privados das
aulas públicas atuais. O fluxo falhará de forma explícita para artefatos futuros
que omitam os novos campos.

A verificação integrada incluirá:

- testes de schema e regras semânticas;
- validação dos manifestos aprovados;
- renderização determinística dos dossiês;
- auditoria dos rascunhos das aulas;
- execução sem erro dos notebooks resolvidos;
- igualdade estrutural entre plano e notebooks;
- confirmação de que nenhum arquivo sob `.interno/` foi rastreado.

## Fora do escopo

- introduzir tratamento detalhado de caracteres na Aula 5;
- fabricar defeitos, duplicidades ou valores ausentes para demonstrar métodos;
- obrigar uma fórmula em todo ciclo;
- obrigar código para todo subassunto;
- publicar revisões das aulas sem aprovação docente do rascunho;
- alterar o grafo quando o nó existente já cobre as páginas necessárias.
