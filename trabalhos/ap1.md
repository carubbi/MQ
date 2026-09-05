# AP1 — Análise exploratória do preço de venda de imóveis residenciais

## Contexto

A base reúne informações sobre imóveis residenciais, seus preços de venda e suas características. Antes de calcular probabilidades ou ajustar modelos, é necessário conhecer a estrutura, a qualidade e o comportamento dos dados.

## Pergunta de pesquisa

Como se distribuem e variam os preços de venda de imóveis residenciais?

## Objetivo da investigação

Caracterizar a distribuição e a variabilidade dos preços de venda e investigar suas relações com características físicas, qualitativas e temporais dos imóveis.

## Dados e característica atribuída

O grupo utilizará o arquivo bruto fornecido pelo professor, conforme a especificação geral. O professor atribuirá uma característica qualitativa $B$ diferente a cada grupo, mas não fornecerá uma base preparada nem classificará previamente os valores ausentes.

## Carregamento dos dados

Uma célula de código exclusiva deverá carregar `data/raw/AmesHousing.txt`. A cópia bruta será preservada sem alterações. Caminho, procedimento de leitura, dimensões, unidade de análise e inspeção inicial deverão aparecer em etapas separadas.

## Etapas obrigatórias

O conjunto mínimo será composto por seis tabelas ou resumos tabulares e seis figuras. Figuras com dois painéis contarão como uma figura. Não deverão ser acrescentadas visualizações que apenas repitam a mesma informação sem nova finalidade analítica.

### 1. Importação e rastreabilidade

- Registrar a identificação e a procedência do arquivo fornecido.
- Importar o arquivo bruto sem alterar a cópia armazenada em `data/raw/`.
- Verificar separador, codificação, dimensões e unidade de análise.
- Identificar os nomes originais das variáveis necessárias.
- Documentar eventual normalização dos nomes.
- Apresentar o nome legível de cada variável seguido do nome original entre parênteses.

### 2. Qualidade e preparação

- Inspecionar tipos de dados.
- Identificar conversões necessárias.
- Investigar duplicidades e valores ausentes.
- Consultar a documentação para interpretar os códigos encontrados.
- Justificar cada tratamento.
- Preservar uma cópia lógica dos dados originais.
- Apresentar um resumo tabular dos tipos, valores ausentes e duplicidades.
- Inspecionar e documentar as colunas `Fireplaces`, `Mas Vnr Area`, `Year Remod/Add` e `Year Built`, necessárias à trilha Binomial da AP2 e, quando corresponderem à característica $B$, à modelagem da AP3.
- Não classificar automaticamente valores ausentes de `Mas Vnr Area` como ausência de revestimento; preservar ou tratar esses valores com justificativa documentada.

### 3. Análise univariada

Analisar:

- preço de venda (`SalePrice`);
- área construída (`Gr Liv Area`);
- característica qualitativa $B$, identificada por seu nome legível e pelo nome original atribuído.

Para preço de venda (`SalePrice`) e área construída (`Gr Liv Area`):

- apresentar, em uma mesma tabela, medidas de posição, dispersão e forma;
- construir histogramas em dois painéis da mesma figura;
- explicitar nos eixos as variáveis e suas unidades.

Para a característica qualitativa $B$:

- apresentar uma tabela de frequências absolutas e relativas;
- construir um gráfico de barras;
- preservar no título ou na legenda o nome legível e o nome original.

### 4. Valores discrepantes

Aplicar obrigatoriamente as cercas de Tukey às variáveis quantitativas selecionadas:

$$
LI=Q_1-1{,}5\,IQR
\quad\text{e}\quad
LS=Q_3+1{,}5\,IQR,
\tag{1.1}
$$

em que $IQR=Q_3-Q_1$.

Apresentar uma tabela com $Q_1$, $Q_3$, $IQR$, limite inferior, limite superior e quantidade de casos sinalizados para preço de venda (`SalePrice`) e área construída (`Gr Liv Area`). Construir os respectivos boxplots em dois painéis da mesma figura.

Os valores sinalizados deverão ser investigados. O grupo decidirá entre manter, corrigir ou excluir, com justificativa contextual. Não será aceita remoção automática. Eventual exclusão deverá ser acompanhada de comparação com os resultados obtidos sem exclusão.

### 5. Característica qualitativa $B$

Antes de comparar os preços entre as categorias:

- descrever o significado de $B$;
- apresentar seu nome legível seguido do nome original no arquivo;
- examinar frequências, categorias raras e valores ausentes;
- justificar eventual agrupamento;
- estabelecer os rótulos finais das categorias.

O agrupamento final deverá considerar significado, quantidade de observações e possibilidade de comparação. A decisão deverá ser registrada antes da análise do preço entre as categorias e preservada para a AP3.

### 6. Análise bivariada

#### 6.1 Preço de venda (`SalePrice`) e ano da venda (`Yr Sold`)

Para preço de venda (`SalePrice`) e ano da venda (`Yr Sold`):

- apresentar uma tabela com a quantidade de vendas e a mediana do preço por ano;
- construir um gráfico de linha da mediana anual do preço;
- manter os anos em ordem cronológica;
- não conectar preços de imóveis individuais;
- discutir que as diferenças podem decorrer da composição dos imóveis vendidos, da inflação e das condições do mercado;
- não interpretar o gráfico como tendência causal, trajetória do mesmo imóvel ou análise formal de série temporal.

O mês da venda (`Mo Sold`) poderá ser utilizado como extensão descritiva, mas não substituirá a agregação anual obrigatória.

#### 6.2 Preço de venda (`SalePrice`) e área construída (`Gr Liv Area`)

Para preço de venda (`SalePrice`) e área construída (`Gr Liv Area`):

- construir o diagrama de dispersão;
- examinar direção, forma, grupos e valores discrepantes;
- calcular a correlação linear de Pearson;
- interpretar intensidade e direção sem atribuir causalidade;
- indicar como valores discrepantes podem afetar o coeficiente.

#### 6.3 Preço de venda (`SalePrice`) e característica qualitativa $B$

Para preço de venda (`SalePrice`) e característica qualitativa $B$:

- apresentar uma tabela com quantidade, mediana, $Q_1$, $Q_3$ e $IQR$ do preço por categoria;
- construir boxplots do preço segundo as categorias de $B$;
- interpretar diferenças de posição, dispersão e valores discrepantes;
- não realizar inferência nem atribuir causalidade às diferenças observadas.

### 7. Exportação do dado pré-processado

O notebook deverá encerrar com um registro explícito de:

- nomes originais e nomes utilizados;
- tratamentos realizados;
- agrupamento final de $B$;
- rótulos finais das categorias de $B$;
- mapeamento dos nomes originais, incluindo `SalePrice`, `Gr Liv Area`, `Yr Sold` e, se utilizado, `Mo Sold`;
- caminho ou procedimento para reproduzir a versão organizada;
- arquivo processado `data/processed/AmesHousing.csv`.

## Limitações mínimas

Discutir:

- natureza observacional dos dados;
- período e local abrangidos;
- limites de representatividade;
- efeito potencial das decisões de preparação;
- diferença entre valor discrepante e erro.
- diferença entre associação e causalidade.
