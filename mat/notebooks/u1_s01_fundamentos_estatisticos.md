# Roteiro do notebook guiado — Fundamentos estatísticos

> Estado: roteiro estrutural em Markdown; não executável. Este arquivo define a implementação futura de `u1_s01_fundamentos_estatisticos.ipynb`.

## 1. Identificação

- **Disciplina:** T199 — Métodos Quantitativos
- **Unidade:** I
- **Semana:** 1
- **Data:** 07/08/2026
- **Aulas:** 1 e 2
- **Duração de referência:** 200 minutos de encontros, distribuíveis conforme a
  configuração de horários do semestre
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

## 6. Caso reduzido, resolução manual ou decisão conceitual

Selecionar, depois do carregamento, um recorte pequeno do próprio arquivo com
identificador, espécie, ilha, data e uma medida corporal.

Solicitar a classificação manual de:

- unidade de análise;
- identificador;
- variável qualitativa;
- variável quantitativa e respectiva unidade;
- valor ausente;
- afirmação descritiva;
- afirmação que exigiria inferência.

Essa classificação preparará a leitura de `DataFrame.dtypes` sem confundir tipo computacional com papel estatístico.

## 7. Sequência funcional do futuro notebook

### Bloco 1 — Apresentação e pergunta

- **Tipo de célula:** Markdown.
- **Função pedagógica:** formulação.
- **Conteúdo:** identificação, fonte, contexto, pergunta principal e evidência esperada.
- **Tempo previsto:** 10 minutos.

### Bloco 2 — Preparação conceitual

- **Tipo de célula:** Markdown.
- **Função pedagógica:** explicação.
- **Conteúdo:** síntese operacional de fonte, registro, unidade de análise,
  variável, população, amostra, descrição e inferência, sem reproduzir os
  slides.
- **Tempo previsto:** 20 minutos.

### Bloco 3 — Dependência e carregamento

- **Tipo de célula:** código.
- **Função pedagógica:** processamento.
- **Entradas:** `../data/raw/penguins_raw.csv`.
- **Ação prevista:** importar `pandas` e usar `pandas.read_csv()`.
- **Produto esperado:** objeto `DataFrame`, sem fornecer resultados inventados
  no roteiro.
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

### Bloco 8 — Comparação e diagnóstico

- **Tipo de célula:** Markdown.
- **Função pedagógica:** verificação.
- **Conteúdo:** comparação entre significado estatístico e representação
  computacional; diagnóstico da correspondência entre a pergunta, os registros
  disponíveis e a população de interesse.
- **Tempo previsto:** 20 minutos.

### Bloco 9 — Evidência e síntese

- **Tipo de célula:** Markdown.
- **Função pedagógica:** evidência e síntese.
- **Conteúdo:** resposta à pergunta principal, acompanhada de fonte, unidade, variáveis, população, limitações e alcance.
- **Tempo previsto:** 25 minutos.

O tempo remanescente permitirá transições, dúvidas e adequação da execução à
configuração dos encontros.

## 8. Verificação e contraste

A futura implementação deverá confrontar:

- significado estatístico e representação computacional;
- população pretendida e registros efetivamente disponíveis;
- afirmações descritivas e inferenciais;
- pergunta formulada e capacidade real dos dados.

Diferenças entre a semântica documentada e a representação computacional
deverão ser explicadas, não apenas apontadas.

## 9. Evidência de aprendizagem

O estudante deverá registrar no futuro notebook:

- a fonte dos dados;
- a unidade de análise;
- duas colunas com tipos estatísticos e computacionais;
- uma pergunta estatística;
- a população de interesse;
- o alcance e uma limitação da conclusão.

A execução de `head()` ou `dtypes`, isoladamente, não constituirá evidência suficiente.

## 10. Síntese e limitações

O fechamento deverá responder:

1. O que representa cada registro?
2. Que pergunta pode ser respondida descritivamente?
3. Que ampliação da conclusão exigiria inferência?
4. Qual aspecto do processo de coleta limita a representatividade?
5. Que informação adicional seria necessária para uma generalização mais ampla?

A conclusão será escrita somente depois da inspeção do arquivo.

## 11. Estudo, exercícios e referências

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

## 12. Critérios para implementação futura

- Executar sequencialmente sem estado oculto.
- Usar apenas o caminho relativo documentado.
- Não depender de conexão externa para carregar o conjunto principal.
- Usar `pandas` somente para as inspeções previstas.
- Separar tipos estatísticos de tipos computacionais.
- Não tratar os 344 registros como amostra aleatória simples.
- Não inventar população-alvo ou desenho amostral.
- Interpretar cada saída relevante em Markdown.
- Comparar significado estatístico e representação computacional.
- Produzir a evidência observável definida para a semana.
