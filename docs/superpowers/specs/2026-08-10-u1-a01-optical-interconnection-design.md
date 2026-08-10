# Adaptação da Aula 1 ao Optical Interconnection Network

## Objetivo

Substituir o Internet Firewall Data pelo Optical Interconnection Network na
Aula 1 da Unidade I, preservando o objetivo de ambientação computacional e de
reconhecimento da estrutura tabular. A adaptação abrange somente
`aulas/u1_a01_ambientacao_dados.md`; o notebook e as demais aulas permanecerão
inalterados até aprovação separada.

## Fonte e unidade de análise

O arquivo será carregado diretamente da distribuição oficial do UCI Machine
Learning Repository. Cada linha será definida como uma medição de desempenho
obtida para uma configuração da simulação de uma rede óptica multiprocessada.
Não será tratada como nó, thread, pacote ou execução independente sem a
qualificação fornecida pela documentação.

## Tratamento do arquivo na Aula 1

O CSV será lido como publicado, com `sep=";"` e `decimal=","`. A aula não
selecionará colunas, removerá espaços dos nomes, excluirá campos vazios nem
corrigirá valores suspeitos. A inspeção deverá evidenciar:

- 640 linhas e 15 colunas carregadas;
- dez colunas documentadas e cinco colunas vazias adicionais;
- espaço final no nome `Processor Utilization `;
- tipos computacionais resultantes da leitura;
- valores de `Channel Utilization` que exigem verificação posterior.

Essas características serão registradas como propriedades do arquivo bruto,
sem antecipar os procedimentos da aula de qualidade e pré-processamento.

## Estrutura didática preservada

A aula manterá três ciclos:

1. menção ao notebook para as instruções de Python e bibliotecas;
2. fonte, registros, colunas e unidade de análise;
3. inspeção computacional do dataframe bruto.

Os casos reduzidos utilizarão linhas do arquivo oficial. Uma coluna `ID*`
poderá ser acrescentada somente para localizar a linha original, com o
asterisco indicando que não pertence ao dataset.

## Conteúdo contextual

O contexto recorrente apresentará as cinco variáveis de configuração:
`Node Number`, `Thread Number`, `Spatial Distribution`,
`Temporal Distribution` e `T/R`; e as cinco métricas de desempenho:
`Processor Utilization `, `Channel Waiting Time`, `Input Waiting Time`,
`Network Response Time` e `Channel Utilization`.

As abreviações espaciais `UN`, `HR`, `BR` e `PS` serão definidas. `T/R` será
apresentada como a razão entre o tempo de transferência da mensagem e o tempo
de execução da thread. A inconsistência entre alguns valores e a descrição da
fonte será registrada como questão de qualidade, não resolvida nesta aula.

## Aplicação computacional

O código permanecerá curto e didático. A leitura, a inspeção de dimensões, os
nomes, as primeiras linhas, os tipos e as cardinalidades ocorrerão em operações
separadas. A saída bruta deverá sustentar a distinção entre:

- estrutura efetivamente carregada;
- variáveis documentadas;
- significado atribuído pela fonte;
- problemas que dependem de avaliação posterior.

## Critérios de aceitação

A adaptação estará correta quando:

- não restarem referências ao Internet Firewall Data na Aula 1;
- o arquivo oficial for carregado sem limpeza antecipada;
- a unidade de análise não for confundida com nó, pacote ou thread;
- os casos reduzidos forem compostos por dados do arquivo;
- as 15 colunas brutas e as dez variáveis documentadas forem distinguidas;
- os problemas de estrutura e valores forem reconhecidos, mas não corrigidos;
- os ciclos, exercícios existentes, duração e resultado de aprendizagem forem
  preservados ou ajustados somente ao novo contexto;
- nenhuma outra aula ou notebook for alterado nesta etapa.

## Verificação

Após a edição, serão verificados o diff restrito ao arquivo da Aula 1, a
ausência de referências residuais ao firewall, a correspondência entre tabelas
e registros do CSV e a execução isolada do código de carregamento e inspeção.
