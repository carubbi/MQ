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

| Variável no arquivo | Unidade | Descrição documentada |
| --- | --- | --- |
| `Node Number` | nós | Número de nós da rede: 16 para a organização $4\times4$ e 64 para a organização $8\times8$. |
| `Thread Number` | threads por nó | Número de threads existentes em cada nó no início da simulação. |
| `Spatial Distribution` | não se aplica | Modelo espacial do tráfego sintético que determina a distribuição das origens e dos destinos das mensagens. |
| `Temporal Distribution` | não se aplica | Modelo temporal de geração dos pacotes, nas modalidades cliente-servidor ou assíncrona. |
| `T/R` | adimensional | Razão entre o tempo de transferência da mensagem $T$ e o tempo de execução da thread $R$. |
| `Processor Utilization ` | proporção, entre 0 e 1\*\* | Proporção do tempo em que as threads permanecem em execução no processador. |
| `Channel Waiting Time` | ciclos de relógio* | Tempo médio de espera de um pacote na fila do canal de saída até o atendimento pelo canal. |
| `Input Waiting Time` | ciclos de relógio* | Tempo médio de espera de um pacote até o atendimento pelo processador. |
| `Network Response Time` | ciclos de relógio* | Tempo entre a entrada de uma mensagem de requisição na fila do canal de saída e o recebimento da mensagem de resposta correspondente na fila de entrada. |
| `Channel Utilization` | proporção, entre 0 e 1\*\* | Proporção do tempo em que o canal permanece ocupado transferindo pacotes pela rede. |

Em `Spatial Distribution`, as abreviações serão definidas como `UN`
(*Uniform*), `HR` (*Hot Region*), `BR` (*Bit Reverse*) e `PS`
(*Perfect Shuffle*). Em `Temporal Distribution`, `Client-Server` representará
o tráfego em que um nó servidor responde às mensagens dos clientes;
`Asynchronous` representará o tráfego inicialmente gerado de modo independente,
cuja geração posterior pode depender das mensagens recebidas.

A documentação não declara explicitamente a unidade de cada métrica temporal.
Quando a unidade for inferida, a aula identificará a inferência e apresentará
sua justificativa. A inconsistência entre alguns valores e a descrição da fonte
será registrada como questão de qualidade, não resolvida nesta aula.

\* Unidade inferida: a documentação define o tempo de transferência $T$ e o
tempo de execução $R$ em ciclos de relógio. Como espera e resposta são durações
produzidas pela mesma simulação, serão interpretadas em ciclos de relógio. A
fonte não declara essa unidade separadamente para cada métrica de saída.

\*\* A documentação descreve as utilizações como percentuais do tempo, enquanto
os valores regulares do arquivo aparecem na escala de 0 a 1. Assim, serão lidos
como proporções; a expressão em porcentagem exige multiplicação por 100. A aula
registrará essa diferença sem converter ou corrigir os dados brutos.

### Como interpretar os valores

A descrição das variáveis será seguida por uma tabela de leitura de valores. Os
exemplos serão retirados do arquivo oficial e não serão apresentados como
medições de pacotes ou nós individuais.

| Variável | Exemplo | Como interpretar |
| --- | ---: | --- |
| `Node Number` | `64` | A rede simulada contém 64 nós, organizados em uma topologia $8\times8$. |
| `Thread Number` | `4` | Cada nó iniciou a simulação com quatro threads. |
| `Spatial Distribution` | `UN` | As origens e os destinos das mensagens seguem uma distribuição uniforme. |
| `Temporal Distribution` | `Client-Server` | Clientes enviam requisições e o servidor produz as respostas correspondentes. |
| `T/R` | `0,4` | O tempo de transferência corresponde a 40% do tempo de execução da thread. |
| `Processor Utilization ` | `0,84` | O processador permaneceu executando threads durante aproximadamente 84% do tempo. |
| `Channel Waiting Time` | `61,85` | Os pacotes aguardaram, em média, 61,85 ciclos de relógio na fila do canal de saída. |
| `Input Waiting Time` | `235,78` | Os pacotes aguardaram, em média, 235,78 ciclos de relógio para serem atendidos pelo processador. |
| `Network Response Time` | `1256,05` | Entre uma requisição e a resposta correspondente transcorreram, em média, 1.256,05 ciclos de relógio. |
| `Channel Utilization` | `0,77` | O canal permaneceu ocupado transmitindo pacotes durante aproximadamente 77% do tempo. |

As cinco métricas de desempenho serão apresentadas como médias produzidas pela
simulação. Elas não descrevem um pacote, nó ou thread individual.

### Como interpretar as métricas conjuntamente

As utilizações não serão classificadas isoladamente como boas ou ruins. A
leitura conjunta relacionará:

- `Processor Utilization ` com `Input Waiting Time`;
- `Channel Utilization` com `Channel Waiting Time`;
- as duas esperas e as utilizações com `Network Response Time`.

Utilização elevada acompanhada de espera elevada poderá indicar saturação.
Utilização baixa acompanhada de espera baixa poderá representar baixa demanda,
sem constituir necessariamente um problema.

Valores de `Channel Utilization` superiores a 1 não receberão interpretação
como proporção. Eles serão identificados na Aula 1 e investigados posteriormente
na aula de qualidade e pré-processamento.

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
- cada variável receber um exemplo de leitura contextualizada;
- as utilizações e os tempos de espera forem interpretados conjuntamente;
- as 15 colunas brutas e as dez variáveis documentadas forem distinguidas;
- os problemas de estrutura e valores forem reconhecidos, mas não corrigidos;
- os ciclos, exercícios existentes, duração e resultado de aprendizagem forem
  preservados ou ajustados somente ao novo contexto;
- nenhuma outra aula ou notebook for alterado nesta etapa.

## Verificação

Após a edição, serão verificados o diff restrito ao arquivo da Aula 1, a
ausência de referências residuais ao firewall, a correspondência entre tabelas
e registros do CSV e a execução isolada do código de carregamento e inspeção.
