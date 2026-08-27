# Notebook mínimo da Aula 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o notebook discente mínimo e o notebook resolvido executado da Aula 2, com a topologia, o código e as saídas definidos na especificação aprovada.

**Architecture:** Os dois notebooks compartilharão sete células Markdown com os mesmos IDs e conteúdos. O discente terá uma célula vazia após cada seção; o resolvido terá 18 células de código simples e independentes, executadas em ordem. Um teste estrutural específico validará topologia, estilo, metadados e saídas salvas.

**Tech Stack:** Jupyter Notebook 4.5, Python 3.12, `nbformat`, `nbconvert`, `pandas` 3.0.5 e `unittest`.

**Spec:** `docs/superpowers/specs/2026-08-27-notebook-aula-2-minimo-design.md`

## Global Constraints

- Criar somente `notebooks/u1_a02.ipynb`, `notebooks/resolvidos/u1_a02.ipynb` e o teste específico relacionado.
- Reutilizar exatamente o conteúdo da primeira célula de `notebooks/u1_a01.ipynb` como cabeçalho.
- Manter sete células Markdown compartilhadas, 12 células totais no discente e 25 no resolvido.
- Manter cinco células de código vazias no discente e 18 células executadas no resolvido.
- Usar somente `pandas`, o CSV público da disciplina e as cinco colunas aprovadas.
- Usar nomes curtos e significativos, uma operação principal por linha e nenhuma chamada de método encadeada.
- Não criar funções próprias, classes, gráficos, comentários de código, listas ou `DataFrame` como saída.
- Produzir quatro células sem saída, duas saídas em `Series` e doze saídas escalares ou textuais no resolvido.
- Preservar todas as alterações não relacionadas já existentes no worktree.

---

### Task 1: Teste do contrato dos notebooks

**Files:**
- Create: `tests/notebooks/test_u1_a02_minimo.py`

**Interfaces:**
- Consumes: `notebooks/u1_a01.ipynb` como fonte do cabeçalho e a especificação aprovada como contrato.
- Produces: suíte `NotebookAula2MinimoTest`, executável com `unittest`, que valida os dois notebooks finais.

- [ ] **Step 1: Escrever o teste estrutural inicialmente falho**

Criar testes que leiam os notebooks com `nbformat` e verifiquem:

```python
STUDENT = ROOT / "notebooks/u1_a02.ipynb"
SOLVED = ROOT / "notebooks/resolvidos/u1_a02.ipynb"
TOTAL_CELLS = {STUDENT: 12, SOLVED: 25}
CODE_CELLS = {STUDENT: 5, SOLVED: 18}
SECTION_CODE_COUNTS = (2, 4, 3, 5, 4)
NO_OUTPUT = (0, 6, 14, 15)
SERIES_OUTPUT = (16, 17)
```

O teste deverá comparar o primeiro Markdown com o cabeçalho de
`notebooks/u1_a01.ipynb`, comparar conteúdos e IDs das sete células Markdown,
confirmar as cinco células vazias do discente, confirmar contagens de execução
de 1 a 18 no resolvido e rejeitar erros salvos.

- [ ] **Step 2: Verificar o estilo do código por AST**

Para cada célula resolvida, analisar a fonte com `ast.parse()` e rejeitar:

```python
assert ";" not in cell.source
assert not any(isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Lambda)) for node in ast.walk(tree))
assert not any(
    isinstance(node, ast.Call)
    and isinstance(node.func, ast.Attribute)
    and isinstance(node.func.value, ast.Call)
    for node in ast.walk(tree)
)
```

Também rejeitar atribuições aos nomes `df`, `x`, `tmp` e `aa`, além de imports
diferentes de `pandas`.

- [ ] **Step 3: Verificar a falha inicial**

Run: `.venv/bin/python -m unittest tests.notebooks.test_u1_a02_minimo -v`

Expected: FAIL porque `notebooks/u1_a02.ipynb` e
`notebooks/resolvidos/u1_a02.ipynb` ainda não existem.

### Task 2: Notebook discente mínimo

**Files:**
- Create: `notebooks/u1_a02.ipynb`
- Test: `tests/notebooks/test_u1_a02_minimo.py`

**Interfaces:**
- Consumes: cabeçalho e metadados de `notebooks/u1_a01.ipynb`.
- Produces: notebook 4.5 com sete células Markdown compartilháveis e cinco células de código vazias.

- [ ] **Step 1: Criar as sete células Markdown canônicas**

Usar IDs estáveis e estes conteúdos após o cabeçalho:

```text
# Aula 2 — Fundamentos estatísticos e investigação com dados
## Carregamento do conjunto de dados
## Ciclo 1 — reconhecer a variabilidade
## Ciclo 2 — comparar descrição amostral e populacional
## Ciclo 3 — delimitar população, amostra e unidades
## Ciclo 4 — comparar amostragem aleatória e por conveniência
```

- [ ] **Step 2: Inserir uma célula de código vazia após cada seção**

Cada célula deverá conter:

```json
{"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],"source":[]}
```

- [ ] **Step 3: Validar o notebook discente**

Run: `.venv/bin/python -m json.tool notebooks/u1_a02.ipynb > /dev/null`

Run: `.venv/bin/python -m unittest tests.notebooks.test_u1_a02_minimo.NotebookAula2MinimoTest.test_notebook_discente -v`

Expected: PASS.

### Task 3: Notebook resolvido e execução

**Files:**
- Create: `notebooks/resolvidos/u1_a02.ipynb`
- Test: `tests/notebooks/test_u1_a02_minimo.py`

**Interfaces:**
- Consumes: os sete Markdown canônicos da Task 2 e `data/raw/penguins_raw.csv` para conferência local.
- Produces: notebook com 18 células de código preenchidas, contagens de 1 a 18 e saídas sem erros.

- [ ] **Step 1: Criar as 18 células de código simples**

Usar, em ordem, estas operações:

```python
import pandas as pd
url = "https://raw.githubusercontent.com/carubbi/MQ/main/data/raw/penguins_raw.csv"
dados = pd.read_csv(url)
colunas = ["studyName", "Individual ID", "Species", "Island", "Body Mass (g)"]
dados = dados[colunas]

dados.info()

massa = dados["Body Mass (g)"]
massa.count()

massa.min()

massa.max()

massa.nunique()

validos = dados.dropna(subset=["Body Mass (g)"])
amostra = validos.sample(n=30, random_state=42)

media = massa.mean()
media

massa_amostra = amostra["Body Mass (g)"]
media_amostra = massa_amostra.mean()
media_amostra

len(dados)

len(amostra)

ids = dados[["studyName", "Individual ID"]]
ids = ids.drop_duplicates()
len(ids)

unidade_analise = "pinguim"
unidade_analise

unidade_observacao = "registro de um pinguim"
unidade_observacao

amostra_aleatoria = dados.sample(n=30, random_state=42)

ilha = dados["Island"]
filtro = ilha == "Biscoe"
biscoe = dados[filtro]
amostra_conveniencia = biscoe.head(30)

especies = amostra_aleatoria["Species"]
contagem_aleatoria = especies.value_counts()
contagem_aleatoria

especies = amostra_conveniencia["Species"]
contagem_conveniencia = especies.value_counts()
contagem_conveniencia
```

Cada bloco separado por linha em branco acima corresponde a uma célula. Não
inserir comentários nas células.

- [ ] **Step 2: Executar o notebook resolvido**

Run: `.venv/bin/jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=120 notebooks/resolvidos/u1_a02.ipynb`

Expected: execução completa, contagens de 1 a 18 e nenhuma saída `error`.

- [ ] **Step 3: Conferir os resultados essenciais**

Os valores salvos deverão incluir:

```text
342
2700.0
6300.0
94
4201.754385964912
4177.5
344
30
344
pinguim
registro de um pinguim
```

As contagens do Ciclo 4 deverão ser 12 Gentoo, 12 Adelie e 6 Chinstrap na
amostra aleatória; e 30 Adelie na amostra por conveniência.

- [ ] **Step 4: Executar toda a suíte específica**

Run: `.venv/bin/python -m unittest tests.notebooks.test_u1_a02_minimo -v`

Expected: PASS em todos os testes.

### Task 4: Auditoria final e registro

**Files:**
- Validate: `notebooks/u1_a02.ipynb`
- Validate: `notebooks/resolvidos/u1_a02.ipynb`
- Validate: `tests/notebooks/test_u1_a02_minimo.py`

**Interfaces:**
- Consumes: artefatos concluídos nas Tasks 1–3.
- Produces: evidência de validade estrutural, execução correta e ausência de alterações acidentais relacionadas.

- [ ] **Step 1: Auditar os dois notebooks**

Run: `.venv/bin/python /Users/carubbi/.codex/skills/scientific-notebook-curation/scripts/audit_notebook.py notebooks/u1_a02.ipynb`

Run: `.venv/bin/python /Users/carubbi/.codex/skills/scientific-notebook-curation/scripts/audit_notebook.py notebooks/resolvidos/u1_a02.ipynb`

Expected: JSON válido, nenhuma saída de erro e as quantidades de células previstas.

- [ ] **Step 2: Executar verificações finais**

Run: `.venv/bin/python -m unittest tests.notebooks.test_u1_a02_minimo -v`

Run: `git diff --check -- notebooks/u1_a02.ipynb notebooks/resolvidos/u1_a02.ipynb tests/notebooks/test_u1_a02_minimo.py`

Expected: todos os testes passam e `git diff --check` não relata problemas.

- [ ] **Step 3: Registrar somente os artefatos relacionados**

```bash
git add notebooks/u1_a02.ipynb notebooks/resolvidos/u1_a02.ipynb tests/notebooks/test_u1_a02_minimo.py
git commit -m "feat: criar notebooks minimos da aula 2"
```
