<img src="https://raw.githubusercontent.com/carubbi/MQ/main/notebooks/assets/imgs/UNIFOR_logo.png" width="400">
<br>
<b>
<font size="6" face="arial" color="blue">
    Graduação em Ciência da Computação
</font>
</b>
<br>
<br>
<b>
<font size="4" face="arial">
    Disciplina: Métodos Quantitativos em Computação
</font>
</b>

**Orientador: Prof. Me. Ricardo Carubbi** <br>
*Docente da Graduação e Pós-Graduação em Ciência de Dados e Inteligência Artificial*<br>
*Laboratório de Ciência de Dados e Inteligência Artificial*<br>
*Universidade de Fortaleza*<br>

Lattes: http://lattes.cnpq.br/5738786447903616 |
GitHub: https://github.com/carubbi/

[Unifor.br](https://unifor.br/) | [Instagram](https://www.instagram.com/uniforcomunica/?hl=pt-br) | [Facebook](https://www.facebook.com/uniforoficial/) | [Twitter](https://www.facebook.com/uniforoficial/) | [LinkedIn](https://www.linkedin.com/school/university-of-fortaleza/?originalSubdomain=pt) | [TV Unifor](https://www.unifor.br/tv-unifor) | [G1/Ensinando e Aprendendo](https://g1.globo.com/ce/ceara/especial-publicitario/unifor/ensinando-e-aprendendo/)

# Tipos, qualidade e pré-processamento básico

- **Unidade:** I
- **Aula:** 5
- **Semana:** 3
- **Data:** 21/08/2026
- **Duração:** 100 minutos
- **Conteúdos formais:** `01.02`
- **Tópicos:** tipos estatísticos e computacionais; completude; consistência; unicidade; conversão; valores ausentes; duplicidades; pré-processamento.
- **Resultado de aprendizagem:** classificar variáveis, diagnosticar problemas básicos de qualidade e justificar transformações que preservem o significado dos dados.

---

## Agenda

1. **Tipos estatísticos de variáveis — 20 min**
2. **Tipo estatístico versus tipo computacional — 20 min**
3. **Completude e valores ausentes — 25 min**
4. **Consistência, unicidade e pré-processamento — 35 min**

Cada tópico percorre um ciclo didático completo: problema e contexto, fundamentação científica, resolução manual, aplicação computacional, comparação, diagnóstico e interpretação.

## Pergunta orientadora

> Como diagnosticar e preparar dados sem alterar seu significado nem ocultar suas limitações?

## Contexto recorrente

A aula retoma a versão bruta do **Palmer Penguins**, apresentada na Aula 1. O arquivo contém 344 observações de pinguins e 17 variáveis sobre coleta, espécie, local, medidas corporais e isótopos. A versão bruta é mantida em `penguins`; as transformações serão aplicadas a uma cópia chamada `dados`.

#### Preparação computacional

- **Pacote:** `pandas`.
- Carregar `penguins_raw.csv` com `pd.read_csv()` em um `DataFrame` chamado `penguins`.
- Criar `dados` com `DataFrame.copy()` para preservar a versão bruta.
- Conferir estrutura e tipos iniciais com `head()`, `shape`, `columns` e `dtypes`.

---

### Ciclo didático 1 — Tipos estatísticos de variáveis

#### Problema e contexto

`Species`, `Individual ID`, `Sample Number`, `Body Mass (g)` e `Date Egg` convivem na mesma tabela, mas não admitem as mesmas operações. O fato de `Sample Number` ser armazenado como inteiro não torna sua média uma característica biológica.

#### Fundamentação científica

- **Qualitativa nominal:** categorias sem ordem intrínseca, como espécie e ilha.
- **Qualitativa ordinal:** categorias ordenadas, mas sem distância numérica necessariamente mensurável.
- **Quantitativa discreta:** contagem com valores separados.
- **Quantitativa contínua:** medida para a qual diferenças numéricas têm significado.
- **Identificador:** código usado para distinguir unidades dentro de um contexto; não é medida apenas por conter números.
- **Temporal:** data ou instante cuja representação requer escala e calendário próprios.

#### Caso reduzido e resolução manual

| `studyName` | `Sample Number` | `Species` | `Individual ID` | `Date Egg` | `Body Mass (g)` |
| --- | ---: | --- | --- | --- | ---: |
| PAL0708 | 1 | Adelie | N1A1 | 2007-11-11 | 3750 |
| PAL0708 | 2 | Adelie | N1A2 | 2007-11-11 | 3800 |
| PAL0910 | 67 | Chinstrap | N100A1 | 2009-11-21 | 4100 |

**Tabela 1 - Variáveis com diferentes significados estatísticos.** `Species` é nominal; `Sample Number` e `Individual ID` são códigos; `Date Egg` é temporal; `Body Mass (g)` é quantitativa contínua registrada em gramas. Fonte: observações reais do Palmer Penguins.

Somar ou calcular a média das massas possui interpretação física. Fazer o mesmo com os números de amostra ou com a parte numérica dos identificadores não descreve os animais.

#### Aplicação computacional

- **Pacote:** `pandas`.
- Contar categorias de `Species` com `Series.value_counts()`.
- Contar valores distintos de `studyName` e `Individual ID` com `DataFrame.nunique()`.
- Resumir as medidas corporais com `DataFrame.agg()`, usando `count`, `min`, `median`, `mean` e `max`.
- Comparar as operações aplicadas a categorias, identificadores e medidas e justificar por que cada uma é estatisticamente coerente.

#### Comparação, diagnóstico e interpretação

| Variável | `dtype` inicial | Tipo estatístico | Operação coerente |
| --- | --- | --- | --- |
| `Species` | texto | qualitativa nominal | contar categorias |
| `Individual ID` | texto | identificador contextual | verificar unicidade com a campanha |
| `Sample Number` | inteiro | código sequencial | ordenar ou localizar registros |
| `Body Mass (g)` | ponto flutuante | quantitativa contínua | resumir medidas válidas |
| `Date Egg` | texto | temporal | converter e calcular intervalos |

O tipo estatístico decorre do significado e do processo de obtenção, não somente do `dtype`.

---

### Ciclo didático 2 — Tipo estatístico versus tipo computacional

#### Problema e contexto

Na leitura do CSV, datas e categorias chegam como texto, enquanto medidas com ausências chegam como `float64`. O armazenamento inicial não documenta todas as operações que fazem sentido.

#### Caso reduzido e resolução manual

| Variável | Antes | Conversão justificada | Controle necessário |
| --- | --- | --- | --- |
| `Date Egg` | texto | `datetime64` | nenhuma data perdida |
| `Species` | texto | `category` | mesmas três categorias e frequências |
| `Body Mass (g)` | `float64` | manter | preservar gramas e ausências |

**Tabela 2 - Conversões orientadas pelo significado.** A conversão é aceitável quando facilita uma operação válida e não altera valores, categorias ou ausências.

#### Aplicação computacional

- **Pacote:** `pandas`.
- Registrar tipos, categorias, frequências e ausências antes das conversões com `dtypes`, `value_counts(dropna=False)` e `isna().sum()`.
- Converter `Date Egg` com `pd.to_datetime()`, definindo o formato ISO e o tratamento explícito de falhas.
- Converter `Species`, `Island` e `Sex` com `Series.astype("category")`.
- Repetir o inventário após as conversões e comparar número de linhas, tipos, domínios e ausências.

As 344 datas são convertidas sem perdas. As categorias preservam seus valores observados. A massa continua como ponto flutuante porque o tipo comporta valores ausentes sem inventar medições.

#### Comparação, diagnóstico e interpretação

Compare antes e depois: número de linhas, ausências, categorias e valores extremos. Uma conversão que aumenta ausências ou altera domínios precisa ser investigada antes de prosseguir.

---

### Ciclo didático 3 — Completude e valores ausentes

#### Problema e contexto

O Palmer Penguins possui ausências reais. Elas não estão distribuídas igualmente: `Comments` tem 290 ausências, `Sex` tem 11 e quatro medidas corporais têm duas cada. A utilidade de uma variável depende do objetivo da análise, não apenas da porcentagem preenchida.

#### Fundamentação científica

A taxa de ausência de uma variável é calculada por:

$$
r_j=\frac{m_j}{n}. \tag{1.1}
$$

em que:

- $j$ identifica a variável analisada;
- $r_j$ é a taxa de ausência da variável $j$;
- $m_j$ é o número de valores ausentes na variável $j$;
- $n$ é o número total de registros.

O número de casos completos nas variáveis exigidas por uma análise é calculado por:

$$
n_{cc}=\sum_{i=1}^{n}I(x_{i1},\ldots,x_{ip}\text{ observados}). \tag{1.2}
$$

em que:

- $n_{cc}$ é o número de casos completos nas variáveis selecionadas;
- $i$ identifica cada registro, de $1$ a $n$;
- $n$ é o número total de registros;
- $p$ é o número de variáveis exigidas pela análise;
- $x_{ij}$ é o valor da variável $j$ no registro $i$;
- $I(\cdot)$ é a função indicadora, igual a 1 quando todos os $p$ valores do registro estão observados e a 0 caso contrário.

Ausência não equivale a zero, categoria negativa ou string vazia.

#### Caso reduzido e resolução manual

| Linha original | `Species` | `Culmen Length (mm)` | `Body Mass (g)` | `Sex` |
| ---: | --- | ---: | ---: | --- |
| 0 | Adelie | 39,1 | 3750 | MALE |
| 1 | Adelie | 39,5 | 3800 | FEMALE |
| 2 | Adelie | 40,3 | 3250 | FEMALE |
| 3 | Adelie | ausente | ausente | ausente |

**Tabela 3 - Ausências reais em quatro observações consecutivas.** Para massa e sexo, há uma ausência em quatro linhas, isto é, 25% neste recorte. A taxa do recorte não deve ser confundida com a taxa no arquivo completo. Fonte: Palmer Penguins.

#### Aplicação computacional

- **Pacote:** `pandas`.
- Detectar ausências com `DataFrame.isna()`.
- Calcular quantidades e proporções por coluna com `sum()` e `mean()`.
- Organizar o diagnóstico em um `DataFrame` e ordenar as variáveis com `sort_values()`.
- Selecionar `Species`, `Body Mass (g)` e `Sex` e contar casos completos com `dropna()` e `shape`.
- Comparar o total de casos completos com as 344 linhas, sem excluir ou imputar registros nesta etapa.

#### Comparação, diagnóstico e interpretação

- **Manter:** preserva os registros e explicita a limitação.
- **Excluir para uma análise específica:** reduz o conjunto e pode alterar sua composição.
- **Imputar:** cria valores analíticos e exige método, justificativa e rastreabilidade.

O diagnóstico antecede a decisão. Não será feita imputação automática nesta aula.

---

### Ciclo didático 4 — Consistência, unicidade e pré-processamento

#### Problema e contexto

O arquivo não possui linhas integralmente duplicadas. Entretanto, `Individual ID` aparece repetido porque o código só é único dentro de uma campanha (`studyName`). Remover essas linhas como duplicatas destruiria observações válidas.

#### Fundamentação científica

A proporção de unicidade de uma chave candidata é calculada por:

$$
u_K=\frac{n_{\text{valores distintos de }K}}{n}. \tag{1.3}
$$

em que:

- $K$ é a chave candidata avaliada;
- $u_K$ é a proporção de valores distintos da chave $K$;
- $n_{\text{valores distintos de }K}$ é o número de valores distintos observados em $K$;
- $n$ é o número total de registros.

Unicidade computacional não prova validade semântica. A chave deve corresponder à unidade de análise e ao processo de coleta.

#### Caso reduzido e resolução manual

| `studyName` | `Sample Number` | `Species` | `Individual ID` |
| --- | ---: | --- | --- |
| PAL0708 | 1 | Adelie | N1A1 |
| PAL0910 | 81 | Gentoo | N1A1 |
| PAL0708 | 2 | Adelie | N1A2 |
| PAL0910 | 82 | Gentoo | N1A2 |

**Tabela 4 - Identificadores repetidos em campanhas diferentes.** `Individual ID` isolado não é chave global; a composição (`studyName`, `Individual ID`) distingue as 344 observações. Fonte: Palmer Penguins.

#### Aplicação computacional

- **Pacote:** `pandas`.
- Definir nomes em `snake_case` e aplicá-los somente à cópia com `DataFrame.rename()`.
- Comparar duplicatas integrais, repetições de `Individual ID` e repetições da chave (`studyName`, `Individual ID`) com `DataFrame.duplicated()` e `sum()`.
- Inspecionar domínios de espécie e ilha com `Series.nunique()`.
- Verificar medidas válidas positivas com `dropna()`, `gt()` e `all()`.
- Verificar a conversão das datas com `notna()` e `all()`.
- Reunir os resultados em um diagnóstico e justificar por que nenhuma linha será removida automaticamente.

O diagnóstico esperado é: zero duplicata integral, 154 repetições adicionais de `Individual ID` isolado e zero repetição da chave composta. A aplicação não deve executar `drop_duplicates()`.

#### Comparação, diagnóstico e interpretação

1. **Bruto:** preserva nomes, tipos e ausências da fonte.
2. **Diagnosticado:** registra tipos, domínios, ausências e chaves sem apagar linhas.
3. **Organizado:** aplica somente conversões e renomeações justificadas em uma cópia.

Para cada transformação, registre problema, regra, registros afetados e efeito produzido.

---

## Erros comuns e cuidados interpretativos

- Confundir tipo estatístico com tipo computacional.
- Tratar número de amostra ou identificador como medida.
- Converter sem comparar perdas antes e depois.
- Interpretar ausência como zero.
- Excluir todas as linhas que contêm alguma ausência.
- Remover registros por uma chave incompleta.
- Sobrescrever a base bruta durante o pré-processamento.

## Estudo e exercícios

### Materiais didáticos

- [Banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf): seção 1.1.2, páginas 8–10, para classificação estatística de variáveis.
- BARBETTA; REIS; BORNIA (2010), capítulo 3, seção 3.1, páginas PDF 52–53: dados, variáveis e tipos de variáveis.
- BRUCE; BRUCE; GEDECK (2020), capítulo 1, seções “Elementos de Dados Estruturados”, “Dados Retangulares” e “Quadros de Dados e Índices”, páginas PDF 23–30: estrutura computacional dos dados.
- [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/): fonte e documentação das variáveis utilizadas no diagnóstico de qualidade.
- [Documentação do pandas](https://pandas.pydata.org/docs/): tipos computacionais, dados categóricos, datas e valores ausentes.
- [Notebook da Aula 5](../notebooks/u1_a05_tipos_qualidade_preprocessamento.ipynb): prática de classificação, conversão, completude, consistência e unicidade.

### Exercícios indicados

- [Banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf), questão 11, página 10: classificar variáveis qualitativas e quantitativas.
- [Banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf), questão 15, página 11: distinguir códigos numéricos de medidas quantitativas.

## Referências

- BARBETTA, Pedro Alberto; BORNIA, Antonio Cezar; REIS, Marcelo Menezes. *Estatística para cursos de engenharia e informática*. 3. ed. São Paulo: Atlas, 2010.
- BRUCE, Peter; BRUCE, Andrew; GEDECK, Peter. *Practical statistics for data scientists*. 2. ed. Sebastopol: O'Reilly, 2020.
- HORST, Allison Marie; HILL, Alison Presmanes; GORMAN, Kristen B. *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. Versão 0.1.0. Zenodo, 2020. DOI: [10.5281/zenodo.3960218](https://doi.org/10.5281/zenodo.3960218).
- PANDAS DEVELOPMENT TEAM. *pandas documentation*. Disponível em: [pandas.pydata.org/docs](https://pandas.pydata.org/docs/).
