# Mockups de aulas e notebooks e sincronização dos cronogramas — desenho

## 1. Objetivo

Estabilizar os caminhos e os metadados de todos os recursos semanais da
disciplina T199 — Métodos Quantitativos em 2026.2 antes da produção integral
dos materiais. Os cronogramas docente e discente poderão apontar para recursos
em construção, desde que o estado seja indicado explicitamente.

Este trabalho produzirá:

- 15 mockups de materiais de aula em Markdown;
- 12 mockups de notebooks em `.ipynb`;
- renomeação dos dois notebooks finalizados da Semana 1;
- inclusão dos recursos e de seus estados no cronograma docente;
- criação do cronograma discente da turma T199-64/65.

Esta especificação substitui, para o estado e a quantidade dos notebooks, as
seções correspondentes de
`docs/superpowers/specs/2026-08-07-recursos-cronograma-docente-design.md`.
Deixa de valer a previsão de um roteiro `.md` por semana de desenvolvimento e
passa a valer a produção de notebooks `.ipynb` finalizados ou em estado de
mockup conforme o inventário deste documento. As regras científicas e
editoriais do desenho anterior continuam válidas para a finalização futura dos
materiais.

## 2. Fontes, autoridade e baseline

### 2.1 Fontes consultadas

- `prof/ensino/cronograma_2026_2_docente.md`: fonte canônica de datas,
  conteúdos, atividades, avaliações, entregas e ocorrências;
- `mat/ensino/proj_ensino_2026.md`: ementa, objetivos e conteúdos formais;
- `mat/ensino/calendario_2026_2.md`: período letivo, feriados, janelas e datas
  institucionais;
- `mat/ensino/turmas_2026_2.md`: turma, horários e sala;
- `prof/refs/mapas/grafo_referencias.json`: vocabulário canônico dos tópicos;
- `mat/aulas/u1_s01_fundamentos_estatisticos.md`: modelo do cabeçalho semanal;
- `mat/notebooks/assets/heads/head_unifor.md`: conteúdo canônico da única
  célula dos notebooks-mockup;
- `mat/notebooks/aula1.ipynb` e `mat/notebooks/aula2.ipynb`: notebooks
  finalizados da Semana 1.

### 2.2 Baseline

Hashes capturados antes da primeira edição:

- cronograma docente:
  `ef121044ff2cfff14fac10ca008850e420486d375d9c4639bf78d36f4fac13dd`;
- projeto de ensino:
  `fe07b9c2f992d1d060091a244af2d2ed8e24fbe4ae7f70c1688164a910d57f56`;
- calendário:
  `870e01460e31b1f446dad003b72e74f268e3fc4c9d633c22425595a199204d30`;
- turmas:
  `51950f56113cefa0734b0b1e35c68da1aea5d7c6b3515ce79c8104233213707b`.

O estado inicial também contém alterações do usuário que não pertencem a esta
execução:

- `mat/ensino/fluxo_ensino.md` modificado;
- `mat/notebooks/u1_s01_fundamentos_estatisticos.md` removido;
- dois notebooks finalizados e seus ativos adicionados em `mat/notebooks/`.

Essas mudanças serão preservadas. A remoção do roteiro Markdown antigo será
mantida, pois ele foi substituído pelos notebooks executáveis finalizados.

### 2.3 Autoridade

- Fatos institucionais virão do calendário, das turmas e do cronograma
  docente.
- Conteúdos, tópicos e resultados de aprendizagem serão derivados do projeto
  de ensino e do detalhamento pedagógico do cronograma docente.
- O grafo será autoridade para a grafia dos tópicos.
- O cronograma discente será projeção do cronograma docente e não poderá
  corrigi-lo.

## 3. Granularidade e estados

### 3.1 Materiais de aula

Haverá um material Markdown por semana com encontro:

- 16 materiais no total;
- 1 material finalizado na Semana 1;
- 15 mockups novos;
- nenhum material nos feriados de 14/08 e 20/11.

As três semanas de revisão e AT receberão material de aula, mas não notebook.

### 3.2 Notebooks

Haverá:

- dois notebooks finalizados na Semana 1;
- um notebook-mockup em cada uma das outras 12 semanas de desenvolvimento;
- nenhum notebook nas semanas de revisão e AT;
- nenhum notebook nos feriados;
- 14 notebooks no total.

### 3.3 Estados nos cronogramas

Os estados serão registrados nos cronogramas, não dentro dos arquivos:

- **finalizado**: material ou notebook já desenvolvido;
- **em construção**: mockup com caminho e metadados estabilizados.

O material e os dois notebooks da Semana 1 serão marcados como finalizados.
Todos os recursos criados nesta execução serão marcados como em construção.

## 4. Estrutura dos mockups

### 4.1 Material de aula

Cada mockup `.md` conterá somente:

```markdown
# Título semanal

- **Disciplina:** T199 — Métodos Quantitativos
- **Unidade:** I, II ou III
- **Semana:** número local da semana na unidade
- **Data:** DD/MM/2026
- **Conteúdos formais:** código, códigos ou intervalo
- **Tópicos:** tópicos canônicos separados por ponto e vírgula
- **Resultado de aprendizagem:** uma frase com verbos observáveis

---
```

Não serão adicionados Agenda, seções vazias, `TODO`, `TBD`, links ou conteúdo
antecipado. A Semana 1 permanecerá integral e não será reduzida ao mockup.

### 4.2 Notebook-mockup

Cada `.ipynb` será um notebook JSON válido, versão 4, contendo:

- uma única célula Markdown;
- conteúdo da célula exatamente igual ao conteúdo integral de
  `mat/notebooks/assets/heads/head_unifor.md`;
- nenhuma célula de código;
- nenhuma saída;
- nenhum título ou marcador de conteúdo futuro;
- metadados mínimos compatíveis com Python 3.

Os notebooks finalizados da Semana 1 não serão reduzidos nem terão células
alteradas.

## 5. Nomenclatura e inventário

| Unidade | Semana | Data | Natureza | Material de aula | Notebook |
| --- | ---: | --- | --- | --- | --- |
| I | 1 | 07/08 | desenvolvimento | `u1_s01_fundamentos_estatisticos.md` — finalizado | `u1_s01_fundamentos_estatisticos_aula01.ipynb` e `u1_s01_fundamentos_estatisticos_aula02.ipynb` — finalizados |
| I | 2 | 14/08 | feriado | — | — |
| I | 3 | 21/08 | desenvolvimento | `u1_s03_organizacao_representacao_dados.md` | `u1_s03_organizacao_representacao_dados.ipynb` |
| I | 4 | 28/08 | desenvolvimento | `u1_s04_analise_univariada.md` | `u1_s04_analise_univariada.ipynb` |
| I | 5 | 04/09 | desenvolvimento | `u1_s05_analise_bivariada.md` | `u1_s05_analise_bivariada.ipynb` |
| I | 6 | 11/09 | desenvolvimento | `u1_s06_probabilidade.md` | `u1_s06_probabilidade.ipynb` |
| II | 1 | 18/09 | revisão e AT1 | `u2_s01_revisao_at1.md` | — |
| II | 2 | 25/09 | desenvolvimento | `u2_s02_variaveis_aleatorias.md` | `u2_s02_variaveis_aleatorias.ipynb` |
| II | 3 | 02/10 | desenvolvimento | `u2_s03_distribuicoes_discretas.md` | `u2_s03_distribuicoes_discretas.ipynb` |
| II | 4 | 09/10 | desenvolvimento | `u2_s04_distribuicoes_continuas.md` | `u2_s04_distribuicoes_continuas.ipynb` |
| II | 5 | 16/10 | desenvolvimento | `u2_s05_normal_auditoria_modelos.md` | `u2_s05_normal_auditoria_modelos.ipynb` |
| II | 6 | 23/10 | revisão e AT2 | `u2_s06_revisao_at2.md` | — |
| III | 1 | 30/10 | desenvolvimento | `u3_s01_amostragem_distribuicoes_amostrais.md` | `u3_s01_amostragem_distribuicoes_amostrais.ipynb` |
| III | 2 | 06/11 | desenvolvimento | `u3_s02_estimacao_testes.md` | `u3_s02_estimacao_testes.ipynb` |
| III | 3 | 13/11 | desenvolvimento | `u3_s03_regressao_linear_simples.md` | `u3_s03_regressao_linear_simples.ipynb` |
| III | 4 | 20/11 | feriado | — | — |
| III | 5 | 27/11 | desenvolvimento | `u3_s05_regressao_simples_multipla.md` | `u3_s05_regressao_simples_multipla.ipynb` |
| III | 6 | 04/12 | revisão e AT3 | `u3_s06_revisao_at3.md` | — |

Renomeações:

- `mat/notebooks/aula1.ipynb` para
  `mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb`;
- `mat/notebooks/aula2.ipynb` para
  `mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb`.

## 6. Metadados pedagógicos dos mockups

### Unidade I

#### Semana 3 — Organização e representação de dados

- **Conteúdos formais:** `01.02`.
- **Tópicos:** Importação de dados; Pré-processamento; Tipos de variáveis;
  Frequência; Tabela; Gráfico.
- **Resultado:** organizar e representar dados, justificando decisões de
  preparação e comparando distribuições de frequências, tabelas e gráficos.

#### Semana 4 — Análise univariada

- **Conteúdos formais:** `01.03`.
- **Tópicos:** Média; Mediana; Moda; Quantil; Amplitude; Variância;
  Desvio-padrão; Intervalo interquartil; Coeficiente de variação; Assimetria;
  Valor discrepante; Boxplot.
- **Resultado:** calcular, comparar e interpretar medidas de posição,
  dispersão e forma, investigando valores discrepantes sem exclusão
  automática.

#### Semana 5 — Análise bivariada

- **Conteúdos formais:** `01.04`.
- **Tópicos:** Tabela de contingência; Associação; Covariância; Correlação
  linear; Gráfico; Valor discrepante.
- **Resultado:** analisar relações entre duas variáveis por tabelas,
  percentuais condicionais, dispersão e correlação, sem confundir associação
  com causalidade.

#### Semana 6 — Probabilidade e entrega da AP1

- **Conteúdos formais:** `02.01`.
- **Tópicos:** Experimento aleatório; Espaço amostral; Evento; Regra da
  adição; Regra do produto; Probabilidade condicional; Independência;
  Probabilidade total; Teorema de Bayes.
- **Resultado:** representar eventos e calcular probabilidades, aplicando
  condicionamento, probabilidade total e Teorema de Bayes a problemas
  reduzidos.

### Unidade II

#### Semana 1 — Revisão e avaliação teórica 1

- **Conteúdos formais:** `01.01` a `01.04` e `02.01`.
- **Tópicos:** Estatística descritiva; Frequência; Tabela; Gráfico; Média;
  Mediana; Variância; Desvio-padrão; Tabela de contingência; Associação;
  Correlação linear; Experimento aleatório; Evento; Probabilidade condicional;
  Teorema de Bayes.
- **Resultado:** integrar os fundamentos de análise descritiva e probabilidade
  para resolver e interpretar as questões da AT1.

#### Semana 2 — Variáveis aleatórias

- **Conteúdos formais:** `02.01` e `02.02`.
- **Tópicos:** Variável aleatória discreta; Variável aleatória contínua;
  Função de probabilidade; Função densidade; Função distribuição acumulada;
  Esperança; Variância.
- **Resultado:** representar variáveis aleatórias discretas e contínuas,
  calcular probabilidades, esperança e variância e comparar resultados
  teóricos e simulados.

#### Semana 3 — Distribuições discretas

- **Conteúdos formais:** `02.03`.
- **Tópicos:** Distribuição binomial; Distribuição de Poisson; Esperança;
  Variância.
- **Resultado:** selecionar, calcular e simular modelos Binomial e Poisson,
  justificando mecanismos, parâmetros e pressupostos.

#### Semana 4 — Distribuições contínuas

- **Conteúdos formais:** `02.03` e `02.04`.
- **Tópicos:** Distribuição uniforme; Distribuição exponencial; Distribuição
  normal; Padronização; Esperança; Variância.
- **Resultado:** distinguir modelos contínuos, calcular probabilidades e
  interpretar parâmetros, áreas, padronização e propriedades dos modelos.

#### Semana 5 — Normal e auditoria de modelos

- **Conteúdos formais:** `02.04`.
- **Tópicos:** Distribuição normal; Padronização; Gráfico; Gráfico Q-Q; Valor
  discrepante; Diagnóstico do modelo.
- **Resultado:** confrontar dados observados, modelo teórico e simulação para
  diagnosticar e comunicar a adequação de um modelo Normal.

#### Semana 6 — Revisão e avaliação teórica 2

- **Conteúdos formais:** `02.02` a `02.04`, mobilizando `02.01`.
- **Tópicos:** Variável aleatória discreta; Variável aleatória contínua;
  Distribuição binomial; Distribuição de Poisson; Distribuição uniforme;
  Distribuição exponencial; Distribuição normal; Esperança; Variância;
  Padronização.
- **Resultado:** integrar variáveis aleatórias e modelos discretos e contínuos
  para resolver, justificar e interpretar as questões da AT2.

### Unidade III

#### Semana 1 — Amostragem e distribuições amostrais

- **Conteúdos formais:** `03.01` e `03.02`.
- **Tópicos:** População; Amostra; Amostragem; Representatividade; Amostragem
  aleatória simples; Amostragem estratificada; Distribuição amostral; Teorema
  central do limite; Erro-padrão; Tamanho amostral.
- **Resultado:** selecionar e comparar amostras e interpretar distribuições
  amostrais, Teorema Central do Limite e erro-padrão.

#### Semana 2 — Estimação e testes

- **Conteúdos formais:** `03.02` e `03.03`.
- **Tópicos:** Estimação pontual; Intervalo de confiança; Erro-padrão; Margem
  de erro; Hipótese nula; Hipótese alternativa; Nível de significância;
  Valor-p; Teste para média; Teste para proporção; Erro tipo I; Erro tipo II;
  Poder do teste.
- **Resultado:** calcular, verificar e comunicar intervalos e testes para uma
  média e uma proporção, explicitando pressupostos, decisão, magnitude e
  limitações.

#### Semana 3 — Regressão linear simples

- **Conteúdos formais:** `03.04`.
- **Tópicos:** Regressão linear simples; Mínimos quadrados; Resíduo; Inferência
  sobre coeficientes; Valor-p; Coeficiente de determinação; Coeficiente de
  determinação ajustado.
- **Resultado:** ajustar uma regressão linear simples e interpretar equação,
  coeficientes, valores ajustados, resíduos, inferência e medidas de ajuste.

#### Semana 5 — Diagnóstico da regressão simples e regressão múltipla

- **Conteúdos formais:** `03.04`.
- **Tópicos:** Diagnóstico do modelo; Resíduo; Gráfico Q-Q; Coeficiente de
  determinação; Coeficiente de determinação ajustado; Regressão linear
  múltipla; Variável indicadora; Inferência sobre coeficientes.
- **Resultado:** diagnosticar a regressão simples, justificar a decisão sobre
  o preditor e ajustar e interpretar uma regressão múltipla com variável
  indicadora.

#### Semana 6 — Revisão e avaliação teórica 3

- **Conteúdos formais:** `03.01` a `03.04`.
- **Tópicos:** Amostragem; Representatividade; Distribuição amostral;
  Estimação pontual; Intervalo de confiança; Teste para média; Teste para
  proporção; Correlação linear; Regressão linear simples; Regressão linear
  múltipla; Diagnóstico do modelo.
- **Resultado:** integrar amostragem, estimação, testes, correlação e regressão
  para resolver e interpretar as questões da AT3.

## 7. Cronograma docente

Alvo existente:

`prof/ensino/cronograma_2026_2_docente.md`

Ao final de cada semana com encontro, depois de **Atividade e evidência**,
acompanhamentos, entregas e ocorrências aplicáveis, será incluído um bloco
**Recursos** com links relativos:

```markdown
- **Recursos:**
  - **Material de aula — em construção:** [Título](../../mat/aulas/arquivo.md).
  - **Notebook guiado — em construção:** [Título](../../mat/notebooks/arquivo.ipynb).
```

Exceções:

- Semana 1: material e dois notebooks com estado **finalizado**;
- revisão/AT: somente material de aula com estado **em construção**;
- feriados: nenhum bloco de recursos;
- sessões extraordinárias de segunda chamada: nenhum mockup próprio.

Nenhuma data, conteúdo, atividade, evidência, avaliação, entrega ou ocorrência
será alterada por esta etapa.

## 8. Cronograma discente

Alvo novo:

`mat/ensino/cronograma_2026_2_t199_64_65.md`

O arquivo será derivado integralmente do cronograma docente para a turma
T199-64/65. Ele deverá:

- declarar que é derivado da fonte docente sem expor caminho em `prof/`;
- manter datas, encontros, conteúdos, atividades, evidências, avaliações,
  entregas, feriados e segundas chamadas;
- converter critérios docentes pertinentes em orientações ao estudante;
- omitir justificativas internas, decisões administrativas e notas de
  validação;
- usar links relativos a `../aulas/` e `../notebooks/`;
- indicar **finalizado** ou **em construção** em cada link;
- não conter marcadores genéricos nem caminhos privados.

## 9. Validação

### 9.1 Materiais Markdown

- exatamente um título, sete campos de identificação e o separador `---`;
- datas e semanas iguais ao cronograma docente;
- códigos existentes no projeto e no grafo;
- tópicos com grafia idêntica à dos nós `topico` do grafo;
- resultado de aprendizagem coerente com **Atividade e evidência**;
- nenhum arquivo nos feriados;
- ausência de seções adicionais, `TODO` e `TBD`.

### 9.2 Notebooks

- os dois notebooks finalizados preservam células, saídas e metadados após a
  renomeação;
- cada mockup é JSON válido no formato notebook 4;
- cada mockup contém uma única célula Markdown;
- o texto reunido da célula é idêntico a `head_unifor.md`;
- não há células de código nem saídas;
- todos os ativos referenciados pelo cabeçalho existem.

### 9.3 Cronogramas

- todos os 16 encontros semanais possuem material;
- as 12 semanas de desenvolvimento posteriores à Semana 1 possuem um
  notebook-mockup;
- a Semana 1 possui dois notebooks finalizados;
- revisão/AT não possui notebook;
- feriados não possuem recursos;
- todos os links locais existem;
- estados dos recursos correspondem à sua condição real;
- cronograma discente contém somente a turma T199-64/65;
- fonte docente permanece autoridade e não sofre alterações além dos blocos de
  recursos;
- calendário, projeto de ensino e cadastro de turmas permanecem inalterados.

## 10. Sequência transacional

1. renomear e validar os notebooks finalizados;
2. criar e validar os 15 mockups de aula;
3. criar e validar os 12 notebooks-mockup;
4. atualizar e validar o cronograma docente;
5. gerar o cronograma discente em área temporária;
6. validar a projeção discente e instalar o arquivo somente após sucesso;
7. conferir hashes das fontes e o estado final do repositório;
8. realizar commits por entregas coerentes, sem incluir alterações alheias.

Uma falha de validação interromperá a instalação dos cronogramas; não será
publicada projeção discente parcial.

## 11. Fora do escopo

- desenvolvimento do conteúdo integral dos 15 materiais;
- implementação de código, exercícios ou resultados nos 12 notebooks-mockup;
- alteração das ATs, APs, instrumentos ou configurações do AVA;
- criação de recursos para feriados ou sessões extraordinárias;
- alteração de datas, carga horária ou decisões pedagógicas do cronograma
  docente;
- push para repositório remoto.
