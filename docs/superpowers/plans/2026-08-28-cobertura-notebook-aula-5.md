# Cobertura computacional da Aula 5 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar `notebook.yaml` da Aula 5 para o contrato 1.1, cobrir todos os subassuntos e regenerar os notebooks com as variáveis derivadas aprovadas.

**Architecture:** A matriz liga cada subassunto a operações ou justificativa teórica. As novas variáveis são criadas na cópia `dados`; o par é executado e validado em diretório temporário antes da promoção conjunta.

**Tech Stack:** Python 3.12, pandas, Jupyter/nbformat, YAML.

**Spec:** `docs/superpowers/specs/2026-08-28-rastreabilidade-aulas-notebooks-design.md`

## Global Constraints

- Depende do manifesto 1.3 aprovado e do validador de cobertura do plano anterior.
- Não criar dados ou defeitos artificiais.
- Manter linhas simples, sem encadeamento de métodos.
- Exibir uma saída por célula quando a separação for possível.
- Promover os dois notebooks conjuntamente.

---

### Task 1: Desenhar e validar a matriz da Aula 5

**Files:**
- Modify: `.interno/prof/aulas/2026-2/u1_a05/notebook.yaml`

- [ ] **Step 1: Alterar o contrato para 1.1**

Adicionar `cobertura_subassuntos` com os 15 subassuntos selecionados, cada um uma vez. Associar tipos, conversão, ausências, duplicidades e transformações às operações correspondentes; justificar representatividade como tratamento teórico dependente do desenho de coleta.

- [ ] **Step 2: Validar a matriz antes de alterar as operações**

Run: `.venv/bin/python /Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/validar_notebooks.py --plano .interno/prof/aulas/2026-2/u1_a05/notebook.yaml --manifesto .interno/prof/aulas/2026-2/u1_a05/selecao.yaml --aula aulas/u1_a05.md --cabecalho /Users/carubbi/.codex/skills/gerar-aula-formal/references/cabecalho-aula.md --discente notebooks/u1_a05.ipynb --resolvido notebooks/resolvidos/u1_a05.ipynb`

Expected: a matriz é aceita e cada um dos 15 subassuntos aparece exatamente uma vez. Nesta etapa, ela referencia somente operações já existentes; as novas operações são acrescentadas na Task 2.

### Task 2: Acrescentar as variáveis derivadas aprovadas

**Files:**
- Modify: `.interno/prof/aulas/2026-2/u1_a05/notebook.yaml`

- [ ] **Step 1: Criar `postura_completa`**

```python
postura = dados["Clutch Completion"]
postura_completa = postura == "Yes"
dados["postura_completa"] = postura_completa
```

Adicionar uma célula para `dados["postura_completa"].dtype` e outra para `dados["postura_completa"].value_counts(dropna=False)`; a `Series` é necessária aqui para verificar os dois valores lógicos e suas frequências.

- [ ] **Step 2: Criar `ano_observacao`**

```python
datas = dados["Date Egg"]
anos = datas.dt.year
dados["ano_observacao"] = anos
```

Adicionar células separadas para `dados["ano_observacao"].dtype`, `dados["ano_observacao"].min()` e `dados["ano_observacao"].max()`.

- [ ] **Step 3: Exibir intervalos de massa sem rótulos**

```python
massa = dados["Body Mass (g)"]
faixas = pd.qcut(massa, q=3)
faixas.cat.categories
```

Esperar os intervalos aproximados `(2699.999, 3700.0]`, `(3700.0, 4550.0]` e `(4550.0, 6300.0]`.

- [ ] **Step 4: Criar `faixa_massa` com rótulos ordenados**

```python
rotulos = ["inferior", "intermediária", "superior"]
faixa_massa = pd.qcut(massa, q=3, labels=rotulos)
dados["faixa_massa"] = faixa_massa
```

Adicionar células separadas para verificar `dados["faixa_massa"].dtype`, `dados["faixa_massa"].cat.ordered` e `dados["faixa_massa"].isna().sum()`.

- [ ] **Step 5: Atualizar objetos, evidências e saídas esperadas**

Registrar `postura_completa`, `anos`, `faixas` e `faixa_massa`; não registrar variáveis temporárias que não sejam retomadas.

- [ ] **Step 6: Confirmar que os notebooks públicos ainda estão desatualizados**

Executar `validar_notebooks.py` com o plano atualizado e os notebooks públicos. Expected: falha somente por células/operações novas ainda ausentes; não pode haver falha de cobertura conceitual.

### Task 3: Gerar e comparar o par temporário

**Files:**
- Generate temporarily: `<tmp>/notebooks/u1_a05.ipynb`
- Generate temporarily: `<tmp>/notebooks/resolvidos/u1_a05.ipynb`

- [ ] **Step 1: Criar diretório temporário**

Run: `mktemp -d`

- [ ] **Step 2: Gerar e executar com a fonte remota aprovada**

Executar `gerar_notebooks.py` com o plano, cabeçalho canônico, `--cwd /Users/carubbi/projects/MQ` e os dois destinos dentro do diretório temporário.

- [ ] **Step 3: Validar o par temporário**

Executar `validar_notebooks.py` contra manifesto, aula, plano e arquivos temporários.

Expected: `notebooks válidos` e exit 0.

- [ ] **Step 4: Comparar por IDs e fontes**

Confirmar que o discente conserva 12 células e uma célula vazia por seção; no resolvido, listar IDs adicionados e exigir que nenhuma fonte existente tenha mudado fora das operações aprovadas.

### Task 4: Promover e verificar os notebooks públicos

**Files:**
- Modify: `notebooks/u1_a05.ipynb`
- Modify: `notebooks/resolvidos/u1_a05.ipynb`

- [ ] **Step 1: Promover o par conjuntamente**

Copiar os dois arquivos temporários somente depois da validação e comparação.

- [ ] **Step 2: Executar validação pública fresca**

Executar novamente `validar_notebooks.py` nos caminhos públicos.

Expected: `notebooks válidos`.

- [ ] **Step 3: Conferir execução e formatação**

Run: `git diff --check -- notebooks/u1_a05.ipynb notebooks/resolvidos/u1_a05.ipynb`

Verificar via `nbformat` que não existe output `error` e que a célula de `qcut` contém os três intervalos esperados.

- [ ] **Step 4: Commit dos notebooks públicos**

```bash
git add notebooks/u1_a05.ipynb notebooks/resolvidos/u1_a05.ipynb
git commit -m "feat: completar cobertura computacional da aula 5"
```
