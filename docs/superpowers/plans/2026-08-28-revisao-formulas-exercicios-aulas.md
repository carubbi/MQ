# Revisão das fórmulas e atividades das aulas — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar as aulas 2 e 5 ao manifesto 1.3, substituir exemplos sem origem por atividades rastreáveis e manter somente fórmulas com função didática observável.

**Architecture:** A curadoria seleciona primeiro as origens; os dossiês são regenerados; cada aula é revisada em rascunho privado e promovida somente após aprovação docente individual.

**Tech Stack:** YAML, grafo JSON, Markdown/LaTeX, CLI `scripts.aulas`.

**Spec:** `docs/superpowers/specs/2026-08-28-rastreabilidade-aulas-notebooks-design.md`

## Global Constraints

- Ler as páginas originais antes de selecionar ou adaptar.
- Priorizar exercício/questão; usar exemplo aplicado somente com justificativa registrada.
- Resolver manualmente, sem código.
- Não publicar uma aula sem aprovação do respectivo rascunho.
- Nada sob `.interno/` pode ser rastreado.

---

### Task 1: Curar as atividades da Aula 2

**Files:**
- Modify: `.interno/prof/aulas/2026-2/u1_a02/selecao.yaml`
- Regenerate: `.interno/prof/aulas/2026-2/u1_a02/dossie.md`

- [ ] **Step 1: Ler os candidatos do grafo e as páginas originais**

Avaliar os exercícios 1–6 da apostila/banco para o ciclo 1; `barbetta-2010-exercicio-1-2` para o ciclo 3; `barbetta-2010-exercicio-2-7` e `navidi-2024-exercicio-1-1-2` para o ciclo 4. Para o ciclo 2, verificar o exemplo aplicado das caixas de laranjas de Barbetta, pp. 18–23.

- [ ] **Step 2: Apresentar uma recomendação por ciclo e parar**

Informar ID, item, página, forma de uso, conceitos e justificativa de eventual `exemplo_aplicado`. Obter aprovação docente antes de editar.

- [ ] **Step 3: Migrar o manifesto aprovado para 1.3**

Registrar `atividade_resolvida` em todos os ciclos e adicionar cada origem à referência do tópico correspondente com papel `exercicio`.

- [ ] **Step 4: Validar e regenerar o dossiê**

Run: `.venv/bin/python -m scripts.aulas.cli validar --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml --grafo .interno/prof/refs/mapas/grafo_referencias.json --exigir-aprovado`

Run: `.venv/bin/python -m scripts.aulas.cli renderizar --manifesto .interno/prof/aulas/2026-2/u1_a02/selecao.yaml --grafo .interno/prof/refs/mapas/grafo_referencias.json --saida .interno/prof/aulas/2026-2/u1_a02/dossie.md`

Expected: manifesto válido e dossiê com uma origem por ciclo.

### Task 2: Curar as atividades da Aula 5

**Files:**
- Modify: `.interno/prof/aulas/2026-2/u1_a05/selecao.yaml`
- Regenerate: `.interno/prof/aulas/2026-2/u1_a05/dossie.md`

- [ ] **Step 1: Selecionar o exercício do ciclo 1**

Comparar os 25 candidatos ligados a `topico-tipos-de-variaveis`, priorizando o exercício que exija classificar variáveis nominais, ordinais, discretas e contínuas.

- [ ] **Step 2: Ler os exemplos aplicados dos ciclos 2–4**

Usar McKinney pp. 108–110/186–190 para tipos e conversão, pp. 209–216 para qualidade e pp. 211–223 para pré-processamento. Confirmar que cada atividade preserva os dados do exemplo de origem.

- [ ] **Step 3: Apresentar a recomendação dos quatro ciclos e parar**

Obter aprovação docente antes da edição do manifesto.

- [ ] **Step 4: Migrar para 1.3 e ampliar McKinney**

Registrar as quatro atividades e ampliar `mckinney-2017-sec-7-2` para pp. 215–223, descrevendo discretização e `qcut()` na cobertura.

- [ ] **Step 5: Validar e regenerar o dossiê**

Run: `.venv/bin/python -m scripts.aulas.cli validar --manifesto .interno/prof/aulas/2026-2/u1_a05/selecao.yaml --grafo .interno/prof/refs/mapas/grafo_referencias.json --exigir-aprovado`

Run: `.venv/bin/python -m scripts.aulas.cli renderizar --manifesto .interno/prof/aulas/2026-2/u1_a05/selecao.yaml --grafo .interno/prof/refs/mapas/grafo_referencias.json --saida .interno/prof/aulas/2026-2/u1_a05/dossie.md`

### Task 3: Auditar fórmulas e redigir a Aula 2

**Files:**
- Create: `.interno/prof/aulas/2026-2/u1_a02/rascunho.md`
- Modify after approval: `aulas/u1_a02.md`

- [ ] **Step 1: Classificar as fórmulas 2.1–2.12**

Para cada tag, registrar em nota de trabalho: fonte, função observável e ponto de reutilização. Remover do rascunho qualquer fórmula sem função; renumerar as restantes.

- [ ] **Step 2: Substituir cada `Exemplo e resolução`**

Parafrasear a atividade aprovada, citar autor/item/página e mostrar os passos manuais que usam os conceitos ou fórmulas retidos.

- [ ] **Step 3: Validar o rascunho e apresentar o diff**

Comparar `.interno/prof/aulas/2026-2/u1_a02/rascunho.md` com `aulas/u1_a02.md`; resumir fórmulas removidas, mantidas, exercícios e citações. Parar para aprovação.

- [ ] **Step 4: Promover somente após aprovação**

Copiar integralmente o rascunho aprovado, conferir igualdade e remover o rascunho privado promovido.

### Task 4: Auditar fórmulas e redigir a Aula 5

**Files:**
- Create: `.interno/prof/aulas/2026-2/u1_a05/rascunho.md`
- Modify after approval: `aulas/u1_a05.md`

- [ ] **Step 1: Classificar as fórmulas 5.1–5.10**

Testar cada fórmula contra cálculo, dedução, definição reutilizada ou interpretação. Tratar 5.1–5.4 e 5.9–5.10 como candidatas prioritárias à remoção; manter 5.5–5.8 somente se a atividade manual as utilizar.

- [ ] **Step 2: Redigir quatro atividades manuais rastreáveis**

Usar os dados das origens aprovadas; explicar a discretização da massa como relativa à amostra, sem transformar os rótulos em limites biológicos.

- [ ] **Step 3: Apresentar o diff e parar para aprovação**

Destacar toda alteração de fórmula, exemplo, citação e numeração.

- [ ] **Step 4: Promover e verificar**

Após aprovação, promover o rascunho, conferir os quatro vínculos de notebook e remover o arquivo privado promovido.

### Task 5: Verificação editorial integrada

- [ ] **Step 1: Conferir tags e citações**

Run: `rg -n '\\tag\{|### Exemplo e resolução|\([A-ZÁ-Ú]+;' aulas/u1_a02.md aulas/u1_a05.md`

Expected: tags sequenciais, quatro exemplos por aula e citação próxima a cada atividade.

- [ ] **Step 2: Conferir vínculos e formatação**

Run: `rg -n '../notebooks/u1_a0[25]\.ipynb' aulas/u1_a02.md aulas/u1_a05.md`

Run: `git diff --check -- aulas/u1_a02.md aulas/u1_a05.md`

- [ ] **Step 3: Commit somente das aulas públicas aprovadas**

```bash
git add aulas/u1_a02.md aulas/u1_a05.md
git commit -m "docs: tornar exemplos e formulas rastreaveis"
```
