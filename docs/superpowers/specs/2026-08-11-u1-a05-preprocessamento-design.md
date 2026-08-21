# Especificação consolidada — Aula 5: tipos, qualidade e pré-processamento básico

## Estado e objetivo

Especificação implementada. A Aula 5 articula classificação de variáveis,
qualidade dos dados e pré-processamento básico sem separar o diagnóstico da
justificativa metodológica. O conjunto bruto do Palmer Penguins é preservado e
cada transformação ocorre em uma cópia auditável.

## Artefatos

- `aulas/u1_a05_tipos_qualidade_preprocessamento.md`;
- `notebooks/u1_a05_tipos_qualidade_preprocessamento.ipynb`;
- `notebooks/resolvidos/u1_a05_tipos_qualidade_preprocessamento.ipynb`.

O notebook anterior `notebooks/u1_s03_organizacao_representacao_dados.ipynb`
foi substituído pela organização por aula. As referências ativas usam o novo
caminho.

## Organização didática

### Ciclo 1 — Tipos estatísticos de variáveis

- distinguir variável qualitativa nominal, qualitativa ordinal, quantitativa
  discreta e quantitativa contínua;
- separar valor numérico de significado quantitativo;
- tratar identificadores como identificadores, mesmo quando armazenados como
  números ou textos.

### Ciclo 2 — Tipo estatístico versus tipo computacional

- relacionar significado estatístico, `dtype` e operações admissíveis;
- converter `Date Egg` para data em uma cópia do conjunto;
- converter categorias somente após verificar valores e ausências;
- conferir se a conversão preserva frequências e significado.

### Ciclo 3 — Completude e valores ausentes

- calcular quantidade, proporção e percentual de ausências;
- definir o subconjunto de variáveis exigido por uma análise;
- informar o denominador após a seleção de casos completos;
- distinguir ausência, zero e valor não aplicável;
- impedir imputações ou exclusões automáticas sem justificativa.

### Ciclo 4 — Consistência, unicidade e pré-processamento

- comparar duplicatas integrais, identificador isolado e chave composta;
- reconhecer que `Individual ID` se repete entre campanhas;
- verificar a chave composta por `studyName` e `Individual ID`;
- padronizar nomes de colunas em `snake_case` na cópia;
- comparar dimensões, tipos, categorias e ausências antes e depois.

Cada ciclo segue a sequência: problema e contexto, fundamentação científica,
caso reduzido e resolução manual, aplicação computacional, comparação,
diagnóstico e interpretação.

## Evidências do conjunto de dados

A aplicação usa `data/raw/penguins_raw.csv`, com 344 observações e 17
variáveis. O arquivo contém ausências em medidas corporais, sexo, isótopos e
comentários; não contém linhas integralmente duplicadas. `Date Egg` é carregada
como texto e pode ser convertida para data. As categorias textuais são
inspecionadas antes de qualquer conversão.

## Contrato do notebook discente

- primeira célula idêntica a `notebooks/assets/heads/head_unifor.md`;
- segunda célula iniciada por `# Resumo` e seguida pelo título da aula;
- quatro ciclos correspondentes ao material teórico;
- células de código compostas apenas por comentários orientadores;
- nenhuma contagem de execução ou saída salva;
- tabelas e perguntas interpretativas vinculadas às operações solicitadas.

## Contrato do notebook resolvido

- mesma sequência, tipos e identificadores de células da versão discente;
- implementação de todas as células de código;
- execução sequencial sem saídas de erro;
- resultados tabulares acompanhados por legendas em UTF-8;
- respostas interpretativas delimitadas pelo conjunto e pelas variáveis
  analisadas.

## Delimitações

- não aprofundar imputação;
- não excluir valores extremos ou duplicidades automaticamente;
- não codificar categorias para modelagem;
- não normalizar ou padronizar escalas;
- não discretizar variáveis contínuas;
- reservar `pd.cut()`, critérios de classes e histogramas para a Aula 6;
- reservar a cerca de Tukey para a análise univariada.

## Critérios de validação

- correspondência entre aula, notebook discente e notebook resolvido;
- cabeçalho institucional canônico;
- JSON e `nbformat` válidos;
- células discentes sem implementação e saídas;
- versão resolvida executada sem erros;
- links locais válidos;
- ausência de referências ativas ao nome anterior;
- testes de recursos didáticos e `git diff --check` aprovados.
