# AP2 — Auditoria de modelos probabilísticos

## Contexto

Na AP1, cada grupo preparou e explorou o conjunto de dados de imóveis residenciais. Nesta etapa, o professor atribuirá uma variável ou um evento e um modelo probabilístico candidato. O grupo deverá confrontar o modelo com os dados, verificar seus pressupostos e emitir um parecer fundamentado sobre sua adequação.

A finalidade não é confirmar o modelo atribuído. Um parecer de inadequação será válido quando sustentado pelo tipo da variável, pelo suporte, pelo mecanismo probabilístico, pelos resultados observados e pela simulação.

## Pergunta de pesquisa

O modelo probabilístico atribuído é adequado para representar o comportamento da variável ou do evento analisado?

## Objetivo da investigação

Avaliar criticamente a adequação de um modelo Binomial, de Poisson ou Normal a partir dos dados observados no Ames Housing, confrontando-os com as propriedades teóricas e os pressupostos do modelo atribuído.

## Atribuição da investigação

O professor atribuirá a cada grupo:

- uma variável ou um evento do conjunto de dados;
- um modelo candidato entre Binomial, Poisson e Normal.

A atribuição será registrada antes da análise e não poderá ser substituída em razão dos resultados encontrados.

### Trilha Binomial

O professor definirá um evento binário, como:

- presença de lareira, `Fireplaces > 0`;
- presença de revestimento de alvenaria, `Mas Vnr Area > 0`;
- registro de reforma, `Year Remod/Add > Year Built`.

O grupo representará o número de ocorrências do evento em $n=20$ seleções sob o modelo Binomial.

### Trilha Poisson

O professor indicará uma contagem discreta não negativa, como:

- número de lareiras (`Fireplaces`);
- capacidade da garagem (`Garage Cars`);
- número de banheiros (`Full Bath`);
- número de quartos (`Bedroom AbvGr`).

Essas variáveis são contagens limitadas por características do imóvel e não correspondem necessariamente a ocorrências em um intervalo. Essa possível incompatibilidade integra a auditoria e não deverá ser omitida.

### Trilha Normal

O professor indicará uma variável quantitativa contínua, como:

- preço de venda (`SalePrice`);
- área construída (`Gr Liv Area`);
- área do lote (`Lot Area`).

O grupo deverá examinar localização, dispersão, simetria, caudas e valores discrepantes. O histograma e o Q–Q plot serão obrigatórios e deverão ser interpretados conjuntamente. A distribuição Normal não poderá ser escolhida ou aceita apenas pela aparência do histograma nem pelo alinhamento parcial dos pontos no Q–Q plot.

## Carregamento dos dados

Uma célula de código exclusiva deverá carregar `data/processed/AmesHousing.csv`, produzido na AP1. O Ames Housing será a única base de dados da AP2. Poderão ser realizadas verificações mínimas de dimensões, tipos e valores ausentes da variável atribuída. A limpeza geral e as decisões registradas na AP1 não serão redefinidas.

## Etapas obrigatórias

### 1. Delimitação da variável aleatória

O grupo deverá:

- identificar a unidade de análise;
- descrever em linguagem natural a variável ou o evento atribuído;
- definir a variável aleatória e seus valores possíveis;
- classificá-la como discreta ou contínua;
- indicar seu suporte observado e o suporte previsto pelo modelo;
- formular a pergunta específica da investigação.

### 2. Compatibilidade inicial do modelo atribuído

Antes de realizar os cálculos e as simulações, o grupo deverá confrontar o modelo atribuído com:

- o tipo da variável;
- o suporte;
- o mecanismo probabilístico;
- os parâmetros;
- os pressupostos essenciais.

A compatibilidade inicial deverá ser apresentada de forma sintética antes de qualquer comparação gráfica. Ela orientará a auditoria, mas não antecipará o parecer final.

### 3. Descrição empírica

O grupo deverá apresentar:

- quantidade de observações válidas e valores ausentes;
- tabela de frequências relativas para variável discreta ou medidas descritivas para variável contínua;
- representação gráfica coerente com o tipo da variável;
- média e variância observadas;
- características relevantes para a auditoria, como concentração, assimetria, caudas, excesso de zeros ou limites naturais.

O gráfico deverá possuir título, eixos, unidades e interpretação. Não serão exigidas visualizações redundantes.

Na trilha Normal, a descrição empírica deverá incluir um histograma e um Q–Q plot. A interpretação do Q–Q plot deverá distinguir o alinhamento na região central de desvios nas caudas e de observações discrepantes.

### 4. Modelo candidato e parâmetros

O grupo deverá definir o modelo, seus parâmetros e suas propriedades.

#### Binomial

Definir:

$$
X\colon \mathrm{Binomial}(20,p),
\tag{2.1}
$$

em que $p$ é a frequência relativa observada do evento atribuído. Calcular e interpretar:

$$
\mathrm{E}(X)=20p
\quad\text{e}\quad
\mathrm{Var}(X)=20p(1-p).
\tag{2.2}
$$

#### Poisson

Definir:

$$
X\colon \mathrm{Poisson}(\lambda),
\tag{2.3}
$$

utilizando a média observada como calibração empírica de $\lambda$. Calcular e interpretar:

$$
\mathrm{E}(X)=\lambda
\quad\text{e}\quad
\mathrm{Var}(X)=\lambda.
\tag{2.4}
$$

A igualdade teórica entre média e variância deverá ser confrontada com os dados, sem ser tratada isoladamente como prova de adequação.

#### Normal

Definir:

$$
X\colon \mathrm{Normal}(\mu,\sigma^2),
\tag{2.5}
$$

utilizando a média e o desvio-padrão observados como calibração empírica de $\mu$ e $\sigma$. Interpretar:

$$
\mathrm{E}(X)=\mu
\quad\text{e}\quad
\mathrm{Var}(X)=\sigma^2.
\tag{2.6}
$$

Essas calibrações têm finalidade descritiva e computacional. Não serão apresentadas como inferência para uma população.

### 5. Simulação reproduzível

Gerar 10.000 realizações do modelo candidato com semente registrada. A simulação deverá utilizar os parâmetros definidos na etapa anterior e funções apropriadas do `numpy.random.Generator` ou do `scipy.stats`.

As realizações simuladas serão utilizadas como instrumento computacional para tornar as propriedades do modelo observáveis. Elas não constituirão uma segunda base de dados nem substituirão os registros do Ames Housing.

O grupo deverá comparar:

- média teórica, observada e simulada;
- variância teórica, observada e simulada;
- comportamento gráfico observado e simulado.

Para comparações gráficas entre amostras de tamanhos diferentes, deverão ser utilizadas frequências relativas ou densidades, conforme o tipo da variável.

### 6. Auditoria dos pressupostos

O grupo deverá examinar os pressupostos correspondentes à sua trilha.

#### Binomial

- número fixo de ensaios;
- dois resultados por ensaio;
- probabilidade constante;
- independência;
- interpretação das seleções no conjunto finito observado.

#### Poisson

- contagem de ocorrências;
- intervalo ou exposição bem definido;
- taxa aproximadamente constante;
- independência das ocorrências;
- ausência de limite estrutural incompatível com o suporte do modelo;
- compatibilidade entre média, variância e frequência de zeros.

#### Normal

- variável quantitativa contínua;
- suporte teórico e limites naturais da variável;
- concentração aproximadamente simétrica;
- comportamento das caudas;
- efeito de valores discrepantes;
- alinhamento e desvios observados no Q–Q plot;
- compatibilidade entre probabilidades observadas e teóricas em intervalos relevantes.

### 7. Parecer de adequação

O grupo deverá classificar o modelo como:

- **adequado:** o mecanismo, o suporte, os pressupostos e as comparações são suficientemente coerentes para a finalidade delimitada;
- **parcialmente adequado:** o modelo oferece aproximação útil, mas apresenta violações ou limitações relevantes;
- **inadequado:** o mecanismo, o suporte ou as evidências tornam seu uso indefensável para a finalidade proposta.

O parecer deverá integrar evidências conceituais, numéricas, gráficas e simuladas. Não será aceita conclusão baseada somente na semelhança visual entre distribuições.

## Delimitações

Não integram esta AP:

- distribuições Uniforme e Exponencial, pois as variáveis selecionadas do Ames Housing não representam, respectivamente, valores contínuos equiprováveis em um intervalo ou tempos de espera associados a um processo com taxa constante;
- testes formais de aderência;
- testes de normalidade;
- estimação por máxima verossimilhança;
- seleção automática de distribuições;
- transformação de variáveis com a finalidade exclusiva de obter ajuste;
- generalização dos resultados para outros mercados imobiliários.

## Conclusão

A conclusão deverá responder diretamente à pergunta de pesquisa, apresentar o parecer de adequação, identificar as evidências decisivas e reconhecer os limites do conjunto de dados e da modelagem realizada.
