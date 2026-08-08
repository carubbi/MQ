# Move Finalized Notebooks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mover os dois notebooks docentes finalizados para `mat/notebooks/resolvidos/`, preservando os materiais auxiliares e corrigindo imagens e links públicos.

**Architecture:** A promoção será manual e sob demanda, sem script permanente. O padrão `^u[1-9][0-9]*_.+\.ipynb$` determina quais notebooks em `prof/notebooks/` podem ser movidos; depois da promoção, `mat/notebooks/resolvidos/` será sua única localização canônica.

**Tech Stack:** Git, JSON de notebooks Jupyter, Markdown e Python 3 para validação.

## Global Constraints

- Mover somente as Aulas 1 e 2 presentes em `prof/notebooks/`.
- Manter `prof/notebooks/examples.ipynb` inalterado.
- Não remover, mover nem sobrescrever notebooks diretamente em `mat/notebooks/`.
- Não criar script de sincronização ou publicação.
- Usar URLs GitHub Raw nas imagens dos notebooks resolvidos.
- Atualizar somente links públicos das Aulas 1 e 2 já finalizadas.

---

### Task 1: Mover e tornar portáveis os notebooks finalizados

**Files:**
- Move: `prof/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb` → `mat/notebooks/resolvidos/u1_s01_fundamentos_estatisticos_aula01.ipynb`
- Move: `prof/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb` → `mat/notebooks/resolvidos/u1_s01_fundamentos_estatisticos_aula02.ipynb`
- Preserve: `prof/notebooks/examples.ipynb`

**Interfaces:**
- Consumes: notebooks docentes cujo nome corresponde ao padrão de unidade.
- Produces: dois notebooks JSON portáveis em `mat/notebooks/resolvidos/`.

- [ ] **Step 1: Registrar os hashes dos arquivos fora do escopo**

~~~bash
shasum prof/notebooks/examples.ipynb mat/notebooks/*.ipynb
~~~

Expected: uma linha para `examples.ipynb` e cada um dos 14 notebooks em elaboração. Guardar a saída para comparação.

- [ ] **Step 2: Validar seleção e JSON antes da movimentação**

~~~bash
python3 - <<'PY'
import json
import re
from pathlib import Path
root = Path("prof/notebooks")
pattern = re.compile(r"^u[1-9][0-9]*_.+\.ipynb$")
selected = sorted(p for p in root.glob("*.ipynb") if pattern.fullmatch(p.name))
assert [p.name for p in selected] == [
    "u1_s01_fundamentos_estatisticos_aula01.ipynb",
    "u1_s01_fundamentos_estatisticos_aula02.ipynb",
]
assert (root / "examples.ipynb").is_file()
for path in selected:
    json.loads(path.read_text(encoding="utf-8"))
print("2 notebooks selecionados; JSON válido; examples.ipynb excluído")
PY
~~~

Expected: `2 notebooks selecionados; JSON válido; examples.ipynb excluído`.

- [ ] **Step 3: Criar o destino e mover somente os dois notebooks**

~~~bash
mkdir -p mat/notebooks/resolvidos
git mv prof/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb mat/notebooks/resolvidos/u1_s01_fundamentos_estatisticos_aula01.ipynb
git mv prof/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb mat/notebooks/resolvidos/u1_s01_fundamentos_estatisticos_aula02.ipynb
~~~

Expected: dois renomes no Git; `examples.ipynb` permanece em `prof/notebooks/`.

- [ ] **Step 4: Corrigir as cinco referências relativas de imagens**

Aplicar estas substituições literais nos arquivos movidos:

- `assets/imgs/UNIFOR_logo.png` → `https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/UNIFOR_logo.png` em ambos os notebooks;
- `assets/imgs/lter_penguins.png` → `https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/lter_penguins.png` na Aula 1;
- `assets/imgs/culmen_depth.png` → `https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/culmen_depth.png` na Aula 1;
- `assets/imgs/01_table_dataframe.svg` → `https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/01_table_dataframe.svg` na Aula 1.

- [ ] **Step 5: Validar destinos, remoção das fontes e URLs**

~~~bash
python3 - <<'PY'
import json
from pathlib import Path
resolved = Path("mat/notebooks/resolvidos")
paths = sorted(resolved.glob("*.ipynb"))
assert [p.name for p in paths] == [
    "u1_s01_fundamentos_estatisticos_aula01.ipynb",
    "u1_s01_fundamentos_estatisticos_aula02.ipynb",
]
remote = "https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/"
count = 0
for path in paths:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    source = "\n".join("".join(c.get("source", [])) for c in notebook["cells"])
    assert not any("assets/imgs/" in line and remote not in line for line in source.splitlines())
    count += source.count(remote)
assert count == 5
assert Path("prof/notebooks/examples.ipynb").is_file()
assert not Path("prof/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb").exists()
assert not Path("prof/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb").exists()
print("2 notebooks resolvidos; 5 URLs externas; fontes removidas")
PY
~~~

Expected: `2 notebooks resolvidos; 5 URLs externas; fontes removidas`.

- [ ] **Step 6: Repetir o comando de hashes do Step 1**

Expected: `examples.ipynb` e os 14 notebooks em elaboração mantêm os hashes originais.

- [ ] **Step 7: Commit da movimentação**

~~~bash
git add prof/notebooks mat/notebooks/resolvidos
git commit -m "Move notebooks finalizados para materiais resolvidos"
~~~

### Task 2: Atualizar links e documentar a promoção sob demanda

**Files:**
- Create: `mat/notebooks/README.md`
- Modify: `README.md:9`
- Modify: `mat/ensino/cronograma_2026_2_t199_64_65.md:59-60`
- Modify: `prof/ensino/cronograma_2026_2_docente.md:61-62`

**Interfaces:**
- Consumes: caminhos canônicos produzidos pela Task 1.
- Produces: seis links públicos válidos e documentação da convenção manual.

- [ ] **Step 1: Demonstrar que seis links ainda apontam para a raiz**

~~~bash
rg -n 'notebooks/u1_s01_fundamentos_estatisticos_aula0[12]\.ipynb' README.md mat/ensino/cronograma_2026_2_t199_64_65.md prof/ensino/cronograma_2026_2_docente.md
~~~

Expected: seis links sem o segmento `resolvidos/`.

- [ ] **Step 2: Atualizar os destinos**

Usar `mat/notebooks/resolvidos/` no README, `../notebooks/resolvidos/` no cronograma discente e `../../mat/notebooks/resolvidos/` no cronograma docente, preservando os nomes dos dois arquivos.

- [ ] **Step 3: Criar `mat/notebooks/README.md`**

O documento deve declarar que a raiz contém notebooks em elaboração, `resolvidos/` contém os finalizados e a promoção ocorre sob demanda por `git mv`. Deve registrar o padrão `^u[1-9][0-9]*_.+\.ipynb$`, a validação JSON, a exigência de URLs GitHub Raw e a necessidade de atualizar links públicos.

- [ ] **Step 4: Validar os seis links**

~~~bash
python3 - <<'PY'
from pathlib import Path
expected = {
    Path("README.md"): "mat/notebooks/resolvidos/",
    Path("mat/ensino/cronograma_2026_2_t199_64_65.md"): "../notebooks/resolvidos/",
    Path("prof/ensino/cronograma_2026_2_docente.md"): "../../mat/notebooks/resolvidos/",
}
for path, prefix in expected.items():
    text = path.read_text(encoding="utf-8")
    for filename in (
        "u1_s01_fundamentos_estatisticos_aula01.ipynb",
        "u1_s01_fundamentos_estatisticos_aula02.ipynb",
    ):
        assert text.count(prefix + filename) == 1
print("6 links públicos válidos")
PY
~~~

Expected: `6 links públicos válidos`.

- [ ] **Step 5: Executar a verificação final**

~~~bash
python3 -m json.tool mat/notebooks/resolvidos/u1_s01_fundamentos_estatisticos_aula01.ipynb >/dev/null
python3 -m json.tool mat/notebooks/resolvidos/u1_s01_fundamentos_estatisticos_aula02.ipynb >/dev/null
test -f prof/notebooks/examples.ipynb
test ! -e prof/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb
test ! -e prof/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb
test -f mat/notebooks/u1_s01_fundamentos_estatisticos_aula01.ipynb
test -f mat/notebooks/u1_s01_fundamentos_estatisticos_aula02.ipynb
git diff --check
~~~

Expected: exit code 0 e nenhuma saída de `git diff --check`.

- [ ] **Step 6: Commit da documentação e dos links**

~~~bash
git add README.md mat/notebooks/README.md mat/ensino/cronograma_2026_2_t199_64_65.md prof/ensino/cronograma_2026_2_docente.md
git commit -m "Atualiza links dos notebooks resolvidos"
~~~
