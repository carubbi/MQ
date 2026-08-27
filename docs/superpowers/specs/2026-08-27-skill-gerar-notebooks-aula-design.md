# Skill para geração de notebooks de aula — desenho

**Data:** 27 de agosto de 2026

**Estado:** desenho aprovado

## 1. Objetivo

Criar a skill pessoal `gerar-notebooks-aula` para planejar, gerar e validar o
par de notebooks associado a uma aula formal já publicada:

```text
notebooks/<aula-id>.ipynb
notebooks/resolvidos/<aula-id>.ipynb
```

O notebook discente oferece somente a estrutura inicial para que o estudante
construa a solução. O notebook resolvido contém todas as células necessárias à
aplicação computacional aprovada. A skill preserva a correspondência dos dois
artefatos com os ciclos conceituais da aula sem generalizar quantidades ou
operações particulares da Aula 2.

## 2. Princípio de autoridade

O manifesto aprovado e a aula pública determinam o objetivo, a questão, o
contraste e a evidência de cada aplicação no notebook. Esses documentos não
determinam, por si sós, conjunto de dados, variáveis, operações, células,
métodos ou saídas.

A skill não inventará essas decisões. Antes de gerar arquivos públicos, ela
proporá um plano operacional por ciclo, registrará a proposta em artefato
privado e aguardará aprovação docente explícita.

## 3. Artefatos

A skill operará sobre:

```text
.interno/prof/aulas/<semestre>/<aula-id>/notebook.yaml
notebooks/<aula-id>.ipynb
notebooks/resolvidos/<aula-id>.ipynb
```

O arquivo `notebook.yaml` será privado, ignorado pelo Git e canônico para as
decisões computacionais da aula. Ele registrará:

- versão do contrato;
- estado `em_planejamento` ou `aprovado`;
- semestre, ID e título da aula;
- fonte e forma de carregamento dos dados;
- objetos, variáveis ou colunas necessários;
- bibliotecas autorizadas;
- seção inicial de carregamento, quando pertinente;
- ciclos vinculados aos IDs do manifesto;
- operações previstas, uma por célula;
- comentário inicial, código e saída esperada de cada operação;
- restrições específicas da aula.

O plano somente poderá assumir `aprovado` após confirmação explícita do
docente. A skill não adicionará arquivos sob `.interno/` ao Git.

## 4. Portão de geração

A geração exigirá cumulativamente:

1. manifesto válido e aprovado, sem decisão pendente;
2. aula pública existente;
3. correspondência entre todos os ciclos da aula, do manifesto e do plano;
4. uma aplicação no notebook aprovada para cada ciclo;
5. `notebook.yaml` no estado `aprovado`;
6. fonte de dados, operações e saídas sem pendências.

Se uma condição falhar, a skill interromperá o fluxo sem alterar os notebooks
públicos.

## 5. Planejamento operacional

Para cada seção e ciclo, a proposta apresentada ao docente incluirá:

- fonte de dados e variáveis utilizadas;
- objetivo computacional;
- operações, na ordem das células;
- comentário inicial de cada célula;
- código proposto;
- tipo e conteúdo esperado da saída;
- correspondência com a evidência didática;
- conceitos computacionais necessários.

O plano deve empregar apenas conceitos estatísticos e computacionais já
disponíveis ao estudante. Mudanças em dados, operações, células, saídas ou
alcance conceitual devolvem o plano a `em_planejamento` e exigem nova aprovação.
Normalização de metadados e correção de IDs inválidos não reabrem decisões
didáticas.

## 6. Estrutura compartilhada

Os dois notebooks compartilharão, com IDs, conteúdo e ordem idênticos:

1. cabeçalho institucional canônico;
2. título da aula;
3. seção de carregamento, quando houver dados externos;
4. uma seção para cada ciclo aprovado, na ordem da aula.

O cabeçalho será obtido de
`gerar-aula-formal/references/cabecalho-aula.md`. A skill não copiará o
cabeçalho da Aula 1 nem manterá uma segunda versão do bloco institucional.

Não haverá quantidade fixa de seções. A topologia será derivada do plano
aprovado.

## 7. Notebook discente

O notebook discente conterá uma única célula de código vazia imediatamente
depois de cada seção operacional. O estudante será responsável por criar as
células adicionais necessárias.

Todas as células de código terão:

- fonte vazia;
- `execution_count` nulo;
- lista de saídas vazia.

O notebook não incluirá respostas, comentários-guia, explicações da solução ou
indicação da quantidade de células que o estudante deverá acrescentar.

## 8. Notebook resolvido

O notebook resolvido conterá todas as operações aprovadas no plano. Cada
operação ou saída independente ocupará uma célula própria.

Cada célula de código:

- começará com um único comentário curto em português, formulado com verbo no
  infinitivo e orientado à finalidade;
- usará variáveis curtas e significativas;
- manterá uma operação principal por linha;
- empregará variáveis intermediárias quando houver mais de uma transformação;
- evitará encadeamento de métodos, funções auxiliares e construções avançadas
  quando uma sequência simples comunicar melhor o procedimento.

Saídas escalares ou textos simples serão o padrão. `Series`, listas, tabelas,
gráficos e outras estruturas conjuntas somente serão usados quando forem o
objeto necessário da análise e estiverem explicitamente aprovados no plano.
Células de preparação, carregamento ou seleção poderão não produzir saída.

A quantidade de células e saídas será derivada do plano. Os totais de 12
células discentes, 25 células resolvidas e 18 células de código resolvidas são
particulares da Aula 2 e não constituem regra da skill.

## 9. Geração protegida

A skill criará inicialmente os dois notebooks em arquivos temporários. Arquivos
públicos existentes permanecerão intactos até a conclusão de todas as
validações.

Antes de substituir um notebook existente, a skill comparará a versão gerada
com a pública. Alterações manuais que não estejam representadas no plano serão
tratadas como decisão docente e bloquearão a substituição silenciosa.

A promoção escreverá somente:

```text
notebooks/<aula-id>.ipynb
notebooks/resolvidos/<aula-id>.ipynb
```

A skill não modificará a aula, o manifesto, a Aula 1 ou notebooks fora do ID
em processamento. Ela não fará commit automaticamente.

## 10. Validador genérico

A skill incluirá um validador determinístico orientado por `notebook.yaml`. O
validador verificará:

- JSON válido e leitura por `nbformat`;
- identidade e ordem das células Markdown compartilhadas;
- uma célula vazia por seção no notebook discente;
- correspondência entre operações aprovadas e células resolvidas;
- comentário inicial único em cada célula resolvida;
- bibliotecas e construções sintáticas autorizadas;
- execução sequencial completa do notebook resolvido;
- ausência de erros;
- quantidade, tipo e conteúdo essencial das saídas conforme o plano;
- coerência dos resultados com o conjunto de dados;
- vínculos entre manifesto, aula e notebooks;
- ausência de problemas detectados por `git diff --check` nos arquivos
  promovidos.

O validador examinará células, objetos e resultados; presença textual isolada
no JSON não constituirá evidência suficiente.

## 11. Fontes de dados e falhas

A validação final executará o código aprovado com a fonte declarada no plano.
Uma fonte remota inacessível, alterada ou incompatível bloqueará a promoção.

Um arquivo local equivalente poderá ser usado apenas para diagnóstico. Ele não
substituirá silenciosamente a fonte aprovada nem validará a versão final.

A skill também interromperá o fluxo quando houver:

- operação ambígua;
- resultado incompatível com a evidência didática;
- conceito ainda não apresentado;
- divergência manual não resolvida;
- falha de execução ou validação.

O bloqueio identificará a seção ou o ciclo afetado e preservará os notebooks
públicos anteriores.

## 12. Fluxo

1. Validar o manifesto e localizar a aula pública.
2. Ler todas as aplicações no notebook.
3. Inspecionar dados e recursos computacionais existentes.
4. Propor o plano operacional por seção e ciclo.
5. Gravar `notebook.yaml` com estado `em_planejamento`.
6. Apresentar dados, operações, células, saídas e correspondência didática.
7. Aguardar aprovação explícita do docente.
8. Marcar o plano como `aprovado`.
9. Gerar temporariamente os notebooks discente e resolvido.
10. Executar o resolvido e validar os dois artefatos.
11. Comparar com versões públicas existentes.
12. Promover os arquivos validados.
13. Apresentar síntese, validações e diferenças produzidas.

## 13. Limites

Esta skill não:

- seleciona ciclos ou conteúdos teóricos;
- modifica decisões do manifesto;
- gera ou revisa a aula formal;
- define automaticamente atividades computacionais a partir de descrições
  pedagógicas genéricas;
- usa a Aula 2 como molde rígido;
- altera notebooks não vinculados à aula em processamento;
- rastreia artefatos privados;
- publica notebooks que não tenham sido executados e validados;
- substitui a aprovação docente do plano operacional.
