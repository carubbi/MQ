# Rastreabilidade dos contratos e skills — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar obrigatórias e validáveis a origem da atividade resolvida e a cobertura dos subassuntos no fluxo de aulas e notebooks.

**Architecture:** O manifesto passa ao contrato 1.3 e registra `atividade_resolvida` por ciclo. O plano computacional passa ao contrato 1.1 e registra `cobertura_subassuntos`; a validação cruzada compara essa matriz ao manifesto e aos IDs de operação.

**Tech Stack:** Python 3.12, JSON Schema 2020-12, PyYAML, jsonschema, unittest, Markdown de skills Codex.

**Spec:** `docs/superpowers/specs/2026-08-28-rastreabilidade-aulas-notebooks-design.md`

## Global Constraints

- Nada sob `.interno/` pode ser rastreado pelo Git.
- Exercício ou questão tem precedência; `exemplo_aplicado` exige justificativa de inexistência de exercício compatível.
- Um subassunto aparece exatamente uma vez na matriz do notebook.
- Cobertura teórica exige justificativa; cobertura computacional exige operação existente.
- Cada skill será testada separadamente antes da seguinte.

---

### Task 1: Contrato 1.3 do manifesto

**Files:**
- Modify: `scripts/aulas/schema_selecao.json`
- Modify: `scripts/aulas/manifesto.py`
- Modify: `tests/aulas/fixtures.py`
- Modify: `tests/aulas/test_manifesto.py`

**Interfaces:**
- Consumes: ciclos e referências selecionadas do manifesto 1.2.
- Produces: manifesto 1.3 com `atividade_resolvida` validada semanticamente.

- [ ] **Step 1: Atualizar a fixture para expressar o contrato desejado**

Adicionar ao ciclo aprovado:

```python
"atividade_resolvida": {
    "referencia_id": "questao-populacao",
    "tipo_origem": "questao",
    "descricao_item": "Questão 1",
    "paginas_pdf": {"inicio": 13, "fim": 13},
    "forma_uso": "parafraseado",
    "conceitos_aplicados": ["População", "Amostra"],
    "justificativa_excecao": None,
}
```

Alterar `versao_contrato` para `1.3` e incluir `questao-populacao` como referência selecionada com papel `exercicio`.

- [ ] **Step 2: Escrever testes RED para estrutura e semântica**

Adicionar testes que rejeitem: campo ausente em manifesto aprovado, ID inexistente, tipo divergente do nó, página fora do nó, origem não selecionada com papel `exercicio` e `exemplo_aplicado` sem justificativa. Adicionar teste que aceite a fixture 1.3.

- [ ] **Step 3: Executar os testes e confirmar RED**

Run: `.venv/bin/python -m unittest tests.aulas.test_manifesto -v`

Expected: falhas por contrato `1.3` ainda não reconhecido e por ausência das novas regras.

- [ ] **Step 4: Implementar o schema e `_activity_findings`**

Criar `$defs.atividadeResolvida` com os campos da fixture; exigir o objeto em cada ciclo. `justificativa_excecao` é nula para `exercicio` e `questao`, mas deve ser texto não vazio para `exemplo_aplicado`. Em `manifesto.py`, validar o nó, o tipo, as páginas, o papel `exercicio` e essa condição.

- [ ] **Step 5: Executar os testes GREEN**

Run: `.venv/bin/python -m unittest tests.aulas.test_manifesto -v`

Expected: todos os testes passam.

- [ ] **Step 6: Commit**

```bash
git add scripts/aulas/schema_selecao.json scripts/aulas/manifesto.py tests/aulas/fixtures.py tests/aulas/test_manifesto.py
git commit -m "feat: validar origem da atividade resolvida"
```

### Task 2: Dossiê com origem da atividade

**Files:**
- Modify: `scripts/aulas/dossie.py`
- Modify: `tests/aulas/test_dossie.py`

**Interfaces:**
- Consumes: `ciclos[].atividade_resolvida` do contrato 1.3.
- Produces: lista legível da origem no dossiê privado.

- [ ] **Step 1: Escrever teste RED de renderização**

Exigir no ciclo renderizado:

```text
- **Atividade resolvida:**
  - **Referência:** `questao-populacao`
  - **Tipo de origem:** questao
  - **Item:** Questão 1
  - **Páginas PDF:** 13
  - **Forma de uso:** parafraseado
```

- [ ] **Step 2: Confirmar RED**

Run: `.venv/bin/python -m unittest tests.aulas.test_dossie -v`

Expected: o bloco ainda não aparece.

- [ ] **Step 3: Renderizar a atividade como lista aninhada**

Estender `_render_cycles` sem criar tabela e reutilizar `_page_label`.

- [ ] **Step 4: Confirmar GREEN e determinismo**

Run: `.venv/bin/python -m unittest tests.aulas.test_dossie -v`

Expected: todos os testes passam, inclusive o teste de determinismo.

- [ ] **Step 5: Commit**

```bash
git add scripts/aulas/dossie.py tests/aulas/test_dossie.py
git commit -m "feat: exibir atividade resolvida no dossie"
```

### Task 3: Contrato 1.1 de cobertura do notebook

**Files:**
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/notebook.schema.json`
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/contrato_notebook.py`
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_contrato_notebook.py`

**Interfaces:**
- Consumes: plano 1.0 e IDs de operação.
- Produces: plano 1.1 com `cobertura_subassuntos` estruturalmente válida.

- [ ] **Step 1: Alterar a fixture de plano para 1.1**

Adicionar:

```python
"cobertura_subassuntos": [
    {
        "topico_id": "topico-populacao",
        "subassunto": "População-alvo",
        "tratamento": "computacional",
        "operacoes": ["r02"],
        "justificativa": None,
    }
],
```

- [ ] **Step 2: Escrever testes RED**

Rejeitar operação inexistente, cobertura computacional sem operação e cobertura teórica sem justificativa; aceitar a fixture completa.

- [ ] **Step 3: Confirmar RED**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_contrato_notebook.py' -v`

Expected: falha porque o contrato 1.1 e a matriz ainda não existem.

- [ ] **Step 4: Implementar schema e validação semântica**

Exigir `cobertura_subassuntos` no topo; condicionar `operacoes` e `justificativa` ao valor de `tratamento`; conferir IDs na união de operações do plano.

- [ ] **Step 5: Confirmar GREEN**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_contrato_notebook.py' -v`

Expected: todos os testes passam.

### Task 4: Validação cruzada de cobertura

**Files:**
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/validar_notebooks.py`
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_validar_notebooks.py`

**Interfaces:**
- Consumes: manifesto 1.3 e plano 1.1.
- Produces: `_validar_cobertura(plano, manifesto) -> list[str]`.

- [ ] **Step 1: Completar a fixture do manifesto com tópico e subassunto**

Usar `topico-populacao`, estado `selecionado` e subassunto `População-alvo`.

- [ ] **Step 2: Escrever testes RED**

Cobrir omissão, duplicação, texto estranho, tópico não selecionado e matriz coerente.

- [ ] **Step 3: Confirmar RED**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -p 'test_validar_notebooks.py' -v`

Expected: os cenários de cobertura ainda não são rejeitados.

- [ ] **Step 4: Implementar comparação por pares exatos**

Comparar `(topico_id, subassunto)` do manifesto e da matriz com `Counter`; chamar a função em `validar_par` antes da topologia dos notebooks.

- [ ] **Step 5: Confirmar GREEN e regressão completa**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -v`

Expected: todos os testes passam.

- [ ] **Step 6: Commit das Tasks 3 e 4**

As alterações ficam na skill pessoal já instalada em `/Users/carubbi/.codex/skills/gerar-notebooks-aula`; não reinstalar a skill nem adicioná-la ao Git do repositório MQ. Se essa skill pertencer a outro repositório Git, registrar a mudança somente nele e em commit separado.

### Task 5: Atualizar e testar as três skills

**Files:**
- Modify: `/Users/carubbi/.codex/skills/curar-aula-formal/SKILL.md`
- Modify: `/Users/carubbi/.codex/skills/gerar-aula-formal/references/contrato-aula.md`
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/SKILL.md`
- Modify: `/Users/carubbi/.codex/skills/gerar-notebooks-aula/references/contrato-plano.md`

**Interfaces:**
- Consumes: contratos 1.3 e 1.1 implementados.
- Produces: instruções que acionam os novos portões corretamente.

- [ ] **Step 1: Executar RED comportamental de `curar-aula-formal`**

Usar um agente em contexto fresco com um manifesto aprovado sem `atividade_resolvida`; registrar se ele aprova a curadoria. O comportamento esperado antes da mudança é a omissão do novo portão.

- [ ] **Step 2: Editar e validar `curar-aula-formal`**

Adicionar a hierarquia exercício/questão → busca no grafo/banco → exemplo aplicado justificado. Executar `quick_validate.py` e repetir o cenário; o agente deve manter o manifesto não aprovado.

- [ ] **Step 3: Executar RED/GREEN de `gerar-aula-formal`**

O cenário exige gerar uma aula com exemplo inventado e fórmula sem uso. Antes da edição, registrar a aceitação indevida; depois, exigir origem rastreável, resolução manual e teste de utilidade da fórmula.

- [ ] **Step 4: Executar RED/GREEN de `gerar-notebooks-aula`**

O cenário usa plano aprovado que omite um subassunto. Antes da edição, registrar aceitação; depois, exigir matriz completa ou justificativa teórica.

- [ ] **Step 5: Validar cada skill**

Run: `.venv/bin/python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/curar-aula-formal`

Run: `.venv/bin/python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-aula-formal`

Run: `.venv/bin/python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-notebooks-aula`

Expected: todas as skills válidas e os cenários GREEN obedecem aos portões.

### Task 6: Verificação integrada do subsistema

**Files:**
- Test only: `scripts/aulas`, `tests/aulas`, `/Users/carubbi/.codex/skills/gerar-notebooks-aula/tests`

- [ ] **Step 1: Executar testes de curadoria**

Run: `.venv/bin/python -m unittest discover -s tests/aulas -v`

- [ ] **Step 2: Executar testes da skill de notebooks**

Run: `.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -v`

- [ ] **Step 3: Verificar formatação e rastreamento**

Run: `git diff --check`

Run: `git ls-files .interno`

Expected: testes passam, `git diff --check` não relata erros e o último comando não lista arquivos.
