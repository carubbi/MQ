# Aulas 5 e 6 com Palmer Penguins — registro de implementação

## Estado

Implementação concluída e validada.

## Objetivo realizado

As Aulas 5 e 6 foram separadas em materiais teóricos e notebooks de aplicação
prática. O Palmer Penguins bruto é a fonte comum dos exemplos e exercícios. As
versões discentes apresentam instruções em células de código sem solução; as
versões resolvidas registram código, resultados e interpretações.

## Artefatos finais

### Aula 5

- Aula: `aulas/u1_a05_tipos_qualidade_preprocessamento.md`.
- Notebook discente:
  `notebooks/u1_a05_tipos_qualidade_preprocessamento.ipynb`.
- Notebook resolvido:
  `notebooks/resolvidos/u1_a05_tipos_qualidade_preprocessamento.ipynb`.

### Aula 6

- Aula: `aulas/u1_a06_frequencias_representacao.md`.
- Notebook discente:
  `notebooks/u1_a06_frequencias_representacao.ipynb`.
- Notebook resolvido:
  `notebooks/resolvidos/u1_a06_frequencias_representacao.ipynb`.

## Organização da Aula 5

O notebook contém 41 células: 28 Markdown e 13 de código. Seus ciclos são:

1. tipos estatísticos de variáveis;
2. tipo estatístico versus tipo computacional;
3. completude e valores ausentes;
4. consistência, unicidade e pré-processamento.

A prática preserva a base bruta, diagnostica ausências e duplicidades, converte
tipos de modo justificado e verifica cada transformação. `Individual ID` não é
tratado como chave isolada; a análise de unicidade considera sua relação com
`studyName`.

## Organização da Aula 6

O notebook contém 51 células: 33 Markdown e 18 de código. Seus ciclos são:

1. frequências absoluta, relativa e acumulada;
2. dados quantitativos agrupados em classes;
3. critérios para definição das classes;
4. escolha da representação.

Sturges e largura fixa integram o núcleo manual. Freedman–Diaconis e Scott são
mantidos como referências computacionais antecipadas, com indicação das medidas
ainda não estudadas. Barras, histogramas, linha e dispersão são produzidos como
figuras independentes, cada uma em sua célula e seguida por legenda própria.

## Delimitações preservadas

- não substituir valores ausentes por zero;
- não remover duplicidades automaticamente;
- não sobrescrever os dados brutos;
- não interpretar associação visual como causalidade;
- não generalizar a composição do arquivo para a composição das espécies na
  natureza;
- preservar lacunas temporais em vez de ligar períodos sem observações.

## Validação registrada

- notebooks válidos em JSON e `nbformat` 4;
- correspondência estrutural entre versões discentes e resolvidas;
- células discentes sem implementação, execução ou saídas;
- versões resolvidas executadas no `.venv`, com contagens sequenciais e sem
  saídas de erro;
- 12 saídas tabulares e 12 legendas na Aula 5;
- nove figuras independentes e nove legendas na Aula 6;
- cronogramas e links ativos sincronizados;
- ausência de referências ativas ao Internet Firewall Data.
