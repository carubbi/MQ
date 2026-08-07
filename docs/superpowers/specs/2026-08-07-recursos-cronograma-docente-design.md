# Recursos do cronograma docente da T199

## 1. Objetivo

Completar os recursos do cronograma docente de T199 — Métodos Quantitativos
por meio de materiais semanais rastreáveis ao projeto de ensino, ao planejamento
das unidades e ao grafo de referências.

A entrega compreenderá:

- materiais científicos de aula em Markdown;
- roteiros, também em Markdown, para a implementação futura dos notebooks
  guiados;
- inserção dos links no cronograma docente somente depois da criação e da
  validação dos respectivos arquivos.

Os instrumentos das ATs não integram este escopo e serão produzidos em etapa
posterior.

## 2. Autoridades e fontes

A produção deverá respeitar a seguinte hierarquia:

1. `mat/ensino/proj_ensino_2026.md`, como autoridade curricular;
2. `prof/ensino/cronograma_2026_2_docente.md`, como fonte canônica das semanas,
   datas, conteúdos, atividades e evidências;
3. `docs/planejamentos/2026-2/` e `docs/detalhamentos/2026-2/`, como
   fundamentação didática;
4. `prof/refs/mapas/grafo_referencias.json`, como índice das referências,
   páginas, tópicos, exercícios, questões e exemplos;
5. materiais públicos já existentes em `mat/`.

O grafo apoia a localização e a rastreabilidade das fontes, mas não substitui a
decisão pedagógica nem constitui, por si só, um recurso de aula.

## 3. Unidade de produção

Cada semana com encontro constitui uma unidade de produção e abrange os dois
blocos consecutivos da sexta-feira.

Uma semana de desenvolvimento receberá:

- um material científico em `mat/aulas/`;
- um roteiro de notebook guiado em `mat/notebooks/`.

Uma semana de revisão e AT receberá somente um material de revisão em
`mat/aulas/`. A prova, o gabarito e sua configuração no AVA permanecerão fora
desta entrega.

Feriados não receberão recursos.

## 4. Organização e nomes dos arquivos

Os dois artefatos de uma semana usarão o mesmo nome-base:

```text
mat/
├── aulas/
│   └── u1_s01_fundamentos_estatisticos.md
└── notebooks/
    └── u1_s01_fundamentos_estatisticos.md
```

O nome identificará:

- unidade, por `u1`, `u2` ou `u3`;
- semana da unidade, preservando a numeração do cronograma;
- tema principal em `snake_case`, sem acentos.

As lacunas decorrentes de feriados serão preservadas. Portanto, uma unidade
poderá possuir `s01` e `s03` sem possuir `s02`.

## 5. Material científico de aula

### 5.1 Finalidade

O arquivo em `mat/aulas/` será o material de apresentação e discussão em sala.
Ele deverá combinar fundamentação científica, notação, formulação matemática,
exemplos e interpretação.

O material será Markdown comum. Não haverá dependência, cabeçalho ou diretiva
de Marp ou de outro renderizador. O separador `---` será usado apenas como
convenção editorial entre slides.

### 5.2 Estrutura

Cada material seguirá, com adaptações justificadas ao tema:

1. título, identificação, data, conteúdos formais e resultado de aprendizagem;
2. pergunta orientadora;
3. conceitos e definições;
4. notação e formulação matemática;
5. exemplo proposto e previsão inicial;
6. resolução do exemplo;
7. aplicação ou discussão em sala;
8. erros comuns e cuidados interpretativos;
9. síntese;
10. estudo e exercícios;
11. referências.

Semanas de revisão reorganizarão essa estrutura em torno de problemas
integradores e não introduzirão conteúdo curricular novo.

### 5.3 Regras científicas e editoriais

- Variáveis e expressões em linha usarão `$...$`.
- Equações destacadas usarão `$$...$$`.
- Não serão usados `\(...\)` ou `\[...\]`.
- Toda variável será definida e, quando aplicável, acompanhada de unidade.
- Um exemplo será apresentado como problema antes da respectiva resolução.
- A resolução explicitará procedimento, cálculos, interpretação, pressupostos
  e limitações pertinentes.
- Resultados numéricos não serão apresentados sem contexto ou interpretação.
- Código será incluído somente quando indispensável à explicação; a progressão
  computacional ficará no roteiro de notebook.
- Material protegido das referências privadas não será reproduzido. Conceitos,
  exemplos e exercícios serão citados, sintetizados ou adaptados de forma
  autoral.

## 6. Roteiro do notebook guiado

### 6.1 Finalidade e estado

O arquivo em `mat/notebooks/` será uma especificação prévia do futuro
`.ipynb`. Ele não será apresentado como notebook executável e não conterá
saídas ou resultados computacionais inventados.

O futuro `.ipynb` poderá usar o mesmo nome-base do roteiro. A documentação
operacional deverá distinguir explicitamente os dois estados:

1. roteiro estrutural em `.md`;
2. implementação executável em `.ipynb`.

### 6.2 Estrutura

Cada roteiro conterá:

1. identificação, unidade, semana, data, conteúdos formais, duração, dados,
   bibliotecas previstas e nome do futuro `.ipynb`;
2. resultado de aprendizagem;
3. contexto e pergunta-problema;
4. preparação conceitual;
5. dados, entradas e dependências;
6. previsão antes da implementação;
7. caso reduzido ou resolução manual;
8. sequência planejada de células;
9. verificação e contraste;
10. evidência de aprendizagem;
11. síntese e limitações;
12. estudo, exercícios e referências;
13. critérios para implementação futura.

### 6.3 Especificação das futuras células

Cada bloco planejado declarará:

- tipo da futura célula: Markdown, código ou interpretação;
- finalidade estatística;
- entradas;
- operação computacional prevista;
- saída esperada quanto à sua forma, sem inventar valores;
- verificações necessárias;
- perguntas interpretativas;
- pressupostos e limitações a registrar.

### 6.4 Critérios para a implementação posterior

O roteiro preparará uma implementação que:

- execute sequencialmente sem estado oculto;
- use caminhos relativos;
- registre dependências;
- seja reproduzível;
- apresente tabelas e gráficos identificados;
- interprete cada saída relevante;
- mantenha separação entre notebook guiado, exercícios e AP.

## 7. Uso do grafo

Para cada semana, a seleção seguirá estas regras:

1. os códigos formais localizarão referências por `corresponde_a`;
2. os tópicos efetivamente ensinados refinarão a busca por `aborda`;
3. apostila e banco de questões poderão ser indicados diretamente aos
   estudantes;
4. os livros em `prof/refs/livros/` serão usados apenas como referências
   privadas para autoria;
5. Escovedo não será usado;
6. uma eventual relação `apoia` não autorizará inclusão automática em material
   discente;
7. conteúdo não previsto no projeto exigirá decisão pedagógica explícita antes
   de qualquer inclusão.

A migração futura de `pertinencia_t199` para valor binário não bloqueia esta
produção. Enquanto a migração não ocorrer, a seleção será governada pelos
códigos curriculares, pelos tópicos e pelas relações explícitas, e não por uma
conversão automática dos valores atuais de pertinência.

ANOVA não será incluída nos materiais de regressão apenas por apoiar a
compreensão da regressão simples ou múltipla.

## 8. Inventário da entrega

| Unidade | Semana | Data | Natureza | Conteúdos | Material de aula | Roteiro |
| --- | ---: | --- | --- | --- | --- | --- |
| I | 1 | 07/08 | desenvolvimento | 01.01 | sim | sim |
| I | 2 | 14/08 | feriado | — | não | não |
| I | 3 | 21/08 | desenvolvimento | 01.02 | sim | sim |
| I | 4 | 28/08 | desenvolvimento | 01.03 | sim | sim |
| I | 5 | 04/09 | desenvolvimento | 01.04 | sim | sim |
| I | 6 | 11/09 | desenvolvimento | 02.01 | sim | sim |
| II | 1 | 18/09 | revisão e AT1 | 01.01–01.04 e 02.01 | sim | não |
| II | 2 | 25/09 | desenvolvimento | 02.01 e 02.02 | sim | sim |
| II | 3 | 02/10 | desenvolvimento | 02.03 | sim | sim |
| II | 4 | 09/10 | desenvolvimento | 02.03 e 02.04 | sim | sim |
| II | 5 | 16/10 | desenvolvimento | 02.04 | sim | sim |
| II | 6 | 23/10 | revisão e AT2 | 02.02–02.04 | sim | não |
| III | 1 | 30/10 | desenvolvimento | 03.01 e 03.02 | sim | sim |
| III | 2 | 06/11 | desenvolvimento | 03.02 e 03.03 | sim | sim |
| III | 3 | 13/11 | desenvolvimento | 03.04 | sim | sim |
| III | 4 | 20/11 | feriado | — | não | não |
| III | 5 | 27/11 | desenvolvimento | 03.04 | sim | sim |
| III | 6 | 04/12 | revisão e AT3 | 03.01–03.04 | sim | não |

Totais:

- 16 materiais de aula;
- 13 roteiros de notebook;
- 29 arquivos Markdown;
- nenhum recurso para os dois feriados.

## 9. Sequência de execução

A produção ocorrerá por unidade:

1. Unidade I;
2. revisão e validação do padrão;
3. Unidade II;
4. revisão e validação;
5. Unidade III;
6. validação integral;
7. inclusão dos links no cronograma docente;
8. identificação dos impactos no futuro cronograma discente.

Os links de uma unidade somente serão inseridos depois que seus arquivos
existirem e passarem pelas validações aplicáveis.

## 10. Validações

Cada unidade deverá satisfazer:

- correspondência com o projeto, o cronograma e o planejamento;
- cobertura somente dos conteúdos previstos;
- referências existentes e rastreáveis no grafo;
- ausência de Escovedo;
- ausência de inclusão automática por relação meramente indireta ou de apoio;
- uso exclusivo de `$...$` e `$$...$$` para LaTeX;
- exemplos resolvidos com interpretação;
- ausência de resultados computacionais inventados;
- ausência de afirmação de executabilidade nos roteiros;
- ausência de títulos vazios, marcadores genéricos, `TODO` ou `TBD`;
- links relativos válidos;
- recursos existentes antes da inclusão no cronograma;
- compatibilidade do volume de conteúdo com os dois blocos da semana.

Ao final, todas as 16 semanas com encontro deverão possuir material de aula e
as 13 semanas de desenvolvimento deverão possuir roteiro de notebook. Os dois
feriados deverão permanecer sem recursos.

## 11. Fora do escopo

Não integram esta entrega:

- implementação dos arquivos `.ipynb`;
- configuração de renderizador de slides;
- exportação para PDF, HTML ou PowerPoint;
- criação dos instrumentos, gabaritos ou configurações das ATs;
- configuração do AVA;
- publicação de cópias dos livros privados;
- geração do cronograma discente.
