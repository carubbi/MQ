# Roteiro do notebook guiado — Fundamentos estatísticos

> Estado: roteiro estrutural em Markdown; não executável. Este arquivo define a implementação futura de `u1_s01_fundamentos_estatisticos.ipynb`.

## 1. Identificação

- **Disciplina:** T199 — Métodos Quantitativos
- **Unidade:** I
- **Semana:** 1
- **Data:** 07/08/2026
- **Aulas:** 1 e 2
- **Duração prevista:** 200 minutos, com intervalo institucional entre os blocos
- **Conteúdos formais:** `01.01`
- **Tópicos:** Investigação estatística; Estatística descritiva; Estatística inferencial; População; Amostra; Amostragem; Representatividade; Unidade de análise; Tipos de variáveis
- **Dados:** `../data/raw/penguins_raw.csv`
- **Bibliotecas previstas:** `pandas`
- **Futura implementação:** `u1_s01_fundamentos_estatisticos.ipynb`

## 2. Resultado de aprendizagem

Ao concluir o futuro notebook, o estudante deverá:

1. carregar e inspecionar a estrutura do Palmer Penguins;
2. identificar fonte, registro, unidade de análise, variáveis e tipos computacionais;
3. formular uma pergunta estatística;
4. distinguir descrição e inferência;
5. delimitar população, amostra, representatividade e alcance das conclusões.

## 3. Contexto e pergunta-problema

O Palmer Penguins reúne informações de pinguins adultos associados a ninhos observados no Arquipélago Palmer. O conjunto bruto contém identificadores, informações da coleta, variáveis qualitativas, medidas corporais e valores ausentes.

Pergunta principal:

> Como os dados estão organizados, o que representa cada registro e que conclusões podem ser sustentadas por sua origem?

O notebook não deverá transformar a inspeção computacional em prova de representatividade. A origem e o desenho da coleta permanecerão centrais.

## 4. Preparação conceitual

Antes do código, a futura implementação deverá apresentar:

- fonte, observação, variável, valor e unidade de análise;
- população, censo, amostra, amostragem e representatividade;
- estatística descritiva e inferencial;
- variabilidade, viés de seleção e viés de medição;
- $N$ como tamanho da população e $n$ como tamanho da amostra;
- $\theta$ como parâmetro e $\widehat{\theta}$ como estatística ou estimativa;
- distinção entre cálculo correto e generalização válida.

## 5. Dados, entradas e dependências

### Arquivo

- Caminho relativo: `../data/raw/penguins_raw.csv`.
- Procedência: pacote `palmerpenguins` 0.1.6 e projeto Palmer Station LTER.
- Estrutura documentada: 344 registros e 17 colunas.

### Colunas iniciais para inspeção

- `Individual ID`;
- `Species`;
- `Island`;
- `Date Egg`;
- `Flipper Length (mm)`;
- `Body Mass (g)`;
- `Sex`.

### Dependência

Somente `pandas` será necessário nesta semana. A futura implementação deverá registrar a versão usada no ambiente, mas não fixará dependências adicionais sem necessidade.

## 6. Antecipação conceitual antes do cálculo ou da execução

Antes de carregar o arquivo, o estudante deverá registrar:

1. o que imagina que cada linha representa;
2. quais colunas provavelmente serão qualitativas, quantitativas ou temporais;
3. qual variável pode funcionar como identificador;
4. uma população de interesse possível;
5. uma limitação que espera encontrar na generalização.

A atividade avaliará a justificativa, não a coincidência exata entre antecipação e estrutura observada.

## 7. Caso reduzido, resolução manual ou decisão conceitual

Exibir, em Markdown, os seis primeiros registros selecionados no material de aula.

Solicitar a classificação manual de:

- unidade de análise;
- identificador;
- variável qualitativa;
- variável quantitativa e respectiva unidade;
- valor ausente;
- afirmação descritiva;
- afirmação que exigiria inferência.

Essa classificação preparará a leitura de `DataFrame.dtypes` sem confundir tipo computacional com papel estatístico.

## 8. Sequência funcional do futuro notebook

### Bloco 1 — Apresentação e pergunta

- **Tipo de célula:** Markdown.
- **Função pedagógica:** formulação.
- **Conteúdo:** identificação, fonte, contexto, pergunta principal e evidência esperada.
- **Tempo previsto:** 10 minutos.

### Bloco 2 — Antecipação

- **Tipo de célula:** Markdown.
- **Função pedagógica:** antecipação.
- **Conteúdo:** campos para o estudante registrar unidade de análise, tipos esperados, população possível e limitação.
- **Tempo previsto:** 10 minutos.

### Bloco 3 — Dependência e carregamento

- **Tipo de célula:** código.
- **Função pedagógica:** processamento.
- **Entradas:** `../data/raw/penguins_raw.csv`.
- **Ação prevista:** importar `pandas` e usar `pandas.read_csv()`.
- **Produto esperado:** objeto `DataFrame`, sem apresentar antecipadamente seus valores.
- **Verificação:** confirmar existência do arquivo e sucesso da leitura.
- **Tempo previsto:** 15 minutos.

### Bloco 4 — Dimensões e nomes

- **Tipo de célula:** código.
- **Função pedagógica:** inspeção.
- **Ações previstas:** consultar `DataFrame.shape`, `DataFrame.columns` e `DataFrame.head()`.
- **Produtos esperados:** dimensões, lista de colunas e recorte inicial.
- **Pergunta interpretativa:** o que representa uma linha e quais colunas ajudam a justificar essa interpretação?
- **Tempo previsto:** 20 minutos.

### Bloco 5 — Tipos computacionais

- **Tipo de célula:** código.
- **Função pedagógica:** inspeção.
- **Ação prevista:** consultar `DataFrame.dtypes`.
- **Produto esperado:** tipos computacionais por coluna.
- **Pergunta interpretativa:** o tipo computacional é suficiente para classificar estatisticamente cada variável?
- **Tempo previsto:** 20 minutos.

### Bloco 6 — Fonte, unidade e variáveis

- **Tipo de célula:** Markdown.
- **Função pedagógica:** interpretação.
- **Conteúdo:** identificação fundamentada da fonte, dos registros, da unidade de análise, de duas variáveis e de seus tipos estatísticos e computacionais.
- **Tempo previsto:** 25 minutos.

### Bloco 7 — Fundamentos da investigação

- **Tipo de célula:** Markdown.
- **Função pedagógica:** explicação e decisão.
- **Conteúdo:** distinção entre descrição e inferência; formulação de uma pergunta estatística; declaração de população de interesse, amostra disponível e alcance.
- **Tempo previsto:** 35 minutos.

### Bloco 8 — Verificação da antecipação

- **Tipo de célula:** Markdown.
- **Função pedagógica:** verificação.
- **Conteúdo:** confronto entre a antecipação e a estrutura observada; explicação das diferenças.
- **Tempo previsto:** 20 minutos.

### Bloco 9 — Evidência e síntese

- **Tipo de célula:** Markdown.
- **Função pedagógica:** evidência e síntese.
- **Conteúdo:** resposta à pergunta principal, acompanhada de fonte, unidade, variáveis, população, limitações e alcance.
- **Tempo previsto:** 25 minutos.

O tempo remanescente será usado para abertura da disciplina, orientação do ambiente e intervalo entre os blocos.

## 9. Verificação e contraste

A futura implementação deverá confrontar:

- tipos antecipados e `DataFrame.dtypes`;
- significado estatístico e representação computacional;
- população pretendida e registros efetivamente disponíveis;
- afirmações descritivas e inferenciais;
- pergunta formulada e capacidade real dos dados.

Uma divergência entre antecipação e resultado deverá ser explicada, não apagada.

## 10. Evidência de aprendizagem

O estudante deverá registrar no futuro notebook:

- a fonte dos dados;
- a unidade de análise;
- duas colunas com tipos estatísticos e computacionais;
- uma pergunta estatística;
- a população de interesse;
- o alcance e uma limitação da conclusão.

A execução de `head()` ou `dtypes`, isoladamente, não constituirá evidência suficiente.

## 11. Síntese e limitações

O fechamento deverá responder:

1. O que representa cada registro?
2. Que pergunta pode ser respondida descritivamente?
3. Que ampliação da conclusão exigiria inferência?
4. Qual aspecto do processo de coleta limita a representatividade?
5. Que informação adicional seria necessária para uma generalização mais ampla?

A conclusão será escrita somente depois da inspeção do arquivo.

## 12. Estudo, exercícios e referências

### Materiais públicos

- [Apostila de Métodos Quantitativos](../apostila/apostila_mq.pdf), seções 1.1–1.3, páginas 8–10.
- [Banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf).
- [Palmer Penguins — arquivo bruto](../data/raw/penguins_raw.csv).

### Exercícios

- Barbetta et al., capítulo 1, exercício 2.
- Barbetta et al., capítulo 2, exercício 7.

### Referências de autoria

- BARBETTA et al., capítulo 1, seções 1.1–1.6; capítulo 2, seções 2.1–2.2.1.
- PINHEIRO et al., capítulo 1, seções 1.1–1.2.
- GORMAN; WILLIAMS; FRASER, 2014.

## 13. Critérios para implementação futura

- Executar sequencialmente sem estado oculto.
- Usar apenas o caminho relativo documentado.
- Não depender de conexão externa para carregar o conjunto principal.
- Usar `pandas` somente para as inspeções previstas.
- Separar tipos estatísticos de tipos computacionais.
- Não tratar os 344 registros como amostra aleatória simples.
- Não inventar população-alvo ou desenho amostral.
- Interpretar cada saída relevante em Markdown.
- Preservar a antecipação e seu contraste.
- Produzir a evidência observável definida para a semana.
