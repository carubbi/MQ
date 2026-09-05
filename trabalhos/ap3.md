# AP3 — Modelagem estatística do preço de venda de imóveis residenciais

## Contexto

Na etapa final, o grupo modelará o preço de venda com base em um preditor quantitativo $X$, escolhido e justificado antes dos ajustes, e na característica qualitativa $B$. Serão ajustados modelos de regressão linear simples e múltipla, com interpretação inferencial dos coeficientes, diagnóstico dos resíduos, comparação dos modelos e discussão dos limites da modelagem.

## Pergunta de pesquisa

Como o preditor quantitativo $X$ e a característica qualitativa $B$ se associam ao preço de venda de imóveis residenciais?

## Objetivo da investigação

Ajustar, interpretar e diagnosticar modelos de regressão linear para analisar a associação do preço de venda com o preditor quantitativo $X$ e com a característica qualitativa $B$.

## Retomada necessária

Retomar, no mesmo repositório, a estrutura congelada na AP1 e declarar:

- unidade de análise;
- população conceitual;
- amostra observacional representada pelos registros e seu processo de obtenção;
- decisões de preparação preservadas;
- característica qualitativa $B$ e suas categorias;
- limitações de representatividade.

## Carregamento dos dados

Uma célula de código exclusiva deverá carregar `data/processed/AmesHousing.csv`, produzido na AP1. Verificações mínimas poderão confirmar dimensões, colunas necessárias e decisões preservadas. Não poderão ser alterados a limpeza e os agrupamentos definidos na AP1.

## Delimitação da modelagem

Antes dos ajustes, o grupo deverá registrar:

- preço de venda (`SalePrice`) como variável resposta;
- preditor quantitativo $X$ escolhido pelo grupo;
- variáveis candidatas consideradas e justificativa da escolha de $X$ com base na pergunta de pesquisa, no significado da variável, na plausibilidade temporal, na qualidade dos dados e na interpretabilidade;
- característica qualitativa $B$ como preditor adicional do modelo múltiplo;
- categorias preservadas de $B$;
- categoria de referência de $B$;
- unidades das variáveis quantitativas;
- caráter observacional dos dados e impossibilidade de concluir causalidade.

A categoria de referência deverá ser escolhida por significado e interpretabilidade antes do exame dos valores-p. Os agrupamentos definidos na AP1 e a categoria de referência não poderão ser alterados para melhorar significância, coeficiente de determinação ou diagnóstico dos resíduos.

A escolha inicial de $X$ e o conjunto de candidatas deverão ser registrados antes de qualquer ajuste ou exame dos resultados. Após o ajuste da regressão simples, o grupo deverá emitir uma decisão explícita de **aprovar** ou **recusar** $X$ e justificá-la considerando conjuntamente o valor-p da inclinação, $R^2$, $R^2_{\mathrm{ajustado}}$ e os diagnósticos de resíduos. Nenhum desses critérios será suficiente isoladamente, e AIC e BIC não poderão orientar a decisão. Se $X$ for recusado, o grupo deverá escolher outra candidata previamente registrada e repetir o ajuste, a avaliação e a decisão, preservando no notebook o histórico das candidatas, dos resultados e das justificativas. A seleção será identificada como exploratória, e os dois modelos obrigatórios deverão utilizar o mesmo $X$ aprovado.

## Etapas obrigatórias

### 1. Regressão linear simples

Utilizar preço de venda como resposta e o preditor quantitativo $X$ previamente escolhido. Conceitualmente:

$$
Y_i=\beta_0+\beta_1x_i+\varepsilon_i,
\tag{3.1}
$$

em que $Y_i$ representa o preço de venda e $x_i$ representa o valor do preditor quantitativo escolhido para o imóvel $i$.

Computacionalmente, substituindo `X` pelo nome efetivo da coluna documentada:

```text
SalePrice ~ X
```

O grupo deverá:

- construir o diagrama de dispersão;
- examinar a plausibilidade da relação linear;
- ajustar o modelo com `statsmodels`;
- apresentar o `OLS Regression Results`;
- interpretar intercepto e inclinação nas unidades do problema;
- calcular ou verificar um valor ajustado e um resíduo;
- apresentar e interpretar o coeficiente de determinação $R^2$ e o coeficiente de determinação ajustado $R^2_{\mathrm{ajustado}}$;
- reconhecer os limites de interpolação e extrapolação.

### 2. Inferência sobre a inclinação

Avaliar:

$$
H_0:\beta_1=0
\quad\text{contra}\quad
H_1:\beta_1\neq0.
\tag{3.2}
$$

Antes da interpretação, o grupo deverá fixar o nível de significância. A partir da saída do `statsmodels`, deverá apresentar e interpretar:

- estimativa de $\beta_1$;
- erro-padrão;
- estatística $t$;
- valor-p;
- intervalo de confiança;
- decisão sobre $H_0$;
- magnitude e direção da associação.

A conclusão deverá distinguir significância estatística, relevância prática e causalidade.

### 3. Diagnóstico do modelo simples

Apresentar:

- resíduos versus valores ajustados;
- gráfico quantil-quantil;
- discussão de linearidade;
- discussão de homoscedasticidade;
- discussão de normalidade dos erros;
- limites para avaliar independência;
- reconhecimento de observações potencialmente influentes.

Nenhuma observação poderá ser removida apenas para melhorar significância, $R^2$, $R^2_{\mathrm{ajustado}}$ ou aparência dos resíduos.

### Decisão sobre o preditor quantitativo

Depois da inferência e do diagnóstico do modelo simples, o grupo deverá declarar uma das decisões:

- **aprovar $X$:** manter o preditor na regressão simples final e acrescentar somente `C(B)` na regressão múltipla;
- **recusar $X$:** justificar a recusa, escolher outra candidata quantitativa previamente registrada e repetir as etapas 1 a 3.

A justificativa deverá articular o valor-p da inclinação, $R^2$, $R^2_{\mathrm{ajustado}}$ e os padrões observados nos resíduos. Não haverá ponto de corte universal para aprovação além do nível de significância previamente fixado; a decisão deverá considerar em conjunto evidência inferencial, capacidade explicativa, adequação dos pressupostos e sentido substantivo.

### 4. Regressão linear múltipla

Adicionar a característica qualitativa $B$ ao modelo por indicadores. Conceitualmente:

$$
Y_i=\beta_0+\beta_1x_i+
\sum_{k=1}^{K-1}\gamma_k I(B_i=b_k)+\varepsilon_i.
\tag{3.3}
$$

Computacionalmente:

```text
SalePrice ~ X + C(B)
```

`C(B)` indica ao `statsmodels` que a característica qualitativa $B$ deverá ser tratada como categórica. O programa criará $K-1$ variáveis indicadoras, utilizando uma das $K$ categorias como referência.

Os nomes computacionais efetivos serão aqueles documentados na AP1.

O grupo deverá:

- indicar a categoria de referência;
- interpretar a inclinação de $X$, controlando por $B$;
- interpretar os coeficientes indicadores de $B$ em relação à categoria de referência;
- calcular ou verificar valores ajustados para categorias distintas;
- evitar interpretação causal.

### 5. Inferência sobre os coeficientes

No modelo múltiplo, avaliar:

$$
H_0:\beta_1=0
\quad\text{contra}\quad
H_1:\beta_1\neq0
\tag{3.4}
$$

e, para cada categoria não utilizada como referência:

$$
H_0:\gamma_k=0
\quad\text{contra}\quad
H_1:\gamma_k\neq0.
\tag{3.5}
$$

Para cada coeficiente relevante, apresentar estimativa, erro-padrão, estatística $t$, valor-p, intervalo de confiança, decisão e interpretação contextual. Os testes dos indicadores deverão ser interpretados como comparações com a categoria de referência, condicionadas a $X$.

Não serão exigidos o teste do intercepto nem o teste $F$ global.

### 6. Comparação e diagnóstico do modelo final

Comparar os modelos simples e múltiplo quanto a:

- estimativa e interpretação da inclinação de $X$;
- incerteza dos coeficientes;
- $R^2$ e $R^2_{\mathrm{ajustado}}$;
- padrões dos resíduos;
- adequação dos pressupostos;
- utilidade e limitações das informações acrescentadas por $B$.

O grupo deverá construir para o modelo múltiplo os gráficos de resíduos versus valores ajustados e quantil-quantil. Na comparação, deverá reconhecer que $R^2$ não diminui com a inclusão de preditores e que $R^2_{\mathrm{ajustado}}$ incorpora uma penalização pela complexidade. A escolha do modelo final não poderá ser justificada somente por essas medidas ou pela quantidade de coeficientes significativos.

## Extensão não avaliada

O professor poderá demonstrar um modelo com a idade do imóvel no momento da venda. Essa extensão:

- não integra os critérios obrigatórios;
- não concede bônus;
- não substitui os modelos exigidos;
- não autoriza seleção automática de variáveis.

## Delimitações

Não integram esta AP:

- divisão entre treino e teste;
- métricas preditivas;
- seleção automática de variáveis;
- regularização;
- interação entre $X$ e $B$;
- teste $F$ global;
- interpretação causal.

## Conclusão

Responder diretamente à pergunta de pesquisa e relacionar:

- associação bruta entre $X$ e preço;
- associação ajustada após a inclusão de $B$;
- evidências inferenciais sobre os coeficientes;
- diagnóstico dos modelos;
- diferenças entre significância estatística e relevância prática;
- pressupostos e limitações dos dados e da modelagem.
