# Remoção dos ciclos e piloto da Aula 7

## Objetivo

Remover o conceito estrutural de ciclos do fluxo ativo de curadoria, geração de
aulas e geração de notebooks. A Aula 7 será o primeiro conjunto produzido com o
novo contrato. As demais aulas e notebooks somente serão migrados após a
validação docente do piloto.

## Princípio editorial

A aula pública apresenta conceitos. O notebook desenvolve aplicações.

A aula pode conter motivação, definições, notação, fórmulas, condições,
propriedades, interpretações e exemplificações mínimas necessárias à compreensão.
Ela não contém implementação, exploração de dados, gráficos computacionais nem
resoluções extensas com conjuntos de dados.

O notebook contém preparação de dados, cálculos, código, gráficos, comparações,
resultados e interpretação aplicada. A organização computacional usa atividades,
sem reproduzir ciclos sob outro nome.

## Contrato de curadoria

`selecao.yaml` passa ao contrato `2.0`, incompatível com o contrato `1.3`. A ordem de
`topicos` estabelece a sequência pedagógica.

São removidos:

- `ciclos`;
- `aplicacao_notebook`;
- `atividade_resolvida` associada a ciclo;
- complexidade, duração mínima e justificativa de partição por ciclo.

Permanecem:

- identificação e duração total da aula;
- escopo incluído, excluído e reservado;
- tópicos e seus estados;
- referências, páginas, papéis e compatibilizações;
- recursos discentes;
- abertura e fechamento do planejamento temporal.

O tempo disponível para desenvolvimento é derivado da duração total menos
abertura e fechamento. Não há divisão temporal obrigatória por tópico ou bloco.

Guias docentes podem misturar fundamentação e aplicação. Durante a curadoria,
cada trecho deve ser classificado pelo destino:

- aula: conteúdo conceitual;
- notebook: conteúdo aplicado ou computacional.

A estrutura do guia não determina a estrutura da aula pública.

## Contrato da aula pública

A aula é organizada diretamente pelos tópicos selecionados, sem títulos, IDs ou
menções a ciclos. Para cada tópico, use somente as partes conceituais pertinentes
e evite repetir definições já apresentadas.

Uma exemplificação curta pode esclarecer uma fórmula ou interpretação. Ela não
pode se transformar em aplicação completa, roteiro computacional ou análise do
conjunto de dados.

Ao final, a aula contém um único vínculo para o notebook correspondente. Não há
seção `Aplicação no notebook` repetida por tópico.

## Contrato do notebook

O plano computacional passa do contrato `1.0` ao contrato `2.0` e substitui
`ciclos` por `atividades`. Cada atividade possui:

- ID próprio no formato `atividade-NN`;
- título e objetivo;
- tópicos selecionados que aplica;
- pergunta investigada;
- evidência esperada;
- origem rastreável, bibliográfica ou autoral;
- operações computacionais ordenadas.

Uma atividade pode integrar vários tópicos. Um tópico pode participar de mais de
uma atividade quando isso for necessário à investigação. Essa relação representa
cobertura aplicada, não uma partição conceitual da aula.

Os validadores devem rejeitar atividades que apontem para tópicos inexistentes ou
não selecionados. Uma origem bibliográfica deve apontar para referência e páginas
selecionadas; uma origem autoral deve trazer justificativa. A aprovação do plano
computacional continua separada da aprovação da aula.

No plano aprovado, todo tópico selecionado deve ser aplicado por ao menos uma
atividade. Isso assegura cobertura sem impor correspondência um para um.

## Alterações no fluxo ativo

A implementação abrange:

- `curar-aula-formal`;
- `gerar-aula-formal`;
- `gerar-notebooks-aula`;
- esquema, validação e renderização em `scripts/aulas`;
- testes dos contratos de curadoria e notebook;
- manifesto, dossiê, aula e notebooks da Aula 7.

As demais aulas, manifestos e notebooks não serão migrados durante o piloto.
Validadores podem deixar de aceitar seus contratos antigos; esses artefatos não
serão usados como prova de conformidade do novo fluxo até a migração posterior.

## Documentos legados

Os documentos anteriores existentes em `docs/superpowers/plans/` e
`docs/superpowers/specs/` serão movidos, preservando seus conteúdos e a mesma
subestrutura, para:

`.interno/bkp/docs/superpowers/`

A presente especificação permanece em `docs/superpowers/` enquanto orientar uma
alteração ativa. O material em `.interno/bkp/` não participa de validações nem de
buscas por contratos vigentes.

## Piloto da Aula 7

O guia `.interno/prof/guia/aula7_medidas_estatisticas.md` é uma fonte mista. Sua
fundamentação orienta a aula; implementações, aplicações e visualizações orientam
os notebooks.

O piloto produz, nesta ordem:

1. manifesto e dossiê da Aula 7 no novo contrato;
2. rascunho da aula conceitual para aprovação docente;
3. aula pública aprovada;
4. plano computacional por atividades;
5. notebooks discente e resolvido;
6. validação conjunta dos artefatos.

As aprovações exigidas pelas skills permanecem independentes. Aprovar este
desenho não aprova automaticamente manifesto, aula ou notebooks.

## Verificação

A alteração será validada por testes escritos antes das mudanças de contrato.
Eles devem cobrir:

- aceitação de manifesto aprovado sem ciclos;
- rejeição do campo legado `ciclos` no novo contrato;
- dossiê organizado por tópicos e sem seção de ciclos;
- plano de notebook com `atividades`;
- rejeição de tópico inexistente ou não selecionado em uma atividade;
- geração de notebooks sem IDs, títulos ou textos estruturais de ciclo;
- ausência de aplicação computacional na aula pública;
- presença das aplicações no notebook resolvido;
- validação formal das três skills modificadas.

Uma busca final pelo vocabulário legado será limitada aos arquivos ativos
alterados. Usos pertencentes ao domínio estudado, como ciclo de execução de
instruções, não são erros.

## Critério de conclusão do piloto

O piloto termina quando a Aula 7 e seus dois notebooks passam nas validações
estruturais e de execução e recebem aprovação docente. A migração das demais
aulas constitui uma etapa posterior e exige nova autorização.
