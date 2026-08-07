# Fluxo de ensino

## Princípios gerais

- A disciplina articula fundamentos estatísticos, investigação com dados e aplicação computacional em Python.
- Cada unidade combina construção conceitual, notebooks guiados, exercícios de consolidação e uma etapa da avaliação prática integrada.
- Correção estatística, justificativa das decisões e interpretação dos resultados têm prioridade sobre sofisticação do código.
- Código executado sem explicação não constitui evidência suficiente de aprendizagem.
- Os notebooks devem usar caminhos relativos, registrar dependências e executar integralmente sem estado oculto.
- Tabelas, gráficos e resultados numéricos devem ser apresentados com identificação, contexto e interpretação.

## Organização dos encontros

A turma `T199-64/65` tem dois blocos consecutivos às sextas-feiras:

- **turma 64 — bloco teórico:** 15h30 às 17h10;
- **turma 65 — bloco prático:** 17h20 às 19h.

Os conteúdos conceituais sustentam a aplicação computacional do mesmo encontro. A separação entre os blocos não significa independência entre teoria e prática.

Consulte [turmas e horários](turmas_2026_2.md) e o [calendário acadêmico](calendario_2026_2.md).

## Materiais de apoio

- A [apostila de Métodos Quantitativos](../apostila/apostila_mq.pdf) e o
  [banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf)
  são materiais públicos da disciplina.
- Os notebooks estão em construção em `mat/notebooks/`. A conclusão e a
  publicação dos notebooks da Unidade I dependem do subgrafo completo dessa
  unidade.
- Os slides serão produzidos em Markdown e publicados em `mat/aulas/`.
- Os conjuntos de dados didáticos estão em [`mat/data/`](../data/).
- O [projeto de ensino](proj_ensino_2026.md) define objetivos, conteúdos, carga horária e critérios institucionais.

# Unidade I — Fundamentos estatísticos e análise exploratória de dados

## Formação conceitual

- investigação estatística, população, amostra, amostragem e representatividade;
- organização, importação e preparação básica de dados;
- tipos de variáveis, distribuições de frequências, tabelas e gráficos;
- medidas de posição, dispersão e forma;
- valores discrepantes e boxplots;
- associação entre variáveis e correlação linear.

## Aplicação computacional

- leitura e inspeção de dados com Python e `pandas`;
- construção e interpretação de tabelas e visualizações;
- cálculo de medidas descritivas;
- comparação de distribuições;
- análise univariada e bivariada com atenção às limitações dos dados.

## AP1 — Análise exploratória

A primeira etapa da avaliação prática organiza e explora o Ames Housing. O grupo documenta a procedência e a preparação dos dados, analisa o preço de venda, investiga valores discrepantes, prepara a característica qualitativa atribuída e produz o conjunto processado que será reutilizado nas unidades seguintes.

Os três acompanhamentos verificam, progressivamente:

1. estrutura do repositório, importação, tipos e ausências;
2. análise univariada, visualizações e investigação de valores discrepantes;
3. análise bivariada, decisões finais de preparação e produção reproduzível dos dados processados.

# Unidade II — Probabilidade e distribuições de probabilidade

## Formação conceitual

- conceitos fundamentais de probabilidade;
- regras da soma e do produto;
- probabilidade condicional, independência, probabilidade total e teorema de Bayes;
- variáveis aleatórias discretas e contínuas;
- esperança e variância;
- distribuições Binomial, Poisson, Uniforme, Exponencial e Normal;
- parâmetros, pressupostos e interpretação de modelos probabilísticos.

## Aplicação computacional

- representação de fenômenos aleatórios;
- cálculo e visualização de probabilidades;
- simulação reproduzível;
- comparação entre comportamento observado, teórico e simulado;
- avaliação crítica dos pressupostos de um modelo.

## AP2 — Auditoria de modelos probabilísticos

Cada grupo recebe uma variável ou um evento e um modelo candidato entre Binomial, Poisson e Normal. A tarefa é verificar se o modelo é compatível com o fenômeno, calibrar seus parâmetros, simular realizações e emitir um parecer fundamentado. Concluir que o modelo é inadequado é válido quando a análise sustenta essa decisão.

Os três acompanhamentos verificam, progressivamente:

1. definição da variável aleatória e compatibilidade inicial;
2. calibração dos parâmetros e planejamento da simulação;
3. comparação dos resultados, auditoria dos pressupostos e parecer final.

# Unidade III — Estatística inferencial

## Formação conceitual

- técnicas de amostragem probabilísticas e não probabilísticas;
- distribuições amostrais da média e da proporção;
- estimação pontual e intervalar;
- erro-padrão e margem de erro;
- testes de hipóteses para uma média e para duas proporções;
- regressão linear simples e múltipla;
- interpretação de coeficientes e análise de resíduos.

## Aplicação computacional

- estimação e quantificação da incerteza;
- realização e interpretação de testes de hipóteses;
- ajuste de modelos de regressão;
- inferência sobre coeficientes;
- diagnóstico e comparação de modelos;
- comunicação de pressupostos, limitações e alcance das conclusões.

## AP3 — Modelagem estatística

A etapa final retoma os dados preparados na AP1 para investigar o preço de venda por regressão. Antes dos ajustes, o grupo registra as candidatas e escolhe e justifica um preditor quantitativo $X$ com base na pergunta, no significado da variável e na qualidade dos dados. Depois da regressão simples, deverá aprovar ou recusar $X$ considerando conjuntamente o valor-p da inclinação, $R^2$, $R^2_{\mathrm{ajustado}}$ e os resíduos; AIC e BIC não serão usados. Uma candidata recusada será substituída por outra previamente registrada e submetida ao mesmo procedimento, com preservação do histórico e identificação da seleção como exploratória. Com o mesmo $X$ aprovado, o grupo ajusta `SalePrice ~ X`, realiza inferência sobre a inclinação, examina os resíduos, acrescenta a característica qualitativa atribuída em `SalePrice ~ X + C(B)` e compara os modelos aninhados.

Os três acompanhamentos verificam, progressivamente:

1. delimitação da investigação e ajuste inicial da regressão simples;
2. inferência, diagnóstico e ajuste da regressão múltipla;
3. comparação dos modelos, conclusão, limitações e reprodutibilidade final.

## Continuidade da avaliação prática

- AP1, AP2 e AP3 são entregas separadas de uma única investigação progressiva.
- O mesmo grupo e o mesmo repositório devem ser mantidos, salvo autorização do professor.
- As decisões de preparação congeladas na AP1 são reutilizadas nas etapas seguintes.
- Cada integrante deve compreender e conseguir explicar as decisões estatísticas e computacionais.
- Os acompanhamentos são formativos e não substituem a entrega final pelo AVA.
- O uso de inteligência artificial deve ser declarado, incluindo finalidade e forma de verificação.
