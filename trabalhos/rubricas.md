# Rubricas da AP integrada

## Regra de aplicação

Cada critério será classificado em um dos níveis:

- **Completo:** correto, reproduzível, justificado e interpretado no contexto.
- **Parcialmente completo:** núcleo correto, mas com omissão localizada de justificativa, interpretação ou verificação.
- **Insuficiente:** procedimento incompleto, incoerente com a pergunta ou com erros estatísticos relevantes.
- **Ausente ou incorreto:** evidência não apresentada, não executável ou incompatível com o método solicitado.

Código mais sofisticado não compensará erro estatístico. A nota de cada critério será proporcional ao nível atingido e ao peso indicado.

## AP1

### Procedência dos dados — 10%

Identificação do arquivo fornecido, unidade de análise, dimensões e mapeamento dos nomes.

### Importação, qualidade, limpeza e documentação — 20%

Carregamento de `data/raw/AmesHousing.txt` em célula própria, tipos, conversões, duplicidades, valores ausentes, consulta à documentação, justificativas, preparação documentada de `Fireplaces`, `Mas Vnr Area`, `Year Remod/Add` e `Year Built`, preservação do original e produção reproduzível de `data/processed/AmesHousing.csv`.

### Análise exploratória e visualizações — 25%

Medidas, frequências e representações coerentes com os tipos de variáveis: resumo quantitativo, histogramas, frequência e barras de $B$, resumo temporal, linha da mediana anual do preço de venda (`SalePrice`), resumo e boxplots do preço por categoria de $B$, dispersão, correlação linear, unidades e interpretação.

### Valores discrepantes e preparação de $B$ — 25%

Cercas de Tukey com `IQR`, investigação sem remoção automática, agrupamento justificado de $B$, rótulos finais e registro das decisões antes da análise do preço por categoria.

### Interpretação e limitações — 10%

Conclusões proporcionais às evidências e reconhecimento dos limites dos dados, das decisões de preparação e do gráfico temporal, sem atribuir tendência causal às diferenças anuais.

### Repositório GitHub, reprodutibilidade, autoria e IA — 10%

`README.md` informativo, notebook em `notebooks/ap1.ipynb`, cabeçalho institucional, título principal, hierarquia coerente de títulos, sequência lógica da investigação, proximidade entre código, saída e interpretação, células curtas, dependências registradas, caminhos relativos, notebook executável, `.gitignore` adequado, ausência de credenciais e arquivos temporários, histórico de commits coerente, contribuições identificadas, declaração de IA e acesso docente. Será avaliada a organização construída pelo grupo e a coerência do histórico com o desenvolvimento, não a quantidade de títulos ou commits.

## AP2

### Formulação e compatibilidade inicial — 25%

Pergunta específica, unidade de análise, definição da variável aleatória ou do evento, classificação, suporte e compatibilidade inicial do modelo atribuído com base no mecanismo e nos pressupostos.

### Modelo candidato e calibração — 20%

Definição do modelo atribuído, parâmetros, esperança, variância, cálculos reproduzíveis e interpretação contextual.

### Comparação e simulação reproduzível — 25%

Descrição empírica, representação gráfica coerente, carregamento de `data/processed/AmesHousing.csv` em célula própria, 10.000 realizações, semente registrada e comparação entre média, variância e comportamento gráfico observado, teórico e simulado.

### Auditoria dos pressupostos e parecer — 20%

Exame dos pressupostos específicos da trilha, consideração conjunta das evidências, classificação do modelo como adequado, parcialmente adequado ou inadequado e reconhecimento das limitações. A rejeição fundamentada não reduzirá a nota.

### Comunicação — 5%

Organização, notação e clareza das interpretações.

### Repositório GitHub, reprodutibilidade, autoria e IA — 5%

Atualização organizada do mesmo repositório, notebook em `notebooks/ap2.ipynb`, cabeçalho institucional, título principal, estrutura acadêmica por células curtas, saídas interpretadas, dependências e caminhos reproduzíveis, notebook executável, histórico de commits coerente, contribuições identificadas, declaração de IA e acesso docente.

## AP3

### Delimitação da modelagem — 10%

Pergunta, objetivo, variável resposta, registro prévio das candidatas e da escolha inicial justificada de $X$, preditores, unidades, categorias de $B$, categoria de referência, população conceitual e limites observacionais. O notebook deverá conter parecer explícito de aprovação ou recusa de $X$, fundamentado conjuntamente no valor-p da inclinação, em $R^2$, em $R^2_{\mathrm{ajustado}}$ e nos resíduos. Candidatas recusadas e repetições do procedimento deverão permanecer documentadas. AIC e BIC não poderão integrar a decisão.

### Regressão simples — 20%

Pergunta, gráfico, ajuste de `SalePrice ~ X`, coeficientes, unidades, incerteza, valor ajustado, resíduo, $R^2$ e $R^2_{\mathrm{ajustado}}$.

### Regressão múltipla com `C(B)` — 20%

Inclusão do mesmo $X$ e de `C(B)`, categoria de referência, indicadores, interpretação condicional e comparação com o modelo simples.

### Inferência sobre os coeficientes — 20%

Hipóteses, nível de significância, estimativas, erros-padrão, estatísticas $t$, valores-p, intervalos, decisões e interpretações contextuais da inclinação e dos indicadores de $B$.

### Comparação e diagnóstico dos modelos — 20%

Comparação entre os modelos por $R^2$ e $R^2_{\mathrm{ajustado}}$, gráficos de resíduos, pressupostos, observações influentes, proibição de exclusões orientadas pelo ajuste e justificativa que não se limite às medidas de ajuste.

### Interpretação e limitações — 5%

Associação bruta e ajustada, significância estatística, relevância prática, representatividade, limitações e ausência de interpretação causal.

### Repositório GitHub, reprodutibilidade, autoria e IA — 5%

Atualização organizada do mesmo repositório, notebook em `notebooks/ap3.ipynb`, cabeçalho institucional, título principal, estrutura acadêmica por células curtas, saídas interpretadas, carregamento de `data/processed/AmesHousing.csv`, instruções finais de execução no `README.md`, dependências e caminhos reproduzíveis, notebooks executáveis, histórico de commits coerente, contribuições identificadas, declaração de IA e acesso docente.
