# Curadoria e geração de aulas estatísticas formais — desenho

**Data:** 26 de agosto de 2026

**Disciplina:** T199 — Métodos Quantitativos em Computação

**Estado:** desenho aprovado para especificação do piloto da Aula 2

## 1. Objetivo

Reformular a produção dos materiais de aula em Markdown a partir da Aula 2,
separando explicitamente:

1. a delimitação curricular e temporal do encontro;
2. a localização e a análise das referências candidatas;
3. a seleção docente dos tópicos e das referências;
4. a geração do material teórico da aula.

Cada encontro de 100 minutos constituirá uma unidade de produção. O material
resultante adotará exposição estatística clássica, notação matemática formal e
profundidade aplicada. Definições, domínio, hipóteses, propriedades, deduções
curtas, exemplos resolvidos e interpretação serão incluídos quando pertinentes.
Demonstrações extensas não serão exigidas, salvo quando forem pedagogicamente
essenciais.

O primeiro incremento abrangerá somente a Aula 2 da Unidade I. As demais aulas
não serão regeneradas até que o piloto e o contrato dos artefatos tenham sido
validados.

## 2. Decisões centrais

- O cronograma delimita o encontro; o grafo não determina sozinho seu escopo.
- O grafo de referências permanece um índice bibliográfico independente das
  decisões específicas de uma aula ou de um semestre.
- O dossiê de curadoria em Markdown é derivado, regenerável e não recebe
  decisões manuais.
- O manifesto YAML é criado antes do dossiê e constitui a fonte canônica das
  evidências de leitura, dos candidatos e da seleção docente.
- Uma aula pode combinar livremente uma ou mais referências por tópico.
- Referências diferentes devem ser compatibilizadas por meio da notação global
  da disciplina ou de exceção explícita registrada no manifesto.
- Nenhuma afirmação teórica pode ser produzida apenas a partir dos títulos ou
  das relações do grafo; as páginas originais selecionadas devem ser
  consultadas.
- O material de aula é teórico e não contém código, pseudocódigo, bibliotecas,
  funções, comandos nem sequências de implementação.
- Cada ciclo didático da aula contém uma subseção `Aplicação no notebook`, que
  representa sua aplicação no ciclo correspondente do notebook sem antecipar
  a implementação computacional.

## 3. Autoridades e responsabilidades

As autoridades possuem responsabilidades distintas e não formam uma única
ordem linear.

### 3.1 Autoridade curricular e temporal

O projeto de ensino define os conteúdos formais da disciplina. O cronograma
docente canônico define data, duração, conteúdo, resultado de aprendizagem,
atividade, evidência e limites de cada encontro. O cronograma discente é um
artefato derivado e não pode ampliar o escopo docente.

### 3.2 Autoridade pedagógica

Os planejamentos e detalhamentos das unidades orientam progressão, profundidade,
pré-requisitos, exclusões e relação com avaliações e projetos. Eles podem
restringir o conjunto inicialmente localizado pelo conteúdo curricular.

### 3.3 Autoridade bibliográfica

O grafo canônico localiza fontes, capítulos, seções, exemplos, exercícios e
questões por conteúdo e tópico. Ele não substitui a leitura das páginas
originais nem decide quais conceitos pertencem ao encontro.

As páginas das referências selecionadas sustentam definições, propriedades,
convenções e exemplos. Quando houver divergência, a convenção global da
disciplina prevalece, salvo exceção docente explícita.

### 3.4 Autoridade da seleção

Depois de aprovado, o manifesto YAML define os tópicos selecionados, rejeitados
ou adiados, as referências e seus papéis, a profundidade e as compatibilizações.
A geração da aula não pode acrescentar tópicos ou referências por iniciativa
própria.

## 4. Identidade e granularidade

Cada encontro de 100 minutos recebe um identificador global composto por
unidade e número da aula, por exemplo `u1_a02`. A numeração local apresentada
no cronograma não será usada isoladamente, pois reinicia em cada unidade.

O piloto usa:

```text
u1_a02 — Fundamentos estatísticos e investigação com dados
```

O título descritivo pode mudar sem alterar o identificador. O identificador é
usado nos nomes dos artefatos, nos comandos e nas relações entre aula e
notebook.

## 5. Arquitetura e fluxo

```text
cronograma docente
        |
        v
delimitação da aula
        |
        v
consulta ao grafo + leitura das páginas originais
        |
        v
manifesto YAML inicial com candidatos e evidências
        |
        v
dossiê Markdown derivado
        |
        v
manifesto YAML selecionado pelo docente
        |
        v
validação estrutural, curricular e bibliográfica
        |
        v
aula Markdown teórica
```

A geração possui dois estados. Um rascunho pode ser produzido enquanto o
notebook correspondente ainda estiver em elaboração, desde que seja
identificado como tal. A publicação exige que todos os vínculos para notebooks
existam e sejam válidos.

## 6. Organização dos artefatos

O piloto criará:

```text
.interno/prof/aulas/
└── 2026-2/
    └── u1_a02/
        ├── dossie.md
        └── selecao.yaml
```

Depois da seleção e validação, a saída pública será:

```text
aulas/u1_a02.md
```

O dossiê e o YAML são privados e permanecerão sob `.interno/`, sem rastreamento
pelo Git. O YAML preservará localmente as evidências de leitura, os candidatos
e a decisão docente e permitirá a reprodução do dossiê e da aula no mesmo
ambiente. A reprodução em outro ambiente exigirá a transferência ou a
restauração privada desse manifesto. A saída pública será o único arquivo
gerado da aula; não haverá uma segunda cópia do material final na pasta interna.

A convenção matemática global não pertencerá a uma aula ou semestre específico
e permanecerá em:

```text
.interno/docs/modelos/notacao-estatistica.md
```

Nenhum arquivo ou diretório sob `.interno/` será rastreado pelo Git. O pipeline
não criará exceções no `.gitignore` nem usará inclusão forçada desses
artefatos. Backup e transferência do conteúdo privado permanecerão fora do
escopo do repositório público.

## 7. Dossiê de curadoria

### 7.1 Finalidade

O dossiê apresenta opções verificadas para decisão. Ele não é uma aula
preliminar nem um compêndio integral das fontes. Seu conteúdo deve ser
suficiente para selecionar assuntos e referências sem produzir antecipadamente
material que poderá ser descartado.

### 7.2 Conteúdo obrigatório

O dossiê conterá:

1. identificação, data, duração, conteúdo formal e resultado de aprendizagem;
2. escopo positivo retirado do cronograma e do planejamento;
3. limites, exclusões e conteúdos reservados a encontros posteriores;
4. tópicos candidatos classificados como centrais, pré-requisitos, opcionais
   ou adiados;
5. matriz por tópico com referências, seções, páginas e pertinência;
6. síntese da cobertura conceitual encontrada em cada referência;
7. notação e convenções relevantes empregadas por cada obra;
8. divergências conceituais, terminológicas ou matemáticas entre as fontes;
9. exemplos e exercícios rastreáveis disponíveis;
10. alertas sobre lacunas, páginas não verificadas ou incompatibilidades.

Cada informação proveniente do grafo deverá preservar o ID canônico da
referência. Sínteses e comparações somente serão incluídas depois da consulta
às páginas originais e serão lidas do manifesto YAML inicial.

### 7.3 Regeneração

O dossiê será totalmente regenerável a partir do manifesto YAML. Nenhum campo
de evidência ou seleção será editado manualmente nele. Uma nova geração poderá
alterar a apresentação, mas não poderá modificar o manifesto YAML existente.

## 8. Manifesto de seleção

### 8.1 Finalidade

O manifesto registra de forma validável a leitura das fontes, os candidatos e
a decisão docente. Ele diferencia seleção, rejeição e adiamento para impedir
que candidatos não escolhidos reapareçam silenciosamente.

### 8.2 Estrutura conceitual

O documento conterá metadados da aula, versão do contrato, estado da seleção,
convenção matemática global, ciclos planejados, tópicos, evidências de leitura,
referências candidatas, recursos discentes e aplicação no notebook. A inclusão
de `recursos_discentes` elevará o contrato do manifesto para a versão `1.2`.

Cada tópico terá:

```yaml
id: topico-populacao
estado: selecionado
referencias:
  - id: barbetta-2010-sec-1-6
    papel: fundamentacao
    paginas_pdf: [18, 23]
    cobertura: "População, amostra, parâmetro e estatística."
    notacao: "N para tamanho da população e n para tamanho da amostra."
  - id: navidi-2024-sec-1-1
    papel: complementar
    paginas_pdf: [25, 34]
    cobertura: "Amostragem, representatividade e vieses."
    notacao: "Compatível com a distinção entre população e amostra."
compatibilizacao:
  convencao: notacao_global
  observacao: "Traduzir a notação das fontes para a convenção da disciplina."
profundidade: formal_aplicada
```

Os estados de tópico permitidos serão `pendente`, `selecionado`, `rejeitado` e
`adiado`. `pendente` será admitido somente enquanto o estado geral do manifesto
for `em_selecao`; um manifesto `aprovado` não poderá conter tópicos pendentes.
Os papéis de referência serão `fundamentacao`, `complementar`, `contraponto`,
`exemplo` e `exercicio`. A profundidade inicial será `formal_aplicada`.

Um tópico selecionado exigirá ao menos uma referência de `fundamentacao`.
Referências adicionais poderão cumprir mais de um papel por meio de entradas
distintas somente quando a distinção for necessária e justificada.

Cada referência candidata exigirá páginas verificadas, síntese de cobertura e
registro da notação relevante. Divergências conceituais, terminológicas ou
matemáticas serão registradas no tópico antes de o dossiê ser renderizado. O
estado inicial de todos os candidatos será `pendente`; a geração não presumirá
seleção.

### 8.3 Compatibilização

O uso de várias referências não autoriza justaposição de definições ou troca
silenciosa de símbolos. O manifesto registrará `notacao_global` quando as
fontes forem normalizadas para a convenção da disciplina. Qualquer exceção
exigirá a convenção adotada, a justificativa e a explicação que deverá aparecer
na aula.

### 8.4 Prioridade linguística e tradução técnica

A seleção priorizará a adequação da cobertura e, entre fontes igualmente
adequadas, dará preferência a livros em língua portuguesa. A mera existência
de uma menção em português não impedirá o uso de uma fonte mais completa em
inglês. A apostila poderá orientar o conteúdo curricular, mas não substituirá
automaticamente a fundamentação teórica.

Quando não houver livro em português com cobertura suficiente, uma obra em
inglês poderá cumprir o papel de `fundamentacao`. Seu uso exigirá consulta
direta ao original, tradução técnica para o português e compatibilização com a
terminologia e a notação global da disciplina. A tradução produzida para a aula
não será apresentada como tradução oficial da obra.

O manifesto preservará a fonte, a edição e as páginas originais e registrará,
em `compatibilizacao.observacao`, as decisões terminológicas ou matemáticas
necessárias. A tradução não poderá alterar o alcance da definição, omitir
condições ou introduzir equivalências conceituais não sustentadas pela fonte.

### 8.5 Recursos discentes

O manifesto registrará explicitamente os itens que deverão aparecer em
`Estudo e exercícios`. A seleção será independente do tipo da fonte: livros,
apostilas e bancos de questões poderão fornecer materiais didáticos ou
exercícios indicados conforme a adequação de cada item ao conteúdo, à
profundidade e aos limites da aula.

```yaml
recursos_discentes:
  materiais_didaticos:
    - id: barbetta-2010-sec-1-1
    - id: apostila-mq-sec-1-1
  exercicios_indicados:
    - id: barbetta-2010-exercicio-2-7
    - id: banco-questoes-2026-2-questao-6
```

Cada entrada preservará o ID canônico do grafo. Título, autoria, seção, número
do item e páginas serão resolvidos a partir do grafo, sem duplicação desses
metadados no manifesto. A ordem registrada no YAML determinará a ordem de
apresentação na aula.

Em `materiais_didaticos`, serão aceitos nós dos tipos `capitulo`, `secao` ou
`exemplo`, desde que sua relação com o conteúdo e os tópicos selecionados seja
comprovada diretamente ou pela cadeia de contenção registrada no grafo. Em
`exercicios_indicados`, serão aceitos somente nós concretos dos tipos
`exercicio` ou `questao`. A origem editorial do item não determinará sua
categoria.

O objeto `recursos_discentes` será obrigatório em um manifesto aprovado. Suas
listas poderão permanecer vazias quando a leitura das fontes não encontrar um
item adequado; nesse caso, a subseção pública correspondente será omitida. A
ausência de recurso é preferível à indicação artificial de conteúdo apenas
para preencher a estrutura.

A seleção dos recursos discentes não alterará os papéis bibliográficos usados
na construção teórica. Uma seção rejeitada como `fundamentacao` poderá ser
indicada como material didático quando houver justificativa pedagógica; de modo
análogo, uma questão insuficiente para fundamentar um tópico poderá ser
selecionada como exercício. Nenhum item será incluído apenas por proximidade
editorial ou por corresponder genericamente ao conteúdo formal: o enunciado ou
as páginas originais deverão ser verificados antes da aprovação.

## 9. Convenção matemática global

Um documento canônico de notação distinguirá, quando aplicável:

- população e amostra;
- $N$ e $n$;
- variável aleatória $X_i$ e valor observado $x_i$;
- parâmetro e estatística;
- $\mu$ e $\bar{x}$;
- $\sigma^2$ e $s^2$;
- $p$ e $\hat{p}$;
- função de probabilidade, densidade e distribuição acumulada;
- variável, índice, conjunto, operador e unidade.

Convenções sensíveis, incluindo o denominador da variância, definições de
quantis e parametrizações de distribuições, serão declaradas explicitamente.
Toda fórmula deverá ser seguida da definição de símbolos, índices, operadores,
condições e unidades pertinentes.

A notação global assegura consistência entre aulas. Quando uma referência usar
outra convenção, a aula poderá informar a tradução, mas empregará a convenção
global salvo exceção aprovada no manifesto.

## 10. Estrutura da aula

Cada aula conterá identificação, resultado de aprendizagem, agenda, pergunta
orientadora, ciclos didáticos, síntese, estudo, exercícios e referências.

### 10.1 Estudo e exercícios

Ao final da exposição, `Estudo e exercícios` será organizado em duas
subseções:

- `Materiais didáticos`, com os capítulos, seções ou recursos selecionados
  para estudo;
- `Exercícios indicados`, com os exercícios e questões selecionados para
  consolidação.

As duas listas serão produzidas exclusivamente de `recursos_discentes` e terão
rastreabilidade ao grafo. Livros, apostilas e bancos de questões poderão
aparecer em qualquer uma delas quando o item cumprir a função correspondente.
Itens da mesma fonte poderão ser consolidados em uma entrada, preservando os
números de seções, exercícios ou questões e as páginas.

A seção apresentará somente recursos aprovados e adequados ao escopo. Não
reintroduzirá conteúdos rejeitados, adiados ou reservados apenas porque a fonte
também cobre tópicos selecionados. Recursos públicos poderão receber vínculo
para acesso discente; fontes privadas serão identificadas bibliograficamente,
sem exposição de caminhos internos.

Cada ciclo seguirá, com omissões apenas quando justificadas pelo conceito:

```text
problema e motivação
        -> definição formal e notação
        -> domínio, condições e pressupostos
        -> propriedades e deduções curtas
        -> exemplo e resolução
        -> interpretação e limitações
        -> Aplicação no notebook
```

O material não conterá código, pseudocódigo, nomes de bibliotecas, funções ou
métodos de APIs, comandos, células ou sequência de implementação. Funções
matemáticas e estatísticas permanecem permitidas e serão apresentadas mediante
notação formal. A resolução apresentada na aula será matemática e
interpretativa.

## 11. Aplicação no notebook

### 11.1 Posição e cardinalidade

`Aplicação no notebook` será uma subseção obrigatória dentro de cada ciclo
didático. Cada ciclo teórico possuirá exatamente uma aplicação correspondente
no notebook.

A aula e o notebook usarão os mesmos identificadores e títulos de ciclo. Essa
correspondência será estrutural, não inferida apenas por semelhança textual.

### 11.2 Conteúdo permitido

A subseção informará somente:

- o conceito do ciclo que será aplicado;
- a questão que será investigada;
- o resultado, relação ou interpretação que deverá ser contrastado;
- a evidência de aprendizagem esperada;
- o ciclo correspondente e o vínculo para o notebook.

### 11.3 Conteúdo proibido

A subseção não conterá:

- código ou pseudocódigo;
- bibliotecas, funções ou métodos de APIs e comandos;
- instruções de implementação;
- respostas dependentes de execução;
- saídas computacionais inventadas.

A aplicação e a verificação computacional propriamente ditas pertencem
exclusivamente ao notebook.

## 12. Validação e falhas

O pipeline rejeitará a geração quando:

- o identificador da aula não corresponder ao encontro delimitado;
- o manifesto não estiver no estado geral `aprovado` ou contiver decisão
  pendente;
- um tópico selecionado não possuir referência de fundamentação;
- uma referência não existir no grafo;
- um recurso discente não existir no grafo ou possuir tipo incompatível com a
  lista em que foi selecionado;
- um recurso discente não possuir páginas verificáveis ou não estiver
  relacionado ao conteúdo e a pelo menos um tópico selecionado da aula;
- o tópico não estiver relacionado explicitamente à referência selecionada;
- as páginas selecionadas não puderem ser verificadas na fonte original;
- uma divergência de notação permanecer sem compatibilização;
- um ciclo não possuir exatamente uma `Aplicação no notebook`;
- a aula incorporar tópico rejeitado, adiado ou reservado para encontro futuro;
- o material contiver código, pseudocódigo, bibliotecas, funções ou métodos de
  APIs, comandos ou instruções computacionais;
- uma publicação apontar para notebook inexistente.

Falhas apresentarão o identificador da aula, o campo ou ciclo afetado e uma
mensagem acionável. Uma falha não alterará o manifesto nem substituirá uma
aula já publicada.

## 13. Verificação

Os testes automatizados cobrirão:

- validação estrutural do YAML;
- estados e papéis permitidos;
- existência e tipos dos nós referenciados no grafo;
- coerência entre conteúdo curricular, tópico e referência;
- preservação do manifesto durante a regeneração do dossiê;
- exclusão de tópicos rejeitados, adiados ou futuros;
- correspondência um para um entre ciclos da aula e do notebook;
- presença e conteúdo permitido em `Aplicação no notebook`;
- ausência das categorias de conteúdo computacional proibidas;
- rastreabilidade das referências e páginas;
- existência, tipo, ordem e rastreabilidade dos recursos discentes;
- correspondência exata entre `recursos_discentes` e as subseções de `Estudo e
  exercícios`;
- independência entre o tipo da fonte e sua função como material didático ou
  exercício indicado;
- distinção entre rascunho e material publicável.

Validações textuais não provarão a correção matemática nem a qualidade da
síntese entre autores. Esses aspectos permanecerão sob revisão docente antes
da publicação. A validação de conteúdo computacional não poderá rejeitar o uso
legítimo de funções matemáticas ou estatísticas em notação formal.

## 14. Piloto da Aula 2

O piloto deverá demonstrar o fluxo completo até a etapa compatível com a
decisão docente:

1. extrair do cronograma o escopo de `u1_a02`;
2. localizar no grafo os tópicos e referências candidatos;
3. consultar as páginas originais necessárias;
4. gerar `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml` com candidatos,
   evidências de leitura e decisões pendentes;
5. renderizar `.interno/prof/aulas/2026-2/u1_a02/dossie.md` exclusivamente a
   partir desse YAML;
6. aguardar a seleção docente;
7. validar o manifesto selecionado;
8. gerar a aula teórica;
9. verificar a correspondência de cada ciclo com sua aplicação no notebook.

A etapa 8 não será executada antes da seleção docente. A aprovação da
arquitetura não equivale à aprovação automática dos tópicos ou referências da
Aula 2.

## 15. Migração do modelo anterior

O novo contrato substitui, para as aulas produzidas por este pipeline, as
regras do modelo anterior que exigiam no próprio Markdown pacotes, funções,
operações e verificação computacional. Essas responsabilidades passam ao
notebook.

As exigências anteriores de motivação, fundamentação científica, resolução
manual quando pertinente, interpretação, rastreabilidade, estudo e exercícios
serão preservadas e adaptadas à exposição formal.

A migração geral das aulas somente será planejada depois da aprovação do
piloto. Arquivos já removidos ou modificados no worktree não serão restaurados,
substituídos ou incorporados automaticamente.

## 16. Fora do escopo do piloto

Não integram o primeiro incremento:

- regeneração das demais aulas;
- criação ou reformulação do notebook da Aula 2;
- alteração do grafo para incluir nós de aula;
- produção automática de provas ou avaliações;
- escolha automática de tópicos ou referências;
- demonstrações formais extensas por padrão;
- publicação de uma aula com notebook ausente;
- restauração dos arquivos atualmente removidos no worktree.

## 17. Critérios de aceite

O desenho estará implementado no piloto quando:

- o dossiê for reproduzível a partir das autoridades declaradas;
- o YAML conservar integralmente as evidências de leitura, os candidatos e as
  decisões docentes;
- referências múltiplas puderem ser compatibilizadas sem troca silenciosa de
  notação;
- a geração aceitar somente tópicos e referências aprovados;
- a aula apresentar formalismo aplicado e não contiver conteúdo computacional;
- cada ciclo possuir uma subseção `Aplicação no notebook` vinculada ao ciclo
  correspondente;
- erros de escopo, rastreabilidade e publicação forem detectados antes de
  sobrescrever qualquer saída;
- o piloto não modificar as remoções já existentes no worktree.
