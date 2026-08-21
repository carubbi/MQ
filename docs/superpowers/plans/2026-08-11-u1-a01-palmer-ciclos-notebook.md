# Palmer Penguins e ciclos da Aula 1 — registro de implementação

## Estado

Implementação concluída e validada.

## Objetivo realizado

O notebook da Aula 1 foi reorganizado para introduzir Google Colab, Python,
`pandas` e estrutura dos dados com o Palmer Penguins. A versão discente mantém
as células de código sem solução e a versão resolvida registra uma execução
reprodutível do mesmo percurso.

## Artefatos finais

- Aula: `aulas/u1_a01_ambientacao_dados.md`.
- Notebook discente: `notebooks/u1_a01_ambientacao_dados.ipynb`.
- Notebook resolvido: `notebooks/resolvidos/u1_a01_ambientacao_dados.ipynb`.
- Cabeçalho canônico: `notebooks/assets/heads/head_unifor.md`.

## Organização didática

O notebook contém 63 células: 37 Markdown e 26 de código. O percurso está
organizado em quatro ciclos:

1. notebook, Python e `pandas`;
2. fonte, carregamento e estruturas do `pandas`;
3. seleção e filtragem;
4. transformação segura e combinação simples.

Os exercícios trabalham com as 344 observações e 17 variáveis da versão bruta
do Palmer Penguins. A identificação considera `studyName` e `Individual ID`;
os exemplos incluem seleção, filtro da ilha Dream, cópia, conversão da massa de
gramas para quilogramas e `pd.concat()` com subconjuntos de observações reais.

## Delimitações preservadas

- não antecipar a classificação estatística das variáveis;
- não antecipar tratamento de valores ausentes;
- não introduzir registros artificiais;
- não sobrescrever o conjunto bruto;
- manter uma transformação por etapa sempre que isso favorecer a leitura do
  estudante.

## Validação registrada

- JSON e `nbformat` válidos;
- quatro ciclos presentes e ordenados;
- células discentes sem implementação, execução ou saídas;
- versão resolvida com execuções sequenciais e sem saídas de erro;
- cabeçalho institucional canônico;
- ausência de referências ao Internet Firewall Data;
- `git diff --check` sem ocorrências.
