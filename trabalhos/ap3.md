# AP3 — Modelagem estatística do preço de venda de imóveis residenciais

## Contexto

Na etapa final, o grupo ajustará uma regressão linear simples para o preço de venda com base em um preditor quantitativo $X$, escolhido e justificado antes do ajuste. Para a regressão múltipla, interpretará saídas fornecidas pelo professor, com o mesmo $X$ e a característica qualitativa $B$. A investigação incluirá interpretação inferencial dos coeficientes, diagnóstico dos resíduos, comparação dos modelos e discussão dos limites da modelagem.

## Pergunta de pesquisa

Como o preditor quantitativo $X$ e a característica qualitativa $B$ se associam ao preço de venda de imóveis residenciais?

## Objetivo da investigação

Ajustar e interpretar a regressão linear simples e interpretar as saídas fornecidas da regressão múltipla, comparando as associações do preço de venda com o preditor quantitativo $X$ e com a característica qualitativa $B$, seus diagnósticos e limitações.

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
- justificativa da escolha de $X$ com base na pergunta de pesquisa, no significado da variável, na plausibilidade temporal, na qualidade dos dados e na interpretabilidade;
- característica qualitativa $B$ como preditor adicional do modelo múltiplo;
- categorias preservadas de $B$;
- categoria de referência de $B$;
- unidades das variáveis quantitativas;
- caráter observacional dos dados e impossibilidade de concluir causalidade.

A categoria de referência deverá ser escolhida por significado e interpretabilidade antes do exame dos valores-p. Os agrupamentos definidos na AP1 e a categoria de referência não poderão ser alterados para melhorar significância, coeficiente de determinação ou diagnóstico dos resíduos.

A escolha de $X$ deverá ser registrada antes do ajuste ou exame dos resultados. O $X$ escolhido será mantido nos dois modelos, mesmo que a associação seja fraca ou os diagnósticos apontem limitações. Essas limitações deverão integrar o parecer e a conclusão; não serão exigidos ciclos de substituição de $X$ para obter significância ou melhorar o ajuste. AIC e BIC não poderão orientar a comparação.

O professor fornecerá as saídas do modelo múltiplo para o $X$, as categorias e a referência registrados pelo grupo. O material incluirá a fórmula efetivamente utilizada, o `OLS Regression Results`, os registros utilizados no ajuste, valores ajustados e resíduos, previsões para categorias distintas com o mesmo valor de $X$ e o gráfico de resíduos versus valores ajustados. Os dois modelos deverão usar os mesmos registros completos nas variáveis necessárias, preservando as decisões de preparação da AP1 e documentando eventuais exclusões por ausência. O grupo identificará o material fornecido no notebook e o incluirá no repositório para conferência.

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
- discussão de linearidade;
- discussão de homoscedasticidade;
- reconhecimento da normalidade dos erros como condição da inferência clássica exata, sem afirmá-la comprovada pelos gráficos utilizados;
- limites para avaliar independência;
- reconhecimento de observações potencialmente influentes.

Nenhuma observação poderá ser removida apenas para melhorar significância, $R^2$, $R^2_{\mathrm{ajustado}}$ ou aparência dos resíduos.

Não será exigido o gráfico quantil-quantil. Os gráficos de dispersão e de resíduos não comprovam normalidade ou independência dos erros. A discussão deverá reconhecer os limites das evidências disponíveis para a inferência.

### Parecer sobre o modelo simples

Articular a evidência inferencial, a magnitude da associação, $R^2$, $R^2_{\mathrm{ajustado}}$ e os padrões dos resíduos para explicar a utilidade e as limitações do modelo. Nenhuma medida isolada determina sua adequação. O parecer não exige substituir $X$ ou refazer a investigação com outro preditor.

### 4. Regressão linear múltipla

Interpretar as saídas fornecidas pelo professor para o modelo que acrescenta a característica qualitativa $B$ por indicadores. Não será exigida a implementação ou execução do ajuste desse modelo pelo grupo. Conceitualmente:

$$
Y_i=\beta_0+\beta_1x_i+
\sum_{k=1}^{K-1}\gamma_k I(B_i=b_k)+\varepsilon_i.
\tag{3.3}
$$

A fórmula computacional correspondente ao ajuste fornecido é:

```text
SalePrice ~ X + C(B)
```

`C(B)` indica ao `statsmodels` que a característica qualitativa $B$ deverá ser tratada como categórica. O programa criará $K-1$ variáveis indicadoras, utilizando uma das $K$ categorias como referência.

Os nomes computacionais efetivos serão aqueles documentados na AP1.

O grupo deverá:

- indicar a categoria de referência;
- interpretar a inclinação de $X$, controlando por $B$;
- interpretar os coeficientes indicadores de $B$ em relação à categoria de referência;
- interpretar as previsões fornecidas para categorias distintas, comparando imóveis com o mesmo valor de $X$;
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

Para cada coeficiente relevante, identificar nas saídas fornecidas a estimativa, o erro-padrão, a estatística $t$, o valor-p e o intervalo de confiança, e apresentar a decisão e a interpretação contextual. Os testes dos indicadores deverão ser interpretados como comparações com a categoria de referência, condicionadas a $X$. Não será exigido calcular novamente as estatísticas ou ajustar o modelo múltiplo.

Não serão exigidos o teste do intercepto nem o teste $F$ global.

### 6. Comparação e diagnóstico do modelo final

Comparar os modelos simples e múltiplo quanto a:

- estimativa e interpretação da inclinação de $X$;
- incerteza dos coeficientes;
- $R^2$ e $R^2_{\mathrm{ajustado}}$;
- padrões dos resíduos;
- adequação dos pressupostos;
- utilidade e limitações das informações acrescentadas por $B$.

O grupo deverá interpretar o gráfico de resíduos versus valores ajustados fornecido para o modelo múltiplo e compará-lo ao gráfico que construiu para o modelo simples. Na comparação de modelos aninhados com intercepto e ajustados aos mesmos registros, deverá reconhecer que $R^2$ não diminui com a inclusão de preditores e que $R^2_{\mathrm{ajustado}}$ incorpora uma penalização pela complexidade. A avaliação da utilidade dos modelos não poderá ser justificada somente por essas medidas ou pela quantidade de coeficientes significativos.

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
