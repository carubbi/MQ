# Recursos da Unidade I Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir e validar os cinco materiais científicos de aula e os cinco roteiros de notebook das semanas com encontro da Unidade I, vinculando-os ao cronograma docente somente depois de sua existência.

**Architecture:** Cada semana será representada por um par de arquivos Markdown com o mesmo nome-base: um material científico em `mat/aulas/` e um roteiro estrutural em `mat/notebooks/`. Um validador reutilizável verificará estrutura, rastreabilidade curricular, tópicos do grafo, links locais e convenções editoriais antes da inclusão dos recursos no cronograma privado.

**Tech Stack:** Markdown comum, LaTeX com `$...$` e `$$...$$`, Python 3.12, `unittest`, JSON e o grafo canônico em `prof/refs/mapas/grafo_referencias.json`.

## Global Constraints

- Trabalhar somente nas semanas 1, 3, 4, 5 e 6 da Unidade I; 14/08 continuará sem recursos por ser feriado.
- Produzir exatamente cinco materiais em `mat/aulas/` e cinco roteiros em `mat/notebooks/`.
- Não criar arquivos `.ipynb`, instrumentos das ATs, configuração do AVA, lista nova em `mat/exs/` ou renderização de slides.
- Usar Markdown comum, sem cabeçalho, dependência ou diretiva de Marp.
- Usar `$...$` e `$$...$$`; não usar `\(...\)` ou `\[...\]`.
- Usar `---` somente como separador editorial dos slides.
- Definir símbolos e unidades na primeira ocorrência.
- Apresentar o problema antes de sua resolução e interpretar cada resultado.
- Organizar cada tópico como ciclo integrado: problema e contexto,
  fundamentação científica, caso reduzido quando pertinente, aplicação
  computacional, comparação, diagnóstico e interpretação.
- Não associar rigidamente etapas pedagógicas a um bloco ou horário
  institucional.
- Manter os slides teóricos genéricos, com exemplos adaptados das fontes ou
  explicitamente sintéticos; reservar datasets da disciplina, suas variáveis e
  seus resultados para os roteiros e futuros notebooks práticos.
- Não inventar saídas computacionais nos roteiros.
- Não criar seção, registro ou verificação obrigatórios de antecipação;
  perguntas sobre o comportamento esperado poderão ocorrer informalmente em
  aula.
- Tratar o item “caso reduzido, resolução manual ou decisão conceitual” como condicional.
- Distinguir tipo de célula — Markdown ou código — de sua função pedagógica.
- Manter a evidência do notebook separada do acompanhamento e da entrega da AP.
- Usar `corresponde_a` para os conteúdos e `aborda` para os tópicos.
- Não usar Escovedo.
- Não promover automaticamente conteúdo ligado apenas por relação indireta ou de apoio.
- Citar livros privados sem criar links para `prof/refs/livros/` nos materiais discentes.
- Adicionar ao cronograma somente links para arquivos existentes e validados.
- Preservar a alteração preexistente do usuário em `mat/ensino/fluxo_ensino.md` e não incluí-la nos commits desta execução.
- Manter `prof/ensino/cronograma_2026_2_docente.md` e `docs/modelos/notebook-guiado.md` privados e fora dos commits.
- Usar `apply_patch` para criar ou alterar arquivos de texto.
- Em cada commit, adicionar somente os caminhos explicitamente indicados no respectivo passo.

## File Structure

### Arquivos públicos a criar

- `mat/aulas/u1_s01_fundamentos_estatisticos.md` — slides das Aulas 1 e 2.
- `mat/notebooks/u1_s01_fundamentos_estatisticos.md` — roteiro do futuro notebook das Aulas 1 e 2.
- `mat/aulas/u1_s03_organizacao_representacao_dados.md` — slides das Aulas 5 e 6.
- `mat/notebooks/u1_s03_organizacao_representacao_dados.md` — roteiro do futuro notebook das Aulas 5 e 6.
- `mat/aulas/u1_s04_analise_univariada.md` — slides das Aulas 7 e 8.
- `mat/notebooks/u1_s04_analise_univariada.md` — roteiro do futuro notebook das Aulas 7 e 8.
- `mat/aulas/u1_s05_analise_bivariada.md` — slides das Aulas 9 e 10.
- `mat/notebooks/u1_s05_analise_bivariada.md` — roteiro do futuro notebook das Aulas 9 e 10.
- `mat/aulas/u1_s06_probabilidade.md` — slides das Aulas 11 e 12.
- `mat/notebooks/u1_s06_probabilidade.md` — roteiro do futuro notebook das Aulas 11 e 12.
- `scripts/grafo_refs/validate_teaching_resources.py` — validador estrutural e curricular reutilizável.
- `tests/grafo_refs/test_validate_teaching_resources.py` — testes unitários e teste integral da Unidade I.

### Arquivos privados a modificar

- `docs/modelos/notebook-guiado.md` — distinguir roteiro `.md` de implementação `.ipynb` e registrar a granularidade semanal.
- `prof/ensino/cronograma_2026_2_docente.md` — receber os links dos dez recursos somente após a validação integral.

### Fontes somente para leitura

- `docs/superpowers/specs/2026-08-07-recursos-cronograma-docente-design.md`
- `mat/ensino/proj_ensino_2026.md`
- `docs/planejamentos/2026-2/unidade-i.md`
- `docs/detalhamentos/2026-2/unidade-i.md`
- `docs/exercicios/2026-2/unidade-i.md`
- `prof/refs/mapas/grafo_referencias.json`
- `mat/data/README.md`
- `mat/data/raw/penguins_raw.csv`
- `mat/data/processed/penguins.csv`
- `mat/apostila/apostila_mq.pdf`
- `mat/apostila/banco_questoes_provas_2026_2.pdf`

---

### Task 1: Contrato executável dos recursos em Markdown

**Files:**
- Create: `scripts/grafo_refs/validate_teaching_resources.py`
- Create: `tests/grafo_refs/test_validate_teaching_resources.py`
- Modify privately: `docs/modelos/notebook-guiado.md`

**Interfaces:**
- Consumes: `prof/refs/mapas/grafo_referencias.json`.
- Produces: `validate_resource(path: Path, kind: str, graph: dict, text: str | None = None) -> list[str]`.
- Produces: CLI `python -m scripts.grafo_refs.validate_teaching_resources --graph GRAPH --aula PATH_A --roteiro PATH_B`.
- Contract: `kind` accepts only `"aula"` or `"roteiro"`; an empty findings list means valid; the CLI returns `0` when all files pass and `1` otherwise.

- [ ] **Step 1: Write the failing validator tests**

Create `tests/grafo_refs/test_validate_teaching_resources.py` with:

```python
import json
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.validate_teaching_resources import validate_resource


ROOT = Path(__file__).resolve().parents[2]
GRAPH = json.loads(
    (ROOT / "prof/refs/mapas/grafo_referencias.json").read_text(encoding="utf-8")
)

VALID_AULA = """# Fundamentos estatísticos

- **Conteúdos formais:** `01.01`
- **Tópicos:** Investigação estatística; População; Amostra

---

## Pergunta orientadora
Pergunta.

## Conceitos e definições
Conceitos.

## Notação e formulação matemática
$n$ é o tamanho da amostra.

## Exemplo proposto
Problema.

## Resolução do exemplo
Resolução e interpretação.

## Aplicação ou discussão em sala
Discussão.

## Erros comuns e cuidados interpretativos
Cuidados.

## Síntese
Síntese.

## Estudo e exercícios
Estudo.

## Referências
Apostila de Métodos Quantitativos, seção 1.1.
"""

VALID_ROTEIRO = """# Roteiro do notebook guiado — Fundamentos estatísticos

> Estado: roteiro estrutural em Markdown; não executável.

## 1. Identificação
- **Conteúdos formais:** `01.01`
- **Tópicos:** Investigação estatística; População; Amostra

## 2. Resultado de aprendizagem
Resultado observável.

## 3. Contexto e pergunta-problema
Pergunta substantiva.

## 4. Preparação conceitual
Conceitos.

## 5. Dados, entradas e dependências
Dados.

## 7. Sequência funcional do futuro notebook
Blocos funcionais.

## 8. Verificação e contraste
Contraste.

## 9. Evidência de aprendizagem
Resultado e justificativa.

## 10. Síntese e limitações
Perguntas de fechamento.

## 11. Estudo, exercícios e referências
Referências.

## 12. Critérios para implementação futura
Critérios específicos.
"""


class TeachingResourceValidatorTests(unittest.TestCase):
    def test_accepts_valid_aula(self):
        self.assertEqual([], validate_resource(Path("aula.md"), "aula", GRAPH, VALID_AULA))

    def test_accepts_valid_roteiro_without_conditional_section_six(self):
        self.assertEqual(
            [], validate_resource(Path("roteiro.md"), "roteiro", GRAPH, VALID_ROTEIRO)
        )

    def test_rejects_forbidden_latex_and_marp(self):
        invalid = VALID_AULA + "\nmarp: true\n\\(x\\)\n"
        findings = validate_resource(Path("aula.md"), "aula", GRAPH, invalid)
        self.assertIn("diretiva Marp proibida", findings)
        self.assertIn("delimitador LaTeX proibido", findings)

    def test_rejects_unknown_content_and_topic(self):
        invalid = VALID_AULA.replace("`01.01`", "`99.99`").replace(
            "Investigação estatística", "Tópico inexistente"
        )
        findings = validate_resource(Path("aula.md"), "aula", GRAPH, invalid)
        self.assertIn("conteúdo curricular desconhecido: 99.99", findings)
        self.assertIn("tópico desconhecido: Tópico inexistente", findings)

    def test_rejects_incomplete_sections(self):
        invalid = VALID_ROTEIRO.replace("## 9. Evidência de aprendizagem", "## Evidência")
        findings = validate_resource(Path("roteiro.md"), "roteiro", GRAPH, invalid)
        self.assertIn("seção ausente: ## 9. Evidência de aprendizagem", findings)

    def test_rejects_formal_anticipation_section(self):
        invalid = (
            VALID_ROTEIRO
            + "\n## 6. Antecipação conceitual antes do cálculo ou da execução\n"
        )
        findings = validate_resource(Path("roteiro.md"), "roteiro", GRAPH, invalid)
        self.assertIn("seção formal de antecipação proibida", findings)

    def test_rejects_escovedo_and_missing_slide_separator(self):
        invalid = VALID_AULA.replace("\n---\n", "\n").replace(
            "Apostila de Métodos Quantitativos", "Escovedo"
        )
        findings = validate_resource(Path("aula.md"), "aula", GRAPH, invalid)
        self.assertIn("referência Escovedo proibida", findings)
        self.assertIn("separador editorial ausente", findings)

    def test_rejects_broken_local_link(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aula.md"
            text = VALID_AULA + "\n[arquivo](arquivo-ausente.csv)\n"
            path.write_text(text, encoding="utf-8")
            findings = validate_resource(path, "aula", GRAPH)
        self.assertIn("link local quebrado: arquivo-ausente.csv", findings)


if __name__ == "__main__":
    unittest.main()
```

The optional `text` parameter isolates unit tests from the filesystem. In
normal CLI usage it remains `None`, and the function reads `path`.

- [ ] **Step 2: Run the tests and verify the expected failure**

Run:

```bash
.venv/bin/python -m unittest tests.grafo_refs.test_validate_teaching_resources -v
```

Expected: `ERROR` with `ModuleNotFoundError` for `validate_teaching_resources`.

- [ ] **Step 3: Implement the validator**

Create `scripts/grafo_refs/validate_teaching_resources.py` with these constants and behaviors:

```python
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


AULA_HEADINGS = (
    "## Pergunta orientadora",
    "## Conceitos e definições",
    "## Notação e formulação matemática",
    "## Exemplo proposto",
    "## Resolução do exemplo",
    "## Aplicação ou discussão em sala",
    "## Erros comuns e cuidados interpretativos",
    "## Síntese",
    "## Estudo e exercícios",
    "## Referências",
)

ROTEIRO_HEADINGS = (
    "## 1. Identificação",
    "## 2. Resultado de aprendizagem",
    "## 3. Contexto e pergunta-problema",
    "## 4. Preparação conceitual",
    "## 5. Dados, entradas e dependências",
    "## 7. Sequência funcional do futuro notebook",
    "## 8. Verificação e contraste",
    "## 9. Evidência de aprendizagem",
    "## 10. Síntese e limitações",
    "## 11. Estudo, exercícios e referências",
    "## 12. Critérios para implementação futura",
)

CONTENT_RE = re.compile(r"\b\d{2}\.\d{2}\b")
TOPICS_RE = re.compile(r"^- \*\*Tópicos:\*\* (.+)$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN_LATEX = ("\\(", "\\)", "\\[", "\\]")
FORBIDDEN_MARKERS = ("TODO", "TBD")
FORBIDDEN_MARP_RE = re.compile(
    r"^(?:marp|theme|paginate|math):\s*", re.MULTILINE | re.IGNORECASE
)
FORMAL_ANTICIPATION_RE = re.compile(
    r"^##\s+(?:\d+\.\s+)?Antecipação\b", re.MULTILINE | re.IGNORECASE
)


def _known_values(graph: dict) -> tuple[set[str], set[str]]:
    contents = {
        node["codigo"]
        for node in graph["nos"]
        if node.get("tipo") == "conteudo_curricular"
    }
    topics = {
        node["nome"]
        for node in graph["nos"]
        if node.get("tipo") == "topico"
    }
    return contents, topics


def _broken_links(path: Path, text: str) -> list[str]:
    findings = []
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = (path.parent / target.split("#", 1)[0]).resolve()
        if not target_path.exists():
            findings.append(f"link local quebrado: {target}")
    return findings


def validate_resource(
    path: Path,
    kind: str,
    graph: dict,
    text: str | None = None,
) -> list[str]:
    if kind not in {"aula", "roteiro"}:
        raise ValueError(f"tipo de recurso inválido: {kind}")
    source = path.read_text(encoding="utf-8") if text is None else text
    findings: list[str] = []
    headings = AULA_HEADINGS if kind == "aula" else ROTEIRO_HEADINGS
    for heading in headings:
        if heading not in source:
            findings.append(f"seção ausente: {heading}")
    if kind == "aula" and "\n---\n" not in source:
        findings.append("separador editorial ausente")
    if kind == "roteiro" and "não executável" not in source:
        findings.append("estado não executável ausente")
    if kind == "roteiro" and FORMAL_ANTICIPATION_RE.search(source):
        findings.append("seção formal de antecipação proibida")
    if FORBIDDEN_MARP_RE.search(source):
        findings.append("diretiva Marp proibida")
    if any(delimiter in source for delimiter in FORBIDDEN_LATEX):
        findings.append("delimitador LaTeX proibido")
    for marker in FORBIDDEN_MARKERS:
        if re.search(rf"\b{marker}\b", source):
            findings.append(f"marcador incompleto proibido: {marker}")

    known_contents, known_topics = _known_values(graph)
    codes = set(CONTENT_RE.findall(source))
    if not codes:
        findings.append("conteúdo formal ausente")
    for code in sorted(codes - known_contents):
        findings.append(f"conteúdo curricular desconhecido: {code}")

    topic_match = TOPICS_RE.search(source)
    if topic_match is None:
        findings.append("tópicos ausentes")
    else:
        topics = {
            item.strip().strip("`")
            for item in topic_match.group(1).split(";")
            if item.strip()
        }
        for topic in sorted(topics - known_topics):
            findings.append(f"tópico desconhecido: {topic}")

    if "escovedo" in source.casefold():
        findings.append("referência Escovedo proibida")
    findings.extend(_broken_links(path, source))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--aula", type=Path, action="append", default=[])
    parser.add_argument("--roteiro", type=Path, action="append", default=[])
    arguments = parser.parse_args()
    if not arguments.aula and not arguments.roteiro:
        parser.error("informe ao menos um recurso")

    graph = json.loads(arguments.graph.read_text(encoding="utf-8"))
    all_findings = []
    for kind, paths in (("aula", arguments.aula), ("roteiro", arguments.roteiro)):
        for path in paths:
            for finding in validate_resource(path, kind, graph):
                all_findings.append(f"{path}: {finding}")
    for finding in all_findings:
        print(finding)
    return 1 if all_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the validator tests**

Run:

```bash
.venv/bin/python -m unittest tests.grafo_refs.test_validate_teaching_resources -v
```

Expected: nine tests, all `OK`.

- [ ] **Step 5: Update the private notebook model**

In `docs/modelos/notebook-guiado.md`:

- add a lifecycle section distinguishing `mat/notebooks/*.md` as structural routes from future `.ipynb` implementations;
- remove anticipation as a formal section, record or mandatory verification;
- allow the teacher to use questions about expected behavior informally when
  pertinent;
- make the reduced manual case conditional;
- distinguish cell type from pedagogical role;
- state that one route covers an integrated topic cycle and does not depend on
  consecutive blocks;
- use the weekly basename examples approved in the specification.

Run:

```bash
rg -n "roteiro estrutural|ciclo didático|tipo da futura célula|função pedagógica|u1_s01" docs/modelos/notebook-guiado.md
```

Expected: all five concepts present. Do not stage this private file.

- [ ] **Step 6: Commit only the validator and its tests**

```bash
git add scripts/grafo_refs/validate_teaching_resources.py tests/grafo_refs/test_validate_teaching_resources.py
git diff --cached --name-only
git commit -m "test: validar recursos didaticos em markdown"
```

Expected staged paths: exactly the validator and its test. Confirm that `mat/ensino/fluxo_ensino.md` and `docs/modelos/notebook-guiado.md` are absent.

---

### Task 2: Semana 1 — Fundamentos estatísticos

**Files:**
- Create: `mat/aulas/u1_s01_fundamentos_estatisticos.md`
- Create: `mat/notebooks/u1_s01_fundamentos_estatisticos.md`

**Interfaces:**
- Consumes: contents `01.01`; topics `Investigação estatística`, `Estatística descritiva`, `Estatística inferencial`, `População`, `Amostra`, `Amostragem`, `Representatividade`, `Unidade de análise` and `Tipos de variáveis`.
- Consumes: `mat/data/raw/penguins_raw.csv`.
- Produces: the validated resource pair linked later by the Week 1 block of the teacher schedule.

- [ ] **Step 1: Verify the graph references**

Run:

```bash
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01
```

Confirm these sources and ranges in the output:

- Apostila, sections 1.1–1.3, PDF pages 8–10;
- Barbetta, sections 1.1–1.6, PDF pages 12–23;
- Barbetta, sections 2.1–2.2.1, PDF pages 24–31;
- Navidi, introduction and section 1.1, PDF pages 23–30;
- Pinheiro, sections 1.1–1.2, PDF pages 20–23.

Do not use Barbetta 2.2.2 on sample-size determination.

- [ ] **Step 2: Create the slide structure and scientific core**

Create `mat/aulas/u1_s01_fundamentos_estatisticos.md` with:

- title, discipline, Unit I, Week 1, date 07/08/2026 and content `01.01`;
- the exact graph topics listed in the task interface;
- an agenda for the complete 200-minute integrated cycle, with topics,
  reference times, adaptable organization and learning evidence, without
  associating the stages rigidly with institutional time slots;
- guiding question: “O que representa cada registro de um conjunto de dados e até onde as conclusões obtidas podem ser generalizadas?”;
- a recurring, explicitly synthetic server-request dataset, whose context is
  adapted from Barbetta, section 1.4;
- a source note after the table caption stating
  `Fonte: adaptado de Barbetta, Bornia e Reis (2010, seção 1.4).` on the same
  Markdown line as the caption;
- presentation of the reduced data and a short observation question before
  the corresponding definitions;
- a worked example mapping the six movements of a statistical investigation
  to the recurring server-request context, adapted from Barbetta, sections
  1.1–1.4;
- `assets/barbetta_fig21.png` in a dedicated slide about statistical
  investigation and `assets/barbetta_fig22.png` in a dedicated slide between
  population, sampling and inference, both with alternative text, sequential
  captions and explicit source;
- sequential captions immediately after each scientific or didactically
  interpretable table, using the approved `**Tabela X - Descrição curta.**`
  pattern without revealing an answer the student must still construct;
- distinction among source, observation, variable, unit of analysis, population, census, sample and sampling;
- distinction between descriptive and inferential statistics;
- notation $N$ for population size, $n$ for sample size, $\theta$ for a population parameter and $\widehat{\theta}$ for a statistic or estimate;
- origin of observational data, variability, selection bias, measurement bias and limits of representativeness.

- [ ] **Step 3: Add the proposed and solved example**

Use one small, explicitly synthetic dataset of server requests throughout the
slides. Do not retain a second dataset of service records. Include request
identifier, time, server, latency in milliseconds and status, with different
latencies, one failed request and one missing latency.

The conceptual progression and resolution must:

- identify one request as the unit of analysis;
- distinguish one observation from one server;
- identify qualitative, quantitative and temporal variables;
- use the observed latencies to make variability visible before defining it;
- distinguish the observed records from a conceptual target population;
- show that missing latency is not zero and that an unusual latency is not
  automatically an error;
- explain why an available database is not automatically a simple random
  sample of the target population;
- delimit descriptive conclusions and warn against unsupported generalization.

Use the proposed example as an integrative return to the same table rather
than reproducing it. Add a short in-class sampling decision based on alternative
logging windows, asking students to approve or reject representativeness with
justification.

- [ ] **Step 4: Add study references and exercises**

Add public links:

- `../apostila/apostila_mq.pdf`, sections 1.1–1.3, pages 8–10;
- `../apostila/banco_questoes_provas_2026_2.pdf`, section 1.1, pages 7–13.

Consolidate these links in **Materiais didáticos**, under **Estudo e
exercícios**. Do not repeat internal teaching-material links in the conceptual
slides.

Cite without private links:

- Apostila, sections 1.1–1.3, pages 8–10;
- Barbetta, chapter 1, sections 1.1–1.6, and chapter 2, sections 2.1–2.2.1;
- Navidi, chapter 1, introduction and section 1.1;
- Pinheiro, chapter 1, sections 1.1–1.2;
- Banco de questões, questions 6 and 13;
- Barbetta, chapter 1, exercise 2, and chapter 2, exercise 7.

- [ ] **Step 5: Create the Week 1 notebook route**

Create `mat/notebooks/u1_s01_fundamentos_estatisticos.md` with the approved
sections 1–12. Section 6 is conditional and will be retained in Week 1 because
the reduced classification activity prepares the computational inspection.

Specify these functional blocks:

1. Markdown — discipline, context and substantive question;
2. code — import `pandas` and read `../data/raw/penguins_raw.csv`;
3. code — inspect `shape`, `columns`, `head()` and `dtypes`;
4. Markdown — identify source, record, variables and types;
5. Markdown — formulate a statistical question and delimit population, sample and reach;
6. Markdown — contrast the conceptual definitions with the observed data
   structure;
7. Markdown — record the evidence and limitations.

The expected output descriptions may say “dimensions”, “column list” and “data types”, but may not supply invented values.

- [ ] **Step 6: Validate the pair**

```bash
.venv/bin/python -m scripts.grafo_refs.validate_teaching_resources \
  --graph prof/refs/mapas/grafo_referencias.json \
  --aula mat/aulas/u1_s01_fundamentos_estatisticos.md \
  --roteiro mat/notebooks/u1_s01_fundamentos_estatisticos.md
```

Expected: exit `0` and no findings.

- [ ] **Step 7: Commit the Week 1 pair**

```bash
git add mat/aulas/u1_s01_fundamentos_estatisticos.md mat/notebooks/u1_s01_fundamentos_estatisticos.md
git diff --cached --name-only
git commit -m "feat: adicionar recursos da semana 1 da unidade I"
```

---

### Task 3: Semana 3 — Organização e representação de dados

**Files:**
- Create: `mat/aulas/u1_s03_organizacao_representacao_dados.md`
- Create: `mat/notebooks/u1_s03_organizacao_representacao_dados.md`

**Interfaces:**
- Consumes: content `01.02`; topics `Importação de dados`, `Pré-processamento`, `Tipos de variáveis`, `Frequência`, `Tabela` and `Gráfico`.
- Consumes: `mat/data/raw/penguins_raw.csv`.
- Produces: the validated resource pair for Week 3.

- [ ] **Step 1: Verify the graph references**

Confirm with `--content 01.02`:

- Apostila, sections 2.1–3.2, pages 11–26;
- Barbetta, sections 3.1–3.3, pages 52–68;
- Pinheiro, sections 1.3–1.4, pages 24–34.

- [ ] **Step 2: Build the scientific slides**

Create the deck with:

- distinction between statistical and computational types;
- completeness, consistency, conversion, missing values and duplicates;
- absolute frequency $f_i$, relative frequency $h_i=f_i/n$ and cumulative frequency $F_i=\sum_{j\le i}f_j$;
- Sturges $k=\lceil 1+\log_2 n\rceil$;
- Freedman–Diaconis $h=2IQR\,n^{-1/3}$;
- Scott $h=3{,}5s\,n^{-1/3}$ as computational reference;
- tables and graphs selected according to variable type.

Use this explicitly synthetic microcase for conversion and duplication:

```text
id,tempo_min,canal
1,"18","A"
2,"NA","A"
2,"NA","A"
3,"erro","B"
```

Resolve which values require conversion, missing-value representation, duplicate investigation and preservation of an audit trail.

For frequencies and histogram classes, use generic or explicitly synthetic
variables. Reserve `species`, `island` and `body_mass_g` for the notebook
route.

- [ ] **Step 3: Add the in-class exercise and interpretation**

Present a short numerical series before its resolution. Calculate absolute, relative and cumulative frequencies, apply Sturges, and explain why changing class limits may change the perceived shape without changing the observations.

State that no class rule is universally optimal and that Scott is a reference, not a new curricular requirement.

- [ ] **Step 4: Add references and exercises**

Link the apostila and bank. Cite:

- Apostila, sections 2.1–3.2;
- Barbetta, sections 3.1–3.3;
- Pinheiro, sections 1.3–1.4;
- Barbetta, chapter 3, complementary exercise 8(a–c);
- Pinheiro, chapter 1, exercise 1.5_P(a).

- [ ] **Step 5: Create the notebook route**

Plan these blocks:

1. load the raw dataset;
2. inspect names, types, missing values and duplicates;
3. justify which variables need conversion and which representations fit them;
4. demonstrate the synthetic microcase separately from the real data;
5. record transformations and reasons;
6. build qualitative frequency tables;
7. group `body_mass_g` using Sturges and Freedman–Diaconis, with Scott as reference;
8. plan bar charts and histograms with titles, axes and units;
9. contrast class criteria and record the Week 3 evidence.

The route must specify output forms, not numeric outputs.

- [ ] **Step 6: Validate and commit**

Run the validator for the pair. Then:

```bash
git add mat/aulas/u1_s03_organizacao_representacao_dados.md mat/notebooks/u1_s03_organizacao_representacao_dados.md
git commit -m "feat: adicionar recursos da semana 3 da unidade I"
```

---

### Task 4: Semana 4 — Análise univariada

**Files:**
- Create: `mat/aulas/u1_s04_analise_univariada.md`
- Create: `mat/notebooks/u1_s04_analise_univariada.md`

**Interfaces:**
- Consumes: content `01.03`; topics `Média`, `Mediana`, `Moda`, `Quantil`, `Amplitude`, `Variância`, `Desvio-padrão`, `Intervalo interquartil`, `Coeficiente de variação`, `Assimetria`, `Valor discrepante` and `Boxplot`.
- Consumes: `mat/data/processed/penguins.csv`.
- Produces: the validated resource pair for Week 4.

- [ ] **Step 1: Verify and delimit references**

Confirm with `--content 01.03`:

- Apostila, sections 4.1–6.1, pages 27–58;
- Barbetta, sections 3.3–3.4, pages 59–83;
- Morettin and Bussab, sections 3.1–3.5, pages 52–68;
- Pinheiro, sections 1.5–1.9, pages 35–58.

Do not include kurtosis from Apostila section 6.2 because it is not required by content `01.03`.

- [ ] **Step 2: Add measures and notation to the slides**

Define and interpret:

```text
\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2
s = \sqrt{s^2}
IQR = Q_3-Q_1
CV = \frac{s}{\bar{x}}\times 100\%
```

Render those expressions with `$$...$$`, define all symbols and state the conditions under which $CV$ has a coherent relative interpretation.

Add grouped-data approximations using class midpoints and identify the median and modal classes without introducing interpolated formulas.

- [ ] **Step 3: Resolve the synthetic example**

Use the labeled synthetic values $3600$, $3700$, $3800$, $3900$ and $6000$ grams.

Show:

- mean $4200$ g;
- median $3800$ g;
- amplitude $2400$ g;
- sample variance $1\,025\,000$ g$^2$;
- sample standard deviation approximately $1012{,}42$ g;
- with the stated quartile convention, $Q_1=3700$ g, $Q_3=3900$ g and $IQR=200$ g;
- Tukey fences at $3400$ g and $4200$ g;
- why $6000$ g is a signal for investigation, not an automatic deletion.

Compare mean and median before and after the extreme value and interpret resistance.

- [ ] **Step 4: Add references and exercises**

Link the apostila and bank. Cite:

- Apostila, sections 4.1–6.1;
- Barbetta, sections 3.3–3.4;
- Morettin and Bussab, sections 3.1–3.5;
- Pinheiro, sections 1.5–1.9;
- Pinheiro, exercise 1.7_P(a,c);
- Barbetta, chapter 3, exercise 4;
- Pinheiro, exercise 1.4_P(b–d).

- [ ] **Step 5: Create the notebook route**

Plan:

1. load the processed dataset;
2. relate center, dispersion and possible group effects to the substantive
   question about `body_mass_g`;
3. calculate a reduced case manually;
4. calculate measures for the full data and by `species`;
5. compare original and grouped-data approximations;
6. plan histogram and boxplot;
7. inspect observations beyond Tukey fences without excluding them;
8. compare measures before and after a labeled synthetic extreme;
9. record evidence with values, units, interpretation and limitation;
10. separate the AP1 accompaniment from the notebook evidence.

- [ ] **Step 6: Validate and commit**

Run the validator for the pair. Then:

```bash
git add mat/aulas/u1_s04_analise_univariada.md mat/notebooks/u1_s04_analise_univariada.md
git commit -m "feat: adicionar recursos da semana 4 da unidade I"
```

---

### Task 5: Semana 5 — Análise bivariada

**Files:**
- Create: `mat/aulas/u1_s05_analise_bivariada.md`
- Create: `mat/notebooks/u1_s05_analise_bivariada.md`

**Interfaces:**
- Consumes: content `01.04`; topics `Tabela de contingência`, `Associação`, `Covariância` and `Correlação linear`.
- Consumes: `mat/data/processed/penguins.csv`.
- Produces: the validated resource pair for Week 5.

- [ ] **Step 1: Verify the references**

Confirm with `--content 01.04`:

- Apostila, sections 15.1–15.2, pages 148–149;
- Barbetta, sections 11.1–11.2, pages 317–324;
- Morettin and Bussab, sections 4.2–4.6, pages 87–106;
- Pinheiro, sections 2.1–2.2, pages 60–71.

- [ ] **Step 2: Build the contingency-table section**

Define $n_{ij}$, row and column marginals and conditional percentages with explicit denominators.

Use this explicitly synthetic contingency table with generic row and column
categories. Do not use `species`, `island` or verified results from the course
dataset in the slides:

```text
           Canal A  Canal B  Canal C
Grupo 1          18       12       10
Grupo 2           9       16       15
Grupo 3          13       12       15
```

Ask for a conditional comparison before resolving it. Explain the effect of the collection design and why the table does not establish causality.

- [ ] **Step 3: Build the correlation section**

Define:

```text
s_{xy} = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})
r = \frac{s_{xy}}{s_xs_y}
```

Use generic variables with explicit units and a small synthetic dataset. Keep
`flipper_length_mm`, `body_mass_g` and results calculated from the course
dataset in the notebook route.

Interpret direction and linear association only after the scatterplot. Discuss
possible hidden groups, outliers, linearity, sensitivity and the absence of an
automatic causal conclusion. Do not introduce Spearman, Kendall, heatmaps or
universal magnitude bands.

- [ ] **Step 4: Add references and exercises**

Link the apostila and bank. Cite:

- Apostila, sections 15.1–15.2;
- Barbetta, sections 11.1–11.2;
- Morettin and Bussab, sections 4.2–4.6;
- Pinheiro, sections 2.1–2.2;
- Pinheiro, exercises 2.1_P, 2.2_P, 2.5_P(c–e) and 2.7_P.

- [ ] **Step 5: Create the notebook route**

Plan:

1. load processed data;
2. formulate the questions about the `species`–`island` pattern and the
   direction of the quantitative relation;
3. build contingency counts and conditional percentages;
4. compare a quantitative variable among groups only descriptively;
5. calculate covariance and Pearson correlation in a reduced case;
6. create the scatterplot before computing the full correlation;
7. calculate the correlation for complete pairs;
8. contrast aggregate and species-aware views without adding a new coefficient;
9. record evidence and limitations;
10. separate AP1 accompaniment.

- [ ] **Step 6: Validate and commit**

Run the validator for the pair. Then:

```bash
git add mat/aulas/u1_s05_analise_bivariada.md mat/notebooks/u1_s05_analise_bivariada.md
git commit -m "feat: adicionar recursos da semana 5 da unidade I"
```

---

### Task 6: Semana 6 — Probabilidade e Bayes

**Files:**
- Create: `mat/aulas/u1_s06_probabilidade.md`
- Create: `mat/notebooks/u1_s06_probabilidade.md`

**Interfaces:**
- Consumes: content `02.01`; topics `Experimento aleatório`, `Espaço amostral`, `Evento`, `Regra da adição`, `Regra do produto`, `Probabilidade condicional`, `Independência`, `Probabilidade total` and `Teorema de Bayes`.
- Produces: the validated resource pair for Week 6.

- [ ] **Step 1: Verify the references**

Confirm with `--content 02.01`:

- Apostila, sections 8.1–8.9, pages 74–89;
- Barbetta, sections 4.1–4.5, pages 94–116;
- Morettin and Bussab, sections 5.1–5.4, pages 120–137;
- Pinheiro, sections 3.1–3.4, pages 89–111.

- [ ] **Step 2: Add the probability definitions and rules**

Define and interpret:

```text
P(A^c)=1-P(A)
P(A\cup B)=P(A)+P(B)-P(A\cap B)
P(A\mid B)=\frac{P(A\cap B)}{P(B)}
P(A\cap B)=P(A\mid B)P(B)
P(A\cap B)=P(A)P(B) \quad \text{under independence}
P(B)=\sum_i P(B\mid A_i)P(A_i)
P(A_i\mid B)=\frac{P(B\mid A_i)P(A_i)}{\sum_jP(B\mid A_j)P(A_j)}
```

Distinguish independence from mutual exclusivity and direct from inverse conditional probability.

- [ ] **Step 3: Resolve the detector example**

Use a synthetic anomaly detector:

- anomaly prevalence $P(A)=0{,}01$;
- sensitivity $P(+\mid A)=0{,}90$;
- false-positive rate $P(+\mid A^c)=0{,}05$.

Before the resolution, ask whether most positive alerts correspond to anomalies.

Resolve:

```text
P(+)=0,90(0,01)+0,05(0,99)=0,0585
P(A\mid +)=\frac{0,90(0,01)}{0,0585}\approx 0,1538
```

Interpret the base-rate effect: despite $90\%$ sensitivity, only about $15{,}38\%$ of positive alerts represent anomalies under the stated model.

- [ ] **Step 4: Add references and exercises**

Link the apostila and bank. Cite:

- Apostila, sections 8.1–8.9;
- Barbetta, sections 4.1–4.5;
- Morettin and Bussab, sections 5.1–5.4;
- Pinheiro, sections 3.1–3.4;
- Pinheiro, exercises 3.8_P, 3.9_P and 3.10_P.

Do not use the Barbetta chapter 5 file because it treats random variables and distributions beyond the Week 6 scope.

- [ ] **Step 5: Create the notebook route**

Plan:

1. formulate events and a finite sample space;
2. represent a union, intersection or conditional relation manually before
   computational verification;
3. represent events by sets, a tree or a frequency table;
4. calculate complement, union, product and conditional probability;
5. verify a simple calculation with a reproducible simulation using `numpy.random.default_rng()` and an explicit seed;
6. solve the anomaly-detector example by total probability and Bayes;
7. contrast $P(+\mid A)$ with $P(A\mid +)$;
8. record evidence and interpretation of the base rate;
9. keep the final 30-minute AP1 accompaniment separate.

- [ ] **Step 6: Validate and commit**

Run the validator for the pair. Then:

```bash
git add mat/aulas/u1_s06_probabilidade.md mat/notebooks/u1_s06_probabilidade.md
git commit -m "feat: adicionar recursos da semana 6 da unidade I"
```

---

### Task 7: Validação integral e links no cronograma docente

**Files:**
- Modify: `tests/grafo_refs/test_validate_teaching_resources.py`
- Modify privately: `prof/ensino/cronograma_2026_2_docente.md`

**Interfaces:**
- Consumes: all ten Unit I resources and `validate_resource`.
- Produces: a regression test for the complete Unit I inventory.
- Produces privately: five valid resource blocks in the teacher schedule.

- [ ] **Step 1: Add the Unit I inventory test**

Append:

```python
    def test_all_unit_i_resources_exist_and_validate(self):
        names = (
            "u1_s01_fundamentos_estatisticos.md",
            "u1_s03_organizacao_representacao_dados.md",
            "u1_s04_analise_univariada.md",
            "u1_s05_analise_bivariada.md",
            "u1_s06_probabilidade.md",
        )
        findings = []
        for name in names:
            for directory, kind in (("aulas", "aula"), ("notebooks", "roteiro")):
                path = ROOT / "mat" / directory / name
                self.assertTrue(path.is_file(), path)
                findings.extend(
                    f"{path}: {finding}"
                    for finding in validate_resource(path, kind, GRAPH)
                )
        self.assertEqual([], findings)
```

- [ ] **Step 2: Run focused and full graph tests**

```bash
.venv/bin/python -m unittest tests.grafo_refs.test_validate_teaching_resources -v
.venv/bin/python -m unittest discover -s tests/grafo_refs -v
```

Expected: all tests `OK`.

- [ ] **Step 3: Commit the inventory gate**

```bash
git add tests/grafo_refs/test_validate_teaching_resources.py
git diff --cached --name-only
git commit -m "test: exigir recursos completos da unidade I"
```

- [ ] **Step 4: Capture the private schedule baseline**

```bash
shasum -a 256 prof/ensino/cronograma_2026_2_docente.md
```

Record the hash in the execution report.

- [ ] **Step 5: Add resource blocks to the five Unit I weeks**

After each week’s “Atividade e evidência”, add:

```markdown
- **Recursos:**
  - **Material de aula:** [título](../../mat/aulas/NOME.md).
  - **Roteiro do notebook guiado:** [título](../../mat/notebooks/NOME.md).
```

Use these exact basenames:

- Week 1: `u1_s01_fundamentos_estatisticos.md`;
- Week 3: `u1_s03_organizacao_representacao_dados.md`;
- Week 4: `u1_s04_analise_univariada.md`;
- Week 5: `u1_s05_analise_bivariada.md`;
- Week 6: `u1_s06_probabilidade.md`.

Add a `Dados` item when the corresponding material uses:

- `../../mat/data/raw/penguins_raw.csv` in Weeks 1 and 3;
- `../../mat/data/processed/penguins.csv` in Weeks 4 and 5.

Week 6 will not receive a dataset link because its microcases are synthetic and specified within the resources.

Do not add a resource block to the 14/08 holiday.

- [ ] **Step 6: Validate all schedule links**

Run a local-link check from `prof/ensino/cronograma_2026_2_docente.md` and confirm:

- the original three authority links remain valid;
- the ten new material/route links are valid;
- the four dataset links are valid;
- no resource block exists under the holiday.

Also run:

```bash
rg -n "\\*\\*Recursos:\\*\\*" prof/ensino/cronograma_2026_2_docente.md
```

Expected: five matches in Unit I.

- [ ] **Step 7: Verify scope and working-tree preservation**

```bash
git status --short
git diff -- mat/ensino/fluxo_ensino.md
git diff -- prof/ensino/cronograma_2026_2_docente.md
```

Expected:

- `mat/ensino/fluxo_ensino.md` retains only the user’s preexisting correction;
- the private schedule shows only the five resource blocks;
- all public implementation changes have already been committed;
- no private book, `.ipynb`, AT instrument or AVA file has been added.

- [ ] **Step 8: Run the final verification**

```bash
.venv/bin/python -m unittest discover -s tests/grafo_refs -v
git log --oneline -8
git status --short --branch
```

Report:

- the ten public resources created;
- the five private schedule blocks added;
- test count and result;
- baseline and final hashes of the private schedule;
- the preserved user modification in `mat/ensino/fluxo_ensino.md`;
- any remaining work for Units II and III.
