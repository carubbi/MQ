# Remoção dos Ciclos e Piloto da Aula 7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Remover ciclos do fluxo ativo e validar o novo contrato com uma aula conceitual e dois notebooks aplicados para u1_a07.

**Architecture:** O manifesto 2.0 ordena tópicos e referências, sem aplicações. A aula pública expõe conceitos por tópico e aponta uma única vez para o notebook. O plano computacional 2.0 organiza código e evidências em atividades que cobrem um ou mais tópicos selecionados.

**Tech Stack:** Markdown, YAML, JSON Schema 2020-12, Python 3, jsonschema, PyYAML, nbformat, nbclient, unittest, pandas, NumPy, SciPy e Matplotlib.

**Spec:** docs/superpowers/specs/2026-09-02-remocao-ciclos-piloto-aula7-design.md

## Global Constraints

- Não migrar aulas, manifestos ou notebooks anteriores durante o piloto.
- Não alterar conteúdo do usuário que não pertença a esta mudança.
- A aula pública contém conceitos; cálculos com Palmer Penguins, código e gráficos pertencem aos notebooks.
- selecao.yaml usa versao_contrato: "2.0" e não admite ciclos, aplicacao_notebook ou atividade_resolvida.
- notebook.yaml usa contrato: "2.0" e organiza a execução em atividades.
- Toda atividade referencia apenas tópicos selecionados; todo tópico selecionado aparece em ao menos uma atividade no plano aprovado.
- Uma origem bibliográfica usa referência e páginas selecionadas; uma origem autoral contém justificativa não vazia.
- Arquivos sob .interno/ permanecem privados e não são adicionados ao Git.
- Aprovações do manifesto, da aula e do plano computacional são independentes.

---

### Task 1: Arquivar os documentos históricos

**Files:**
- Move: documentos anteriores em docs/superpowers/plans/
- Move: documentos anteriores em docs/superpowers/specs/
- Preserve: docs/superpowers/plans/2026-09-02-remocao-ciclos-piloto-aula7.md
- Preserve: docs/superpowers/specs/2026-09-02-remocao-ciclos-piloto-aula7-design.md
- Destination: .interno/bkp/docs/superpowers/plans/
- Destination: .interno/bkp/docs/superpowers/specs/

- [ ] **Step 1: Registrar arquivos e hashes antes da movimentação**

Run:

~~~bash
find docs/superpowers/plans docs/superpowers/specs -type f -print | sort
find .interno/bkp/docs/superpowers -type f -print 2>/dev/null | sort
shasum -a 256 docs/superpowers/plans/*.md docs/superpowers/specs/*.md
~~~

Expected: os dois documentos ativos de 2026-09-02 aparecem; nenhum destino colide com um caminho que será movido.

- [ ] **Step 2: Mover somente os documentos anteriores**

~~~bash
mkdir -p .interno/bkp/docs/superpowers/plans .interno/bkp/docs/superpowers/specs
find docs/superpowers/plans -maxdepth 1 -type f ! -name '2026-09-02-remocao-ciclos-piloto-aula7.md' -exec mv -n {} .interno/bkp/docs/superpowers/plans/ \;
find docs/superpowers/specs -maxdepth 1 -type f ! -name '2026-09-02-remocao-ciclos-piloto-aula7-design.md' -exec mv -n {} .interno/bkp/docs/superpowers/specs/ \;
~~~

Expected: cada arquivo anterior deixa sua pasta de origem e aparece no destino com o mesmo nome.

- [ ] **Step 3: Verificar preservação e escopo**

~~~bash
find docs/superpowers -type f -print | sort
find .interno/bkp/docs/superpowers -type f -print | sort
git status --short -- docs/superpowers
~~~

Expected: docs/superpowers/ contém somente a especificação e este plano; o backup contém os anteriores.

- [ ] **Step 4: Commit das remoções rastreadas**

~~~bash
git add -u docs/superpowers
git commit -m "docs: arquivar planos e especificacoes legados"
~~~

### Task 2: Substituir o contrato de curadoria por tópicos

**Files:**
- Modify: tests/aulas/fixtures.py
- Modify: tests/aulas/test_manifesto.py
- Modify: tests/aulas/test_dossie.py
- Modify: scripts/aulas/schema_selecao.json
- Modify: scripts/aulas/manifesto.py
- Modify: scripts/aulas/dossie.py

**Interfaces:**
- Consumes: selecao.yaml com tópicos ordenados e planejamento temporal geral.
- Produces: validate_manifest(manifest, graph, require_approved=False) -> list[str] sem ciclos e render_dossier(manifest, graph) -> str por tópicos.

- [ ] **Step 1: Atualizar a fixture para o contrato desejado**

Em VALID_MANIFEST, use:

~~~python
"versao_contrato": "2.0",
"planejamento_tempo": {
    "abertura_minutos": 5,
    "fechamento_minutos": 10,
},
~~~

Remova ciclos. Em approved_manifest(), mantenha somente a aprovação do tópico e das referências.

- [ ] **Step 2: Escrever os testes do novo comportamento**

~~~python
def test_accepts_approved_manifest_without_cycles(self):
    self.assertEqual(
        [],
        validate_manifest(approved_manifest(), GRAPH, require_approved=True),
    )

def test_rejects_legacy_cycles_field(self):
    manifest = approved_manifest()
    manifest["ciclos"] = []
    findings = validate_manifest(manifest, GRAPH)
    self.assertTrue(any("Additional properties" in item for item in findings))

def test_rejects_time_plan_without_development_time(self):
    manifest = approved_manifest()
    manifest["planejamento_tempo"] = {
        "abertura_minutos": 60,
        "fechamento_minutos": 40,
    }
    self.assertIn(
        "planejamento temporal não deixa minutos para desenvolvimento",
        validate_manifest(manifest, GRAPH),
    )
~~~

Em test_dossie.py, exija “Disponível para desenvolvimento: 85 minutos” e ausência de “Ciclos conceituais”, “Aplicação no notebook” e “ciclo-01”.

- [ ] **Step 3: Executar os testes e confirmar RED**

~~~bash
.venv/bin/python -m unittest tests.aulas.test_manifesto tests.aulas.test_dossie -v
~~~

Expected: FAIL porque o schema ainda exige o contrato 1.3 e ciclos.

- [ ] **Step 4: Implementar o schema 2.0**

No nível superior, exija versao_contrato, estado, aula, notacao, escopo, planejamento_tempo e topicos. Fixe versao_contrato em 2.0. Preserve recursos_discentes obrigatório quando estado for aprovado. Exclua propriedades e definições de ciclo, aplicacaoNotebook e atividadeResolvida.

- [ ] **Step 5: Simplificar a validação temporal**

Remova Counter, ACTIVITY_NODE_TYPES, _cycle_findings() e _activity_findings(). Acrescente:

~~~python
def _time_findings(manifest: dict) -> list[str]:
    lesson_duration = manifest.get("aula", {}).get("duracao_minutos")
    timing = manifest.get("planejamento_tempo", {})
    if not isinstance(timing, dict):
        return []
    opening = timing.get("abertura_minutos")
    closing = timing.get("fechamento_minutos")
    if not all(
        isinstance(value, int)
        for value in (lesson_duration, opening, closing)
    ):
        return []
    if lesson_duration - opening - closing <= 0:
        return [
            "planejamento temporal não deixa minutos para desenvolvimento"
        ]
    return []
~~~

Chame _time_findings(manifest) ao final de _semantic_findings().

- [ ] **Step 6: Simplificar o dossiê**

Em _render_time_plan(), use:

~~~python
f"- **Disponível para desenvolvimento:** {available} minutos",
~~~

Exclua _render_cycles() e sua chamada. Preserve a ordem: escopo, planejamento temporal, recursos discentes e tópicos candidatos.

- [ ] **Step 7: Executar a suíte de curadoria**

~~~bash
.venv/bin/python -m unittest discover -s tests/aulas -v
~~~

Expected: PASS.

- [ ] **Step 8: Commit do contrato**

~~~bash
git add scripts/aulas tests/aulas
git commit -m "refactor: organizar curadoria por topicos"
~~~

### Task 3: Atualizar as skills e os modelos da aula conceitual

**Files:**
- Modify: /Users/carubbi/.codex/skills/curar-aula-formal/SKILL.md
- Delete: /Users/carubbi/.codex/skills/curar-aula-formal/references/ciclos-e-tempo.md
- Create: /Users/carubbi/.codex/skills/curar-aula-formal/references/topicos-e-tempo.md
- Modify: /Users/carubbi/.codex/skills/curar-aula-formal/references/criterios-estados.md
- Modify: /Users/carubbi/.codex/skills/gerar-aula-formal/SKILL.md
- Modify: /Users/carubbi/.codex/skills/gerar-aula-formal/references/contrato-aula.md
- Modify: /Users/carubbi/.codex/skills/gerar-aula-formal/references/rascunho-e-publicacao.md
- Modify: .interno/docs/modelos/aula-markdown.md
- Modify: .interno/docs/modelos/notebook-guiado.md
- Modify: ensino/cronograma_2026_2_t199_64_65.md

**Interfaces:**
- Consumes: manifesto 2.0 e guias docentes que podem ser fontes mistas.
- Produces: curadoria por tópicos e aula direta com um único vínculo ao notebook.

- [ ] **Step 1: Reexecutar o caso de regressão editorial**

~~~bash
rg -n 'ciclo|Aplicação no notebook|Exemplo e resolução' \
  /Users/carubbi/.codex/skills/curar-aula-formal \
  /Users/carubbi/.codex/skills/gerar-aula-formal \
  .interno/docs/modelos/aula-markdown.md \
  .interno/docs/modelos/notebook-guiado.md \
  ensino/cronograma_2026_2_t199_64_65.md
~~~

Expected: ocorrências que prescrevem ciclos e aplicações repetidas na aula.

- [ ] **Step 2: Atualizar curar-aula-formal**

Inclua a regra:

~~~markdown
Guias docentes são fontes potencialmente mistas. Classifique cada trecho pelo
destino: conceitos, fórmulas e interpretações breves pertencem à aula;
implementações, cálculos com dados, gráficos e comparações pertencem ao notebook.
Não replique a estrutura do guia no material público.
~~~

Troque o roteamento “ciclos e tempo” por “tópicos e tempo”. A nova referência estabelece ordem pelo array topicos, tempo somente no nível geral e ausência de planejamento computacional no manifesto.

- [ ] **Step 3: Atualizar gerar-aula-formal**

Substitua ciclos por tópicos na ordem do manifesto. Para cada tópico permita: motivação curta; definição e notação; condições; propriedades essenciais; exemplificação conceitual mínima; interpretação e limites.

Defina um único bloco final “Notebook da aula”, com objetivo geral e vínculo relativo ../notebooks/<aula-id>.ipynb. Proíba cálculos com o conjunto, código, bibliotecas, APIs, gráficos computacionais e resultados empíricos.

- [ ] **Step 4: Atualizar modelos e cronograma**

Em aula-markdown.md, use tópicos e um único vínculo final. Em notebook-guiado.md, use atividades. No cronograma, substitua “ciclos didáticos por tópico” por “tópicos em sequência pedagógica, com conceitos no material de aula e aplicações nos notebooks”.

- [ ] **Step 5: Validar skills e vocabulário**

~~~bash
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/curar-aula-formal
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-aula-formal
rg -n 'ciclo|aplicacao_notebook|atividade_resolvida' \
  /Users/carubbi/.codex/skills/curar-aula-formal \
  /Users/carubbi/.codex/skills/gerar-aula-formal \
  .interno/docs/modelos/aula-markdown.md \
  .interno/docs/modelos/notebook-guiado.md
~~~

Expected: skills válidas e nenhuma ocorrência estrutural legada.

- [ ] **Step 6: Commit do arquivo público rastreável**

~~~bash
git add ensino/cronograma_2026_2_t199_64_65.md
git commit -m "docs: separar conceitos de aplicacoes"
~~~

Não adicione arquivos sob .interno/; as skills pessoais ficam fora deste repositório.

### Task 4: Substituir ciclos por atividades no contrato do notebook

**Files:**
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_contrato_notebook.py
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_gerar_notebooks.py
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests/test_validar_notebooks.py
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/references/notebook.schema.json
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/contrato_notebook.py
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts/validar_notebooks.py

**Interfaces:**
- Consumes: plano 2.0, manifesto 2.0 aprovado e aula com vínculo único.
- Produces: secoes_operacionais(plano) -> list[dict] com dados antes das atividades e validar_par(...) -> list[str] com cobertura por tópico.

- [ ] **Step 1: Converter as fixtures para atividades**

Use contrato 2.0 e este nó:

~~~python
{
    "id": "atividade-01",
    "titulo": "## Atividade 1 — examinar um valor",
    "objetivo": "Aplicar o conceito ao valor observado.",
    "topicos": ["topico-populacao"],
    "pergunta": "O que o valor representa?",
    "evidencia": "Valor exibido e interpretado.",
    "origem": {
        "tipo": "autoral",
        "justificativa": "Exemplo mínimo criado para validar o contrato.",
    },
    "operacoes": [
        {
            "id": "r02",
            "comentario": "Exibir o valor.",
            "codigo": "valor",
            "saida": {
                "quantidade": 1,
                "tipos_nbformat": ["execute_result"],
                "contem": ["2"],
            },
        }
    ],
}
~~~

O manifesto de teste possui topico-populacao selecionado. A aula contém [Notebook da aula](../notebooks/u1_a03.ipynb) uma única vez.

- [ ] **Step 2: Escrever testes de contrato e currículo**

Inclua, além dos testes existentes de operações e saídas:

~~~python
def test_rejeita_campo_legado_ciclos(self):
    plano = self.plano_valido()
    plano["ciclos"] = []
    with self.assertRaisesRegex(ValueError, "Additional properties"):
        contrato.carregar_plano(self.gravar_yaml(plano))

def test_rejeita_atividade_sem_operacao(self):
    plano = self.plano_valido()
    plano["atividades"][0]["operacoes"] = []
    with self.assertRaisesRegex(ValueError, "operacoes"):
        contrato.carregar_plano(self.gravar_yaml(plano))

def test_rejeita_topico_nao_selecionado(self):
    self.plano["atividades"][0]["topicos"] = ["topico-ausente"]
    self.assertTrue(any("topico-ausente" in erro for erro in self.validar()))

def test_rejeita_topico_selecionado_sem_atividade(self):
    self.manifesto["topicos"].append(
        {"id": "topico-sem-atividade", "estado": "selecionado"}
    )
    self.assertTrue(any("sem atividade" in erro for erro in self.validar()))

def test_rejeita_aula_sem_vinculo_para_notebook(self):
    self.aula = "# Aula 3 — Exemplo\n"
    self.assertTrue(any("vínculo" in erro for erro in self.validar()))

def test_rejeita_aula_com_vinculo_duplicado(self):
    self.aula += "\n[Repetido](../notebooks/u1_a03.ipynb)\n"
    self.assertTrue(any("exatamente um vínculo" in erro for erro in self.validar()))
~~~

Para a origem bibliográfica, altere origem para referencia_id secao-populacao e páginas 10–12; confirme aceitação. Depois use referencia_id ausente e fim 13 em testes separados; espere, respectivamente, “referência não selecionada” e “páginas fora do intervalo”.

- [ ] **Step 3: Executar testes e confirmar RED**

~~~bash
.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -v
~~~

Expected: FAIL porque o contrato 1.0 exige ciclos e o validador procura ciclos na aula e no manifesto.

- [ ] **Step 4: Implementar o schema 2.0**

Troque ciclos por atividades. A definição atividade exige id, titulo, objetivo, topicos, pergunta, evidencia, origem e operacoes. Use:

~~~json
"id": {"type": "string", "pattern": "^atividade-[0-9]{2}$"},
"titulo": {"type": "string", "pattern": "^## Atividade [0-9]+"},
"topicos": {
  "type": "array",
  "minItems": 1,
  "uniqueItems": true,
  "items": {"type": "string", "pattern": "^topico-[a-z0-9-]+$"}
}
~~~

origem usa oneOf: bibliografica com tipo, referencia_id e paginas_pdf; autoral com tipo e justificativa.

- [ ] **Step 5: Atualizar carregamento e validação**

Em contrato_notebook.py:

~~~python
def secoes_operacionais(plano: dict) -> list[dict]:
    secoes = [] if plano["dados"] is None else [plano["dados"]["secao"]]
    return [*secoes, *plano["atividades"]]
~~~

Em _validar_curriculo(), valide tópicos por atividade, cobertura completa dos selecionados e origem bibliográfica dentro das referências/páginas selecionadas. Exija exatamente uma ocorrência de ../notebooks/<aula-id>.ipynb na aula. Remova a correspondência com IDs de ciclo.

- [ ] **Step 6: Executar a suíte**

~~~bash
.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -v
~~~

Expected: PASS.

### Task 5: Atualizar a skill de notebooks

**Files:**
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/SKILL.md
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/references/contrato-plano.md
- Modify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/references/fluxo-geracao.md

- [ ] **Step 1: Substituir o portão por cobertura de tópicos**

Exija manifesto 2.0 aprovado, aula com vínculo único, atividades cobrindo todos os tópicos selecionados e notebook.yaml aprovado. Quando o plano estiver em elaboração, proponha dados e atividades sem alterar a aula.

- [ ] **Step 2: Atualizar exemplo e fluxo**

O exemplo usa atividade-01 da Task 4. O fluxo confere vínculo único e cobertura dos tópicos, sem IDs compartilhados com a aula.

- [ ] **Step 3: Validar a skill**

~~~bash
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-notebooks-aula
rg -n 'ciclo|aplicacao_notebook|atividade_resolvida' \
  /Users/carubbi/.codex/skills/gerar-notebooks-aula/SKILL.md \
  /Users/carubbi/.codex/skills/gerar-notebooks-aula/references/contrato-plano.md \
  /Users/carubbi/.codex/skills/gerar-notebooks-aula/references/fluxo-geracao.md
~~~

Expected: skill válida e nenhuma ocorrência estrutural legada.

### Task 6: Curar a Aula 7 no contrato 2.0

**Files:**
- Create: .interno/prof/aulas/2026-2/u1_a07/selecao.yaml
- Create: .interno/prof/aulas/2026-2/u1_a07/dossie.md
- Read: .interno/prof/guia/aula7_medidas_estatisticas.md
- Read: .interno/prof/refs/mapas/grafo_referencias.json
- Read: .interno/docs/modelos/notacao-estatistica.md

- [ ] **Step 1: Ler a fundamentação candidata**

Confira nas páginas originais: apostila-mq-sec-4, apostila-mq-sec-5, morettin-bussab-2010-sec-3-1, morettin-bussab-2010-sec-3-2, morettin-bussab-2010-sec-3-3, pinheiro-2009-sec-1-5 e pinheiro-2009-sec-1-6.

- [ ] **Step 2: Criar o manifesto em seleção**

Use contrato 2.0, aula u1_a07, data 2026-08-28, duração 100, conteúdo 01.03, abertura 5 e fechamento 10. Ordene:

~~~yaml
- topico-media
- topico-mediana
- topico-moda
- topico-quantil
- topico-amplitude
- topico-variancia
- topico-desvio-padrao
- topico-intervalo-interquartil
- topico-coeficiente-de-variacao
~~~

Registre aproximações agrupadas como subassuntos. Reserve assimetria, resistência, outliers, histogramas e boxplots para a Aula 8.

- [ ] **Step 3: Validar e renderizar**

~~~bash
.venv/bin/python -m scripts.aulas.cli validar --manifesto .interno/prof/aulas/2026-2/u1_a07/selecao.yaml --grafo .interno/prof/refs/mapas/grafo_referencias.json
.venv/bin/python -m scripts.aulas.cli renderizar --manifesto .interno/prof/aulas/2026-2/u1_a07/selecao.yaml --grafo .interno/prof/refs/mapas/grafo_referencias.json --saida .interno/prof/aulas/2026-2/u1_a07/dossie.md
~~~

Expected: manifesto válido e dossiê sem ciclos ou aplicações.

- [ ] **Step 4: Portão docente do manifesto**

Apresente tópicos, referências, exclusões e recursos recomendados. Pare. Após aprovação explícita, marque decisões e estado aprovado, regenere o dossiê e execute validar --exigir-aprovado.

### Task 7: Gerar e aprovar a aula conceitual u1_a07

**Files:**
- Create: .interno/prof/aulas/2026-2/u1_a07/rascunho.md
- Replace after approval: aulas/u1_a07.md

- [ ] **Step 1: Escrever o rascunho**

Organize por medidas de posição, quantis, dispersão e aproximações agrupadas. Preserve fórmulas e notação do guia, numeradas 7.1, 7.2, ...; defina apenas variáveis ainda não apresentadas. Use o exemplo mínimo de Q3 somente para esclarecer p=j/m, H_p, i e d.

Não transfira os blocos Implementação manual, Implementação com biblioteca, Aplicação, Visualização ou comparações empíricas. Termine com:

~~~markdown
## Notebook da aula

As medidas serão calculadas e comparadas com a massa corporal dos pinguins no
[notebook da Aula 7](../notebooks/u1_a07.ipynb).
~~~

- [ ] **Step 2: Revisar automaticamente**

~~~bash
rg -n '~~~python|import pandas|import numpy|matplotlib|seaborn|Series\.|DataFrame|Aplicação no notebook|ciclo' .interno/prof/aulas/2026-2/u1_a07/rascunho.md
rg -n '^## Notebook da aula$|\.\./notebooks/u1_a07\.ipynb' .interno/prof/aulas/2026-2/u1_a07/rascunho.md
~~~

Expected: primeira busca sem ocorrências; segunda com uma seção e um vínculo.

- [ ] **Step 3: Portão docente da aula**

Apresente síntese e diff contra aulas/u1_a07.md. Pare. Após aprovação explícita, substitua o público, valide novamente e remova o rascunho promovido.

- [ ] **Step 4: Commit da aula**

~~~bash
git add aulas/u1_a07.md
git commit -m "docs: publicar aula 7 conceitual"
~~~

### Task 8: Planejar as atividades do notebook da Aula 7

**Files:**
- Create: .interno/prof/aulas/2026-2/u1_a07/notebook.yaml
- Read: .interno/prof/guia/aula7_medidas_estatisticas.md
- Read: data/processed/penguins.csv

- [ ] **Step 1: Criar o plano 2.0 em planejamento**

Use a fonte https://raw.githubusercontent.com/carubbi/MQ/main/data/processed/penguins.csv. Autorize pandas, numpy, scipy e matplotlib. Preserve 344 linhas, 342 massas observadas e duas ausências.

Defina:

1. atividade-01: média, mediana e moda; amostra Adelie original versus cópia com 8000 g.
2. atividade-02: quantis e IQR; cálculo manual, NumPy e pandas com interpolação linear e curva acumulada.
3. atividade-03: amplitude, variância amostral, desvio-padrão e CV; comparação entre espécies.
4. atividade-04: aproximações por classes; pontos médios, medidas aproximadas, classe mediana, classes modais e comparação com dados individuais.

Cubra os nove tópicos. Use origem autoral com justificativa de adaptação das aplicações aprovadas no guia docente.

Distribua as operações do guia nesta ordem: carregamento e remoção de ausências; funções auxiliares; funções manuais; equivalentes de biblioteca; aplicação numérica; visualização; comparação final. Use IDs r01, r02, ... sem repetição. Cada bloco Python do guia incorporado ao plano deve ser copiado integralmente para codigo; resultados executados determinam quantidade, tipos_nbformat e contem antes da apresentação docente.

- [ ] **Step 2: Validar o plano em planejamento**

~~~bash
.venv/bin/python -c 'import sys; from pathlib import Path; sys.path.insert(0, "/Users/carubbi/.codex/skills/gerar-notebooks-aula/scripts"); from contrato_notebook import carregar_plano; carregar_plano(Path(".interno/prof/aulas/2026-2/u1_a07/notebook.yaml"))'
~~~

Expected: exit 0.

- [ ] **Step 3: Portão docente do plano**

Apresente dados, atividades, cobertura, operações, código e saídas. Pare. Após aprovação explícita, altere somente estado para aprovado e valide com exigir_aprovado=True.

### Task 9: Gerar e validar os notebooks pareados

**Files:**
- Create after approval: notebooks/u1_a07.ipynb
- Create after approval: notebooks/resolvidos/u1_a07.ipynb

- [ ] **Step 1: Executar a suíte do gerador**

~~~bash
.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -v
~~~

Expected: PASS.

- [ ] **Step 2: Gerar e executar em diretório temporário**

Crie a raiz com mktemp -d. Execute gerar_notebooks.py conforme fluxo-geracao.md, usando plano aprovado, cabeçalho canônico e --cwd /Users/carubbi/projects/MQ.

Expected: discente vazio e não executado; resolvido executado sem erro.

- [ ] **Step 3: Validar o par temporário**

Execute validar_notebooks.py com manifesto, aula, cabeçalho e arquivos temporários.

Expected: “notebooks válidos” e exit 0.

- [ ] **Step 4: Comparar e promover conjuntamente**

Use git diff --no-index separadamente. Se não houver edição pública ausente do plano, copie os dois arquivos e repita a validação pública.

- [ ] **Step 5: Verificar ausência estrutural de ciclos**

~~~bash
rg -n 'ciclo-|Ciclo [0-9]|ciclos didáticos' notebooks/u1_a07.ipynb notebooks/resolvidos/u1_a07.ipynb
~~~

Expected: nenhuma ocorrência.

- [ ] **Step 6: Commit dos notebooks**

~~~bash
git add notebooks/u1_a07.ipynb notebooks/resolvidos/u1_a07.ipynb
git commit -m "feat: publicar notebooks aplicados da aula 7"
~~~

### Task 10: Auditar e encerrar o piloto

**Files:**
- Verify: scripts/aulas/
- Verify: tests/aulas/
- Verify: /Users/carubbi/.codex/skills/curar-aula-formal/
- Verify: /Users/carubbi/.codex/skills/gerar-aula-formal/
- Verify: /Users/carubbi/.codex/skills/gerar-notebooks-aula/
- Verify: aulas/u1_a07.md
- Verify: notebooks/u1_a07.ipynb
- Verify: notebooks/resolvidos/u1_a07.ipynb

- [ ] **Step 1: Executar validações completas**

~~~bash
.venv/bin/python -m unittest discover -s tests/aulas -v
.venv/bin/python -m unittest discover -s /Users/carubbi/.codex/skills/gerar-notebooks-aula/tests -v
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/curar-aula-formal
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-aula-formal
python /Users/carubbi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/carubbi/.codex/skills/gerar-notebooks-aula
~~~

Expected: suítes e skills válidas.

- [ ] **Step 2: Validar os artefatos públicos**

Execute o CLI de curadoria com --exigir-aprovado e validar_notebooks.py contra os caminhos públicos.

Expected: manifesto válido e notebooks válidos.

- [ ] **Step 3: Revisar escopo**

~~~bash
git diff --check
git status --short
git log --oneline -8
~~~

Confirme que nenhuma aula ou notebook anterior foi migrado e que alterações preexistentes do usuário não entraram nos commits.

- [ ] **Step 4: Solicitar validação docente final**

Apresente os caminhos da Aula 7, os resultados dos testes e as pendências. Pare antes de migrar qualquer outra aula.
