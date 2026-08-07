# Adaptação do AVA para T199 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconstruir os blocos locais do AVA/Moodle para T199 — Métodos Quantitativos, eliminando resíduos de RPG e sincronizando conteúdos, avaliações e recursos com as fontes canônicas de 2026.2.

**Architecture:** Os arquivos continuarão como fragmentos HTML independentes, organizados por finalidade e publicados manualmente no Moodle. O cronograma docente e o projeto de ensino serão as autoridades; o cronograma discente fornecerá a linguagem pública e os estados dos recursos, enquanto `plataformas.md` fornecerá os recursos externos.

**Tech Stack:** HTML sem scripts, Markdown para documentação, Python 3.12 da `.venv` para validações estruturais e Git para checkpoints.

## Global Constraints

- Alterar somente `prof/AVA`; fontes canônicas e materiais públicos são somente leitura.
- Preservar `prof/AVA/imgs/MQ_bkg.jpg` sem alteração.
- Manter 14 blocos HTML comuns e somente `aval_T199-64-65.html` como bloco de avaliação.
- Remover `aval_T290-09-19_62-63.html` e `aval_T290-16-17_30-31.html`.
- Não mencionar RPG, grafos, DFS, BFS, Java, `Accepted` ou apresentações de trabalhos.
- Cada AT vale 10 pontos, contém dez questões objetivas de 1 ponto e usa SEB com tolerância de 15 minutos.
- A AT1 contém oito questões de análise descritiva e duas de probabilidade.
- Cada AP vale 10 pontos: processo e acompanhamentos 4, produto técnico 4, interpretação e domínio 2.
- Acompanhamentos são formativos, não geram notas isoladas e subsidiam o fechamento da dimensão processual.
- Usar `AV = 0,70 × AT + 0,30 × AP`.
- APs usam Python em Jupyter Notebook.
- Não anunciar apresentação oral enquanto ela não estiver formalizada no cronograma docente.
- Links externos devem usar `target="_blank" rel="noopener noreferrer"`.
- Os HTMLs são fragmentos: não adicionar `html`, `head`, `body`, scripts ou folhas de estilo.
- Estilos inline somente no layout de `mini_cv.html`.
- `prof/AVA` está ignorado por `.gitignore`; adicionar os arquivos finais com `git add -f`.
- Preservar as alterações preexistentes fora de `prof/AVA`, inclusive `mat/ensino/fluxo_ensino.md`, os dois relatórios removidos em `.superpowers/sdd` e as duas imagens Barbetta não rastreadas.

---

### Task 1: Registrar baselines e reconstruir a identidade da disciplina

**Files:**
- Modify: `prof/AVA/apres.html`
- Modify: `prof/AVA/visao_geral.html`
- Modify: `prof/AVA/plan_ensino.html`
- Modify: `prof/AVA/pre-req.html`
- Modify: `prof/AVA/motivacao.html`

**Interfaces:**
- Consumes: `mat/ensino/proj_ensino_2026.md` e a especificação aprovada.
- Produces: cinco blocos comuns com identidade, estrutura curricular e motivação de T199.

- [ ] **Step 1: Capturar baselines protegidos**

Run:

```bash
shasum -a 256 \
  prof/ensino/cronograma_2026_2_docente.md \
  mat/ensino/proj_ensino_2026.md \
  mat/ensino/cronograma_2026_2_t199_64_65.md \
  mat/ensino/plataformas.md \
  prof/AVA/imgs/MQ_bkg.jpg
git status --short
```

Expected source hashes:

- cronograma docente: `05a4a79a713d82f9f5d48c65074186688b5f1682c8687740e0168d38bec2136d`;
- projeto de ensino: `fe07b9c2f992d1d060091a244af2d2ed8e24fbe4ae7f70c1688164a910d57f56`;
- cronograma discente: `e7dd92a8f0015e94afb99b53c469d8ea979065546f50ed8ffc9fd7745312f284`;
- plataformas: `3b7b8f3f0690c124d8e5f75e57e3f3c040a392c31856443cb19e79b870a2ef13`.

Record the image hash from the command for the final protected-file check.

- [ ] **Step 2: Confirmar que os cinco blocos ainda contêm o legado**

Run:

```bash
rg -n -i \
  "Resolução de Problemas com Grafos|grafos|DFS|BFS|Python ou Java|T198" \
  prof/AVA/apres.html \
  prof/AVA/visao_geral.html \
  prof/AVA/plan_ensino.html \
  prof/AVA/pre-req.html \
  prof/AVA/motivacao.html
```

Expected: matches in all files except where a specific term does not occur; this is the RED gate demonstrating that the legacy remains.

- [ ] **Step 3: Reescrever `apres.html` e `visao_geral.html`**

Use `apply_patch`.

`apres.html` must contain:

- welcome to T199 — Métodos Quantitativos in 2026.2;
- investigation with data, statistical reasoning, manual resolution and computational verification;
- references to methodology, schedule, assessments and teaching materials.

`visao_geral.html` must contain:

- 72-hour workload;
- Unit I: statistical foundations and exploratory data analysis;
- Unit II: probability and probability distributions;
- Unit III: statistical inference and regression;
- one overall result stating that the student will organize, analyze, model and interpret data with statistical and computational support.

- [ ] **Step 4: Reescrever `plan_ensino.html`**

Use `apply_patch`. Copy exactly from the project:

- discipline: `T199 — Métodos Quantitativos`;
- official denomination: `T199 — MÉT QUANT EM COMPUTAÇÃO`;
- workload: 72 hours;
- modality: in person;
- prerequisite: `T100 — Modelagem para Matemática`;
- ementa;
- conceptual, procedural and attitudinal objectives of each unit;
- contents `01.01` through `03.04`;
- ODS 9.

Do not copy unchecked template text from the institutional project file.

- [ ] **Step 5: Reescrever `pre-req.html` e `motivacao.html`**

Use `apply_patch`.

`pre-req.html` must identify T100 and recommend:

- basic algebra and functions;
- interpretation of tables and graphs;
- elementary Python and Jupyter Notebook;
- willingness to justify analytical decisions.

`motivacao.html` must explain:

- decisions supported by data;
- variability and uncertainty;
- descriptive, probabilistic and inferential reasoning;
- model construction and diagnosis.

Remove all four graph-image placeholders and do not add replacement placeholders.

- [ ] **Step 6: Validar o primeiro conjunto**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path

paths = [
    Path("prof/AVA/apres.html"),
    Path("prof/AVA/visao_geral.html"),
    Path("prof/AVA/plan_ensino.html"),
    Path("prof/AVA/pre-req.html"),
    Path("prof/AVA/motivacao.html"),
]
text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
required = [
    "T199",
    "Métodos Quantitativos",
    "01.01",
    "03.04",
    "T100",
    "Jupyter",
    "variabilidade",
    "incerteza",
]
for item in required:
    assert item in text, item
for forbidden in ("Resolução de Problemas com Grafos", "DFS", "BFS", "Java"):
    assert forbidden not in text, forbidden
for path in paths:
    source = path.read_text(encoding="utf-8")
    assert "<html" not in source and "<body" not in source
print("identidade e plano de T199: OK")
PY
for path in \
  prof/AVA/apres.html \
  prof/AVA/visao_geral.html \
  prof/AVA/plan_ensino.html \
  prof/AVA/pre-req.html \
  prof/AVA/motivacao.html
do
  git diff --check --no-index /dev/null "$path" >/dev/null || test $? -eq 1
done
```

Expected: all assertions pass and the loop reports no whitespace error.

- [ ] **Step 7: Commit**

```bash
git add -f \
  prof/AVA/apres.html \
  prof/AVA/visao_geral.html \
  prof/AVA/plan_ensino.html \
  prof/AVA/pre-req.html \
  prof/AVA/motivacao.html
git commit -m "docs: adaptar identidade do AVA para T199"
```

---

### Task 2: Reconstruir metodologia, contrato, integridade e avaliações

**Files:**
- Modify: `prof/AVA/metodo.html`
- Modify: `prof/AVA/contrato.html`
- Modify: `prof/AVA/fraude.html`
- Create: `prof/AVA/aval_T199-64-65.html`
- Delete: `prof/AVA/aval_T290-09-19_62-63.html`
- Delete: `prof/AVA/aval_T290-16-17_30-31.html`

**Interfaces:**
- Consumes: cronograma docente, projeto de ensino e regras de avaliação aprovadas.
- Produces: políticas e agenda avaliativa consistentes para T199-64/65.

- [ ] **Step 1: Confirmar os conflitos avaliativos legados**

Run:

```bash
rg -n -i \
  "Accepted|Python ou Java|apresentação|4 pontos|2 pontos|T290|14/09|15/09|26/10|27/10|07/12|08/12" \
  prof/AVA/metodo.html \
  prof/AVA/contrato.html \
  prof/AVA/fraude.html \
  prof/AVA/aval_T290-09-19_62-63.html \
  prof/AVA/aval_T290-16-17_30-31.html
```

Expected: legacy matches, establishing the RED gate.

- [ ] **Step 2: Reescrever `metodo.html`**

Use `apply_patch`. Include these sections:

1. cycle: problem and context; scientific foundation; reduced case and manual resolution; computational application; comparison, diagnosis and interpretation;
2. AT: 0–10, ten objective questions worth 1 point, no consultation, SEB, 15-minute tolerance;
3. AP: Python in Jupyter Notebook, same repository across units, formative checkpoints and final delivery by AVA;
4. AP rubric:
   - process and checkpoints: 4 points;
   - technical product: 4 points;
   - interpretation and mastery: 2 points;
5. composition: `AV = (0,70 × AT) + (0,30 × AP)`;
6. approval:
   - `MP = (AV1 + AV2) / 2`;
   - `MP < 4` fails;
   - `AV3 < 4` fails;
   - `NF = (MP + AV3) / 2`;
   - approval requires `NF ≥ 5` and attendance of at least 75%.

State explicitly that checkpoints have no isolated grade. Omit any section or
claim about oral presentations.

- [ ] **Step 3: Reescrever `contrato.html` e `fraude.html`**

Use `apply_patch`.

`contrato.html` must preserve:

- AVA/Moodle and institutional communication channels;
- 15-minute arrival tolerance and student responsibility for attendance;
- appropriate device use;
- participation in checkpoints;
- repository access, deadlines and individual understanding.

Replace “acompanhamentos avaliativos” with formative checkpoints whose full
evidence supports the final process score.

`fraude.html` must address:

- unauthorized consultation or assistance in AT;
- copied notebooks, fabricated data, commits, execution or evidence;
- citation of datasets, books, code and external tools;
- declared AI use and purpose in the repository README;
- individual explanation of statistical choices, code, results and limitations;
- institutional accountability.

- [ ] **Step 4: Criar `aval_T199-64-65.html`**

Use `apply_patch`. The exact schedule is:

| Item | Checkpoints / delivery / application |
| --- | --- |
| AP1 | checkpoints 28/08 and 04/09; final checkpoint and delivery 11/09 at 23:59 |
| AT1 | 18/09; 10 questions, 8 descriptive analysis and 2 probability |
| AT1 second call | 25/09, `N6CD`, 21:00–22:40 |
| AP2 | checkpoints 02/10 and 09/10; final checkpoint 16/10; delivery 23/10 at 23:59 |
| AT2 | 23/10; contents `02.02`–`02.04`, mobilizing `02.01` |
| AT2 second call | 13/11, `N6CD`, 21:00–22:40 |
| AP3 | checkpoints 13/11 and 27/11; final checkpoint and delivery 04/12 at 23:59 |
| AT3 | 04/12; contents `03.01`–`03.04` |
| AT3 second call | 09/12, `N4AB`, 19:00–20:40 |

Also include:

- each AT is 0–10 with ten equal-weight questions;
- each AP is 0–10 with the `4 + 4 + 2` rubric;
- AP1 scope: reading, cleaning, descriptive analysis and presentation of data;
- AP2 scope: identification and application of probabilistic models;
- AP3 scope: relationships between variables, linear models, variance,
  parameter significance and variable selection;
- APs have no second call;
- only one AT application, first or second call;
- SEB and 15-minute entry tolerance;
- scope paragraphs:
  - AT1: descriptive analysis and probability `02.01`;
  - AT2: random variables and discrete/continuous models;
  - AT3: sampling, estimation, tests, correlation and regression.

Do not include an oral presentation.

- [ ] **Step 5: Remover os dois blocos T290**

Use `apply_patch` with `*** Delete File` for:

- `prof/AVA/aval_T290-09-19_62-63.html`;
- `prof/AVA/aval_T290-16-17_30-31.html`.

- [ ] **Step 6: Validar metodologia e avaliações**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path

root = Path("prof/AVA")
paths = [
    root / "metodo.html",
    root / "contrato.html",
    root / "fraude.html",
    root / "aval_T199-64-65.html",
]
text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
for item in (
    "0,70",
    "0,30",
    "10 pontos",
    "1 ponto",
    "4 pontos",
    "2 pontos",
    "Safe Exam Browser",
    "15 minutos",
    "28/08",
    "18/09",
    "25/09",
    "23/10",
    "13/11",
    "04/12",
    "09/12",
    "N6CD",
    "N4AB",
):
    assert item in text, item
for forbidden in (
    "T290",
    "Accepted",
    "Python ou Java",
    "apresentação oral",
    "apresentação do trabalho",
    "apresentação dos trabalhos",
    "14/09",
    "15/09",
    "26/10",
    "27/10",
    "07/12",
    "08/12",
):
    assert forbidden.casefold() not in text.casefold(), forbidden
assert not (root / "aval_T290-09-19_62-63.html").exists()
assert not (root / "aval_T290-16-17_30-31.html").exists()
print("metodologia e avaliações: OK")
PY
```

Expected: all assertions pass.

- [ ] **Step 7: Commit**

```bash
git add -f \
  prof/AVA/metodo.html \
  prof/AVA/contrato.html \
  prof/AVA/fraude.html \
  prof/AVA/aval_T199-64-65.html
git commit -m "docs: adaptar avaliações do AVA para T199"
```

The two T290 files were ignored and untracked, so their removal is validated
on the filesystem but does not appear as a Git deletion.

---

### Task 3: Atualizar bibliografia e recursos externos

**Files:**
- Modify: `prof/AVA/bibliografia.html`
- Modify: `prof/AVA/recursos.html`
- Modify: `prof/AVA/refs.html`
- Modify: `prof/AVA/saiba_mais.html`

**Interfaces:**
- Consumes: bibliography from the project, `mat/ensino/plataformas.md` and `mat/data/README.md`.
- Produces: official bibliography and optional external support without graph-related links.

- [ ] **Step 1: Confirmar as referências legadas**

Run:

```bash
rg -n -i \
  "Sedgewick|Wayne|Boaventura|Goldbarg|grafos|Coursera|SNAP|VisuAlgo|Graph Online|Nature" \
  prof/AVA/bibliografia.html \
  prof/AVA/recursos.html \
  prof/AVA/refs.html \
  prof/AVA/saiba_mais.html
```

Expected: graph-course references are present.

- [ ] **Step 2: Reescrever `bibliografia.html`**

Use `apply_patch`. Preserve the official project categories and entries:

**Basic:**

- Barbetta, Bornia and Reis (2010);
- Montgomery, Hubele and Runger (2004);
- Morettin and Bussab (2010);
- Pinheiro et al. (2009);
- Navidi (2012), *Statistics for Engineers and Scientists*.

**Complementary:**

- Moore, Flinger and Notz (2017);
- Cramer (1973);
- Fonseca and Martins (2015);
- Melsa and Sage (1973);
- Navidi (2012), *Probabilidade e estatística para ciências exatas*.

**Periodicals:**

- ACM Transactions on Programming Languages and Systems;
- Numerical Algorithms;
- Random Structures & Algorithms.

Use the catalog links already present in the project for the digital works.
Do not retain any graph bibliography.

- [ ] **Step 3: Reescrever `recursos.html`**

Use `apply_patch`. Organize:

- Khan Academy — statistics and probability;
- Kaggle Learn — Pandas and Data Visualization;
- CODAP — browser data exploration;
- Seeing Theory — interactive probability and inference.

Copy the exact URLs from `mat/ensino/plataformas.md`. State that they are
complementary and do not replace official notebooks or constitute assessment
unless explicitly assigned.

- [ ] **Step 4: Reescrever `refs.html` e `saiba_mais.html`**

Use `apply_patch`.

`refs.html` must include:

- OpenIntro Statistics:
  `https://www.openintro.org/book/os/`;
- Palmer Penguins project and dataset reference:
  `https://allisonhorst.github.io/palmerpenguins/`;
- the discipline's public repository:
  `https://github.com/carubbi/MQ`;
- the official project:
  `https://github.com/carubbi/MQ/blob/main/mat/ensino/proj_ensino_2026.md`;
- the teaching flow:
  `https://github.com/carubbi/MQ/blob/main/mat/ensino/fluxo_ensino.md`.

`saiba_mais.html` must include optional, non-assessed routes:

- Seeing Theory for conceptual visualization:
  `https://seeing-theory.brown.edu/`;
- OpenIntro examples and laboratories:
  `https://www.openintro.org/book/os/`;
- CODAP for exploratory investigation:
  `https://codap.concord.org/`;
- Palmer Penguins scientific article identified in `mat/data/README.md`:
  `https://doi.org/10.1371/journal.pone.0090081`.

Do not repeat graph, network or Nature links from the legacy block.

- [ ] **Step 5: Validar links e segurança**

Run:

```bash
.venv/bin/python - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))

paths = [
    Path("prof/AVA/bibliografia.html"),
    Path("prof/AVA/recursos.html"),
    Path("prof/AVA/refs.html"),
    Path("prof/AVA/saiba_mais.html"),
]
all_links = []
for path in paths:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    for attrs in parser.links:
        href = attrs.get("href", "")
        assert urlparse(href).scheme == "https", (path, href)
        assert attrs.get("target") == "_blank", (path, href)
        assert attrs.get("rel") == "noopener noreferrer", (path, href)
        all_links.append(href)
text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
for forbidden in ("Sedgewick", "Wayne", "grafos", "VisuAlgo", "Graph Online"):
    assert forbidden.casefold() not in text.casefold(), forbidden
assert len(all_links) >= 12
print(f"links externos seguros: {len(all_links)}")
PY
```

Expected: all assertions pass and at least 12 HTTPS links are found.

- [ ] **Step 6: Commit**

```bash
git add -f \
  prof/AVA/bibliografia.html \
  prof/AVA/recursos.html \
  prof/AVA/refs.html \
  prof/AVA/saiba_mais.html
git commit -m "docs: atualizar referências do AVA de T199"
```

---

### Task 4: Publicar o mapa de materiais de apoio

**Files:**
- Modify: `prof/AVA/mat_apoio.html`

**Interfaces:**
- Consumes: the validated 16-material and 14-notebook inventory from the student schedule.
- Produces: a public GitHub link map grouped by unit and state.

- [ ] **Step 1: Confirmar que o bloco ainda aponta para RPG**

Run:

```bash
rg -n "github.com/carubbi/RPG|A1_|A2_|BFS|DFS|algs4|mat/exs|mat/trabalhos" \
  prof/AVA/mat_apoio.html
```

Expected: legacy links are found.

- [ ] **Step 2: Reescrever o cabeçalho e os recursos gerais**

Use `apply_patch`.

Use `https://github.com/carubbi/MQ` as base and include:

- repository home;
- `mat/apostila/apostila_mq.pdf`;
- `mat/apostila/banco_questoes_provas_2026_2.pdf`;
- `mat/data/`;
- `mat/ensino/cronograma_2026_2_t199_64_65.md`.

State that the AVA remains the channel for communication, assessments, grades
and submissions.

- [ ] **Step 3: Incluir os 16 materiais de aula**

Use `apply_patch`. Group by unit and link to these exact repository paths:

**Finalized:**

- `mat/aulas/u1_s01_fundamentos_estatisticos.md`.

**Under construction:**

- `mat/aulas/u1_s03_organizacao_representacao_dados.md`;
- `mat/aulas/u1_s04_analise_univariada.md`;
- `mat/aulas/u1_s05_analise_bivariada.md`;
- `mat/aulas/u1_s06_probabilidade.md`;
- `mat/aulas/u2_s01_revisao_at1.md`;
- `mat/aulas/u2_s02_variaveis_aleatorias.md`;
- `mat/aulas/u2_s03_distribuicoes_discretas.md`;
- `mat/aulas/u2_s04_distribuicoes_continuas.md`;
- `mat/aulas/u2_s05_normal_auditoria_modelos.md`;
- `mat/aulas/u2_s06_revisao_at2.md`;
- `mat/aulas/u3_s01_amostragem_distribuicoes_amostrais.md`;
- `mat/aulas/u3_s02_estimacao_testes.md`;
- `mat/aulas/u3_s03_regressao_linear_simples.md`;
- `mat/aulas/u3_s05_regressao_simples_multipla.md`;
- `mat/aulas/u3_s06_revisao_at3.md`.

- [ ] **Step 4: Incluir os 14 notebooks**

Use `apply_patch`. Group by unit and link to these exact repository paths:

**Finalized:**

- `mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb`;
- `mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb`.

**Under construction:**

- `mat/notebooks/u1_s03_organizacao_representacao_dados.ipynb`;
- `mat/notebooks/u1_s04_analise_univariada.ipynb`;
- `mat/notebooks/u1_s05_analise_bivariada.ipynb`;
- `mat/notebooks/u1_s06_probabilidade.ipynb`;
- `mat/notebooks/u2_s02_variaveis_aleatorias.ipynb`;
- `mat/notebooks/u2_s03_distribuicoes_discretas.ipynb`;
- `mat/notebooks/u2_s04_distribuicoes_continuas.ipynb`;
- `mat/notebooks/u2_s05_normal_auditoria_modelos.ipynb`;
- `mat/notebooks/u3_s01_amostragem_distribuicoes_amostrais.ipynb`;
- `mat/notebooks/u3_s02_estimacao_testes.ipynb`;
- `mat/notebooks/u3_s03_regressao_linear_simples.ipynb`;
- `mat/notebooks/u3_s05_regressao_simples_multipla.ipynb`.

- [ ] **Step 5: Validar o inventário e os destinos locais**

Run:

```bash
.venv/bin/python - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))

path = Path("prof/AVA/mat_apoio.html")
parser = LinkParser()
parser.feed(path.read_text(encoding="utf-8"))
hrefs = [item["href"] for item in parser.links]
materials = [item for item in hrefs if "/mat/aulas/" in item]
notebooks = [item for item in hrefs if "/mat/notebooks/" in item]
assert len(materials) == 16, len(materials)
assert len(notebooks) == 14, len(notebooks)
for href in materials + notebooks:
    parsed = urlparse(href)
    local = Path(unquote(parsed.path.split("/MQ/blob/main/", 1)[1]))
    assert local.exists(), local
text = path.read_text(encoding="utf-8")
assert text.count("finalizado") == 3
assert text.count("em construção") == 27
for attrs in parser.links:
    assert attrs.get("target") == "_blank", attrs
    assert attrs.get("rel") == "noopener noreferrer", attrs
print("materiais=16 notebooks=14 finalizados=3 em_construcao=27")
PY
```

Expected: all assertions pass.

- [ ] **Step 6: Commit**

```bash
git add -f prof/AVA/mat_apoio.html
git commit -m "docs: vincular materiais de T199 no AVA"
```

---

### Task 5: Revisar minicurrículo e reconstruir o mapa de publicação

**Files:**
- Modify: `prof/AVA/mini_cv.html` only if the structural review finds a defect
- Modify: `prof/AVA/README.md`

**Interfaces:**
- Consumes: final HTML inventory from Tasks 1–4.
- Produces: publication instructions matching the local T199 blocks.

- [ ] **Step 1: Validar `mini_cv.html`**

Run:

```bash
.venv/bin/python - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

path = Path("prof/AVA/mini_cv.html")
source = path.read_text(encoding="utf-8")
parser = HTMLParser()
parser.feed(source)
for item in (
    "Prof. Me. Ricardo Carubbi",
    "Currículo Lattes",
    "role=\"presentation\"",
    "Inserir fotografia do professor",
):
    assert item in source, item
for item in ("T290", "RPG", "grafos", "Java", "Accepted"):
    assert item.casefold() not in source.casefold(), item
print("minicurrículo compatível: nenhuma mudança pedagógica necessária")
PY
```

Expected: pass. If parsing or required content fails, use `apply_patch` only
to correct the specific structural defect, then repeat the command. The file
must be force-added even when its content remains unchanged because the whole
AVA directory is currently ignored.

- [ ] **Step 2: Reescrever `README.md`**

Use `apply_patch`. Document:

- purpose: local Moodle blocks for T199 in 2026.2;
- 14 common blocks;
- exactly one evaluation block: `aval_T199-64-65.html`;
- publication map for T199-64/65;
- source precedence;
- AT and AP rules;
- exact AP rubric `4 + 4 + 2`;
- exact first and second-call dates;
- material count and status;
- technical HTML standard;
- prepublication checklist;
- workflow: update local files, validate, then copy manually to Moodle.

Do not mention the two deleted T290 filenames as active alternatives.

- [ ] **Step 3: Validar inventário documentado**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path

root = Path("prof/AVA")
common = {
    "apres.html",
    "bibliografia.html",
    "contrato.html",
    "fraude.html",
    "mat_apoio.html",
    "metodo.html",
    "mini_cv.html",
    "motivacao.html",
    "plan_ensino.html",
    "pre-req.html",
    "recursos.html",
    "refs.html",
    "saiba_mais.html",
    "visao_geral.html",
}
html = {path.name for path in root.glob("*.html")}
assert html == common | {"aval_T199-64-65.html"}, sorted(html)
readme = (root / "README.md").read_text(encoding="utf-8")
for name in sorted(html):
    assert f"`{name}`" in readme, name
for item in ("T290", "RPG", "Resolução de Problemas com Grafos"):
    assert item not in readme, item
print("README e inventário final: OK")
PY
```

Expected: all assertions pass.

- [ ] **Step 4: Commit**

```bash
git add -f \
  prof/AVA/README.md \
  prof/AVA/mini_cv.html \
  prof/AVA/imgs/MQ_bkg.jpg
git commit -m "docs: documentar publicação do AVA de T199"
```

---

### Task 6: Executar a validação integral

**Files:**
- No new files expected.

**Interfaces:**
- Consumes: final `prof/AVA` inventory.
- Produces: verification evidence and final handoff.

- [ ] **Step 1: Validar estrutura HTML, links e termos proibidos**

Run:

```bash
.venv/bin/python - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

root = Path("prof/AVA")
paths = sorted(root.glob("*.html"))
assert len(paths) == 15, len(paths)
forbidden = (
    "T290",
    "RPG",
    "Resolução de Problemas com Grafos",
    "DFS",
    "BFS",
    "Python ou Java",
    "Accepted",
    "apresentação oral",
    "apresentação do trabalho",
    "apresentação dos trabalhos",
    "14/09",
    "15/09",
    "26/10",
    "27/10",
    "07/12",
    "08/12",
)
for path in paths:
    source = path.read_text(encoding="utf-8")
    parser = HTMLParser()
    parser.feed(source)
    assert "<html" not in source.casefold(), path
    assert "<head" not in source.casefold(), path
    assert "<body" not in source.casefold(), path
    assert "<script" not in source.casefold(), path
    if path.name != "mini_cv.html":
        assert "style=" not in source.casefold(), path
    for item in forbidden:
        assert item.casefold() not in source.casefold(), (path, item)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.items.append(dict(attrs))

count = 0
for path in paths:
    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    for attrs in parser.items:
        href = attrs.get("href", "")
        assert urlparse(href).scheme == "https", (path, href)
        assert attrs.get("target") == "_blank", (path, href)
        assert attrs.get("rel") == "noopener noreferrer", (path, href)
        count += 1
print(f"fragmentos={len(paths)} links_https={count}")
PY
```

Expected: all assertions pass.

- [ ] **Step 2: Validar fatos avaliativos**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path

text = "\n".join(
    path.read_text(encoding="utf-8")
    for path in (
        Path("prof/AVA/metodo.html"),
        Path("prof/AVA/contrato.html"),
        Path("prof/AVA/aval_T199-64-65.html"),
    )
)
required = (
    "10 pontos",
    "dez questões",
    "1 ponto",
    "8 questões",
    "2 questões",
    "4 pontos",
    "0,70",
    "0,30",
    "Safe Exam Browser",
    "15 minutos",
    "28/08",
    "04/09",
    "11/09",
    "18/09",
    "25/09",
    "02/10",
    "09/10",
    "16/10",
    "23/10",
    "13/11",
    "27/11",
    "04/12",
    "09/12",
    "N6CD",
    "N4AB",
)
for item in required:
    assert item in text, item
assert "não terão segunda chamada" in text
assert "notas isoladas" in text
print("fatos avaliativos: OK")
PY
```

Expected: all assertions pass.

- [ ] **Step 3: Revalidar fontes protegidas e worktree**

Run:

```bash
shasum -a 256 \
  prof/ensino/cronograma_2026_2_docente.md \
  mat/ensino/proj_ensino_2026.md \
  mat/ensino/cronograma_2026_2_t199_64_65.md \
  mat/ensino/plataformas.md \
  prof/AVA/imgs/MQ_bkg.jpg
git diff --check
git status --short
```

Expected:

- the four source hashes equal the Task 1 values;
- `MQ_bkg.jpg` equals its Task 1 hash;
- no uncommitted changes under `prof/AVA`;
- only the preexisting external changes remain:
  - two removed `.superpowers/sdd` reports;
  - modified `mat/ensino/fluxo_ensino.md`;
  - untracked `mat/notebooks/assets/imgs/barbetta_fig21.png`;
  - untracked `mat/notebooks/assets/imgs/barbetta_fig22.png`.

- [ ] **Step 4: Confirmar o escopo versionado**

Run:

```bash
git log --oneline --name-status -5 -- prof/AVA
git ls-files -- prof/AVA | sort
```

Expected: README, 15 HTML fragments and `imgs/MQ_bkg.jpg`; the final file list
contains no T290 evaluation file.

- [ ] **Step 5: Relatar**

Report:

- `prof/AVA` adapted for T199;
- 14 common blocks plus one T199-64/65 assessment block;
- old T290 files removed;
- AT 10-point and AP `4 + 4 + 2` rules;
- exact material counts and states;
- validations and protected hashes;
- compatible `mini_cv.html` preservation;
- preexisting worktree changes left untouched;
- Moodle was not configured and no push was performed.
