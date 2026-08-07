# Adaptação dos blocos do AVA para T199 — desenho

## 1. Objetivo

Reconstruir os blocos HTML de `prof/AVA` para T199 — Métodos Quantitativos,
eliminando conteúdos herdados de Resolução de Problemas com Grafos e
preservando o formato modular usado para publicação no AVA/Moodle.

O trabalho será restrito aos arquivos locais de `prof/AVA`. Não haverá
configuração direta do Moodle nem alterações no projeto de ensino, nos
cronogramas ou nos materiais públicos.

## 2. Fontes e autoridade

As informações serão obtidas nesta ordem:

1. `prof/ensino/cronograma_2026_2_docente.md`: datas, acompanhamentos,
   entregas, ATs, APs e segundas chamadas;
2. `mat/ensino/proj_ensino_2026.md`: identificação, pré-requisito, ementa,
   objetivos, conteúdos e bibliografia;
3. `mat/ensino/cronograma_2026_2_t199_64_65.md`: linguagem pública, grupo de
   turmas e estado dos recursos semanais;
4. `mat/ensino/plataformas.md`: plataformas de exercícios e recursos
   interativos;
5. decisões aprovadas nesta especificação;
6. conteúdo legado do AVA, somente quando genérico e compatível.

Em caso de divergência, o conteúdo legado será substituído pela fonte de maior
autoridade. Nenhum bloco publicará caminho interno de `prof/`.

## 3. Inventário final

### 3.1 Blocos comuns

Serão mantidos e reconstruídos:

- `apres.html`;
- `bibliografia.html`;
- `contrato.html`;
- `fraude.html`;
- `mat_apoio.html`;
- `metodo.html`;
- `mini_cv.html`;
- `motivacao.html`;
- `plan_ensino.html`;
- `pre-req.html`;
- `recursos.html`;
- `refs.html`;
- `saiba_mais.html`;
- `visao_geral.html`.

### 3.2 Avaliações

Os arquivos:

- `aval_T290-09-19_62-63.html`;
- `aval_T290-16-17_30-31.html`;

serão removidos e substituídos por:

- `aval_T199-64-65.html`.

O código de turma permanecerá restrito ao nome interno do bloco de avaliação
e ao mapa de publicação do `README.md`.

### 3.3 Documentação e ativo

- `README.md` será reescrito para documentar o inventário, as fontes, o mapa de
  publicação e as validações de T199.
- `imgs/MQ_bkg.jpg` será preservado sem alteração.

## 4. Conteúdo por bloco

| Arquivo | Conteúdo de T199 |
| --- | --- |
| `apres.html` | Boas-vindas; investigação estatística; resolução manual e verificação computacional |
| `visao_geral.html` | Carga horária; três unidades; resultado geral de aprendizagem |
| `plan_ensino.html` | Identificação, ementa, objetivos e conteúdos `01.01` a `03.04` |
| `pre-req.html` | Pré-requisito T100 e conhecimentos recomendados para matemática, Python e Jupyter |
| `metodo.html` | Ciclo didático integrado; AT; AP; acompanhamentos; composição das avaliações e critérios de aprovação |
| `aval_T199-64-65.html` | Datas, escopos, entregas, acompanhamentos e segundas chamadas |
| `contrato.html` | Comunicação, frequência, dispositivos, participação, repositório e prazos |
| `fraude.html` | Integridade em ATs, notebooks, repositório, dados, referências e uso declarado de IA |
| `bibliografia.html` | Bibliografia básica, complementar e periódicos do projeto de ensino |
| `mat_apoio.html` | Repositório MQ, materiais semanais, notebooks, apostila, banco de questões e dados |
| `recursos.html` | Plataformas de exercícios e recursos interativos catalogados |
| `refs.html` | Referências e recursos estatísticos adicionais |
| `saiba_mais.html` | Aprofundamento opcional em estatística, dados e inferência |
| `motivacao.html` | Decisões com dados, variabilidade, incerteza e modelagem |
| `mini_cv.html` | Minicurrículo existente, com revisão de consistência HTML |

Os quatro placeholders de imagens sobre grafos serão removidos de
`motivacao.html`. Não serão criados placeholders substitutos nesta etapa.

## 5. Metodologia e avaliações

### 5.1 Abordagem didática

Os blocos apresentarão o ciclo didático integrado:

1. problema e contexto;
2. fundamentação científica;
3. caso reduzido e resolução manual, quando pertinentes;
4. aplicação computacional;
5. comparação, diagnóstico e interpretação.

As APs serão desenvolvidas em Python com Jupyter Notebook. Não haverá menção a
Java, `Accepted` ou implementação de algoritmos.

### 5.2 Avaliação teórica

- Cada AT será avaliada de 0 a 10 pontos.
- Cada AT terá dez questões objetivas de mesmo peso, valendo 1 ponto cada.
- A AT1 terá oito questões de análise descritiva e duas de probabilidade.
- AT2 e AT3 seguirão os escopos definidos no cronograma docente.
- As ATs serão realizadas sem consulta no AVA/Moodle com Safe Exam Browser.
- A entrada será permitida até 15 minutos após o início.

### 5.3 Avaliação prática

Cada AP será avaliada de 0 a 10 pontos:

| Dimensão | Pontos | Evidências |
| --- | ---: | --- |
| Processo e acompanhamentos | 4,0 | Participação, entregas intermediárias, histórico do repositório, justificativas e incorporação das orientações |
| Produto técnico | 4,0 | Dados, código, cálculos, gráficos, correção estatística, organização e reprodutibilidade |
| Interpretação e domínio | 2,0 | Conclusões, limitações, comunicação dos resultados, declaração de IA e justificativa individual das decisões |

Os acompanhamentos serão formativos e não produzirão notas isoladas. A
dimensão processual será atribuída no fechamento da AP, considerando o
conjunto das evidências.

Não haverá anúncio de apresentação oral dos trabalhos nesta versão. Uma
apresentação somente poderá ser incluída depois de formalizada no cronograma
docente.

### 5.4 Composição

Cada AV será calculada por:

$$
AV = 0{,}70 \times AT + 0{,}30 \times AP
$$

AT e AP serão avaliadas individualmente de 0 a 10 pontos.

Os critérios de aprovação serão preservados:

$$
MP = \frac{AV1 + AV2}{2}
$$

- $MP < 4$ implica reprovação;
- $AV3 < 4$ implica reprovação;
- $NF = (MP + AV3) / 2$;
- a aprovação exige $NF \geq 5$ e frequência mínima de 75%.

## 6. Materiais e links

`mat_apoio.html` apontará para o repositório público
`https://github.com/carubbi/MQ` e organizará:

- 16 materiais de aula, sendo o primeiro finalizado e os demais identificados
  como em construção;
- 14 notebooks, sendo os dois primeiros finalizados e os demais identificados
  como em construção;
- `mat/apostila/apostila_mq.pdf`;
- `mat/apostila/banco_questoes_provas_2026_2.pdf`;
- conjuntos de dados públicos em `mat/data`;
- plataformas externas de exercícios catalogadas em
  `mat/ensino/plataformas.md`.

`recursos.html`, `refs.html` e `saiba_mais.html` usarão prioritariamente os
destinos já catalogados em `mat/ensino/plataformas.md` e nas fontes
bibliográficas da disciplina. Recursos externos serão descritos como apoio e
não como avaliações.

Links externos abrirão em nova aba com:

```html
target="_blank" rel="noopener noreferrer"
```

## 7. Padrão técnico

- Os arquivos permanecerão fragmentos HTML, sem `html`, `head` ou `body`.
- A hierarquia de títulos começará em `h3`.
- Serão usados parágrafos curtos, listas e tabelas apenas quando contribuírem
  para a leitura no Moodle.
- Não serão adicionados scripts.
- Estilos inline serão evitados, exceto no layout já necessário ao
  minicurrículo.
- Não haverá códigos individuais de turma dentro dos blocos comuns.
- Não haverá caminhos locais ou referências a `prof/`.

## 8. Validação

A implementação deverá comprovar:

1. presença dos 14 blocos comuns e de `aval_T199-64-65.html`;
2. ausência dos dois arquivos `aval_T290-*`;
3. ausência de T290, RPG, grafos, DFS, BFS, Java, `Accepted`, apresentações e
   datas das turmas legadas;
4. correspondência dos conteúdos `01.01` a `03.04`, datas de AT/AP,
   acompanhamentos, entregas e segundas chamadas com as fontes;
5. ATs de 0 a 10, dez questões de 1 ponto e matriz específica da AT1;
6. APs de 0 a 10, rubrica `4 + 4 + 2` e acompanhamentos sem notas isoladas;
7. fórmula `AV = 0,70 × AT + 0,30 × AP` consistente;
8. links do GitHub apontando para arquivos públicos existentes;
9. atributos de segurança em todos os links externos;
10. fragmentos HTML estruturalmente válidos;
11. correspondência do `README.md` com o inventário e o mapa de publicação;
12. ausência de alterações fora de `prof/AVA`.

## 9. Limites

Esta etapa não:

- publica ou configura os blocos no Moodle;
- cria instrumentos detalhados das ATs ou APs;
- formaliza apresentações dos trabalhos;
- conclui materiais ou notebooks marcados como em construção;
- altera cronogramas, projeto de ensino ou recursos públicos.
