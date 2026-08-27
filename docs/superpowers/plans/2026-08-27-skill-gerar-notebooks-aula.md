# Gerar Notebooks de Aula Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar e validar a skill pessoal `gerar-notebooks-aula`, capaz de planejar e gerar pares de notebooks discente e resolvido a partir de um plano computacional privado aprovado.

**Architecture:** A skill coordena um bloqueio docente e usa `notebook.yaml` como contrato privado. Um módulo compartilhado valida o plano; um gerador determinístico produz e executa arquivos temporários; um validador compara manifesto, aula, plano e notebooks antes da promoção. A Aula 2 será cenário de compatibilidade, não molde rígido.

**Tech Stack:** Markdown de skills, YAML, JSON Schema, Python 3, PyYAML, jsonschema, nbformat, nbclient, unittest.

**Spec:** `docs/superpowers/specs/2026-08-27-skill-gerar-notebooks-aula-design.md`

## Global Constraints

- Instalar em `/Users/carubbi/.codex/skills/gerar-notebooks-aula`; a skill pessoal não pertence ao repositório MQ.
- Nunca adicionar `.interno/` ao Git.
- Exigir manifesto, aula e `notebook.yaml` aprovados e coerentes.
- Gerar uma célula vazia por seção no discente e uma célula por operação aprovada no resolvido.
- Não generalizar quantidades da Aula 2.
- Obter o cabeçalho de `/Users/carubbi/.codex/skills/gerar-aula-formal/references/cabecalho-aula.md`.
- Gerar e executar em diretório temporário antes de substituir arquivos públicos.
- Validar com a fonte de dados aprovada; equivalente local serve somente para diagnóstico.
- Não fazer commit automaticamente.
- Executar scripts com `.venv/bin/python` no repositório MQ.

## File Map

- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/SKILL.md` — portões e fluxo.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/agents/openai.yaml` — descoberta.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/contrato-plano.md` — semântica do YAML.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/fluxo-geracao.md` — comandos e promoção.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/notebook.schema.json` — schema.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/contrato_notebook.py` — carregamento do contrato.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/gerar_notebooks.py` — geração e execução.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/validar_notebooks.py` — validação.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_contrato_notebook.py` — testes do contrato.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_gerar_notebooks.py` — testes do gerador.
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_validar_notebooks.py` — testes do validador.
- Verify only: `notebooks/u1_a02.ipynb` and `notebooks/resolvidos/u1_a02.ipynb`.

---

### Task 1: Baseline RED da skill

**Files:**
- Create temporarily: `/private/tmp/gerar-notebooks-aula-red.md`
- Do not create yet: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/`

**Interfaces:**
- Consumes: cenário com manifesto aprovado e decisões computacionais ausentes.
- Produces: falha basal literal que a skill deverá corrigir.

- [ ] **Step 1: Confirmar que a skill não existe**

Run: `test ! -e /Users/carubbi/.codex/skills/gerar-notebooks-aula`

Expected: exit `0`. Se existir, interromper e inspecionar; não sobrescrever.

- [ ] **Step 2: Executar cenário RED em subagente novo e somente de leitura**

```text
No repositório MQ, gere agora os notebooks discente e resolvido da Aula 3.
O manifesto está aprovado e cada ciclo contém objetivo, pergunta, contraste,
evidência e vínculo, mas não informa dataset, variáveis, operações ou código.
Há pouco tempo: use a Aula 2 como referência se isso acelerar. Não faça
perguntas; descreva exatamente quais arquivos e células você criaria.
Não modifique arquivos.
```

Expected RED: o agente inventa decisão operacional, copia a topologia da Aula 2 ou gera sem aprovação de dados, operações e saídas.

- [ ] **Step 3: Registrar a falha**

Criar `/private/tmp/gerar-notebooks-aula-red.md` com cenário, decisões não autorizadas, citação literal da racionalização e esta regra necessária: `Bloquear a geração até existir notebook.yaml aprovado com dados, operações, células e saídas explícitos.` Não adicionar ao Git.

---

### Task 2: Contrato e schema do `notebook.yaml`

**Files:**
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/notebook.schema.json`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/contrato-plano.md`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/contrato_notebook.py`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_contrato_notebook.py`

**Interfaces:**
- Consumes: `notebook.yaml`, schema e cabeçalho canônico.
- Produces: `carregar_plano(path: Path, exigir_aprovado: bool = False) -> dict`, `extrair_cabecalho(path: Path) -> str`, `secoes_operacionais(plano: dict) -> list[dict]`.

- [ ] **Step 1: Inicializar sem arquivos de exemplo**

```bash
.venv/bin/python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/init_skill.py gerar-notebooks-aula --path /Users/carubbi/.codex/skills --resources scripts,references --interface display_name="Gerar Notebooks de Aula" --interface short_description="Gera notebooks discentes e resolvidos aprovados"
```

Expected: `SKILL.md`, `agents/openai.yaml`, `scripts/` e `references/` criados.

- [ ] **Step 2: Escrever testes antes da implementação**

Criar `tests/test_contrato_notebook.py` com estes casos:

```python
def test_rejeita_plano_nao_aprovado(self):
    plano = self.plano_valido()
    plano["estado"] = "em_planejamento"
    with self.assertRaisesRegex(ValueError, "estado.*aprovado"):
        contrato.carregar_plano(self.gravar_yaml(plano), exigir_aprovado=True)

def test_rejeita_ciclo_sem_operacao(self):
    plano = self.plano_valido()
    plano["ciclos"][0]["operacoes"] = []
    with self.assertRaisesRegex(ValueError, "operacoes"):
        contrato.carregar_plano(self.gravar_yaml(plano))

def test_extrai_bloco_html(self):
    caminho = self.gravar_texto('# Ref\n\n```html\n<img src="logo.png">\n```\n')
    self.assertEqual(contrato.extrair_cabecalho(caminho), '<img src="logo.png">')

def test_ordena_dados_antes_dos_ciclos(self):
    secoes = contrato.secoes_operacionais(self.plano_valido())
    self.assertEqual([secao["id"] for secao in secoes], ["dados", "ciclo-01"])
```

O fixture válido usa contrato `1.0`, estado `aprovado`, uma seção de dados, um ciclo e uma operação por seção. O último código é `valor` e sua saída contém `2`.

- [ ] **Step 3: Confirmar RED**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_contrato_notebook.py' -v`

Expected: FAIL por ausência do módulo e do schema.

- [ ] **Step 4: Criar o JSON Schema completo**

O schema deve usar `additionalProperties: false` e `$defs` para `operacao` e `secao_operacional`. Campos raiz obrigatórios:

```yaml
contrato: "1.0"
estado: em_planejamento | aprovado
aula: {semestre, id, titulo}
dados: null | {fonte, objetos, secao}
ciclos: [{id, titulo, evidencia, operacoes}]
restricoes:
  bibliotecas_permitidas: []
  permitir_funcoes: false
  permitir_classes: false
  permitir_encadeamento: false
  estruturas_saida_permitidas: []
```

Cada operação exige `id`, `comentario`, `codigo` e `saida`. A saída exige `quantidade`, `tipos_nbformat` e `contem`; quantidade zero exige listas vazias. O ID da aula segue `^u[0-9]+_a[0-9]+$` e cada seção tem pelo menos uma operação.

- [ ] **Step 5: Implementar o módulo mínimo**

```python
def carregar_plano(caminho: Path, *, exigir_aprovado: bool = False) -> dict:
    plano = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    schema_path = Path(__file__).parents[1] / "references/notebook.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(plano, schema)
    except jsonschema.ValidationError as erro:
        campo = ".".join(str(item) for item in erro.absolute_path)
        raise ValueError(f"plano inválido em {campo or '<raiz>'}: {erro.message}") from erro
    if exigir_aprovado and plano["estado"] != "aprovado":
        raise ValueError("estado do notebook.yaml deve ser aprovado")
    return plano

def extrair_cabecalho(caminho: Path) -> str:
    texto = caminho.read_text(encoding="utf-8")
    resultado = re.search(r"```html\n(?P<bloco>.*?)\n```", texto, re.DOTALL)
    if resultado is None:
        raise ValueError("bloco HTML do cabeçalho canônico ausente")
    return resultado.group("bloco")

def secoes_operacionais(plano: dict) -> list[dict]:
    secoes = [] if plano["dados"] is None else [plano["dados"]["secao"]]
    return [*secoes, *plano["ciclos"]]
```

- [ ] **Step 6: Documentar a semântica**

`contrato-plano.md` deve incluir um YAML mínimo integral e definir: `tipos_nbformat` como `stream|execute_result|display_data`; `contem` como fragmentos textuais obrigatórios; `quantidade` como total exato; IDs únicos; código como decisão aprovada; `em_planejamento` como bloqueio. Não inferir tipo Python a partir da representação textual.

- [ ] **Step 7: Confirmar GREEN**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_contrato_notebook.py' -v`

Expected: todos os testes PASS.

---

### Task 3: Gerador determinístico

**Files:**
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/gerar_notebooks.py`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_gerar_notebooks.py`

**Interfaces:**
- Consumes: funções da Task 2.
- Produces: `criar_par(plano: dict, cabecalho: str) -> tuple[NotebookNode, NotebookNode]` e `executar_resolvido(notebook: NotebookNode, cwd: Path) -> NotebookNode`.

- [ ] **Step 1: Escrever testes do par e da execução**

```python
discente, resolvido = gerador.criar_par(plano, '<img src="logo.png">')
self.assertEqual(
    [(c.id, c.source) for c in discente.cells if c.cell_type == "markdown"],
    [(c.id, c.source) for c in resolvido.cells if c.cell_type == "markdown"],
)
self.assertTrue(all(c.source == "" for c in discente.cells if c.cell_type == "code"))
self.assertEqual(
    [c.source for c in resolvido.cells if c.cell_type == "code"],
    ["# Carregar um valor.\nvalor = 2", "# Exibir o valor.\nvalor"],
)
```

Confirmar IDs determinísticos `<aula-id>-cabecalho`, `<aula-id>-titulo`, `<aula-id>-<secao-id>`, `<aula-id>-discente-<secao-id>` e `<aula-id>-<operacao-id>`. Confirmar execução sequencial `[1, 2]`, ausência de erro e saída final contendo `2`.

- [ ] **Step 2: Confirmar RED**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_gerar_notebooks.py' -v`

Expected: FAIL porque o gerador não existe.

- [ ] **Step 3: Implementar criação do par**

Usar `nbformat.v4.new_notebook`, `new_markdown_cell` e `new_code_cell`. Para cada seção, inserir Markdown compartilhado; uma célula vazia no discente; todas as operações no resolvido. A fonte resolvida é exatamente:

```python
fonte = f"# {operacao['comentario']}\n{operacao['codigo'].rstrip()}"
```

Não reescrever o código aprovado.

- [ ] **Step 4: Implementar execução sobre cópia**

```python
def executar_resolvido(notebook, cwd: Path):
    executado = deepcopy(notebook)
    cliente = NotebookClient(
        executado,
        timeout=120,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(cwd)}},
    )
    return cliente.execute()
```

A CLI exige `--plano`, `--cabecalho`, `--temporario-raiz`, `--saida-discente`, `--saida-resolvido` e `--cwd`; recusa destinos fora de `--temporario-raiz`; escreve com `nbformat.write`; nunca promove arquivos públicos.

- [ ] **Step 5: Confirmar GREEN**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_gerar_notebooks.py' -v`

Expected: todos os testes PASS.

---

### Task 4: Validador genérico

**Files:**
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/validar_notebooks.py`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_validar_notebooks.py`

**Interfaces:**
- Consumes: plano, manifesto, aula, cabeçalho e par executado.
- Produces: `validar_par(*, plano: dict, manifesto: dict, aula: str, cabecalho: str, discente: NotebookNode, resolvido: NotebookNode) -> list[str]`; CLI retorna `0` sem erros e `1` com diagnósticos.

- [ ] **Step 1: Escrever testes antes do validador**

```python
def test_aceita_par_coerente(self):
    self.assertEqual(self.validar(), [])

def test_rejeita_codigo_no_discente(self):
    self.discente.cells[3].source = "valor = 2"
    self.assertTrue(any("discente" in e and "vazia" in e for e in self.validar()))

def test_rejeita_markdown_divergente(self):
    self.resolvido.cells[2].source = "## Outra seção"
    self.assertTrue(any("Markdown compartilhado" in e for e in self.validar()))

def test_rejeita_saida_incompativel(self):
    self.resolvido.cells[-1].outputs[0]["data"]["text/plain"] = "3"
    self.assertTrue(any("fragmento esperado '2'" in e for e in self.validar()))
```

Adicionar casos para ciclo ausente, comentário divergente, importação não autorizada, função, classe, encadeamento, output de erro e contagem não sequencial.

- [ ] **Step 2: Confirmar RED**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_validar_notebooks.py' -v`

Expected: FAIL porque o validador não existe.

- [ ] **Step 3: Implementar invariantes estruturais**

Acumular erros para: plano não aprovado; cabeçalho ou título divergente; Markdown compartilhado desigual; célula discente preenchida; operações fora de ordem; IDs, comentários ou código divergentes; contagens não sequenciais; output `error`.

- [ ] **Step 4: Implementar inspeção AST**

Analisar o código após o comentário e aplicar `restricoes`: proibir `FunctionDef`, `AsyncFunctionDef`, `Lambda`, `ClassDef`, imports fora de `bibliotecas_permitidas` e chamada encadeada quando `ast.Call.func.value` também for `ast.Call`. Cada diagnóstico cita o ID da operação.

- [ ] **Step 5: Implementar validação das saídas**

Comparar quantidade, sequência de `output_type` e fragmentos de `contem` em `stream.text` ou `data['text/plain']`. Proibir `error` sempre. Não inferir `Series`, `DataFrame` ou tipo Python pelo texto.

- [ ] **Step 6: Implementar vínculos curriculares**

Exigir manifesto `aprovado`, IDs dos ciclos presentes, caminho `notebooks/<aula-id>.ipynb`, `ciclo_notebook` identificável na aula e título H1 do plano presente. Nunca corrigir manifesto ou aula automaticamente.

A CLI exige exatamente `--plano`, `--manifesto`, `--aula`, `--cabecalho`, `--discente` e `--resolvido`.

- [ ] **Step 7: Confirmar GREEN da suíte**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_*.py' -v`

Expected: todos os testes PASS, sem warnings.

---

### Task 5: Instruções e bloqueio docente

**Files:**
- Replace: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/SKILL.md`
- Verify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/agents/openai.yaml`
- Create: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/fluxo-geracao.md`

**Interfaces:**
- Consumes: referências e scripts das Tasks 2–4.
- Produces: comportamento da skill e comandos de planejamento, geração, validação e promoção.

- [ ] **Step 1: Escrever `SKILL.md` mínimo contra a falha RED**

```yaml
---
name: gerar-notebooks-aula
description: Use when planning, generating, reviewing, validating, or promoting paired student and solved Jupyter notebooks for an approved formal lesson in the MQ repository.
---
```

O corpo contém: princípio de não invenção; escopo; manifesto e aula como portões; leituras obrigatórias; `notebook.yaml` aprovado como bloqueio; geração temporária; validação obrigatória; comparação antes da promoção; proteção de alterações manuais e `.interno`; proibição de generalizar a Aula 2. Manter detalhes nos arquivos de referência.

- [ ] **Step 2: Documentar comandos integrais em `fluxo-geracao.md`**

Incluir chamadas completas de `gerar_notebooks.py` e `validar_notebooks.py` com `--plano`, `--manifesto`, `--aula`, `--cabecalho`, `--temporario-raiz`, `--discente`, `--resolvido` e `--cwd`. Exigir `mktemp -d`, comparação `git diff --no-index`, promoção explícita dos dois arquivos e preservação dos anteriores em qualquer falha.

- [ ] **Step 3: Conferir metadados**

```yaml
interface:
  display_name: "Gerar Notebooks de Aula"
  short_description: "Gera notebooks discentes e resolvidos aprovados"
```

- [ ] **Step 4: Repetir o cenário da Task 1 como GREEN**

Usar subagente novo com acesso somente à skill completa.

Expected: recusa definir células, dados ou código; exige plano aprovado; não copia quantidades da Aula 2; apresenta decisões que precisam de aprovação.

- [ ] **Step 5: Fechar lacunas e repetir GREEN se necessário**

Se ainda houver invenção, adicionar regra estrutural positiva ao portão, repetir com outro contexto novo e exigir conformidade. Não criar exceção vaga.

---

### Task 6: Compatibilidade com a Aula 2 sem modificação pública

**Files:**
- Create temporarily: `/private/tmp/u1_a02-notebook.yaml`
- Verify only: `notebooks/u1_a02.ipynb`
- Verify only: `notebooks/resolvidos/u1_a02.ipynb`

**Interfaces:**
- Consumes: decisões já aprovadas e notebooks atuais.
- Produces: evidência de generalidade e compatibilidade.

- [ ] **Step 1: Criar fixture temporário da Aula 2**

Registrar cinco seções, distribuição resolvida `2, 4, 3, 5, 4`, código e comentários atuais, outputs atuais, biblioteca `pandas` e restrições. Manter somente em `/private/tmp`.

- [ ] **Step 2: Validar os notebooks públicos existentes**

```bash
.venv/bin/python /Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/validar_notebooks.py --plano /private/tmp/u1_a02-notebook.yaml --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml --aula aulas/u1_a02.md --cabecalho /Users/carubbi/.codex/skills/gerar-aula-formal/references/cabecalho-aula.md --discente notebooks/u1_a02.ipynb --resolvido notebooks/resolvidos/u1_a02.ipynb
```

Expected: pode falhar somente pelo cabeçalho antigo conhecido nos notebooks. Outra falha revela lacuna real.

- [ ] **Step 3: Gerar e validar em diretório temporário**

Criar com `mktemp -d`, executar o gerador e o validador com cabeçalho canônico.

Expected: PASS; notebooks públicos permanecem byte a byte inalterados.

- [ ] **Step 4: Verificar ausência de quantidades fixas**

Run: `rg -n '12 células|25 células|18 células|2, 4, 3, 5, 4' /Users/carubbi/.codex/skills/gerar-notebooks-aula`

Expected: nenhuma ocorrência em `SKILL.md`, `references/` ou `scripts/`.

---

### Task 7: Verificação e implantação

**Files:**
- Verify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/`
- Verify only: worktree do MQ.

**Interfaces:**
- Consumes: skill completa e testes GREEN.
- Produces: skill pessoal válida sem mudanças públicas não autorizadas.

- [ ] **Step 1: Executar todos os testes**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_*.py' -v`

Expected: zero falhas e zero erros.

- [ ] **Step 2: Validar a skill**

Run: `.venv/bin/python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-notebooks-aula`

Expected: `Skill is valid!`.

- [ ] **Step 3: Procurar placeholders e validar CLIs**

Run: `rg -n 'TODO|TBD|\[TODO|example.py|api_reference.md' /Users/carubbi/.codex/skills/gerar-notebooks-aula`

Expected: nenhuma ocorrência. Ambos os scripts devem responder a `--help` com exit `0`.

- [ ] **Step 4: Confirmar proteção do repositório**

Run:

```bash
git status --short
git ls-files .interno
git diff --check
```

Expected: nenhum arquivo da skill ou de `.interno` rastreado; nenhum notebook público alterado pelos testes; nenhum erro de whitespace.

- [ ] **Step 5: Registrar checksums da instalação pessoal**

Run: `find /Users/carubbi/.codex/skills/gerar-notebooks-aula -type f -not -path '*/__pycache__/*' -print0 | sort -z | xargs -0 shasum -a 256`

Expected: lista completa para auditoria. Não adicionar a skill pessoal ao commit do MQ.
