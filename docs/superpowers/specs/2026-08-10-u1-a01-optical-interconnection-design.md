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

As variáveis serão descritas conforme a documentação da UCI:

| Variável no arquivo | Descrição documentada | Unidade |
| --- | --- | --- |
| `Node Number` | Número de nós da rede: 16 para a organização $4\times4$ e 64 para a organização $8\times8$. | nós |
| `Thread Number` | Número de threads existentes em cada nó no início da simulação. | threads por nó |
| `Spatial Distribution` | Modelo espacial do tráfego sintético que determina a distribuição das origens e dos destinos das mensagens. | não se aplica |
| `Temporal Distribution` | Modelo temporal de geração dos pacotes, nas modalidades cliente-servidor ou assíncrona. | não se aplica |
| `T/R` | Razão entre o tempo de transferência da mensagem $T$ e o tempo de execução da thread $R$. | adimensional |
| `Processor Utilization ` | Proporção do tempo em que as threads permanecem em execução no processador. | proporção do tempo* |
| `Channel Waiting Time` | Tempo médio de espera de um pacote na fila do canal de saída até o atendimento pelo canal. | não informada pela UCI |
| `Input Waiting Time` | Tempo médio de espera de um pacote até o atendimento pelo processador. | não informada pela UCI |
| `Network Response Time` | Tempo entre a entrada de uma mensagem de requisição na fila do canal de saída e o recebimento da mensagem de resposta correspondente na fila de entrada. | não informada pela UCI |
| `Channel Utilization` | Proporção do tempo em que o canal permanece ocupado transferindo pacotes pela rede. | proporção do tempo* |

Em `Spatial Distribution`, as abreviações serão definidas como `UN`
(*Uniform*), `HR` (*Hot Region*), `BR` (*Bit Reverse*) e `PS`
(*Perfect Shuffle*). Em `Temporal Distribution`, `Client-Server` representará
o tráfego em que um nó servidor responde às mensagens dos clientes;
`Asynchronous` representará o tráfego inicialmente gerado de modo independente,
cuja geração posterior pode depender das mensagens recebidas.

A documentação não será ampliada com unidades que ela não declara. A
inconsistência entre alguns valores e a descrição da fonte será registrada como
questão de qualidade, não resolvida nesta aula.

\* A documentação descreve as utilizações como percentuais do tempo, enquanto
os valores regulares do arquivo aparecem predominantemente na escala de 0 a 1.
A aula registrará essa diferença sem converter ou corrigir os dados.

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
- as dez variáveis forem descritas, com suas unidades ou a ausência delas,
  conforme a documentação da UCI;
- as 15 colunas brutas e as dez variáveis documentadas forem distinguidas;
- os problemas de estrutura e valores forem reconhecidos, mas não corrigidos;
- os ciclos, exercícios existentes, duração e resultado de aprendizagem forem
  preservados ou ajustados somente ao novo contexto;
- nenhuma outra aula ou notebook for alterado nesta etapa.

## Verificação

Após a edição, serão verificados o diff restrito ao arquivo da Aula 1, a
ausência de referências residuais ao firewall, a correspondência entre tabelas
e registros do CSV e a execução isolada do código de carregamento e inspeção.
