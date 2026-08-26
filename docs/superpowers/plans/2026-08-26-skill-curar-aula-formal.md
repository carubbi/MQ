# Formal Lesson Curation Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar o contrato temporal `1.1`, migrar com segurança a curadoria da Aula 2 e criar a skill privada `curar-aula-formal` para orientar as próximas aulas.

**Architecture:** O repositório continuará sendo a autoridade determinística para schema, validação e renderização; a skill privada apenas orquestrará essas interfaces e apoiará decisões docentes. O YAML privado permanecerá canônico, o dossiê será uma visão derivada em listas e nenhuma decisão será promovida para `aprovado` sem confirmação explícita.

**Tech Stack:** Python 3, biblioteca padrão, PyYAML, jsonschema Draft 2020-12, unittest, Markdown, YAML e infraestrutura local de skills do Codex.

**Spec:** `docs/superpowers/specs/2026-08-26-skill-curar-aula-formal-design.md`

## Global Constraints

- Nenhum arquivo sob `.interno/` será rastreado ou incluído à força no Git.
- A skill será privada em `~/.codex/skills/curar-aula-formal/` e não será copiada para o repositório.
- O contrato será atualizado de `1.0` para `1.1`; formatos anteriores deverão falhar com mensagem de schema.
- `selecao.yaml` continuará sendo a fonte canônica e `dossie.md` continuará sendo integralmente derivado.
- O dossiê apresentará escopo, planejamento, ciclos, tópicos e referências com listas, nunca tabelas.
- `ciclos[].topicos` será preservado e conterá IDs de tópicos selecionados.
- Não haverá estado por ciclo nem quantidade fixa de ciclos.
- O tempo dos ciclos deverá satisfazer `soma(duracao_minima_minutos) <= duracao_minutos - abertura_minutos - fechamento_minutos`.
- A Aula 2 conservará todas as decisões bibliográficas existentes; sua migração estrutural não aprovará aplicações de notebook ainda não confirmadas.
- O manifesto da Aula 2 permanecerá `em_selecao` e com `ciclos: []` até a aprovação docente das aplicações.
- `Aplicação no notebook` não conterá código, pseudocódigo, bibliotecas, funções, comandos ou resultados inventados.
- Livros em português terão preferência quando a cobertura for suficiente; livros em inglês poderão fundamentar lacunas mediante tradução técnica e compatibilização; a apostila não substituirá automaticamente fundamentação teórica adequada.
- As remoções e modificações preexistentes no worktree não serão restauradas, alteradas, staged nem incluídas em commits.
- Durante a criação da skill, o executor deverá invocar e seguir `skill-creator` e `superpowers:writing-skills` antes de escrever em `~/.codex/skills`.

---

## File Structure

### Código público e rastreado

- `scripts/aulas/schema_selecao.json`: define o contrato `1.1`, o orçamento temporal e os metadados exigidos por ciclo.
- `scripts/aulas/manifesto.py`: valida orçamento, cobertura e unicidade da partição de tópicos nos ciclos.
- `scripts/aulas/dossie.py`: renderiza planejamento temporal e ciclos como listas legíveis.
- `tests/aulas/fixtures.py`: fornece manifestos `em_selecao` e `aprovado` no contrato `1.1`.
- `tests/aulas/test_manifesto.py`: cobre schema, estados, partição conceitual e viabilidade temporal.
- `tests/aulas/test_dossie.py`: cobre a apresentação do orçamento e dos ciclos sem tabelas.
- `tests/aulas/test_cli.py`: confirma que a CLI aceita `1.1` e preserva o YAML ao renderizar.

### Artefatos privados e não rastreados

- `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`: recebe somente a migração estrutural para `1.1` e `planejamento_tempo`.
- `.interno/prof/aulas/2026-2/u1_a02/dossie.md`: é regenerado a partir do manifesto migrado.
- `~/.codex/skills/curar-aula-formal/SKILL.md`: contém gatilhos, fases, pontos de parada, comandos e invariantes.
- `~/.codex/skills/curar-aula-formal/references/criterios-estados.md`: define critérios de estados de tópicos, referências e manifesto.
- `~/.codex/skills/curar-aula-formal/references/politica-referencias.md`: define precedência bibliográfica, tradução e compatibilização.
- `~/.codex/skills/curar-aula-formal/references/ciclos-e-tempo.md`: define partição conceitual, calibração e teste temporal.

---

### Task 1: Upgrade the Manifest Schema to Contract 1.1

**Files:**
- Modify: `scripts/aulas/schema_selecao.json`
- Modify: `tests/aulas/fixtures.py`
- Modify: `tests/aulas/test_manifesto.py`

**Interfaces:**
- Consumes: manifesto Python `dict` com `versao_contrato: "1.1"`.
- Produces: `$defs.planejamentoTempo` e campos temporais obrigatórios em `$defs.ciclo`.

- [ ] **Step 1: Add a valid approved-manifest fixture for contract 1.1**

Em `tests/aulas/fixtures.py`, importar `copy`, mudar `VALID_MANIFEST["versao_contrato"]` para `"1.1"` e inserir após `escopo`:

```python
"planejamento_tempo": {
    "abertura_minutos": 5,
    "fechamento_minutos": 10,
},
```

Acrescentar ao fim do arquivo:

```python
def approved_manifest() -> dict:
    manifest = copy.deepcopy(VALID_MANIFEST)
    manifest["estado"] = "aprovado"
    topic = manifest["topicos"][0]
    topic["estado"] = "selecionado"
    reference = topic["referencias"][0]
    reference["estado"] = "selecionada"
    reference["papeis"] = ["fundamentacao"]
    manifest["ciclos"] = [
        {
            "id": "ciclo-01",
            "titulo": "População e amostra",
            "topicos": ["topico-populacao"],
            "complexidade": "moderada",
            "duracao_minima_minutos": 20,
            "justificativa_particao": (
                "O ciclo reúne a definição do universo de interesse e sua redução amostral."
            ),
            "aplicacao_notebook": {
                "objetivo": "Identificar população e amostra no conjunto estudado.",
                "pergunta": "Qual população sustenta a conclusão pretendida?",
                "contraste": "Comparar o grupo observado ao alvo da conclusão.",
                "evidencia": "Identificação justificada da população e da amostra.",
                "ciclo_notebook": "ciclo-01",
                "caminho": "notebooks/u1_a02_fundamentos_investigacao_dados.ipynb",
            },
        }
    ]
    return manifest
```

- [ ] **Step 2: Write failing schema tests**

Importar `approved_manifest` em `tests/aulas/test_manifesto.py` e acrescentar:

```python
def test_accepts_approved_contract_1_1_manifest(self):
    self.assertEqual(
        [],
        validate_manifest(approved_manifest(), GRAPH, require_approved=True),
    )

def test_rejects_contract_1_0(self):
    manifest = copy.deepcopy(VALID_MANIFEST)
    manifest["versao_contrato"] = "1.0"

    findings = validate_manifest(manifest, GRAPH)

    self.assertTrue(
        any("'1.1' was expected" in finding for finding in findings),
        findings,
    )

def test_rejects_missing_time_plan(self):
    manifest = copy.deepcopy(VALID_MANIFEST)
    del manifest["planejamento_tempo"]

    findings = validate_manifest(manifest, GRAPH)

    self.assertTrue(
        any("'planejamento_tempo' is a required property" in finding for finding in findings),
        findings,
    )

def test_rejects_cycle_without_complexity_and_minimum_duration(self):
    manifest = approved_manifest()
    del manifest["ciclos"][0]["complexidade"]
    del manifest["ciclos"][0]["duracao_minima_minutos"]
    del manifest["ciclos"][0]["justificativa_particao"]

    findings = validate_manifest(manifest, GRAPH)

    self.assertTrue(any("'complexidade' is a required property" in item for item in findings))
    self.assertTrue(
        any("'duracao_minima_minutos' is a required property" in item for item in findings)
    )
    self.assertTrue(
        any("'justificativa_particao' is a required property" in item for item in findings)
    )
```

- [ ] **Step 3: Run the schema tests and verify the red state**

Run:

```bash
.venv/bin/python -m unittest \
  tests.aulas.test_manifesto.ManifestValidationTests.test_accepts_approved_contract_1_1_manifest \
  tests.aulas.test_manifesto.ManifestValidationTests.test_rejects_contract_1_0 \
  tests.aulas.test_manifesto.ManifestValidationTests.test_rejects_missing_time_plan \
  tests.aulas.test_manifesto.ManifestValidationTests.test_rejects_cycle_without_complexity_and_minimum_duration -v
```

Expected: FAIL porque o schema ainda exige `1.0` e rejeita os novos campos.

- [ ] **Step 4: Implement the 1.1 schema**

Em `scripts/aulas/schema_selecao.json`:

1. mudar `versao_contrato.const` para `"1.1"`;
2. acrescentar `"planejamento_tempo"` à lista `required` do objeto raiz;
3. acrescentar `"planejamento_tempo": {"$ref": "#/$defs/planejamentoTempo"}` às propriedades;
4. acrescentar este `$def`:

```json
"planejamentoTempo": {
  "type": "object",
  "additionalProperties": false,
  "required": ["abertura_minutos", "fechamento_minutos"],
  "properties": {
    "abertura_minutos": {"type": "integer", "minimum": 0},
    "fechamento_minutos": {"type": "integer", "minimum": 0}
  }
}
```

No `$defs.ciclo`, acrescentar à lista `required`:

```json
"complexidade",
"duracao_minima_minutos",
"justificativa_particao"
```

E acrescentar às propriedades:

```json
"complexidade": {"enum": ["baixa", "moderada", "alta"]},
"duracao_minima_minutos": {"type": "integer", "minimum": 1},
"justificativa_particao": {"$ref": "#/$defs/texto"}
```

- [ ] **Step 5: Run the complete manifest test module**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto -v
```

Expected: PASS para todos os testes do módulo.

- [ ] **Step 6: Commit the contract upgrade**

```bash
git add scripts/aulas/schema_selecao.json tests/aulas/fixtures.py tests/aulas/test_manifesto.py
git commit -m "feat: add temporal planning to lesson manifests"
```

---

### Task 2: Validate Conceptual Partition and Time Feasibility

**Files:**
- Modify: `scripts/aulas/manifesto.py`
- Modify: `tests/aulas/test_manifesto.py`

**Interfaces:**
- Consumes: `manifest["planejamento_tempo"]`, `manifest["ciclos"]` e IDs de `manifest["topicos"]`.
- Produces: `_cycle_findings(manifest: dict) -> list[str]`, chamado por `_semantic_findings`.

- [ ] **Step 1: Write failing semantic tests**

Acrescentar a `ManifestValidationTests`:

```python
def test_rejects_time_reserve_that_consumes_the_lesson(self):
    manifest = approved_manifest()
    manifest["planejamento_tempo"] = {
        "abertura_minutos": 60,
        "fechamento_minutos": 40,
    }

    self.assertIn(
        "planejamento temporal não deixa minutos disponíveis para ciclos",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_cycle_minimum_duration_over_available_time(self):
    manifest = approved_manifest()
    manifest["ciclos"][0]["duracao_minima_minutos"] = 86

    self.assertIn(
        "duração mínima dos ciclos (86 min) excede o tempo disponível (85 min)",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_unknown_topic_inside_cycle(self):
    manifest = approved_manifest()
    manifest["ciclos"][0]["topicos"] = ["topico-inexistente"]

    self.assertIn(
        "ciclo ciclo-01 contém tópico desconhecido: topico-inexistente",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_rejected_topic_inside_cycle(self):
    manifest = approved_manifest()
    manifest["topicos"][0]["estado"] = "rejeitado"

    self.assertIn(
        "ciclo ciclo-01 contém tópico não selecionado: topico-populacao",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_selected_topic_missing_from_cycles(self):
    manifest = approved_manifest()
    manifest["ciclos"] = []

    self.assertIn(
        "tópico selecionado ausente dos ciclos: topico-populacao",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_selected_topic_repeated_across_cycles(self):
    manifest = approved_manifest()
    duplicate = copy.deepcopy(manifest["ciclos"][0])
    duplicate["id"] = "ciclo-02"
    duplicate["aplicacao_notebook"]["ciclo_notebook"] = "ciclo-02"
    manifest["ciclos"].append(duplicate)

    self.assertIn(
        "tópico selecionado aparece em mais de um ciclo: topico-populacao",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_mismatched_notebook_cycle_id(self):
    manifest = approved_manifest()
    manifest["ciclos"][0]["aplicacao_notebook"]["ciclo_notebook"] = "ciclo-02"

    self.assertIn(
        "aplicação do ciclo ciclo-01 aponta para ciclo-02",
        validate_manifest(manifest, GRAPH),
    )
```

- [ ] **Step 2: Run the semantic tests and verify the red state**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto.ManifestValidationTests -v
```

Expected: FAIL nos sete testes novos porque o validador ainda não examina a partição nem o orçamento.

- [ ] **Step 3: Implement `_cycle_findings`**

Em `scripts/aulas/manifesto.py`, importar `Counter` junto de `defaultdict`:

```python
from collections import Counter, defaultdict
```

Adicionar antes de `_semantic_findings`:

```python
def _cycle_findings(manifest: dict) -> list[str]:
    findings: list[str] = []
    lesson_duration = manifest.get("aula", {}).get("duracao_minutos")
    timing = manifest.get("planejamento_tempo", {})
    opening = timing.get("abertura_minutos")
    closing = timing.get("fechamento_minutos")
    cycles = manifest.get("ciclos", [])

    if not all(isinstance(value, int) for value in (lesson_duration, opening, closing)):
        return findings

    available = lesson_duration - opening - closing
    if available <= 0:
        findings.append(
            "planejamento temporal não deixa minutos disponíveis para ciclos"
        )

    durations = [
        cycle.get("duracao_minima_minutos")
        for cycle in cycles
        if isinstance(cycle, dict)
    ]
    if all(isinstance(value, int) for value in durations):
        required = sum(durations)
        if available > 0 and required > available:
            findings.append(
                f"duração mínima dos ciclos ({required} min) excede "
                f"o tempo disponível ({available} min)"
            )

    topic_states = {
        topic.get("id"): topic.get("estado")
        for topic in manifest.get("topicos", [])
        if isinstance(topic, dict) and isinstance(topic.get("id"), str)
    }
    cycle_topics: list[str] = []
    for cycle in cycles:
        if not isinstance(cycle, dict):
            continue
        cycle_id = cycle.get("id")
        for topic_id in cycle.get("topicos", []):
            cycle_topics.append(topic_id)
            if topic_id not in topic_states:
                findings.append(
                    f"ciclo {cycle_id} contém tópico desconhecido: {topic_id}"
                )
            elif topic_states[topic_id] != "selecionado":
                findings.append(
                    f"ciclo {cycle_id} contém tópico não selecionado: {topic_id}"
                )
        notebook_cycle = cycle.get("aplicacao_notebook", {}).get("ciclo_notebook")
        if isinstance(cycle_id, str) and isinstance(notebook_cycle, str):
            if notebook_cycle != cycle_id:
                findings.append(
                    f"aplicação do ciclo {cycle_id} aponta para {notebook_cycle}"
                )

    counts = Counter(cycle_topics)
    for topic_id, count in counts.items():
        if count > 1:
            findings.append(
                f"tópico selecionado aparece em mais de um ciclo: {topic_id}"
            )
    if manifest.get("estado") == "aprovado":
        for topic_id, state in topic_states.items():
            if state == "selecionado" and counts[topic_id] == 0:
                findings.append(
                    f"tópico selecionado ausente dos ciclos: {topic_id}"
                )
    return findings
```

No final de `_semantic_findings`, antes do `return`, acrescentar:

```python
findings.extend(_cycle_findings(manifest))
```

- [ ] **Step 4: Verify that incomplete selection remains valid**

O teste existente `test_accepts_complete_manifest_in_selection` deve continuar passando porque a cobertura completa dos tópicos nos ciclos somente é exigida no estado `aprovado`. Acrescentar também:

```python
def test_allows_selected_topic_without_cycle_during_selection(self):
    manifest = copy.deepcopy(VALID_MANIFEST)
    manifest["topicos"][0]["estado"] = "selecionado"
    reference = manifest["topicos"][0]["referencias"][0]
    reference["estado"] = "selecionada"
    reference["papeis"] = ["fundamentacao"]

    self.assertEqual([], validate_manifest(manifest, GRAPH))
```

O teste de tópico rejeitado e o teste de tópico desconhecido continuam válidos sempre que um ciclo existir, mesmo em `em_selecao`.

- [ ] **Step 5: Run all lesson-manifest tests**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto -v
```

Expected: PASS para todos os testes do módulo, incluindo o manifesto `em_selecao` sem ciclos.

- [ ] **Step 6: Commit semantic validation**

```bash
git add scripts/aulas/manifesto.py tests/aulas/test_manifesto.py
git commit -m "feat: validate lesson cycle partition and timing"
```

---

### Task 3: Render Time Planning and Cycles as Readable Lists

**Files:**
- Modify: `scripts/aulas/dossie.py`
- Modify: `tests/aulas/test_dossie.py`
- Modify: `tests/aulas/test_cli.py`

**Interfaces:**
- Consumes: manifesto `1.1`, inclusive com `ciclos: []`.
- Produces: `render_dossier(manifest: dict) -> str` com seções `Planejamento temporal` e `Ciclos conceituais`.

- [ ] **Step 1: Write failing dossier tests**

Importar `approved_manifest` em `tests/aulas/test_dossie.py` e acrescentar:

```python
def test_renders_time_plan_as_list(self):
    rendered = render_dossier(VALID_MANIFEST)

    self.assertIn("## Planejamento temporal", rendered)
    self.assertIn("- **Abertura:** 5 minutos", rendered)
    self.assertIn("- **Fechamento:** 10 minutos", rendered)
    self.assertIn("- **Disponível para ciclos:** 85 minutos", rendered)

def test_renders_empty_cycle_selection_explicitly(self):
    rendered = render_dossier(VALID_MANIFEST)

    self.assertIn("## Ciclos conceituais", rendered)
    self.assertIn("Ciclos ainda não definidos.", rendered)

def test_renders_approved_cycles_as_nested_lists(self):
    rendered = render_dossier(approved_manifest())

    self.assertIn("### ciclo-01 — População e amostra", rendered)
    self.assertIn("- **Tópicos:** `topico-populacao`", rendered)
    self.assertIn("- **Complexidade:** moderada", rendered)
    self.assertIn("- **Duração mínima:** 20 minutos", rendered)
    self.assertIn("- **Aplicação no notebook:**", rendered)
    self.assertIn("  - **Pergunta:** Qual população sustenta", rendered)
    self.assertNotIn("| Ciclo |", rendered)
```

- [ ] **Step 2: Run dossier tests and verify the red state**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_dossie -v
```

Expected: FAIL porque as duas seções ainda não são renderizadas.

- [ ] **Step 3: Implement list renderers**

Adicionar em `scripts/aulas/dossie.py`:

```python
def _render_time_plan(manifest: dict) -> list[str]:
    lesson_minutes = manifest["aula"]["duracao_minutos"]
    timing = manifest["planejamento_tempo"]
    opening = timing["abertura_minutos"]
    closing = timing["fechamento_minutos"]
    available = lesson_minutes - opening - closing
    return [
        "## Planejamento temporal",
        "",
        f"- **Duração da aula:** {lesson_minutes} minutos",
        f"- **Abertura:** {opening} minutos",
        f"- **Fechamento:** {closing} minutos",
        f"- **Disponível para ciclos:** {available} minutos",
    ]


def _render_cycles(cycles: list[dict]) -> list[str]:
    lines = ["## Ciclos conceituais", ""]
    if not cycles:
        return [*lines, "Ciclos ainda não definidos."]
    for cycle in cycles:
        application = cycle["aplicacao_notebook"]
        topics = ", ".join(f"`{topic_id}`" for topic_id in cycle["topicos"])
        lines.extend(
            [
                f"### {cycle['id']} — {cycle['titulo']}",
                "",
                f"- **Tópicos:** {topics}",
                f"- **Complexidade:** {cycle['complexidade']}",
                (
                    "- **Duração mínima:** "
                    f"{cycle['duracao_minima_minutos']} minutos"
                ),
                (
                    "- **Justificativa da partição:** "
                    f"{cycle['justificativa_particao']}"
                ),
                "- **Aplicação no notebook:**",
                f"  - **Objetivo:** {application['objetivo']}",
                f"  - **Pergunta:** {application['pergunta']}",
                f"  - **Contraste:** {application['contraste']}",
                f"  - **Evidência:** {application['evidencia']}",
                f"  - **Ciclo:** `{application['ciclo_notebook']}`",
                f"  - **Caminho:** `{application['caminho']}`",
                "",
            ]
        )
    return lines
```

Em `render_dossier`, inserir `_render_time_plan(manifest)` depois do escopo e `_render_cycles(manifest["ciclos"])` antes de `## Tópicos candidatos`.

- [ ] **Step 4: Confirm CLI preservation under contract 1.1**

Em `tests/aulas/test_cli.py`, manter o teste de bytes do manifesto e acrescentar ao teste de renderização:

```python
self.assertIn(
    "## Planejamento temporal",
    self.dossier_path.read_text(encoding="utf-8"),
)
```

- [ ] **Step 5: Run renderer and CLI tests**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_dossie tests.aulas.test_cli -v
```

Expected: PASS para todos os testes dos dois módulos.

- [ ] **Step 6: Commit dossier rendering**

```bash
git add scripts/aulas/dossie.py tests/aulas/test_dossie.py tests/aulas/test_cli.py
git commit -m "feat: render lesson cycle planning as lists"
```

---

### Task 4: Migrate the Private Aula 2 Manifest Without Approving New Decisions

**Files:**
- Modify, private and ignored: `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`
- Regenerate, private and ignored: `.interno/prof/aulas/2026-2/u1_a02/dossie.md`

**Interfaces:**
- Consumes: CLI `python -m scripts.aulas.cli validar|renderizar` e grafo `.interno/prof/refs/mapas/grafo_referencias.json`.
- Produces: manifesto Aula 2 válido em `1.1`, ainda `em_selecao`, e dossiê derivado.

- [ ] **Step 1: Preserve a private comparison copy before migration**

Run:

```bash
cp \
  .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  /private/tmp/u1_a02-selecao-before-1.1.yaml
shasum -a 256 .interno/prof/aulas/2026-2/u1_a02/selecao.yaml
```

Expected: a cópia privada existe e uma linha de checksum registra o manifesto anterior.

- [ ] **Step 2: Apply only the approved structural migration**

Em `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`, mudar:

```yaml
versao_contrato: "1.0"
```

para:

```yaml
versao_contrato: "1.1"
```

E inserir entre `escopo` e `ciclos`:

```yaml
planejamento_tempo:
  abertura_minutos: 5
  fechamento_minutos: 10
```

Manter `estado: em_selecao`, `ciclos: []` e todos os tópicos, referências, páginas, papéis e compatibilizações sem alteração.

- [ ] **Step 3: Validate the migrated manifest**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli validar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json
```

Expected: exit code 0 e nenhuma mensagem em stderr.

- [ ] **Step 4: Regenerate the private dossier**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli renderizar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --saida .interno/prof/aulas/2026-2/u1_a02/dossie.md
```

Expected: exit code 0; o dossiê contém `## Planejamento temporal`, `85 minutos` e `Ciclos ainda não definidos.`.

- [ ] **Step 5: Verify privacy and decision preservation**

Run:

```bash
diff -u \
  /private/tmp/u1_a02-selecao-before-1.1.yaml \
  .interno/prof/aulas/2026-2/u1_a02/selecao.yaml
git check-ignore \
  .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  .interno/prof/aulas/2026-2/u1_a02/dossie.md
git status --short
```

Expected: o diff contém somente a mudança de versão e a inserção de `planejamento_tempo`; os dois caminhos aparecem como ignorados; nenhum caminho sob `.interno/` aparece no status; as remoções e modificações preexistentes permanecem inalteradas.

O comando `diff -u` retorna código 1 quando mostra as duas mudanças esperadas;
nesse passo, isso representa diferença encontrada, não falha da migração.

Não criar commit para esta tarefa, pois os dois arquivos são privados.

---

### Task 5: Create the Private `curar-aula-formal` Skill

**Files:**
- Create, private: `~/.codex/skills/curar-aula-formal/SKILL.md`
- Create, private: `~/.codex/skills/curar-aula-formal/references/criterios-estados.md`
- Create, private: `~/.codex/skills/curar-aula-formal/references/politica-referencias.md`
- Create, private: `~/.codex/skills/curar-aula-formal/references/ciclos-e-tempo.md`

**Interfaces:**
- Consumes: semestre, ID da aula, cronograma docente, planejamentos, grafo, fontes originais, convenção matemática e CLI `scripts.aulas.cli`.
- Produces: dossiê e manifesto privados; recomendações explicadas; pontos de parada antes de decisões e aprovação.

- [ ] **Step 1: Load the mandatory skill-authoring instructions**

Antes de criar qualquer arquivo, invocar e ler integralmente:

```text
skill-creator
superpowers:writing-skills
```

Aplicar o fluxo de testes e validação definido por essas skills. Em caso de divergência operacional, as instruções atuais dessas skills prevalecem, mas os requisitos funcionais desta especificação não podem ser removidos.

- [ ] **Step 2: Record baseline failures for three skill scenarios**

Executar, sem a nova skill, estes três prompts em modo somente descritivo, sem permitir escrita, e salvar as respostas apenas em diretório temporário:

```text
1. Avaliação sem escrita: descreva como curaria u1_a03 para 2026-2 e onde pararia antes das decisões docentes.
2. Avaliação sem escrita: recomende ciclos para uma aula de 100 minutos com seis blocos de alta complexidade.
3. Avaliação sem escrita: selecione a fundamentação quando houver uma menção breve em português e um livro em inglês com definição completa.
```

Expected baseline gaps:

- o primeiro prompt não garante o ponto de parada antes da seleção;
- o segundo tende a contar ciclos sem demonstrar a desigualdade temporal;
- o terceiro pode priorizar idioma em vez da suficiência da cobertura.

- [ ] **Step 3: Initialize the private skill package**

Solicitar a autorização de escrita fora do workspace para o alvo exato `~/.codex/skills/curar-aula-formal`. Usar o inicializador indicado por `skill-creator`, com nome `curar-aula-formal` e somente o diretório `references/`; não criar `scripts/`, `assets/` nem cópias de dados do projeto.

Expected: diretório contendo `SKILL.md` e `references/`, sem arquivos de exemplo não utilizados.

- [ ] **Step 4: Write `SKILL.md` with the exact operational contract**

O frontmatter deverá ser:

```yaml
---
name: curar-aula-formal
description: Use para preparar, revisar ou concluir a curadoria privada de uma aula estatística formal a partir do cronograma docente, grafo de referências e fontes originais, incluindo dossiê, estados, referências, compatibilização, ciclos conceituais e viabilidade temporal antes da geração da aula pública.
---
```

O corpo deverá conter, nesta ordem:

1. propósito e limites;
2. autoridades e precedência;
3. descoberta obrigatória dos caminhos do repositório;
4. fase de preparação com parada para decisão docente;
5. fase de recomendação e registro apenas após confirmação;
6. comandos `validar` e `renderizar` da CLI;
7. condição de aprovação geral;
8. regras de privacidade e de preservação do worktree;
9. roteamento explícito para os três arquivos de `references/`;
10. handoff para `gerar-aula-formal`, sem tentar gerar a aula.

Incluir literalmente estes invariantes:

```text
- Nunca derive conteúdo teórico apenas dos metadados do grafo; leia as páginas originais.
- Nunca marque o manifesto como aprovado sem confirmação docente explícita.
- Nunca edite dossie.md manualmente; regenere-o a partir de selecao.yaml.
- Nunca rastreie, force-add ou publique arquivos sob .interno/.
- Nunca imponha três, quatro ou qualquer outra quantidade fixa de ciclos.
- Nunca inclua código ou instruções computacionais em Aplicação no notebook.
```

- [ ] **Step 5: Write the state criteria reference**

`references/criterios-estados.md` deverá definir:

```text
Tópico selecionado: necessário ao resultado de aprendizagem e compatível com escopo, profundidade e tempo.
Tópico adiado: pertinente, mas melhor situado em aula ou unidade posterior.
Tópico rejeitado: irrelevante, redundante ou inadequado ao encontro.
Tópico pendente: falta decisão ou evidência verificável; estado transitório.

Referência selecionada: cobertura verificada e papel explícito.
Referência rejeitada: cobertura indireta, insuficiente, redundante, avançada demais ou incompatível.
Referência pendente: falta leitura, classificação ou decisão.

Manifesto em_selecao: admite pendências ou ciclos ausentes.
Manifesto aprovado: não admite pendências; exige fundamentação, partição temporal viável, aplicações completas, validação determinística e confirmação docente.
```

Explicar que ciclos não recebem estado próprio.

- [ ] **Step 6: Write the reference-selection policy**

`references/politica-referencias.md` deverá ordenar a decisão assim:

1. avaliar suficiência e pertinência da cobertura pelas páginas originais;
2. preferir livro em português entre coberturas suficientes;
3. usar apostila como orientação de conteúdo quando livros não cobrirem adequadamente, sem promovê-la automaticamente a fundamentação;
4. usar livro em inglês como fundamentação quando não houver livro em português suficiente;
5. traduzir tecnicamente e registrar terminologia, notação, fonte, edição e páginas;
6. aceitar múltiplas referências compatíveis e atribuir papéis explícitos;
7. rejeitar menções meramente indiretas como fundamentação.

Incluir dois exemplos contrastantes: `unidade de análise`, fundamentada por Morden quando as fontes em português forem insuficientes, e `população`, fundamentada por Barbetta/Pinheiro e complementada por Navidi.

- [ ] **Step 7: Write the cycle and time policy**

`references/ciclos-e-tempo.md` deverá conter:

```text
Um ciclo é um bloco conceitual coerente, não um tópico isolado nem uma referência.
Criar novo ciclo quando mudar objeto, resultado parcial, notação/pressupostos, exemplo estruturante, interpretação ou evidência no notebook.
Unir tópicos quando compartilharem pergunta, formalização, exemplo, interpretação e evidência.
```

Incluir a desigualdade:

```math
\sum_{j=1}^{k} t_j^{\min}
\leq
T_{\text{aula}}-T_{\text{abertura}}-T_{\text{fechamento}}.
```

Registrar as calibrações `baixa: 12–15`, `moderada: 18–25` e `alta: 25–35` minutos como aproximações, não como regra fixa. Incluir a Aula 2 como exemplo de 20 + 15 + 25 + 25 = 85 minutos e afirmar que ela não constitui molde global.

- [ ] **Step 8: Validate the skill package**

Executar o validador indicado por `skill-creator`. Se a instalação atual mantiver a interface existente, usar:

```bash
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/carubbi/.codex/skills/curar-aula-formal
```

Expected: validação bem-sucedida, frontmatter aceito e referências locais resolvíveis.

Não criar commit: a skill é privada e externa ao repositório.

---

### Task 6: Evaluate the Skill and Verify the Complete Workflow

**Files:**
- Read: `docs/superpowers/specs/2026-08-26-skill-curar-aula-formal-design.md`
- Read: `~/.codex/skills/curar-aula-formal/SKILL.md`
- Read: `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`
- Temporary only: diretório criado com `mktemp -d` para cópias de avaliação.

**Interfaces:**
- Consumes: skill instalada e contrato `1.1` implementado.
- Produces: evidência de que a skill orienta decisões sem alterar fontes canônicas indevidamente.

- [ ] **Step 1: Run the complete tracked lesson test suite**

Run:

```bash
.venv/bin/python -m unittest discover -s tests/aulas -v
```

Expected: todos os testes de `tests/aulas` passam, sem falhas nem erros.

- [ ] **Step 2: Revalidate and rerender Aula 2**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli validar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json
.venv/bin/python -m scripts.aulas.cli renderizar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --saida .interno/prof/aulas/2026-2/u1_a02/dossie.md
```

Expected: ambos os comandos retornam exit code 0.

- [ ] **Step 3: Re-run the three skill scenarios**

Executar novamente os prompts da Task 5, agora invocando `curar-aula-formal`. Avaliar as respostas pelos seguintes critérios observáveis:

```text
Scenario 1: identifica cronograma, grafo e páginas originais; cria artefatos em .interno; para antes de selecionar.
Scenario 2: propõe partição conceitual, estima t_j^min, demonstra a desigualdade e recomenda adiamento quando exceder o orçamento.
Scenario 3: decide pela suficiência da cobertura; não aceita menção breve como fundamentação; exige tradução e compatibilização da fonte inglesa.
```

Expected: todos os critérios são atendidos. Se algum falhar, ajustar apenas as instruções privadas responsáveis pelo comportamento e repetir o cenário afetado e o validador da skill.

- [ ] **Step 4: Exercise Aula 2 without mutating its approved decisions**

Criar a cópia de avaliação:

```bash
mkdir -p /private/tmp/curar-aula-formal-u1-a02
cp \
  .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  /private/tmp/curar-aula-formal-u1-a02/selecao.yaml
shasum -a 256 .interno/prof/aulas/2026-2/u1_a02/selecao.yaml
```

Solicitar à skill uma recomendação de ciclos e aplicações usando exclusivamente a cópia. A resposta deverá:

- propor quatro ciclos com durações 20, 15, 25 e 25 minutos;
- manter todos os oito tópicos selecionados;
- produzir exatamente uma aplicação sem código por ciclo;
- manter o estado geral `em_selecao` até confirmação docente;
- não modificar o manifesto canônico da Aula 2.

Executar novamente:

```bash
shasum -a 256 .interno/prof/aulas/2026-2/u1_a02/selecao.yaml
```

Expected: checksum idêntico ao registrado antes da avaliação.

- [ ] **Step 5: Verify repository privacy and commit isolation**

Run:

```bash
git diff --check -- scripts/aulas tests/aulas
git diff --cached --name-status
git status --short
```

Expected: nenhum arquivo `.interno/` ou `~/.codex/skills/` aparece; o índice está vazio; apenas alterações preexistentes do usuário podem permanecer no worktree.

- [ ] **Step 6: Report the handoff state**

Informar ao docente:

```text
- contrato 1.1 implementado e testes executados;
- manifesto e dossiê privados da Aula 2 migrados, ainda em_selecao;
- skill privada instalada e validada;
- aplicações e aprovação final da Aula 2 continuam dependendo de confirmação docente;
- gerar-aula-formal permanece fora do escopo.
```

Não marcar o manifesto como `aprovado` e não gerar `aulas/u1_a02.md` nesta implementação.
