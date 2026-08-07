# Mockups de aulas e notebooks e cronogramas T199 — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar e validar os mockups semanais de T199, versionar os notebooks finalizados da Semana 1, vincular os recursos no cronograma docente e gerar o cronograma discente T199-64/65.

**Architecture:** Os metadados pedagógicos e o inventário estão fixados na especificação `docs/superpowers/specs/2026-08-07-mockups-aulas-notebooks-cronogramas-design.md`. Os recursos serão arquivos estáticos versionados; um validador dedicado distinguirá mockups de materiais completos e um construtor pequeno produzirá notebooks de uma célula a partir do cabeçalho canônico. O cronograma docente continuará como fonte canônica, e o cronograma discente será uma projeção transacional.

**Tech Stack:** Markdown, Jupyter Notebook JSON `nbformat` 4, Python 3.12, `unittest`, grafo JSON e Git.

## Global Constraints

- Trabalhar diretamente na branch `main`, conforme autorização já registrada.
- Preservar a alteração independente em `mat/ensino/fluxo_ensino.md`.
- Preservar integralmente o conteúdo dos dois notebooks finalizados da Semana 1; somente renomeá-los.
- Manter removido `mat/notebooks/u1_s01_fundamentos_estatisticos.md`.
- Criar 15 mockups Markdown e 12 notebooks-mockup.
- Não criar recursos para 14/08 ou 20/11.
- Não criar notebooks para revisão/AT ou segundas chamadas.
- Cada mockup Markdown terá somente título, sete campos de identificação e `---`.
- Cada notebook-mockup terá uma única célula Markdown igual a `mat/notebooks/assets/heads/head_unifor.md`.
- Não inserir `TODO`, `TBD`, seções vazias, código ou saídas nos mockups.
- Usar somente tópicos existentes em `prof/refs/mapas/grafo_referencias.json`.
- Marcar os mockups como **em construção** nos cronogramas.
- Marcar o material e os dois notebooks da Semana 1 como **finalizado**.
- Não alterar datas, conteúdos, avaliações, entregas ou ocorrências do cronograma docente.
- Não expor caminhos `prof/` no cronograma discente.
- Não incluir `mat/notebooks/assets/imgs/barbetta_fig21.png` ou `barbetta_fig22.png` em commits enquanto permanecerem sem referência nos notebooks.
- Não executar push.

---

### Task 1: Versionar e renomear os notebooks finalizados da Semana 1

**Files:**
- Rename: `mat/notebooks/aula1.ipynb` → `mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb`
- Rename: `mat/notebooks/aula2.ipynb` → `mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb`
- Add: `mat/notebooks/assets/heads/head_unifor.md`
- Add: `mat/notebooks/assets/imgs/01_table_dataframe.svg`
- Add: `mat/notebooks/assets/imgs/UNIFOR_logo.png`
- Add: `mat/notebooks/assets/imgs/culmen_depth.png`
- Add: `mat/notebooks/assets/imgs/lter_penguins.png`
- Delete: `mat/notebooks/u1_s01_fundamentos_estatisticos.md`

**Interfaces:**
- Consumes: notebooks e ativos adicionados pelo usuário.
- Produces: dois notebooks finalizados com nomes definitivos e todos os ativos efetivamente referenciados.

- [ ] **Step 1: Capturar o baseline dos notebooks e ativos**

Run:

```bash
shasum -a 256 \
  mat/notebooks/aula1.ipynb \
  mat/notebooks/aula2.ipynb \
  mat/notebooks/assets/heads/head_unifor.md \
  mat/notebooks/assets/imgs/01_table_dataframe.svg \
  mat/notebooks/assets/imgs/UNIFOR_logo.png \
  mat/notebooks/assets/imgs/culmen_depth.png \
  mat/notebooks/assets/imgs/lter_penguins.png
```

Expected notebook hashes:

```text
378e2c1a42de311009c9fdd8d7c950dbbc0d86d6b96f664f269e466027b0a2bf  mat/notebooks/aula1.ipynb
02f31dd64a000361650c6130b4ea691743058ab64a9a5e8bc4788a3fb811de81  mat/notebooks/aula2.ipynb
```

- [ ] **Step 2: Renomear sem modificar conteúdo**

Run:

```bash
mv mat/notebooks/aula1.ipynb mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb
mv mat/notebooks/aula2.ipynb mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb
```

- [ ] **Step 3: Verificar preservação e estrutura**

Run:

```bash
shasum -a 256 \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb
.venv/bin/python -m json.tool mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb >/dev/null
.venv/bin/python -m json.tool mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb >/dev/null
rg -o 'assets/[A-Za-z0-9_./-]+' \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb | sort -u
```

Expected: hashes unchanged; JSON válido; somente os quatro ativos listados em **Files** são referenciados.

- [ ] **Step 4: Confirmar que todos os links locais existem**

Run:

```bash
for notebook_path in \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb
do
  rg -o 'assets/[A-Za-z0-9_./-]+' "$notebook_path" | while IFS= read -r target
  do
    test -f "mat/notebooks/$target" || exit 1
  done
done
```

Expected: zero caminhos ausentes.

- [ ] **Step 5: Commit**

Stage only the two renamed notebooks, four referenced images, `head_unifor.md`, and deletion of the old route. Do not stage `fluxo_ensino.md` or the two unused Barbetta images.

```bash
git add -u mat/notebooks/u1_s01_fundamentos_estatisticos.md
git add \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb \
  mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb \
  mat/notebooks/assets/heads/head_unifor.md \
  mat/notebooks/assets/imgs/01_table_dataframe.svg \
  mat/notebooks/assets/imgs/UNIFOR_logo.png \
  mat/notebooks/assets/imgs/culmen_depth.png \
  mat/notebooks/assets/imgs/lter_penguins.png
git commit -m "feat: finalizar notebooks da semana 1"
```

---

### Task 2: Criar validador e construtor de mockups

**Files:**
- Create: `scripts/grafo_refs/teaching_mockups.py`
- Create: `tests/grafo_refs/test_teaching_mockups.py`

**Interfaces:**
- Produces: `validate_aula_mockup(path: Path, graph: dict) -> list[str]`
- Produces: `validate_notebook_mockup(path: Path, head_text: str) -> list[str]`
- Produces: `build_notebook_mockup(head_text: str) -> dict`
- CLI validation: `python scripts/grafo_refs/teaching_mockups.py --graph GRAPH --head HEAD --aula PATH... --notebook PATH...`
- CLI creation: `python scripts/grafo_refs/teaching_mockups.py --head HEAD --create-notebook PATH...`

- [ ] **Step 1: Escrever testes que falham**

Create tests covering:

```python
def test_accepts_exact_aula_mockup():
    findings = validate_aula_mockup(path, GRAPH)
    self.assertEqual([], findings)

def test_rejects_extra_section_in_aula_mockup():
    self.assertIn("conteúdo adicional no mockup", findings)

def test_rejects_unknown_topic_and_content():
    self.assertIn("conteúdo curricular desconhecido: 99.99", findings)
    self.assertIn("tópico desconhecido: Tópico inexistente", findings)

def test_builds_one_cell_notebook_from_head():
    notebook = build_notebook_mockup(HEAD_TEXT)
    self.assertEqual(1, len(notebook["cells"]))
    self.assertEqual("markdown", notebook["cells"][0]["cell_type"])
    self.assertEqual(HEAD_TEXT, "".join(notebook["cells"][0]["source"]))

def test_rejects_code_or_second_cell_in_notebook_mockup():
    self.assertIn("mockup deve conter uma única célula Markdown", findings)

def test_rejects_head_content_difference():
    self.assertIn("cabeçalho do notebook divergente", findings)

def test_cli_refuses_to_overwrite_existing_notebook():
    self.assertNotEqual(0, completed.returncode)
    self.assertIn("arquivo já existe", completed.stderr)
```

Fixtures must use real temporary files and the real graph; do not mock filesystem or JSON parsing.

- [ ] **Step 2: Executar os testes e confirmar RED**

Run:

```bash
.venv/bin/python -m unittest tests.grafo_refs.test_teaching_mockups -v
```

Expected: `ModuleNotFoundError` for `scripts.grafo_refs.teaching_mockups`.

- [ ] **Step 3: Implementar o mínimo necessário**

The Markdown validator must enforce this exact order:

```text
# título

- **Disciplina:**
- **Unidade:**
- **Semana:**
- **Data:**
- **Conteúdos formais:**
- **Tópicos:**
- **Resultado de aprendizagem:**

---
```

It must validate codes against nodes `conteudo_curricular` and split topics by `;` before validating exact names against nodes `topico`.

`build_notebook_mockup()` must return:

```python
{
    "cells": [
        {
            "cell_type": "markdown",
            "id": "head-unifor",
            "metadata": {},
            "source": head_text.splitlines(keepends=True),
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
```

For each `--create-notebook PATH`, the CLI must refuse an existing target,
serialize the builder result with UTF-8, `ensure_ascii=False`, and indentation
1, and terminate without partially creating later targets if any requested
path already exists.

- [ ] **Step 4: Executar testes unitários e regressão**

Run:

```bash
.venv/bin/python -m unittest \
  tests.grafo_refs.test_teaching_mockups \
  tests.grafo_refs.test_validate_teaching_resources -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/grafo_refs/teaching_mockups.py tests/grafo_refs/test_teaching_mockups.py
git commit -m "test: validar mockups de aulas e notebooks"
```

---

### Task 3: Criar mockups da Unidade I

**Files:**
- Create: `mat/aulas/u1_s03_organizacao_representacao_dados.md`
- Create: `mat/aulas/u1_s04_analise_univariada.md`
- Create: `mat/aulas/u1_s05_analise_bivariada.md`
- Create: `mat/aulas/u1_s06_probabilidade.md`
- Create: matching `.ipynb` files in `mat/notebooks/`

**Interfaces:**
- Consumes: exact metadata from specification section 6, Unit I.
- Produces: four weekly pairs marked later as **em construção**.

- [ ] **Step 1: Criar os quatro Markdown**

Use `apply_patch`. Copy title, date, content, topics and result verbatim from specification sections:

- `Unidade I / Semana 3`;
- `Unidade I / Semana 4`;
- `Unidade I / Semana 5`;
- `Unidade I / Semana 6`.

Every file must identify `T199 — Métodos Quantitativos`, use the local week number and end immediately after `---`.

- [ ] **Step 2: Criar os quatro notebooks**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --create-notebook mat/notebooks/u1_s03_organizacao_representacao_dados.ipynb \
  --create-notebook mat/notebooks/u1_s04_analise_univariada.ipynb \
  --create-notebook mat/notebooks/u1_s05_analise_bivariada.ipynb \
  --create-notebook mat/notebooks/u1_s06_probabilidade.ipynb
```

Expected: four new files; no existing path overwritten.

- [ ] **Step 3: Validar a unidade**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --graph prof/refs/mapas/grafo_referencias.json \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --aula mat/aulas/u1_s03_organizacao_representacao_dados.md \
  --aula mat/aulas/u1_s04_analise_univariada.md \
  --aula mat/aulas/u1_s05_analise_bivariada.md \
  --aula mat/aulas/u1_s06_probabilidade.md \
  --notebook mat/notebooks/u1_s03_organizacao_representacao_dados.ipynb \
  --notebook mat/notebooks/u1_s04_analise_univariada.ipynb \
  --notebook mat/notebooks/u1_s05_analise_bivariada.ipynb \
  --notebook mat/notebooks/u1_s06_probabilidade.ipynb
```

Expected: exit 0 and no findings.

- [ ] **Step 4: Commit**

```bash
git add \
  mat/aulas/u1_s03_organizacao_representacao_dados.md \
  mat/aulas/u1_s04_analise_univariada.md \
  mat/aulas/u1_s05_analise_bivariada.md \
  mat/aulas/u1_s06_probabilidade.md \
  mat/notebooks/u1_s03_organizacao_representacao_dados.ipynb \
  mat/notebooks/u1_s04_analise_univariada.ipynb \
  mat/notebooks/u1_s05_analise_bivariada.ipynb \
  mat/notebooks/u1_s06_probabilidade.ipynb
git commit -m "docs: criar mockups da unidade I"
```

---

### Task 4: Criar mockups da Unidade II

**Files:**
- Create: `mat/aulas/u2_s01_revisao_at1.md`
- Create: `mat/aulas/u2_s02_variaveis_aleatorias.md`
- Create: `mat/aulas/u2_s03_distribuicoes_discretas.md`
- Create: `mat/aulas/u2_s04_distribuicoes_continuas.md`
- Create: `mat/aulas/u2_s05_normal_auditoria_modelos.md`
- Create: `mat/aulas/u2_s06_revisao_at2.md`
- Create notebooks matching weeks 2–5 only.

**Interfaces:**
- Consumes: exact metadata from specification section 6, Unit II.
- Produces: six materials and four notebooks.

- [ ] **Step 1: Criar os seis Markdown**

Use `apply_patch` and the exact Unit II metadata in the specification. AT1 must use `01.01` to `01.04` plus `02.01`; AT2 must use `02.02` to `02.04`, mobilizing `02.01`.

- [ ] **Step 2: Criar notebooks somente para semanas 2–5**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --create-notebook mat/notebooks/u2_s02_variaveis_aleatorias.ipynb \
  --create-notebook mat/notebooks/u2_s03_distribuicoes_discretas.ipynb \
  --create-notebook mat/notebooks/u2_s04_distribuicoes_continuas.ipynb \
  --create-notebook mat/notebooks/u2_s05_normal_auditoria_modelos.ipynb
```

Assert that no notebook exists for `u2_s01_revisao_at1` or
`u2_s06_revisao_at2`.

- [ ] **Step 3: Validar a unidade**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --graph prof/refs/mapas/grafo_referencias.json \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --aula mat/aulas/u2_s01_revisao_at1.md \
  --aula mat/aulas/u2_s02_variaveis_aleatorias.md \
  --aula mat/aulas/u2_s03_distribuicoes_discretas.md \
  --aula mat/aulas/u2_s04_distribuicoes_continuas.md \
  --aula mat/aulas/u2_s05_normal_auditoria_modelos.md \
  --aula mat/aulas/u2_s06_revisao_at2.md \
  --notebook mat/notebooks/u2_s02_variaveis_aleatorias.ipynb \
  --notebook mat/notebooks/u2_s03_distribuicoes_discretas.ipynb \
  --notebook mat/notebooks/u2_s04_distribuicoes_continuas.ipynb \
  --notebook mat/notebooks/u2_s05_normal_auditoria_modelos.ipynb
```

Expected: exit 0 and no findings.

- [ ] **Step 4: Commit**

```bash
git add \
  mat/aulas/u2_s01_revisao_at1.md \
  mat/aulas/u2_s02_variaveis_aleatorias.md \
  mat/aulas/u2_s03_distribuicoes_discretas.md \
  mat/aulas/u2_s04_distribuicoes_continuas.md \
  mat/aulas/u2_s05_normal_auditoria_modelos.md \
  mat/aulas/u2_s06_revisao_at2.md \
  mat/notebooks/u2_s02_variaveis_aleatorias.ipynb \
  mat/notebooks/u2_s03_distribuicoes_discretas.ipynb \
  mat/notebooks/u2_s04_distribuicoes_continuas.ipynb \
  mat/notebooks/u2_s05_normal_auditoria_modelos.ipynb
git commit -m "docs: criar mockups da unidade II"
```

---

### Task 5: Criar mockups da Unidade III

**Files:**
- Create: `mat/aulas/u3_s01_amostragem_distribuicoes_amostrais.md`
- Create: `mat/aulas/u3_s02_estimacao_testes.md`
- Create: `mat/aulas/u3_s03_regressao_linear_simples.md`
- Create: `mat/aulas/u3_s05_regressao_simples_multipla.md`
- Create: `mat/aulas/u3_s06_revisao_at3.md`
- Create notebooks matching weeks 1, 2, 3 and 5 only.

**Interfaces:**
- Consumes: exact metadata from specification section 6, Unit III.
- Produces: five materials and four notebooks.

- [ ] **Step 1: Criar os cinco Markdown**

Use `apply_patch` and the exact Unit III metadata in the specification.
Do not create Week 4 files.

- [ ] **Step 2: Criar notebooks somente para semanas 1, 2, 3 and 5**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --create-notebook mat/notebooks/u3_s01_amostragem_distribuicoes_amostrais.ipynb \
  --create-notebook mat/notebooks/u3_s02_estimacao_testes.ipynb \
  --create-notebook mat/notebooks/u3_s03_regressao_linear_simples.ipynb \
  --create-notebook mat/notebooks/u3_s05_regressao_simples_multipla.ipynb
```

Assert that no notebook exists for `u3_s06_revisao_at3`.

- [ ] **Step 3: Validar a unidade**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --graph prof/refs/mapas/grafo_referencias.json \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --aula mat/aulas/u3_s01_amostragem_distribuicoes_amostrais.md \
  --aula mat/aulas/u3_s02_estimacao_testes.md \
  --aula mat/aulas/u3_s03_regressao_linear_simples.md \
  --aula mat/aulas/u3_s05_regressao_simples_multipla.md \
  --aula mat/aulas/u3_s06_revisao_at3.md \
  --notebook mat/notebooks/u3_s01_amostragem_distribuicoes_amostrais.ipynb \
  --notebook mat/notebooks/u3_s02_estimacao_testes.ipynb \
  --notebook mat/notebooks/u3_s03_regressao_linear_simples.ipynb \
  --notebook mat/notebooks/u3_s05_regressao_simples_multipla.ipynb
```

Expected: exit 0 and no findings.

- [ ] **Step 4: Commit**

```bash
git add \
  mat/aulas/u3_s01_amostragem_distribuicoes_amostrais.md \
  mat/aulas/u3_s02_estimacao_testes.md \
  mat/aulas/u3_s03_regressao_linear_simples.md \
  mat/aulas/u3_s05_regressao_simples_multipla.md \
  mat/aulas/u3_s06_revisao_at3.md \
  mat/notebooks/u3_s01_amostragem_distribuicoes_amostrais.ipynb \
  mat/notebooks/u3_s02_estimacao_testes.ipynb \
  mat/notebooks/u3_s03_regressao_linear_simples.ipynb \
  mat/notebooks/u3_s05_regressao_simples_multipla.ipynb
git commit -m "docs: criar mockups da unidade III"
```

---

### Task 6: Validar o inventário integral

**Files:**
- Modify: `tests/grafo_refs/test_teaching_mockups.py`

**Interfaces:**
- Consumes: all resources from Tasks 1, 3, 4 and 5.
- Produces: integration test guarding filenames, counts and forbidden resources.

- [ ] **Step 1: Escrever o teste integral**

Add a test with literal expected path sets:

- 16 material paths, including the completed Week 1 material;
- 14 notebook paths, including the two completed Week 1 notebooks;
- no paths for Unit I Week 2 or Unit III Week 4;
- no notebook paths for Unit II Weeks 1/6 or Unit III Week 6.

The test must validate all 15 Markdown mockups and 12 notebook mockups with the real graph and head.

- [ ] **Step 2: Executar e confirmar o resultado**

Run:

```bash
.venv/bin/python -m unittest tests.grafo_refs.test_teaching_mockups -v
```

Expected: all unit and integration tests pass.

- [ ] **Step 3: Commit**

```bash
git add tests/grafo_refs/test_teaching_mockups.py
git commit -m "test: validar inventário de recursos de T199"
```

---

### Task 7: Atualizar o cronograma docente canônico

**Files:**
- Modify: `prof/ensino/cronograma_2026_2_docente.md`

**Interfaces:**
- Consumes: all validated resource paths.
- Produces: canonical schedule with resource links and explicit state.

- [ ] **Step 1: Reconfirmar baseline and delta**

Run:

```bash
shasum -a 256 prof/ensino/cronograma_2026_2_docente.md
git diff -- prof/ensino/cronograma_2026_2_docente.md
```

Expected before edit: hash from specification and no preexisting diff. If either differs, stop and reconcile against the new baseline before editing.

- [ ] **Step 2: Add resource blocks at the end of each meeting week**

For Week 1 use:

```markdown
- **Recursos:**
  - **Material de aula — finalizado:** [Fundamentos estatísticos e investigação com dados](../../mat/aulas/u1_s01_fundamentos_estatisticos.md).
  - **Notebook guiado — finalizado:** [Aula 1 — ambientação computacional e manipulação básica de dados](../../mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb).
  - **Notebook guiado — finalizado:** [Aula 2 — amostragem, variabilidade e viés](../../mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb).
```

For development mockups use:

```markdown
- **Recursos:**
  - **Material de aula — em construção:** [Organização e representação de dados](../../mat/aulas/u1_s03_organizacao_representacao_dados.md).
  - **Notebook guiado — em construção:** [Organização e representação de dados](../../mat/notebooks/u1_s03_organizacao_representacao_dados.ipynb).
```

For the other weeks, use the exact title/path pairs from specification section
5. For review/AT use only the material line. Do not add resources to feriados
or extraordinary second-call sessions.

- [ ] **Step 3: Validate only the delta**

Check:

- 16 material links;
- 14 notebook links;
- 3 finalized links in Week 1;
- all other links marked **em construção**;
- no changes outside resource blocks;
- all relative targets exist.

- [ ] **Step 4: Commit**

```bash
git add -f prof/ensino/cronograma_2026_2_docente.md
git commit -m "docs: vincular recursos ao cronograma docente"
```

---

### Task 8: Gerar o cronograma discente T199-64/65

**Files:**
- Create: `mat/ensino/cronograma_2026_2_t199_64_65.md`

**Interfaces:**
- Consumes: final state of `prof/ensino/cronograma_2026_2_docente.md`.
- Produces: public projection for the single T199-64/65 group.

- [ ] **Step 1: Invoke the schedule projection workflow**

Read and apply `gerar-cronograma-discente` and its contract. Capture the final hash of the canonical schedule and record the target as absent baseline.

- [ ] **Step 2: Prepare the projection in a temporary directory**

The projection must contain:

1. identification and derivation statement;
2. T199-64/65 schedule and D18 room;
3. student-facing evaluation and submission guidance;
4. all three units and all 18 weeks;
5. content, activities, evidence, AP checkpoints, ATs and second calls;
6. resources with **finalizado** or **em construção**;
7. no private paths, planning criteria or internal validation notes.

Convert resource links:

- `../../mat/aulas/...` → `../aulas/...`;
- `../../mat/notebooks/...` → `../notebooks/...`.

- [ ] **Step 3: Validate the temporary projection**

Check:

- only T199-64/65 appears;
- dates, weekdays and institutional occurrences match the source;
- AT/AP composition, deadlines and second calls match the source;
- 16 material links and 14 notebook links resolve;
- no string `prof/` appears;
- no `TODO` or `TBD`;
- canonical schedule hash is unchanged.

- [ ] **Step 4: Install and commit**

Install only after every validation passes.

```bash
git add mat/ensino/cronograma_2026_2_t199_64_65.md
git commit -m "docs: gerar cronograma discente T199-64/65"
```

---

### Task 9: Verificação integral e relatório de sincronização

**Files:**
- No new files expected.

**Interfaces:**
- Consumes: final repository state.
- Produces: verification evidence and handoff report.

- [ ] **Step 1: Run all automated tests**

```bash
.venv/bin/python -m unittest \
  tests.grafo_refs.test_validate_teaching_resources \
  tests.grafo_refs.test_teaching_mockups -v
```

- [ ] **Step 2: Validate all resource links**

Run:

```bash
.venv/bin/python scripts/grafo_refs/teaching_mockups.py \
  --graph prof/refs/mapas/grafo_referencias.json \
  --head mat/notebooks/assets/heads/head_unifor.md \
  --aula mat/aulas/u1_s03_organizacao_representacao_dados.md \
  --aula mat/aulas/u1_s04_analise_univariada.md \
  --aula mat/aulas/u1_s05_analise_bivariada.md \
  --aula mat/aulas/u1_s06_probabilidade.md \
  --aula mat/aulas/u2_s01_revisao_at1.md \
  --aula mat/aulas/u2_s02_variaveis_aleatorias.md \
  --aula mat/aulas/u2_s03_distribuicoes_discretas.md \
  --aula mat/aulas/u2_s04_distribuicoes_continuas.md \
  --aula mat/aulas/u2_s05_normal_auditoria_modelos.md \
  --aula mat/aulas/u2_s06_revisao_at2.md \
  --aula mat/aulas/u3_s01_amostragem_distribuicoes_amostrais.md \
  --aula mat/aulas/u3_s02_estimacao_testes.md \
  --aula mat/aulas/u3_s03_regressao_linear_simples.md \
  --aula mat/aulas/u3_s05_regressao_simples_multipla.md \
  --aula mat/aulas/u3_s06_revisao_at3.md \
  --notebook mat/notebooks/u1_s03_organizacao_representacao_dados.ipynb \
  --notebook mat/notebooks/u1_s04_analise_univariada.ipynb \
  --notebook mat/notebooks/u1_s05_analise_bivariada.ipynb \
  --notebook mat/notebooks/u1_s06_probabilidade.ipynb \
  --notebook mat/notebooks/u2_s02_variaveis_aleatorias.ipynb \
  --notebook mat/notebooks/u2_s03_distribuicoes_discretas.ipynb \
  --notebook mat/notebooks/u2_s04_distribuicoes_continuas.ipynb \
  --notebook mat/notebooks/u2_s05_normal_auditoria_modelos.ipynb \
  --notebook mat/notebooks/u3_s01_amostragem_distribuicoes_amostrais.ipynb \
  --notebook mat/notebooks/u3_s02_estimacao_testes.ipynb \
  --notebook mat/notebooks/u3_s03_regressao_linear_simples.ipynb \
  --notebook mat/notebooks/u3_s05_regressao_simples_multipla.ipynb
```

Then validate all local links in both cronograms.

- [ ] **Step 3: Verify protected files and working tree**

Confirm:

- `mat/ensino/proj_ensino_2026.md` hash unchanged;
- `mat/ensino/calendario_2026_2.md` hash unchanged;
- `mat/ensino/turmas_2026_2.md` hash unchanged;
- `mat/ensino/fluxo_ensino.md` remains modified but unstaged and uncommitted;
- unused Barbetta notebook images remain untouched;
- `git diff --check` passes;
- no unexpected untracked files were created.

- [ ] **Step 4: Report according to both schedule contracts**

Report:

- canonical target and `editado: sim`;
- sources and baseline;
- delta restricted to resource blocks;
- discente target as `criado`;
- group T199-64/65;
- final resource counts and states;
- validations and test count;
- preserved user changes;
- any remaining untracked files;
- no push performed.
