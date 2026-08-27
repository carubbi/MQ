# Recursos discentes no manifesto 1.2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar `recursos_discentes` uma entrada canônica, validável e renderizável do manifesto de curadoria 1.2 antes da criação da skill `gerar-aula-formal`.

**Architecture:** O manifesto armazenará somente IDs ordenados do grafo em duas listas fonte-neutras: materiais didáticos e exercícios indicados. Um módulo compartilhado concentrará travessia, ancestralidade e páginas do grafo; o validador verificará tipo, cobertura curricular e relação com tópicos, enquanto o dossiê apresentará a seleção de modo legível. A Aula 2 será migrada privadamente e a skill `curar-aula-formal` passará a exigir essa decisão antes da aprovação.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, PyYAML, `jsonschema`, `unittest`, Markdown e YAML.

**Spec:** `docs/superpowers/specs/2026-08-26-curadoria-aulas-formais-design.md`

## Global Constraints

- O contrato resultante terá `versao_contrato: "1.2"`; manifestos `1.1` serão rejeitados.
- `recursos_discentes` será obrigatório em manifesto aprovado e conterá `materiais_didaticos` e `exercicios_indicados`.
- Livros, apostilas e bancos de questões serão avaliados pela adequação do item, nunca pelo tipo da fonte.
- Materiais aceitarão nós `capitulo`, `secao` ou `exemplo`; exercícios aceitarão somente `exercicio` ou `questao`.
- Cada recurso deverá corresponder a um conteúdo formal e abordar ao menos um tópico selecionado, diretamente ou, para materiais, por cadeia `contem`.
- Títulos, números e páginas serão resolvidos pelo grafo; o manifesto armazenará apenas IDs e ordem.
- Listas vazias serão válidas e causarão omissão da subseção correspondente, sem criação de conteúdo artificial.
- Nenhum arquivo sob `.interno/` será rastreado ou incluído em commit.
- Esta implementação não gerará `aulas/<aula-id>.md`; ela apenas estabilizará a entrada da futura skill.

## Requisito deliberadamente adiado

A correspondência automática entre `recursos_discentes` e a seção pública
`Estudo e exercícios` será implementada e testada no plano de
`gerar-aula-formal`. Neste incremento, a correspondência da Aula 2 será apenas
auditada contra o exemplar público já revisado; não haverá gerador parcial ou
segunda fonte de escrita para `aulas/u1_a02.md`.

---

### Task 1: Atualizar o contrato estrutural para 1.2

**Files:**
- Modify: `scripts/aulas/schema_selecao.json`
- Modify: `tests/aulas/fixtures.py`
- Modify: `tests/aulas/test_manifesto.py`

**Interfaces:**
- Consumes: manifesto YAML carregado como `dict`.
- Produces: objeto opcional `recursos_discentes` em `em_selecao` e obrigatório em `aprovado`, com entradas no formato `{"id": str}`.

- [ ] **Step 1: Acrescentar recursos representativos ao grafo de teste**

Em `tests/aulas/fixtures.py`, acrescente um capítulo e uma questão ao `GRAPH`:

```python
{
    "id": "capitulo-fundamentos",
    "tipo": "capitulo",
    "numero_impresso": "1",
    "titulo": "Fundamentos",
    "pagina_pdf_inicio": 10,
    "pagina_pdf_fim": 13,
},
{
    "id": "questao-populacao",
    "tipo": "questao",
    "numero_impresso": "1",
    "pagina_pdf": 13,
    "pertinencia_t199": "direta",
},
```

Substitua a aresta direta `fonte-a -> secao-populacao` pelas relações abaixo e acrescente as relações curriculares da questão:

```python
{"origem": "fonte-a", "tipo": "contem", "destino": "capitulo-fundamentos"},
{"origem": "capitulo-fundamentos", "tipo": "contem", "destino": "secao-populacao"},
{"origem": "capitulo-fundamentos", "tipo": "contem", "destino": "questao-populacao"},
{"origem": "questao-populacao", "tipo": "corresponde_a", "destino": "conteudo-01-01"},
{"origem": "questao-populacao", "tipo": "aborda", "destino": "topico-populacao"},
```

- [ ] **Step 2: Migrar a fixture do manifesto para 1.2**

Altere `VALID_MANIFEST["versao_contrato"]` para `"1.2"` e inclua:

```python
"recursos_discentes": {
    "materiais_didaticos": [{"id": "capitulo-fundamentos"}],
    "exercicios_indicados": [{"id": "questao-populacao"}],
},
```

- [ ] **Step 3: Escrever testes estruturais que falham**

Em `tests/aulas/test_manifesto.py`, substitua os testes de versão por:

```python
def test_accepts_approved_contract_1_2_manifest(self):
    self.assertEqual(
        [],
        validate_manifest(approved_manifest(), GRAPH, require_approved=True),
    )

def test_rejects_contract_1_1(self):
    manifest = copy.deepcopy(VALID_MANIFEST)
    manifest["versao_contrato"] = "1.1"

    findings = validate_manifest(manifest, GRAPH)

    self.assertTrue(
        any("'1.2' was expected" in finding for finding in findings),
        findings,
    )

def test_approved_manifest_requires_student_resources(self):
    manifest = approved_manifest()
    del manifest["recursos_discentes"]

    findings = validate_manifest(manifest, GRAPH, require_approved=True)

    self.assertTrue(
        any("'recursos_discentes' is a required property" in finding for finding in findings),
        findings,
    )

def test_selection_manifest_may_omit_student_resources(self):
    manifest = copy.deepcopy(VALID_MANIFEST)
    del manifest["recursos_discentes"]

    self.assertEqual([], validate_manifest(manifest, GRAPH))
```

- [ ] **Step 4: Executar os testes e confirmar a falha estrutural**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto.ManifestValidationTests -v
```

Expected: FAIL nos testes que esperam contrato `1.2` e `recursos_discentes` obrigatório em manifesto aprovado.

- [ ] **Step 5: Implementar o schema 1.2**

Em `scripts/aulas/schema_selecao.json`, altere a constante da versão e adicione a propriedade:

```json
"versao_contrato": {"const": "1.2"},
"recursos_discentes": {"$ref": "#/$defs/recursosDiscentes"}
```

No ramo `then` do estado `aprovado`, acrescente `"required": ["recursos_discentes"]` sem remover `ciclos.minItems`. Em `$defs`, acrescente:

```json
"recursoDiscente": {
  "type": "object",
  "additionalProperties": false,
  "required": ["id"],
  "properties": {
    "id": {"$ref": "#/$defs/texto"}
  }
},
"recursosDiscentes": {
  "type": "object",
  "additionalProperties": false,
  "required": ["materiais_didaticos", "exercicios_indicados"],
  "properties": {
    "materiais_didaticos": {
      "type": "array",
      "items": {"$ref": "#/$defs/recursoDiscente"},
      "uniqueItems": true
    },
    "exercicios_indicados": {
      "type": "array",
      "items": {"$ref": "#/$defs/recursoDiscente"},
      "uniqueItems": true
    }
  }
}
```

- [ ] **Step 6: Executar os testes estruturais**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto.ManifestValidationTests -v
```

Expected: PASS para a versão e a obrigatoriedade estrutural; testes semânticos de recursos serão acrescentados na próxima tarefa.

- [ ] **Step 7: Commit**

```bash
git add scripts/aulas/schema_selecao.json tests/aulas/fixtures.py tests/aulas/test_manifesto.py
git commit -m "feat: adicionar recursos discentes ao manifesto 1.2"
```

### Task 2: Validar recursos discentes contra o grafo

**Files:**
- Create: `scripts/aulas/grafo.py`
- Modify: `scripts/aulas/manifesto.py`
- Create: `tests/aulas/test_grafo.py`
- Modify: `tests/aulas/test_manifesto.py`

**Interfaces:**
- Produces: `graph_indexes(graph)`, `source_ancestors(node_id, nodes, contains)`, `node_and_descendant_ids(node_id, contains)` e `page_interval(node)` em `scripts.aulas.grafo`.
- Consumes: `recursos_discentes` do manifesto 1.2 e índices do grafo.
- Produces: achados semânticos acionáveis por `validate_manifest(...) -> list[str]`.

- [ ] **Step 1: Escrever testes do módulo de grafo**

Crie `tests/aulas/test_grafo.py`:

```python
import unittest

from scripts.aulas.grafo import (
    graph_indexes,
    node_and_descendant_ids,
    page_interval,
    source_ancestors,
)
from tests.aulas.fixtures import GRAPH


class GraphHelpersTests(unittest.TestCase):
    def test_traverses_containment_in_both_directions_needed_by_curation(self):
        nodes, relations = graph_indexes(GRAPH)

        self.assertEqual(
            {"capitulo-fundamentos", "secao-populacao", "questao-populacao"},
            node_and_descendant_ids("capitulo-fundamentos", relations["contem"]),
        )
        self.assertEqual(
            {"fonte-a"},
            source_ancestors("secao-populacao", nodes, relations["contem"]),
        )

    def test_reads_single_page_and_interval_nodes(self):
        nodes, _ = graph_indexes(GRAPH)

        self.assertEqual((10, 12), page_interval(nodes["secao-populacao"]))
        self.assertEqual((13, 13), page_interval(nodes["questao-populacao"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Executar os testes e confirmar a ausência do módulo**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_grafo -v
```

Expected: ERROR com `ModuleNotFoundError: No module named 'scripts.aulas.grafo'`.

- [ ] **Step 3: Extrair os auxiliares compartilhados do grafo**

Crie `scripts/aulas/grafo.py` com assinaturas e comportamento determinísticos:

```python
"""Índices e travessias compartilhados do grafo de referências."""

from __future__ import annotations

from collections import defaultdict


def graph_indexes(graph: dict) -> tuple[dict[str, dict], dict[str, set[tuple[str, str]]]]:
    nodes = {
        node["id"]: node
        for node in graph.get("nos", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    relations: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for edge in graph.get("relacoes", []):
        if not isinstance(edge, dict):
            continue
        values = (edge.get("tipo"), edge.get("origem"), edge.get("destino"))
        if all(isinstance(value, str) for value in values):
            relation_type, origin, destination = values
            relations[relation_type].add((origin, destination))
    return nodes, relations


def source_ancestors(
    node_id: str,
    nodes: dict[str, dict],
    contains: set[tuple[str, str]],
) -> set[str]:
    parents: dict[str, set[str]] = defaultdict(set)
    for parent, child in contains:
        parents[child].add(parent)
    found: set[str] = set()
    pending = list(parents.get(node_id, set()))
    visited: set[str] = set()
    while pending:
        ancestor_id = pending.pop()
        if ancestor_id in visited:
            continue
        visited.add(ancestor_id)
        if nodes.get(ancestor_id, {}).get("tipo") == "fonte":
            found.add(ancestor_id)
        pending.extend(parents.get(ancestor_id, set()))
    return found


def node_and_descendant_ids(
    node_id: str,
    contains: set[tuple[str, str]],
) -> set[str]:
    children: dict[str, set[str]] = defaultdict(set)
    for parent, child in contains:
        children[parent].add(child)
    found = {node_id}
    pending = list(children.get(node_id, set()))
    while pending:
        descendant_id = pending.pop()
        if descendant_id in found:
            continue
        found.add(descendant_id)
        pending.extend(children.get(descendant_id, set()))
    return found


def page_interval(node: dict) -> tuple[int | None, int | None]:
    if isinstance(node.get("pagina_pdf"), int):
        return node["pagina_pdf"], node["pagina_pdf"]
    return node.get("pagina_pdf_inicio"), node.get("pagina_pdf_fim")
```

Remova as implementações equivalentes de `scripts/aulas/manifesto.py` e importe os quatro auxiliares necessários.

- [ ] **Step 4: Executar os testes do grafo**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_grafo -v
```

Expected: PASS.

- [ ] **Step 5: Escrever testes semânticos dos recursos**

Acrescente a `ManifestValidationTests`:

```python
def test_accepts_empty_student_resource_lists(self):
    manifest = approved_manifest()
    manifest["recursos_discentes"] = {
        "materiais_didaticos": [],
        "exercicios_indicados": [],
    }

    self.assertEqual([], validate_manifest(manifest, GRAPH, require_approved=True))

def test_rejects_unknown_student_resource(self):
    manifest = approved_manifest()
    manifest["recursos_discentes"]["materiais_didaticos"] = [{"id": "ausente"}]

    self.assertIn(
        "recurso discente desconhecido: ausente",
        validate_manifest(manifest, GRAPH),
    )

def test_rejects_resource_type_in_wrong_list(self):
    manifest = approved_manifest()
    manifest["recursos_discentes"]["materiais_didaticos"] = [
        {"id": "questao-populacao"}
    ]

    self.assertIn(
        "recurso questao-populacao do tipo questao é inválido em materiais_didaticos",
        validate_manifest(manifest, GRAPH),
    )

def test_accepts_chapter_related_through_contained_section(self):
    self.assertEqual([], validate_manifest(approved_manifest(), GRAPH))

def test_rejects_resource_without_pages(self):
    graph = copy.deepcopy(GRAPH)
    chapter = next(node for node in graph["nos"] if node["id"] == "capitulo-fundamentos")
    del chapter["pagina_pdf_inicio"]
    del chapter["pagina_pdf_fim"]

    self.assertIn(
        "recurso capitulo-fundamentos não possui páginas verificáveis",
        validate_manifest(approved_manifest(), graph),
    )

def test_rejects_resource_without_source_ancestor(self):
    graph = copy.deepcopy(GRAPH)
    graph["relacoes"] = [
        edge
        for edge in graph["relacoes"]
        if not (
            edge["origem"] == "fonte-a"
            and edge["tipo"] == "contem"
            and edge["destino"] == "capitulo-fundamentos"
        )
    ]

    self.assertIn(
        "recurso capitulo-fundamentos não pertence a uma fonte",
        validate_manifest(approved_manifest(), graph),
    )

def test_rejects_resource_unrelated_to_selected_topics(self):
    graph = copy.deepcopy(GRAPH)
    graph["relacoes"] = [
        edge
        for edge in graph["relacoes"]
        if not (edge["origem"] == "questao-populacao" and edge["tipo"] == "aborda")
    ]

    self.assertIn(
        "recurso questao-populacao não aborda tópico selecionado da aula",
        validate_manifest(approved_manifest(), graph),
    )
```

- [ ] **Step 6: Executar os testes e confirmar as falhas semânticas**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto.ManifestValidationTests -v
```

Expected: FAIL nos novos testes porque `_semantic_findings` ainda ignora `recursos_discentes`.

- [ ] **Step 7: Implementar `_student_resource_findings`**

Em `scripts/aulas/manifesto.py`, defina:

```python
STUDENT_RESOURCE_TYPES = {
    "materiais_didaticos": {"capitulo", "secao", "exemplo"},
    "exercicios_indicados": {"exercicio", "questao"},
}


def _student_resource_findings(
    manifest: dict,
    nodes: dict[str, dict],
    relations: dict[str, set[tuple[str, str]]],
    formal_ids: set[str],
) -> list[str]:
    findings: list[str] = []
    selected_topic_ids = {
        topic.get("id")
        for topic in manifest.get("topicos", [])
        if isinstance(topic, dict) and topic.get("estado") == "selecionado"
    }
    resources = manifest.get("recursos_discentes", {})
    if not isinstance(resources, dict):
        return findings

    for list_name, accepted_types in STUDENT_RESOURCE_TYPES.items():
        for entry in resources.get(list_name, []):
            if not isinstance(entry, dict):
                continue
            resource_id = entry.get("id")
            node = nodes.get(resource_id)
            if node is None:
                findings.append(f"recurso discente desconhecido: {resource_id}")
                continue
            node_type = node.get("tipo")
            if node_type not in accepted_types:
                findings.append(
                    f"recurso {resource_id} do tipo {node_type} é inválido em {list_name}"
                )
                continue
            candidates = (
                node_and_descendant_ids(resource_id, relations["contem"])
                if list_name == "materiais_didaticos"
                else {resource_id}
            )
            start, end = page_interval(node)
            if not all(isinstance(value, int) for value in (start, end)):
                findings.append(f"recurso {resource_id} não possui páginas verificáveis")
            if not source_ancestors(resource_id, nodes, relations["contem"]):
                findings.append(f"recurso {resource_id} não pertence a uma fonte")
            if formal_ids and not any(
                (candidate_id, content_id) in relations["corresponde_a"]
                for candidate_id in candidates
                for content_id in formal_ids
            ):
                findings.append(f"recurso {resource_id} não corresponde aos conteúdos da aula")
            if selected_topic_ids and not any(
                (candidate_id, topic_id) in relations["aborda"]
                for candidate_id in candidates
                for topic_id in selected_topic_ids
            ):
                findings.append(
                    f"recurso {resource_id} não aborda tópico selecionado da aula"
                )
    return findings
```

Chame a função em `_semantic_findings` depois da validação dos tópicos e antes de `_cycle_findings`:

```python
findings.extend(
    _student_resource_findings(manifest, nodes, relations, formal_ids)
)
```

- [ ] **Step 8: Executar os testes semânticos e a suíte de manifesto**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_grafo tests.aulas.test_manifesto -v
```

Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add scripts/aulas/grafo.py scripts/aulas/manifesto.py tests/aulas/test_grafo.py tests/aulas/test_manifesto.py
git commit -m "feat: validar recursos discentes pelo grafo"
```

### Task 3: Renderizar recursos no dossiê

**Files:**
- Modify: `scripts/aulas/dossie.py`
- Modify: `scripts/aulas/cli.py`
- Modify: `tests/aulas/test_dossie.py`
- Modify: `tests/aulas/test_cli.py`

**Interfaces:**
- Consumes: `render_dossier(manifest: dict, graph: dict) -> str`.
- Produces: seção `## Recursos discentes` em listas legíveis, preservando a ordem do manifesto e sem tabelas.

- [ ] **Step 1: Escrever testes de renderização que falham**

Atualize todas as chamadas existentes para `render_dossier(manifest, GRAPH)` e acrescente:

```python
def test_renders_student_resources_as_ordered_readable_lists(self):
    rendered = render_dossier(approved_manifest(), GRAPH)

    self.assertIn("## Recursos discentes", rendered)
    self.assertIn("### Materiais didáticos", rendered)
    self.assertIn("1. **`capitulo-fundamentos`**", rendered)
    self.assertIn("- **Fonte:** `fonte-a`", rendered)
    self.assertIn("- **Páginas PDF:** 10–13", rendered)
    self.assertIn("### Exercícios indicados", rendered)
    self.assertIn("1. **`questao-populacao`**", rendered)
    self.assertNotIn("| Recurso |", rendered)

def test_omits_empty_student_resource_subsection(self):
    manifest = approved_manifest()
    manifest["recursos_discentes"]["exercicios_indicados"] = []

    rendered = render_dossier(manifest, GRAPH)

    self.assertIn("### Materiais didáticos", rendered)
    self.assertNotIn("### Exercícios indicados", rendered)
```

- [ ] **Step 2: Atualizar o teste da CLI para exigir recursos**

Em `tests/aulas/test_cli.py::test_render_command_writes_only_dossier`, acrescente:

```python
self.assertIn(
    "## Recursos discentes",
    self.dossier_path.read_text(encoding="utf-8"),
)
```

- [ ] **Step 3: Executar os testes e confirmar a quebra de interface**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_dossie tests.aulas.test_cli -v
```

Expected: FAIL porque `render_dossier` ainda recebe apenas o manifesto e não renderiza os recursos.

- [ ] **Step 4: Implementar a renderização fonte-neutra**

Em `scripts/aulas/dossie.py`, importe `graph_indexes`, `page_interval` e `source_ancestors`. Adicione auxiliares com estas assinaturas:

```python
def _page_label(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}–{end}"


def _render_resource_list(
    title: str,
    entries: list[dict],
    nodes: dict[str, dict],
    contains: set[tuple[str, str]],
) -> list[str]:
    if not entries:
        return []
    lines = [f"### {title}", ""]
    for index, entry in enumerate(entries, start=1):
        resource_id = entry["id"]
        node = nodes[resource_id]
        start, end = page_interval(node)
        source_ids = sorted(source_ancestors(resource_id, nodes, contains))
        number = node.get("numero_impresso")
        label = node.get("titulo") or (f"Item {number}" if number else resource_id)
        lines.extend(
            [
                f"{index}. **`{resource_id}`** — {label}",
                f"   - **Fonte:** `{source_ids[0]}`",
                f"   - **Tipo:** {node['tipo']}",
                f"   - **Páginas PDF:** {_page_label(start, end)}",
                "",
            ]
        )
    return lines


def _render_student_resources(manifest: dict, graph: dict) -> list[str]:
    resources = manifest.get("recursos_discentes", {})
    materials = resources.get("materiais_didaticos", [])
    exercises = resources.get("exercicios_indicados", [])
    if not materials and not exercises:
        return []
    nodes, relations = graph_indexes(graph)
    lines = ["## Recursos discentes", ""]
    lines.extend(
        _render_resource_list("Materiais didáticos", materials, nodes, relations["contem"])
    )
    lines.extend(
        _render_resource_list("Exercícios indicados", exercises, nodes, relations["contem"])
    )
    return lines
```

Altere a assinatura pública para:

```python
def render_dossier(manifest: dict, graph: dict) -> str:
```

Insira `_render_student_resources(manifest, graph)` depois dos ciclos e antes dos tópicos candidatos. Em `scripts/aulas/cli.py`, passe `graph` na chamada:

```python
render_dossier(manifest, graph)
```

- [ ] **Step 5: Executar testes de dossiê e CLI**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_dossie tests.aulas.test_cli -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/aulas/dossie.py scripts/aulas/cli.py tests/aulas/test_dossie.py tests/aulas/test_cli.py
git commit -m "feat: renderizar recursos discentes no dossie"
```

### Task 4: Migrar privadamente a Aula 2

**Files:**
- Modify, untracked: `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`
- Regenerate, untracked: `.interno/prof/aulas/2026-2/u1_a02/dossie.md`
- Verify only: `aulas/u1_a02.md`

**Interfaces:**
- Consumes: contrato 1.2 e IDs existentes em `.interno/prof/refs/mapas/grafo_referencias.json`.
- Produces: manifesto privado aprovado e dossiê derivado, sem alteração automática da aula pública.

- [ ] **Step 1: Migrar a versão e registrar materiais didáticos na ordem pública**

Altere `versao_contrato` para `"1.2"` e acrescente ao manifesto:

```yaml
recursos_discentes:
  materiais_didaticos:
    - id: barbetta-2010-sec-1-1
    - id: barbetta-2010-sec-1-2
    - id: barbetta-2010-sec-1-6
    - id: barbetta-2010-sec-2-2
    - id: morettin-bussab-2010-sec-1-1
    - id: morettin-bussab-2010-sec-1-2
    - id: pinheiro-2009-sec-1-1
    - id: pinheiro-2009-sec-1-2
    - id: morden-2024-sec-3-7
    - id: navidi-2024-sec-1-1
    - id: montgomery-2018-sec-1-1-1
    - id: montgomery-2018-sec-1-1-2
    - id: montgomery-2018-sec-1-2-2
    - id: apostila-mq-sec-1-1
    - id: apostila-mq-sec-1-2
    - id: apostila-mq-sec-1-3
  exercicios_indicados:
    - id: barbetta-2010-exercicio-2-7
    - id: banco-questoes-2026-2-questao-1
    - id: banco-questoes-2026-2-questao-2
    - id: banco-questoes-2026-2-questao-4
    - id: banco-questoes-2026-2-questao-5
    - id: banco-questoes-2026-2-questao-6
```

Não inclua a questão 3 do banco: tamanho amostral, estimação e margem de erro permanecem reservados à Unidade III.

- [ ] **Step 2: Validar o manifesto aprovado real**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli validar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --exigir-aprovado
```

Expected: exit code 0 e nenhuma saída em stderr.

- [ ] **Step 3: Regenerar o dossiê exclusivamente pelo CLI**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli renderizar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --saida .interno/prof/aulas/2026-2/u1_a02/dossie.md
```

Expected: exit code 0; o dossiê contém `## Recursos discentes`, as duas subseções e os IDs aprovados.

- [ ] **Step 4: Verificar que a migração privada não alterou a aula pública**

Run:

```bash
git diff -- aulas/u1_a02.md
```

Expected: nenhuma alteração produzida por esta tarefa. Alterações públicas anteriores do usuário podem continuar no worktree, mas não serão modificadas pela migração.

- [ ] **Step 5: Confirmar que nada privado está rastreado**

Run:

```bash
git ls-files .interno/prof/aulas/2026-2/u1_a02
```

Expected: nenhuma saída. Não criar commit para esta tarefa.

### Task 5: Atualizar a documentação e a skill de curadoria

**Files:**
- Modify: `docs/superpowers/specs/2026-08-26-skill-curar-aula-formal-design.md`
- Modify outside repo: `/Users/carubbi/.codex/skills/curar-aula-formal/SKILL.md`
- Create outside repo: `/Users/carubbi/.codex/skills/curar-aula-formal/references/recursos-discentes.md`

**Interfaces:**
- Consumes: manifesto 1.2 validado e páginas originais.
- Produces: curadoria que trata recursos discentes como decisão independente da fundamentação e impede aprovação sem `recursos_discentes`.

- [ ] **Step 1: Atualizar o desenho da skill**

Acrescente ao desenho público uma subseção `Recursos discentes` que determine:

```text
- livros, apostilas e bancos de questões são elegíveis conforme a adequação do item;
- materiais didáticos e exercícios indicados são decisões distintas dos papéis teóricos;
- o grafo localiza candidatos, mas capítulos, seções, exemplos, exercícios e questões devem ser lidos antes da seleção;
- um manifesto aprovado exige recursos_discentes validado, ainda que uma das listas esteja vazia;
- a ordem dos IDs aprovados será preservada na aula pública.
```

Atualize o fluxo e os critérios de aprovação para incluir seleção, validação e renderização dos recursos.

- [ ] **Step 2: Criar a referência operacional da skill**

Crie `references/recursos-discentes.md` com este conteúdo normativo:

```markdown
# Recursos discentes

## Princípio

Classifique pela função pedagógica do item, não pelo tipo da fonte. Livros,
apostilas e bancos de questões podem fornecer materiais didáticos ou exercícios
indicados quando as páginas originais comprovarem adequação ao escopo.

## Materiais didáticos

Selecione IDs de `capitulo`, `secao` ou `exemplo` que apoiem o estudo dos
tópicos aprovados. Não promova a fonte a fundamentação apenas por indicá-la ao
discente.

## Exercícios indicados

Selecione somente IDs de `exercicio` ou `questao`. Leia o enunciado integral e
rejeite itens que dependam de conteúdo reservado, mesmo quando o grafo os
relacionar ao mesmo conteúdo formal.

## Registro

Registre somente IDs canônicos em `recursos_discentes`, na ordem de apresentação.
Listas vazias são válidas quando não houver item adequado. Antes de aprovar,
valide o manifesto e regenere o dossiê; nunca edite o dossiê manualmente.
```

- [ ] **Step 3: Atualizar o roteamento e o gate da skill**

Em `SKILL.md`, acrescente ao roteamento:

```markdown
- materiais de estudo e exercícios: [recursos discentes](references/recursos-discentes.md).
```

No fluxo de decisão, exija leitura e aprovação de `recursos_discentes`. Na lista anterior a `aprovado`, acrescente “objeto `recursos_discentes` presente e validado”. Nos invariantes, acrescente:

```markdown
- Nunca classifique um recurso pela origem editorial; avalie o item e suas páginas.
- Nunca use a indicação discente para alterar silenciosamente o papel teórico de uma referência.
```

- [ ] **Step 4: Validar a skill modificada**

Run:

```bash
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/carubbi/.codex/skills/curar-aula-formal
```

Expected: `Skill is valid!`

- [ ] **Step 5: Verificar o diff documental e fazer commit somente do arquivo público**

Run:

```bash
git diff --check -- docs/superpowers/specs/2026-08-26-skill-curar-aula-formal-design.md
```

Expected: nenhuma saída.

```bash
git add docs/superpowers/specs/2026-08-26-skill-curar-aula-formal-design.md
git commit -m "docs: integrar recursos discentes a curadoria"
```

Não tente adicionar `/Users/carubbi/.codex/skills/` ao repositório MQ.

### Task 6: Verificação integrada e handoff para `gerar-aula-formal`

**Files:**
- Verify: `scripts/aulas/`
- Verify: `tests/aulas/`
- Verify, untracked: `.interno/prof/aulas/2026-2/u1_a02/`
- Verify outside repo: `/Users/carubbi/.codex/skills/curar-aula-formal/`

**Interfaces:**
- Consumes: implementação concluída das Tasks 1–5.
- Produces: evidência de que o contrato 1.2 está pronto para ser usado como entrada da futura skill `gerar-aula-formal`.

- [ ] **Step 1: Executar toda a suíte de curadoria**

Run:

```bash
.venv/bin/python -m unittest discover -s tests/aulas -v
```

Expected: todos os testes PASS, sem erros ou falhas.

- [ ] **Step 2: Validar e renderizar novamente a Aula 2**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli validar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --exigir-aprovado
```

Expected: exit code 0.

Run:

```bash
.venv/bin/python -m scripts.aulas.cli renderizar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --saida .interno/prof/aulas/2026-2/u1_a02/dossie.md
```

Expected: exit code 0 e dossiê regenerado deterministicamente.

- [ ] **Step 3: Confirmar o conteúdo mínimo do dossiê real**

Run:

```bash
rg -n "^## Recursos discentes|^### Materiais didáticos|^### Exercícios indicados|barbetta-2010-exercicio-2-7|banco-questoes-2026-2-questao-6" \
  .interno/prof/aulas/2026-2/u1_a02/dossie.md
```

Expected: ocorrências para as duas subseções e para os recursos amostrais indicados.

- [ ] **Step 4: Validar novamente a skill de curadoria**

Run:

```bash
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/carubbi/.codex/skills/curar-aula-formal
```

Expected: `Skill is valid!`

- [ ] **Step 5: Auditar rastreamento e alterações pendentes**

Run:

```bash
git ls-files .interno
```

Expected: nenhuma saída.

Run:

```bash
git status --short
```

Expected: nenhuma inclusão de `.interno/`; mudanças preexistentes e a aula pública do usuário podem permanecer sem commit.

- [ ] **Step 6: Registrar o estado de prontidão**

Informe ao docente:

```text
Contrato 1.2 validado; manifesto e dossiê privados da Aula 2 migrados;
curar-aula-formal atualizada. O próximo incremento pode especificar e criar
gerar-aula-formal usando somente manifesto aprovado 1.2 e grafo canônico.
```

Não crie a skill `gerar-aula-formal` neste plano; esse trabalho começa somente após a verificação integrada acima.
