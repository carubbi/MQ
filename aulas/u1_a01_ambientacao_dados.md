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

[Unifor.br](https://unifor.br/) | [Instagram](https://www.instagram.com/uniforcomunica/?hl=pt-br) | [Facebook](https://www.facebook.com/uniforoficial/) | [Twitter](https://www.facebook.com/uniforoficial/)  | [LinkedIn](https://www.linkedin.com/school/university-of-fortaleza/?originalSubdomain=pt) | [TV Unifor](https://www.unifor.br/tv-unifor) | [G1/Ensinando e Aprendendo](https://g1.globo.com/ce/ceara/especial-publicitario/unifor/ensinando-e-aprendendo/)

# Ambientação computacional e introdução aos dados tabulares

- **Unidade:** I
- **Aula:** 1
- **Semana:** 1
- **Data:** 07/08/2026
- **Duração:** 100 minutos
- **Conteúdo formal:** `01.01`
- **Tópicos:** Google Colab; Python; pandas; `DataFrame`; `Series`; fonte; observações; variáveis; tipos computacionais; unidade de análise; seleção; filtragem; cópia; coluna derivada; concatenação simples
- **Resultado de aprendizagem:** carregar uma base pública, interpretar sua estrutura e realizar manipulações básicas com pandas sem modificar os dados originais.

---

## Pergunta orientadora e percurso

> Como carregar, compreender e realizar manipulações básicas em um conjunto de dados?

- **Ciclo 1:** Notebook, Python e pandas.
- **Ciclo 2:** Fonte, carregamento e estruturas do pandas.
- **Ciclo 3:** Seleção e filtragem.
- **Ciclo 4:** Transformação segura e combinação simples.
- **Evidência:** notebook preenchido e executado integralmente pelos estudantes.

---

## Ciclo didático 1 — Notebook, Python e pandas

### Problema e contexto

Em um notebook, texto, código e resultados permanecem no mesmo documento, mas cumprem funções diferentes. A execução fora de ordem pode utilizar objetos desatualizados ou ainda inexistentes. Antes de analisar os dados, é necessário compreender como registrar explicações, executar instruções e conferir o estado produzido por cada célula.

### Fundamentação científica

- O Google Colab oferece um ambiente de notebooks Jupyter hospedado e sem configuração local.[5]
- Células Markdown registram orientações, interpretações, fórmulas e equações matemáticas com [LaTeX](https://www.latex-project.org/).[6]
- Células de código executam instruções em Python.
- A ordem de execução determina quais objetos estão disponíveis.
- O pandas organiza e manipula dados tabulares por meio de `DataFrame` e `Series`.[4]
- As instruções e as atividades estão no [notebook da Aula 1](../notebooks/u1_a01_ambientacao_dados.ipynb).
- Todas as células de código serão preenchidas e executadas pelos estudantes.

<small>Rodapé — [4] PANDAS DEVELOPMENT TEAM, seção “What kind of data does pandas handle?”. [5] GOOGLE, seção “Perguntas frequentes — Noções básicas”. [6] LATEX PROJECT, seção “LaTeX — A document preparation system”.</small>

---

## Ciclo didático 2 — Fonte, carregamento e estruturas do pandas

### Problema e contexto — Palmer Penguins

O Palmer Penguins reúne 344 observações e 17 variáveis documentadas, mas o arquivo isolado não explica o significado de suas linhas e colunas. Antes de realizar qualquer análise, é necessário identificar a fonte, a unidade de análise e o significado das variáveis, distinguindo a estrutura armazenada pelo pandas do contexto científico dos dados.[1]

<p align="center">
  <img src="https://raw.githubusercontent.com/carubbi/MQ/main/notebooks/assets/imgs/lter_penguins.png"
       alt="Ilustração das espécies Chinstrap, Gentoo e Adelie"
       width="65%">
</p>

- **Figura 1:** espécies presentes no Palmer Penguins; ilustração de Allison Horst (`@allison_horst`).

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seções “About the data” e “Artwork — Meet the Palmer penguins”.</small>

---

### Medidas e contexto da coleta

- `Culmen Length (mm)` registra o comprimento da crista dorsal do bico.[1]
- `Culmen Depth (mm)` registra a profundidade dessa crista.[1]
- `Flipper Length (mm)` registra o comprimento da nadadeira.[1]
- `Body Mass (g)` registra a massa corporal.[1]
- Unidade, significado e contexto não devem ser inferidos apenas pelo nome da coluna.

<p align="center">
  <img src="https://raw.githubusercontent.com/carubbi/MQ/main/notebooks/assets/imgs/culmen_depth.png"
       alt="Comprimento e profundidade do bico de um pinguim"
       width="65%">
</p>

- **Figura 2:** comprimento e profundidade do bico; ilustração de Allison Horst (`@allison_horst`).

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seções “penguins_raw — Format” e “Artwork — Bill dimensions”.</small>

---

### Variáveis de identificação e estudo

| Variável | Unidade | Significado documentado |
| --- | --- | --- |
| `studyName` | não se aplica | Expedição de amostragem. |
| `Sample Number` | não se aplica | Numeração sequencial da amostra. |
| `Species` | não se aplica | Espécie do pinguim. |
| `Region` | não se aplica | Região da grade de amostragem. |
| `Island` | não se aplica | Ilha onde ocorreu a coleta. |
| `Stage` | não se aplica | Estágio reprodutivo na amostragem. |
| `Individual ID` | não se aplica | Identificador do indivíduo no conjunto. |
| `Clutch Completion` | não se aplica | Presença de postura completa com dois ovos. |
| `Date Egg` | data | Data da observação do ninho com um ovo. |

- O par `studyName` e `Individual ID` identifica o indivíduo no contexto do estudo.
- Identificadores não devem ser interpretados como medidas.

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seção “penguins_raw — Format”.</small>

---

### Medidas e informações complementares

| Variável | Unidade | Significado documentado |
| --- | --- | --- |
| `Culmen Length (mm)` | mm | Comprimento da crista dorsal do bico. |
| `Culmen Depth (mm)` | mm | Profundidade da crista dorsal do bico. |
| `Flipper Length (mm)` | mm | Comprimento da nadadeira. |
| `Body Mass (g)` | g | Massa corporal. |
| `Sex` | não se aplica | Sexo do animal. |
| `Delta 15 N (o/oo)` | ‰ | Razão entre os isótopos 15N e 14N. |
| `Delta 13 C (o/oo)` | ‰ | Razão entre os isótopos 13C e 12C. |
| `Comments` | não se aplica | Informação textual adicional. |

- A classificação estatística das variáveis será estudada na Aula 5.
- Ausências serão reconhecidas nesta aula e tratadas posteriormente.

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seção “penguins_raw — Format”.</small>

---

### Conceitos fundamentais

- **Fonte:** origem documentada dos dados.
- **Unidade de análise:** elemento pesquisado representado por uma linha.[3][8]
- **Registro ou caso:** linha que reúne os valores observados nessa unidade.[3][8]
- **Observação:** conjunto de valores observado para o caso; em uso corrente, também pode designar o próprio registro.[3][8]
- **Variável:** característica registrada nas diferentes unidades.[3][8]
- **Valor:** conteúdo de uma variável em determinado registro.
- **Tipo computacional:** forma de armazenamento usada pelo software.
- Tipo computacional e significado estatístico são propriedades distintas.

<small>Rodapé — [3] BRUCE; BRUCE (2019), cap. 1, seções “Elementos de Dados Estruturados” e “Dados Retangulares”, p. PDF 23–28. [8] BARBETTA; REIS; BORNIA (2010), cap. 3, seção 3.1, p. PDF 52–53.</small>

---

### Caso reduzido e resolução manual

| `studyName` | `Individual ID` | `Species` | `Island` | `Flipper Length (mm)` | `Body Mass (g)` |
| --- | --- | --- | --- | ---: | ---: |
| PAL0708 | N1A1 | Adelie Penguin (Pygoscelis adeliae) | Torgersen | 181 | 3750 |
| PAL0708 | N1A2 | Adelie Penguin (Pygoscelis adeliae) | Torgersen | 186 | 3800 |
| PAL0708 | N31A1 | Gentoo penguin (Pygoscelis papua) | Biscoe | 211 | 4500 |
| PAL0708 | N61A1 | Chinstrap penguin (Pygoscelis antarctica) | Dream | 192 | 3500 |

- **Fonte:** publicação e documentação do Palmer Penguins por Horst, Hill e Gorman.[1]
- **Unidade de análise:** um pinguim observado.
- **Registro ou caso:** a linha identificada por `PAL0708` e `N1A1`.
- **Observação:** o conjunto dos seis valores exibidos nessa linha.
- **Variável:** `Body Mass (g)`, característica registrada para os pinguins.
- **Valor:** `3750`, conteúdo de `Body Mass (g)` no caso `PAL0708`/`N1A1`.
- **Tipo computacional:** `float64` para `Body Mass (g)` após o carregamento do arquivo completo com pandas; não pode ser determinado apenas pelo recorte.[4]
- **`Island`:** característica do local; não é a unidade de análise.
- **Alcance:** o recorte não representa toda a diversidade da base.

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seção “penguins_raw — Format”. [3] BRUCE; BRUCE (2019), cap. 1, seção “Elementos de Dados Estruturados”, p. PDF 23–26. [4] PANDAS DEVELOPMENT TEAM, seção “What kind of data does pandas handle?”.</small>

---

### Aplicação computacional

- Importar pandas com o alias `pd`.[4]
- Definir o endereço oficial de `penguins_raw.csv`.[1]
- Carregar o CSV com `pd.read_csv()`.[4]
- Conferir os primeiros registros com `head()`.[4]
- Verificar dimensões com `shape`: resultado esperado `(344, 17)`.[1]
- Consultar nomes com `columns` e tipos com `dtypes`.[4]
- Resumir estrutura e valores não ausentes com `info()`.[4]
- Selecionar `Species` como `Series`.[4]
- Selecionar medidas corporais como `DataFrame`.[4]

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seções “About the data” e “penguins_raw — Format”. [4] PANDAS DEVELOPMENT TEAM, seções “How do I read and write tabular data?” e “What kind of data does pandas handle?”.</small>

---

### Comparação, diagnóstico e interpretação

| Afirmação | Diagnóstico |
| --- | --- |
| “Há 344 espécies.” | Unidade de análise incorreta. |
| “Há 344 observações de pinguins.” | Compatível com a documentação. |
| “A tabela possui 17 variáveis.” | Compatível com o arquivo bruto. |
| “`Date Egg` não é data porque foi carregada como texto.” | Confunde armazenamento e significado. |
| “Uma coluna isolada pode ser uma `Series`.” | Compatível com o pandas. |

- Registrar fonte, arquivo, dimensões e significado de uma linha.
- Comparar nomes e tipos carregados com a documentação.
- Reconhecer ausências sem corrigi-las silenciosamente.
- Não usar `head()` como representação da distribuição completa.

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seção “penguins_raw — Format”. [3] BRUCE; BRUCE (2019), cap. 1, seções “Dados Retangulares” e “Quadros de Dados e Índices”, p. PDF 27–30. [4] PANDAS DEVELOPMENT TEAM, seção “What kind of data does pandas handle?”.</small>

---

## Ciclo didático 3 — Seleção e filtragem

### Problema e contexto

Uma pergunta geralmente utiliza apenas parte das linhas ou colunas disponíveis. Entretanto, selecionar por posição, rótulo ou condição produz resultados diferentes, e uma escolha inadequada pode incluir registros indevidos ou alterar a estrutura esperada. O problema consiste em escolher a operação de seleção compatível com o recorte pretendido.

### Seleção e filtragem no pandas

- `df["coluna"]` seleciona uma coluna como `Series`.[4]
- `df[["coluna_a", "coluna_b"]]` mantém duas dimensões.[4]
- `iloc` seleciona linhas e colunas por posição inteira.[4]
- `loc` seleciona por rótulos e nomes de colunas.[4]
- Comparações produzem uma `Series` booleana.[4]
- Uma condição booleana mantém somente as linhas avaliadas como `True`.[4]
- Em `iloc`, o limite final de um intervalo é excluído.
- Em `loc`, o rótulo final é incluído quando existe.

<small>Rodapé — [4] PANDAS DEVELOPMENT TEAM, seção “How do I select a subset of a DataFrame?”.</small>

---

### Caso reduzido e resolução manual

- **Condição:** `Island == "Dream"`.
- **Colunas mantidas:** `Species`, `Island` e `Body Mass (g)`.

| `Species` | `Island` | `Body Mass (g)` |
| --- | --- | ---: |
| Chinstrap penguin (Pygoscelis antarctica) | Dream | 3500 |

- A linha pertence ao arquivo original.
- A linha satisfaz a condição definida.
- A filtragem não cria observações nem altera valores.

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seção “penguins_raw — Format”. [4] PANDAS DEVELOPMENT TEAM, seção “How do I select a subset of a DataFrame?”.</small>

---

### Aplicação, comparação e diagnóstico

- Selecionar `Species` como `Series`.
- Selecionar três medidas corporais como `DataFrame`.
- Obter as cinco primeiras posições de linha com `iloc`.
- Selecionar identificadores, espécie e ilha com `loc`.
- Construir e aplicar a condição `Island == "Dream"`.
- Conferir o tipo e o conteúdo de cada resultado intermediário.

| Operação | Critério | Resultado |
| --- | --- | --- |
| uma coluna entre colchetes | nome | `Series` |
| lista de colunas | nomes | `DataFrame` |
| `iloc[0:5, :]` | posições | cinco posições de linha |
| `loc[0:4, colunas]` | rótulos | rótulos de 0 a 4 |
| `loc[condicao, colunas]` | valores booleanos | linhas verdadeiras |

- Escolher a operação conforme posição, rótulo ou valor.
- Não interpretar um recorte como representação automática da base.

<small>Rodapé — [4] PANDAS DEVELOPMENT TEAM, seção “How do I select a subset of a DataFrame?”.</small>

---

## Ciclo didático 4 — Transformação segura e combinação simples

### Problema e contexto

Converter unidades ou combinar subconjuntos modifica o objeto utilizado na análise. Se a transformação sobrescrever os valores originais ou reunir tabelas incompatíveis, perde-se a possibilidade de conferir o resultado. Por isso, as operações devem preservar o objeto original, explicitar as unidades e combinar somente estruturas com o mesmo significado.

### Cópia, colunas derivadas e concatenação

- `copy()` cria um objeto de trabalho independente.[4]
- Uma coluna derivada registra uma transformação calculada.
- A unidade original deve permanecer disponível para conferência.
- `pd.concat()` combina tabelas compatíveis.[4]
- A concatenação desta aula reúne somente subconjuntos reais.
- Linhas artificiais não serão misturadas ao conjunto científico.
- Operações simples serão escritas em etapas separadas.

<small>Rodapé — [4] PANDAS DEVELOPMENT TEAM, seções “Copy-on-Write” e “Merge, join, concatenate and compare”.</small>

---

### Caso reduzido e resolução manual

- **Conversão:** $\text{massa em kg}=\text{massa em g}/1000$.
- **Coluna didática:** `Body Mass (kg)*` não pertence ao arquivo original.

| `Individual ID` | `Body Mass (g)` | `Body Mass (kg)*` |
| --- | ---: | ---: |
| N1A1 | 3750 | 3,75 |
| N1A2 | 3800 | 3,80 |
| N31A1 | 4500 | 4,50 |
| N61A1 | 3500 | 3,50 |

- Os valores em gramas permanecem inalterados.
- A nova unidade deve aparecer no nome da coluna.
- O `*` identifica a coluna acrescentada para fins didáticos.

<small>Rodapé — [1] HORST; HILL; GORMAN (2020), seção “penguins_raw — Format”.</small>

---

### Aplicação, comparação e diagnóstico

- Criar uma cópia com `copy()`.[4]
- Calcular `Body Mass (kg)` a partir de `Body Mass (g)`.
- Comparar as duas unidades.
- Confirmar que a nova coluna não existe no objeto original.
- Formar dois subconjuntos reais com as mesmas colunas.
- Combinar os subconjuntos com `pd.concat(..., ignore_index=True)`.[4]

| Procedimento | Efeito | Diagnóstico |
| --- | --- | --- |
| transformar uma cópia | preserva o original | permite conferir antes e depois |
| transformar o original | modifica a fonte de trabalho | dificulta reiniciar a análise |
| concatenar subconjuntos reais | preserva os valores | mantém rastreabilidade |
| inserir linha fictícia | mistura naturezas distintas | não será realizado |

- Declarar objeto alterado, fórmula e unidades.
- Manter o mesmo significado das colunas concatenadas.

<small>Rodapé — [4] PANDAS DEVELOPMENT TEAM, seções “Copy-on-Write” e “Merge, join, concatenate and compare”.</small>

---

## Fechamento — cuidados interpretativos

- Executar as células na ordem planejada.
- Consultar a documentação, não apenas o nome do arquivo.
- Distinguir pinguim observado, registro, espécie, ilha e ninho.
- Interpretar `Individual ID` no contexto de `studyName`.
- Distinguir tipo computacional e significado estatístico.
- Não usar `head()` como retrato da distribuição completa.
- Distinguir posições de `iloc` e rótulos de `loc`.
- Transformar uma cópia e preservar o objeto original.
- Não inserir linhas fictícias no conjunto científico.
- Registrar fonte, unidade de análise e transformações.

<small>Rodapé — [3] BRUCE; BRUCE (2019), cap. 1, seções “Elementos de Dados Estruturados”, “Dados Retangulares” e “Quadros de Dados e Índices”, p. PDF 23–30. [4] PANDAS DEVELOPMENT TEAM, seções “What kind of data does pandas handle?”, “How do I select a subset of a DataFrame?” e “Copy-on-Write”.</small>

---

## Estudo e exercícios

### Materiais didáticos

- [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/): fonte, documentação e arquivos do conjunto.
- [Notebook da Aula 1](../notebooks/u1_a01_ambientacao_dados.ipynb): prática de Google Colab, Python, pandas e manipulações básicas.
- BRUCE; BRUCE (2019), cap. 1, seções “Elementos de Dados Estruturados”, “Dados Retangulares” e “Quadros de Dados e Índices”, p. PDF 23–30: observação, variável, unidade de análise e organização retangular dos dados.
- BARBETTA; REIS; BORNIA (2010), cap. 3, seção 3.1, p. PDF 52–53: unidades, casos, observações e variáveis na organização de um conjunto de dados.
- [Apostila de Métodos Quantitativos](../apostila/apostila_mq.pdf), cap. 1, seção 1.2 “Conceitos Fundamentais”, p. PDF 9–10: variável, dado e informação.

### Exercícios indicados

- [Tutorial oficial do Google Colab](https://colab.research.google.com/notebook).
- [Tutorial oficial do Python](https://docs.python.org/3/tutorial/).
- [Tutorial oficial do pandas](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html).
- Banco de questões, seção 1.1.2, questão 7, página 8: identificar variáveis e explicar quais informações elas fornecem ao estudo.

---

## Referências

- [1] HORST, Allison Marie; HILL, Alison Presmanes; GORMAN, Kristen B. *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. Versão 0.1.0. Zenodo, 2020. DOI: [10.5281/zenodo.3960218](https://doi.org/10.5281/zenodo.3960218).
- [2] FISHER, R. A. *Iris* [Dataset]. UCI Machine Learning Repository, 1936. DOI: [10.24432/C56C76](https://doi.org/10.24432/C56C76).
- [3] BRUCE, Peter; BRUCE, Andrew. *Estatística prática para cientistas de dados: 50 conceitos essenciais*. Rio de Janeiro: Alta Books, 2019.
- [4] PANDAS DEVELOPMENT TEAM. *pandas documentation*. Disponível em: <https://pandas.pydata.org/docs/>. Acesso em: 11 ago. 2026.
- [5] GOOGLE. *Google Colab: perguntas frequentes*. Disponível em: <https://research.google.com/colaboratory/intl/pt-BR/faq.html>. Acesso em: 11 ago. 2026.
- [6] LATEX PROJECT. *LaTeX — A document preparation system*. Disponível em: <https://www.latex-project.org/>. Acesso em: 11 ago. 2026.
- [7] ARAÚJO, Cledinaldo Castro; SILVA, Vera Lúcia. *Métodos quantitativos para engenharia: questões contextualizadas & exercícios*. 2. ed. Disponível em: [Apostila de Métodos Quantitativos](../apostila/apostila_mq.pdf).
- [8] BARBETTA, Pedro Alberto; REIS, Marcelo Menezes; BORNIA, Antonio Cezar. *Estatística para cursos de engenharia e informática*. 3. ed. São Paulo: Atlas, 2010.
- [9] MORETTIN, Pedro Alberto; BUSSAB, Wilton de Oliveira. *Estatística básica*. 6. ed. rev. e atual. São Paulo: Saraiva, 2010.
