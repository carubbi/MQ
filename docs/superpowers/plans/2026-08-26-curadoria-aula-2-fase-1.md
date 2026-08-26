# Aula 2 Curation Pilot Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir e executar a fase privada de curadoria da Aula 2 até produzir `selecao.yaml` com evidências verificadas e `dossie.md` pronto para a decisão docente.

**Architecture:** O YAML privado será a fonte canônica das evidências, dos candidatos e das decisões; o Markdown será uma visualização determinística desse YAML. Código público e testável validará o contrato contra o grafo e renderizará o dossiê, enquanto os dois artefatos da aula e a convenção matemática permanecerão sob `.interno/`, ignorados pelo Git.

**Tech Stack:** Python 3, biblioteca padrão, PyYAML, jsonschema Draft 2020-12, unittest, grafo JSON e ferramentas locais de extração de PDF.

**Spec:** `docs/superpowers/specs/2026-08-26-curadoria-aulas-formais-design.md`

## Global Constraints

- A Fase 1 termina no bloqueio humano de seleção; não cria `aulas/u1_a02.md`.
- Nenhum arquivo sob `.interno/` será rastreado ou incluído à força no Git.
- Os únicos artefatos privados da Aula 2 serão `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml` e `.interno/prof/aulas/2026-2/u1_a02/dossie.md`.
- A convenção compartilhada ficará em `.interno/docs/modelos/notacao-estatistica.md`.
- `dossie.md` será sempre derivado de `selecao.yaml` e nunca receberá edição manual.
- O grafo localiza referências; sínteses, notações e divergências exigem leitura das páginas originais.
- A seleção inicial não presumirá tópicos nem referências: ambos começarão em estado `pendente`.
- Os arquivos públicos já removidos no worktree não serão restaurados, substituídos, staged ou commitados.
- A suíte integral legada não será usada como critério desta fase porque seus testes de inventário dependem dos arquivos públicos atualmente removidos; somente os testes novos e os testes de consulta do grafo serão executados.

---

## File Structure

### Código público e rastreado

- `requirements.txt`: acrescenta PyYAML.
- `scripts/aulas/__init__.py`: declara o pacote de curadoria de aulas.
- `scripts/aulas/schema_selecao.json`: contrato estrutural do manifesto privado.
- `scripts/aulas/manifesto.py`: carregamento YAML e validação estrutural e semântica.
- `scripts/aulas/dossie.py`: renderização Markdown determinística.
- `scripts/aulas/cli.py`: comandos `validar` e `renderizar`.
- `tests/aulas/__init__.py`: declara o pacote de testes.
- `tests/aulas/fixtures.py`: grafo e manifesto mínimos reutilizáveis.
- `tests/aulas/test_manifesto.py`: testes do contrato e da validação semântica.
- `tests/aulas/test_dossie.py`: testes da visão derivada e da preservação do YAML.
- `tests/aulas/test_cli.py`: testes de integração da linha de comando.

### Artefatos privados e não rastreados

- `.interno/docs/modelos/notacao-estatistica.md`: convenção matemática global.
- `.interno/docs/modelos/aula-markdown.md`: modelo editorial ajustado ao novo contrato.
- `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`: evidências, candidatos e decisões pendentes.
- `.interno/prof/aulas/2026-2/u1_a02/dossie.md`: visão derivada para seleção.

---

### Task 1: Manifest Contract and Semantic Validator

**Files:**
- Create: `scripts/aulas/__init__.py`
- Create: `scripts/aulas/schema_selecao.json`
- Create: `scripts/aulas/manifesto.py`
- Create: `tests/aulas/__init__.py`
- Create: `tests/aulas/fixtures.py`
- Create: `tests/aulas/test_manifesto.py`
- Modify: `requirements.txt`

**Interfaces:**
- Consumes: grafo canônico como `dict` e manifesto YAML como `dict`.
- Produces: `load_manifest(path: Path) -> dict`, `validate_manifest(manifest: dict, graph: dict, *, require_approved: bool = False) -> list[str]` e `dump_manifest(manifest: dict) -> str`.

- [ ] **Step 1: Acrescentar a dependência declarada**

Adicionar ao fim de `requirements.txt`:

```text
PyYAML
```

Instalar no ambiente local:

```bash
.venv/bin/python -m pip install PyYAML
```

Expected: `Successfully installed PyYAML` ou indicação de requisito já satisfeito.

- [ ] **Step 2: Criar o fixture mínimo compartilhado**

Criar `tests/aulas/fixtures.py` com um grafo que contenha fonte, seção, conteúdo `01.01`, tópico `topico-populacao` e as relações `contem`, `corresponde_a` e `aborda`. Incluir este manifesto-base:

```python
VALID_MANIFEST = {
    "versao_contrato": "1.0",
    "estado": "em_selecao",
    "aula": {
        "id": "u1_a02",
        "semestre": "2026-2",
        "unidade": "I",
        "numero": 2,
        "data": "2026-08-07",
        "duracao_minutos": 100,
        "titulo": "Fundamentos da Estatística e processo de investigação",
        "conteudos_formais": ["01.01"],
        "resultado_aprendizagem": (
            "Distinguir descrição e inferência e avaliar representatividade."
        ),
    },
    "notacao": {
        "convencao": "global",
        "caminho": ".interno/docs/modelos/notacao-estatistica.md",
    },
    "escopo": {
        "incluidos": ["População e amostra"],
        "excluidos": ["Técnicas detalhadas de amostragem"],
        "reservados": ["Distribuições amostrais"],
    },
    "ciclos": [],
    "topicos": [
        {
            "id": "topico-populacao",
            "nome": "População",
            "classificacao": "central",
            "subassuntos": [],
            "estado": "pendente",
            "divergencias": [],
            "compatibilizacao": {
                "convencao": "notacao_global",
                "observacao": "Normalizar os símbolos pela convenção global.",
            },
            "profundidade": "formal_aplicada",
            "referencias": [
                {
                    "id": "secao-populacao",
                    "fonte_id": "fonte-a",
                    "estado": "pendente",
                    "papeis": [],
                    "paginas_pdf": {"inicio": 10, "fim": 12},
                    "cobertura": "Definição de população e amostra.",
                    "notacao": "N para população e n para amostra.",
                }
            ],
        }
    ],
}
```

- [ ] **Step 3: Escrever os testes estruturais e semânticos que devem falhar**

Criar em `tests/aulas/test_manifesto.py` testes com `copy.deepcopy(VALID_MANIFEST)` que comprovem:

```python
def test_accepts_complete_manifest_in_selection():
    assert validate_manifest(VALID_MANIFEST, GRAPH) == []


def test_rejects_unknown_topic():
    manifest = deepcopy(VALID_MANIFEST)
    manifest["topicos"][0]["id"] = "topico-inexistente"
    assert "tópico desconhecido: topico-inexistente" in validate_manifest(
        manifest, GRAPH
    )


def test_rejects_reference_without_explicit_topic_relation():
    graph = deepcopy(GRAPH)
    graph["relacoes"] = [
        edge for edge in graph["relacoes"] if edge["tipo"] != "aborda"
    ]
    assert (
        "referência secao-populacao não aborda topico-populacao"
        in validate_manifest(VALID_MANIFEST, graph)
    )


def test_rejects_pages_outside_reference_interval():
    manifest = deepcopy(VALID_MANIFEST)
    manifest["topicos"][0]["referencias"][0]["paginas_pdf"]["fim"] = 13
    assert (
        "páginas fora do intervalo de secao-populacao: 10-13"
        in validate_manifest(manifest, GRAPH)
    )


def test_approved_manifest_rejects_pending_decisions():
    manifest = deepcopy(VALID_MANIFEST)
    manifest["estado"] = "aprovado"
    findings = validate_manifest(manifest, GRAPH, require_approved=True)
    assert "manifesto aprovado contém tópico pendente: topico-populacao" in findings


def test_selected_topic_requires_fundamentation_reference():
    manifest = deepcopy(VALID_MANIFEST)
    manifest["estado"] = "aprovado"
    topic = manifest["topicos"][0]
    topic["estado"] = "selecionado"
    reference = topic["referencias"][0]
    reference["estado"] = "selecionada"
    reference["papeis"] = ["complementar"]
    assert (
        "tópico selecionado sem referência de fundamentação: topico-populacao"
        in validate_manifest(manifest, GRAPH, require_approved=True)
    )
```

- [ ] **Step 4: Executar os testes para confirmar a falha inicial**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto -v
```

Expected: `ERROR` por ausência de `scripts.aulas.manifesto`.

- [ ] **Step 5: Implementar o JSON Schema**

Criar `scripts/aulas/schema_selecao.json` com `additionalProperties: false` em todos os objetos e com estes valores fechados:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": [
    "versao_contrato", "estado", "aula", "notacao",
    "escopo", "ciclos", "topicos"
  ],
  "properties": {
    "versao_contrato": {"const": "1.0"},
    "estado": {"enum": ["em_selecao", "aprovado"]},
    "aula": {"$ref": "#/$defs/aula"},
    "notacao": {"$ref": "#/$defs/notacao"},
    "escopo": {"$ref": "#/$defs/escopo"},
    "ciclos": {"type": "array", "items": {"$ref": "#/$defs/ciclo"}},
    "topicos": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/$defs/topico"}
    }
  }
}
```

Nos `$defs`, exigir os campos usados em `VALID_MANIFEST`. Fechar os enums de tópico em `pendente`, `selecionado`, `rejeitado`, `adiado`; os estados de referência em `pendente`, `selecionada`, `rejeitada`; os papéis em `fundamentacao`, `complementar`, `contraponto`, `exemplo`, `exercicio`; a classificação em `central`, `prerequisito`, `opcional`, `adiado`; e a profundidade em `formal_aplicada`. Permitir `ciclos: []` somente em `em_selecao`; exigir ao menos um ciclo quando `estado` for `aprovado` por meio de `if`/`then`.

- [ ] **Step 6: Implementar carregamento, serialização e validação**

Criar `scripts/aulas/manifesto.py` com:

```python
from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).with_name("schema_selecao.json")


def load_manifest(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifesto deve ser um objeto YAML")
    return value


def dump_manifest(manifest: dict) -> str:
    return yaml.safe_dump(
        manifest,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )


def validate_manifest(
    manifest: dict,
    graph: dict,
    *,
    require_approved: bool = False,
) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    findings = [
        f"schema: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(manifest),
            key=lambda error: (list(error.absolute_path), error.message),
        )
    ]
    if findings:
        return findings
    return _semantic_findings(
        manifest,
        graph,
        require_approved=require_approved,
    )
```

Implementar `_semantic_findings(manifest, graph, *, require_approved) -> list[str]` sem alterar o manifesto recebido. A função indexará `graph["nos"]` por ID e `graph["relacoes"]` como conjuntos de pares por tipo. Para cada tópico, confirmará nó de tipo `topico`. Para cada referência, aceitará somente `secao`, `exemplo`, `exercicio` ou `questao`; confirmará a relação `aborda` com o tópico e `corresponde_a` com ao menos um conteúdo formal da aula; e validará o intervalo informado dentro de `pagina_pdf` ou `pagina_pdf_inicio`–`pagina_pdf_fim`. Com `require_approved=True`, exigirá estado geral `aprovado`, ausência de tópicos e referências pendentes, ao menos uma referência selecionada com papel `fundamentacao` em cada tópico selecionado e ao menos um ciclo.

- [ ] **Step 7: Executar os testes e confirmar aprovação**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_manifesto -v
```

Expected: todos os testes `OK`.

- [ ] **Step 8: Commitar o contrato público**

```bash
git add requirements.txt scripts/aulas tests/aulas
git commit -m "feat: validate private lesson selection manifests"
```

---

### Task 2: Deterministic Dossier Renderer and CLI

**Files:**
- Create: `scripts/aulas/dossie.py`
- Create: `scripts/aulas/cli.py`
- Create: `tests/aulas/test_dossie.py`
- Create: `tests/aulas/test_cli.py`

**Interfaces:**
- Consumes: `load_manifest()` e `validate_manifest()` da Task 1.
- Produces: `render_dossier(manifest: dict) -> str` e `main(argv: list[str] | None = None) -> int`.

- [ ] **Step 1: Escrever os testes do renderizador**

Criar `tests/aulas/test_dossie.py`:

```python
from copy import deepcopy

from scripts.aulas.dossie import render_dossier
from tests.aulas.fixtures import VALID_MANIFEST


def test_renders_scope_topics_references_and_evidence():
    rendered = render_dossier(VALID_MANIFEST)
    assert rendered.startswith("# Dossiê de curadoria — u1_a02\n")
    assert "## Escopo do encontro" in rendered
    assert "## Tópicos candidatos" in rendered
    assert "### População — pendente" in rendered
    assert "`secao-populacao`" in rendered
    assert "Definição de população e amostra." in rendered
    assert "N para população e n para amostra." in rendered


def test_rendering_is_deterministic_and_does_not_mutate_manifest():
    manifest = deepcopy(VALID_MANIFEST)
    before = deepcopy(manifest)
    assert render_dossier(manifest) == render_dossier(manifest)
    assert manifest == before


def test_dossier_contains_no_editable_selection_controls():
    rendered = render_dossier(VALID_MANIFEST)
    assert "[ ]" not in rendered
    assert "[x]" not in rendered.casefold()
```

- [ ] **Step 2: Escrever os testes da CLI**

Em `tests/aulas/test_cli.py`, criar arquivos temporários para manifesto, grafo e dossiê e testar:

```python
def test_render_command_writes_only_dossier():
    before = manifest_path.read_bytes()
    completed = run_cli("renderizar", manifest_path, graph_path, dossier_path)
    assert completed.returncode == 0
    assert dossier_path.read_text(encoding="utf-8").startswith(
        "# Dossiê de curadoria — u1_a02"
    )
    assert manifest_path.read_bytes() == before


def test_validate_command_reports_semantic_errors_without_writing():
    completed = run_cli("validar", invalid_manifest_path, graph_path)
    assert completed.returncode == 1
    assert "tópico desconhecido" in completed.stderr
```

- [ ] **Step 3: Executar os testes para confirmar a falha inicial**

Run:

```bash
.venv/bin/python -m unittest tests.aulas.test_dossie tests.aulas.test_cli -v
```

Expected: `ERROR` por ausência de `scripts.aulas.dossie` e `scripts.aulas.cli`.

- [ ] **Step 4: Implementar o renderizador puro**

Criar `scripts/aulas/dossie.py` com:

```python
def render_dossier(manifest: dict) -> str:
    aula = manifest["aula"]
    lines = [
        f"# Dossiê de curadoria — {aula['id']}",
        "",
        f"- **Título:** {aula['titulo']}",
        f"- **Data:** {aula['data']}",
        f"- **Duração:** {aula['duracao_minutos']} minutos",
        f"- **Conteúdos formais:** {', '.join(aula['conteudos_formais'])}",
        f"- **Estado:** {manifest['estado']}",
        "",
        "## Escopo do encontro",
        "",
    ]
    lines.extend(_render_scope(manifest["escopo"]))
    lines.extend(["", "## Tópicos candidatos", ""])
    for topic in manifest["topicos"]:
        lines.extend(_render_topic(topic))
    lines.extend(
        [
            "",
            "---",
            "",
            "Este dossiê é derivado de `selecao.yaml`; registre decisões somente no YAML.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
```

Implementar `_render_scope(scope: dict) -> list[str]` com três subseções — incluídos, excluídos e reservados — e `_render_topic(topic: dict) -> list[str]` com título, classificação, subassuntos, divergências, compatibilização e uma tabela de referências. Cada linha da tabela exibirá ID, fonte, estado, papéis, páginas PDF, cobertura e notação na ordem do YAML.

- [ ] **Step 5: Implementar a CLI sem escrita no manifesto**

Criar `scripts/aulas/cli.py` com subcomandos:

```text
validar --manifesto PATH --grafo PATH [--exigir-aprovado]
renderizar --manifesto PATH --grafo PATH --saida PATH
```

`renderizar` deverá validar primeiro, criar somente o diretório pai da saída e escrever apenas o dossiê. Erros serão enviados a `stderr`, um por linha, com retorno `1`. Sucesso retornará `0`.

- [ ] **Step 6: Executar os testes do pacote**

Run:

```bash
.venv/bin/python -m unittest discover -s tests/aulas -v
```

Expected: todos os testes `OK`.

- [ ] **Step 7: Executar regressão da consulta ao grafo**

Run:

```bash
.venv/bin/python -m unittest tests.grafo_refs.test_query_graph -v
```

Expected: todos os testes `OK`.

- [ ] **Step 8: Commitar renderizador e CLI**

```bash
git add scripts/aulas/dossie.py scripts/aulas/cli.py tests/aulas/test_dossie.py tests/aulas/test_cli.py
git commit -m "feat: render lesson curation dossiers"
```

---

### Task 3: Private Mathematical and Editorial Contracts

**Files:**
- Create: `.interno/docs/modelos/notacao-estatistica.md`
- Modify: `.interno/docs/modelos/aula-markdown.md`

**Interfaces:**
- Consumes: decisões das seções 9–11 da especificação.
- Produces: convenção matemática compartilhada e modelo teórico sem implementação computacional.

- [ ] **Step 1: Criar a convenção matemática global**

Criar `.interno/docs/modelos/notacao-estatistica.md` com estas seções e decisões explícitas:

```markdown
# Convenção matemática da disciplina T199

## Princípios
## População, amostra e índices
## Variáveis aleatórias e valores observados
## Parâmetros e estatísticas
## Probabilidade e distribuições
## Estimação e testes
## Regressão
## Tradução entre referências
```

Registrar $U=\{1,\ldots,N\}$ para uma população finita indexada, $S\subseteq U$ para a amostra, $N$ e $n$ para seus tamanhos, $X_i$ para variável aleatória e $x_i$ para valor observado, $\mu$, $\sigma^2$ e $p$ para parâmetros, e $\bar{x}$, $s^2$ e $\hat p$ para estatísticas. Definir $s^2=(n-1)^{-1}\sum_{i=1}^{n}(x_i-\bar{x})^2$ como variância amostral por padrão e exigir declaração explícita quando outra convenção for adotada.

- [ ] **Step 2: Reformular o modelo privado das aulas**

Em `.interno/docs/modelos/aula-markdown.md`, substituir a sequência centrada em aplicação computacional por esta estrutura de ciclo:

```markdown
### Ciclo didático N — Título

#### Problema e motivação
#### Definição formal e notação
#### Domínio, condições e pressupostos
#### Propriedades e deduções curtas
#### Exemplo e resolução
#### Interpretação e limitações
#### Aplicação no notebook
```

Definir `Aplicação no notebook` como objetivo, questão, contraste, evidência e vínculo para o ciclo correspondente. Proibir nessa subseção código, pseudocódigo, bibliotecas, APIs, comandos e instruções de implementação; preservar funções matemáticas em notação formal.

- [ ] **Step 3: Verificar as duas estruturas privadas**

Run:

```bash
rg -n '^## (População, amostra e índices|Parâmetros e estatísticas|Tradução entre referências)$' .interno/docs/modelos/notacao-estatistica.md
rg -n '^#### (Definição formal e notação|Aplicação no notebook)$' .interno/docs/modelos/aula-markdown.md
```

Expected: três correspondências no primeiro comando e duas no segundo.

- [ ] **Step 4: Confirmar que os contratos permanecem privados**

Run:

```bash
git check-ignore -v .interno/docs/modelos/notacao-estatistica.md
git check-ignore -v .interno/docs/modelos/aula-markdown.md
```

Expected: ambos apontam para `.gitignore:1:.interno/`.

Não executar `git add -f` e não criar commit para esta task.

---

### Task 4: Curate and Render the Private Aula 2 Pilot

**Files:**
- Create: `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`
- Create: `.interno/prof/aulas/2026-2/u1_a02/dossie.md`

**Interfaces:**
- Consumes: cronograma docente, planejamento e detalhamento da Unidade I, grafo, páginas originais, `dump_manifest()`, `validate_manifest()` e `render_dossier()`.
- Produces: manifesto `em_selecao` completo e dossiê derivado pronto para revisão docente.

- [ ] **Step 1: Fixar o escopo curricular da Aula 2**

Usar exclusivamente:

```text
.interno/prof/ensino/cronograma_2026_2_docente.md
.interno/docs/planejamentos/2026-2/unidade-i.md
.interno/docs/detalhamentos/2026-2/unidade-i.md
```

Registrar `01.01`, 7 de agosto de 2026, 100 minutos e o resultado observável do planejamento. Usar estes tópicos normalizados do grafo:

```text
topico-investigacao-estatistica
topico-estatistica-descritiva
topico-estatistica-inferencial
topico-populacao
topico-amostra
topico-amostragem
topico-representatividade
topico-unidade-de-analise
```

Registrar `variabilidade` como subassunto de investigação estatística; `vieses` e `limites de generalização` como subassuntos de representatividade. Reservar técnicas detalhadas de amostragem, distribuições amostrais, margem de erro e inferência formal para a Unidade III.

- [ ] **Step 2: Extrair todas as referências explicitamente relacionadas**

Executar uma consulta por tópico, sempre intersectada com `01.01`:

```bash
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-investigacao-estatistica
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-estatistica-descritiva
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-estatistica-inferencial
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-populacao
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-amostra
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-amostragem
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-representatividade
.venv/bin/python scripts/grafo_refs/query_graph.py --content 01.01 --topic topico-unidade-de-analise
```

Incluir no YAML todas as seções retornadas. Manter exemplos, exercícios e questões como candidatos de papel `exemplo` ou `exercicio`, sem promovê-los a fundamentação. Não incluir capítulos ou itens apenas por proximidade editorial.

- [ ] **Step 3: Consultar as páginas originais**

Os oito cruzamentos alcançam sete fontes. Executar a extração local uma vez para cada uma:

```bash
.venv/bin/python scripts/grafo_refs/extract_pdf.py apostila-mq
.venv/bin/python scripts/grafo_refs/extract_pdf.py banco-questoes-2026-2
.venv/bin/python scripts/grafo_refs/extract_pdf.py barbetta-2010
.venv/bin/python scripts/grafo_refs/extract_pdf.py montgomery-2018
.venv/bin/python scripts/grafo_refs/extract_pdf.py morettin-bussab-2010
.venv/bin/python scripts/grafo_refs/extract_pdf.py navidi-2024
.venv/bin/python scripts/grafo_refs/extract_pdf.py pinheiro-2009
```

Ler os sete arquivos `.extract.json` correspondentes somente nos intervalos retornados pelo grafo. Renderizar as páginas de controle editorial e as extremidades dos intervalos relevantes:

```bash
.venv/bin/python scripts/grafo_refs/extract_pdf.py apostila-mq --render 8,9,10,168,173
.venv/bin/python scripts/grafo_refs/extract_pdf.py banco-questoes-2026-2 --render 7,8,13
.venv/bin/python scripts/grafo_refs/extract_pdf.py barbetta-2010 --render 12,18,23,24,33,50
.venv/bin/python scripts/grafo_refs/extract_pdf.py montgomery-2018 --render 20,32
.venv/bin/python scripts/grafo_refs/extract_pdf.py morettin-bussab-2010 --render 18,21
.venv/bin/python scripts/grafo_refs/extract_pdf.py navidi-2024 --render 23,25,34
.venv/bin/python scripts/grafo_refs/extract_pdf.py pinheiro-2009 --render 20,23
```

Para cada referência, registrar cobertura conceitual objetiva, notação efetivamente usada e divergências em relação às demais fontes. Não transcrever passagens extensas.

- [ ] **Step 4: Escrever o manifesto privado inicial**

Criar `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml` com `estado: em_selecao`, `ciclos: []`, os oito tópicos na ordem pedagógica definida no Step 1, todos com `estado: pendente`, e todas as referências com `estado: pendente` e `papeis: []`. Preencher integralmente páginas, cobertura e notação; campos vazios não são aceitos.

- [ ] **Step 5: Validar o manifesto inicial**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli validar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json
```

Expected: retorno `0` e nenhuma saída em `stderr`.

- [ ] **Step 6: Renderizar o dossiê**

Run:

```bash
.venv/bin/python -m scripts.aulas.cli renderizar \
  --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml \
  --grafo .interno/prof/refs/mapas/grafo_referencias.json \
  --saida .interno/prof/aulas/2026-2/u1_a02/dossie.md
```

Expected: retorno `0`; o dossiê contém oito tópicos e todas as referências verificadas.

- [ ] **Step 7: Verificar preservação e privacidade**

Run:

```bash
.venv/bin/python -m unittest discover -s tests/aulas -v
.venv/bin/python -m unittest tests.grafo_refs.test_query_graph -v
git check-ignore -v .interno/prof/aulas/2026-2/u1_a02/selecao.yaml
git check-ignore -v .interno/prof/aulas/2026-2/u1_a02/dossie.md
git status --short
```

Expected: testes `OK`; ambos os artefatos apontam para `.gitignore:1:.interno/`; `git status` não mostra os artefatos privados nem alterações além das remoções públicas preexistentes.

- [ ] **Step 8: Parar no bloqueio docente**

Entregar ao docente os caminhos de `dossie.md` e `selecao.yaml`. Não preencher estados de seleção, papéis de referências, ciclos ou compatibilizações em nome do docente. Não criar `aulas/u1_a02.md`.

---

## Phase 1 Completion Evidence

Antes de declarar a fase concluída, registrar:

```text
- saída dos testes de tests/aulas;
- saída de tests.grafo_refs.test_query_graph;
- validação sem achados do manifesto;
- contagem de oito tópicos no dossiê;
- confirmação de que os dois artefatos privados são ignorados;
- confirmação de que nenhuma remoção pública preexistente foi staged.
```

A Fase 2 somente será planejada após o docente alterar o manifesto para `aprovado`, selecionar ou rejeitar todos os tópicos e referências, atribuir papéis, definir ciclos e registrar as compatibilizações necessárias. Essa segunda fase cobrirá validação de aprovação, geração de `aulas/u1_a02.md`, correspondência com o notebook e verificação editorial final.
