import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.teaching_mockups import (
    build_notebook_mockup,
    validate_aula_mockup,
    validate_notebook_mockup,
)


ROOT = Path(__file__).resolve().parents[2]
GRAPH = json.loads(
    (ROOT / "prof/refs/mapas/grafo_referencias.json").read_text(encoding="utf-8")
)
HEAD_TEXT = (
    ROOT / "mat/notebooks/assets/heads/head_unifor.md"
).read_text(encoding="utf-8")
SCRIPT = ROOT / "scripts/grafo_refs/teaching_mockups.py"

VALID_AULA = """# Organização e representação de dados

- **Disciplina:** T199 — Métodos Quantitativos
- **Unidade:** I
- **Semana:** 3
- **Data:** 21/08/2026
- **Conteúdos formais:** `01.02`
- **Tópicos:** Importação de dados; Pré-processamento; Tipos de variáveis
- **Resultado de aprendizagem:** organizar dados e justificar decisões.

---
"""


class TeachingMockupTests(unittest.TestCase):
    def test_accepts_exact_aula_mockup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aula.md"
            path.write_text(VALID_AULA, encoding="utf-8")
            findings = validate_aula_mockup(path, GRAPH)
        self.assertEqual([], findings)

    def test_rejects_extra_section_in_aula_mockup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aula.md"
            path.write_text(
                VALID_AULA + "\n## Agenda\nConteúdo.\n",
                encoding="utf-8",
            )
            findings = validate_aula_mockup(path, GRAPH)
        self.assertIn("conteúdo adicional no mockup", findings)

    def test_rejects_unknown_topic_and_content(self):
        invalid = VALID_AULA.replace("`01.02`", "`99.99`").replace(
            "Importação de dados",
            "Tópico inexistente",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aula.md"
            path.write_text(invalid, encoding="utf-8")
            findings = validate_aula_mockup(path, GRAPH)
        self.assertIn("conteúdo curricular desconhecido: 99.99", findings)
        self.assertIn("tópico desconhecido: Tópico inexistente", findings)

    def test_builds_one_cell_notebook_from_head(self):
        notebook = build_notebook_mockup(HEAD_TEXT)
        self.assertEqual(1, len(notebook["cells"]))
        self.assertEqual("markdown", notebook["cells"][0]["cell_type"])
        self.assertEqual(
            HEAD_TEXT,
            "".join(notebook["cells"][0]["source"]),
        )
        self.assertEqual(4, notebook["nbformat"])
        self.assertEqual(5, notebook["nbformat_minor"])

    def test_accepts_valid_notebook_mockup(self):
        notebook = build_notebook_mockup(HEAD_TEXT)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mockup.ipynb"
            path.write_text(
                json.dumps(notebook, ensure_ascii=False, indent=1),
                encoding="utf-8",
            )
            findings = validate_notebook_mockup(path, HEAD_TEXT)
        self.assertEqual([], findings)

    def test_rejects_code_or_second_cell_in_notebook_mockup(self):
        notebook = build_notebook_mockup(HEAD_TEXT)
        notebook["cells"].append(
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [],
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mockup.ipynb"
            path.write_text(
                json.dumps(notebook, ensure_ascii=False, indent=1),
                encoding="utf-8",
            )
            findings = validate_notebook_mockup(path, HEAD_TEXT)
        self.assertIn(
            "mockup deve conter uma única célula Markdown",
            findings,
        )

    def test_rejects_head_content_difference(self):
        notebook = build_notebook_mockup(HEAD_TEXT + "\nTexto adicional.\n")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mockup.ipynb"
            path.write_text(
                json.dumps(notebook, ensure_ascii=False, indent=1),
                encoding="utf-8",
            )
            findings = validate_notebook_mockup(path, HEAD_TEXT)
        self.assertIn("cabeçalho do notebook divergente", findings)

    def test_complete_t199_resource_inventory(self):
        expected_materials = {
            "u1_s01_fundamentos_estatisticos.md",
            "u1_s03_organizacao_representacao_dados.md",
            "u1_s04_analise_univariada.md",
            "u1_s05_analise_bivariada.md",
            "u1_s06_probabilidade.md",
            "u2_s01_revisao_at1.md",
            "u2_s02_variaveis_aleatorias.md",
            "u2_s03_distribuicoes_discretas.md",
            "u2_s04_distribuicoes_continuas.md",
            "u2_s05_normal_auditoria_modelos.md",
            "u2_s06_revisao_at2.md",
            "u3_s01_amostragem_distribuicoes_amostrais.md",
            "u3_s02_estimacao_testes.md",
            "u3_s03_regressao_linear_simples.md",
            "u3_s05_regressao_simples_multipla.md",
            "u3_s06_revisao_at3.md",
        }
        expected_notebooks = {
            "u1_s01_fundamentos_estatisticos_aula01.ipynb",
            "u1_s01_fundamentos_estatisticos_aula02.ipynb",
            "u1_s03_organizacao_representacao_dados.ipynb",
            "u1_s04_analise_univariada.ipynb",
            "u1_s05_analise_bivariada.ipynb",
            "u1_s06_probabilidade.ipynb",
            "u2_s02_variaveis_aleatorias.ipynb",
            "u2_s03_distribuicoes_discretas.ipynb",
            "u2_s04_distribuicoes_continuas.ipynb",
            "u2_s05_normal_auditoria_modelos.ipynb",
            "u3_s01_amostragem_distribuicoes_amostrais.ipynb",
            "u3_s02_estimacao_testes.ipynb",
            "u3_s03_regressao_linear_simples.ipynb",
            "u3_s05_regressao_simples_multipla.ipynb",
        }

        materials_dir = ROOT / "mat/aulas"
        notebooks_dir = ROOT / "mat/notebooks"
        actual_materials = {
            path.name for path in materials_dir.glob("u*_s*.md")
        }
        actual_notebooks = {
            path.name for path in notebooks_dir.glob("u*_s*.ipynb")
        }

        self.assertEqual(expected_materials, actual_materials)
        self.assertEqual(expected_notebooks, actual_notebooks)

        for name in sorted(expected_materials - {
            "u1_s01_fundamentos_estatisticos.md"
        }):
            self.assertEqual(
                [],
                validate_aula_mockup(materials_dir / name, GRAPH),
                name,
            )
        for name in sorted(expected_notebooks - {
            "u1_s01_fundamentos_estatisticos_aula01.ipynb",
            "u1_s01_fundamentos_estatisticos_aula02.ipynb",
        }):
            self.assertEqual(
                [],
                validate_notebook_mockup(
                    notebooks_dir / name,
                    HEAD_TEXT,
                ),
                name,
            )

    def test_cli_refuses_to_overwrite_existing_notebook(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            head = root / "head.md"
            existing = root / "existing.ipynb"
            fresh = root / "fresh.ipynb"
            head.write_text(HEAD_TEXT, encoding="utf-8")
            existing.write_text("preservar", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--head",
                    str(head),
                    "--create-notebook",
                    str(existing),
                    "--create-notebook",
                    str(fresh),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, completed.returncode)
            self.assertIn("arquivo já existe", completed.stderr)
            self.assertEqual(
                "preservar",
                existing.read_text(encoding="utf-8"),
            )
            self.assertFalse(fresh.exists())


if __name__ == "__main__":
    unittest.main()
