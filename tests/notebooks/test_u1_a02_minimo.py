"""Contrato dos notebooks mínimo e resolvido da Aula 2."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "notebooks/u1_a01.ipynb"
STUDENT = ROOT / "notebooks/u1_a02.ipynb"
SOLVED = ROOT / "notebooks/resolvidos/u1_a02.ipynb"

TITLE = "# Aula 2 — Fundamentos estatísticos e investigação com dados"
SECTIONS = (
    "## Carregamento do conjunto de dados",
    "## Ciclo 1 — reconhecer a variabilidade",
    "## Ciclo 2 — comparar descrição amostral e populacional",
    "## Ciclo 3 — delimitar população, amostra e unidades",
    "## Ciclo 4 — comparar amostragem aleatória e por conveniência",
)


class NotebookAula2MinimoTest(unittest.TestCase):
    def _read(self, path: Path):
        self.assertTrue(path.is_file(), f"arquivo ausente: {path}")
        return nbformat.read(path, as_version=4)

    @staticmethod
    def _cells(notebook, cell_type: str):
        return [
            cell for cell in notebook.cells if cell.cell_type == cell_type
        ]

    @staticmethod
    def _output_text(output) -> str:
        if output.output_type == "stream":
            return output.text
        text = output.get("data", {}).get("text/plain", "")
        if isinstance(text, list):
            return "".join(text)
        return text

    @staticmethod
    def _section_code_counts(notebook) -> tuple[int, ...]:
        counts: list[int] = []
        current: int | None = None
        for cell in notebook.cells:
            if cell.cell_type == "markdown" and cell.source in SECTIONS:
                counts.append(0)
                current = len(counts) - 1
            elif cell.cell_type == "code" and current is not None:
                counts[current] += 1
        return tuple(counts)

    def test_notebook_discente(self) -> None:
        base = self._read(BASE)
        notebook = self._read(STUDENT)
        markdown = self._cells(notebook, "markdown")
        code = self._cells(notebook, "code")

        self.assertEqual(len(notebook.cells), 12)
        self.assertEqual(len(markdown), 7)
        self.assertEqual(len(code), 5)
        self.assertEqual(markdown[0].source, base.cells[0].source)
        self.assertEqual(markdown[0].id, base.cells[0].id)
        self.assertEqual(markdown[1].source, TITLE)
        self.assertEqual(tuple(cell.source for cell in markdown[2:]), SECTIONS)
        self.assertEqual(self._section_code_counts(notebook), (1, 1, 1, 1, 1))
        for cell in code:
            self.assertEqual(cell.source, "")
            self.assertIsNone(cell.execution_count)
            self.assertEqual(cell.outputs, [])

    def test_notebook_resolvido(self) -> None:
        base = self._read(BASE)
        notebook = self._read(SOLVED)
        markdown = self._cells(notebook, "markdown")
        code = self._cells(notebook, "code")

        self.assertEqual(len(notebook.cells), 25)
        self.assertEqual(len(markdown), 7)
        self.assertEqual(len(code), 18)
        self.assertEqual(markdown[0].source, base.cells[0].source)
        self.assertEqual(markdown[0].id, base.cells[0].id)
        self.assertEqual(markdown[1].source, TITLE)
        self.assertEqual(tuple(cell.source for cell in markdown[2:]), SECTIONS)
        self.assertEqual(self._section_code_counts(notebook), (2, 4, 3, 5, 4))
        self.assertTrue(all(cell.source.strip() for cell in code))
        self.assertEqual(
            [cell.execution_count for cell in code],
            list(range(1, 19)),
        )
        self.assertFalse(
            any(
                output.output_type == "error"
                for cell in code
                for output in cell.outputs
            )
        )

    def test_markdown_compartilhado(self) -> None:
        student = self._read(STUDENT)
        solved = self._read(SOLVED)
        student_markdown = self._cells(student, "markdown")
        solved_markdown = self._cells(solved, "markdown")

        self.assertEqual(
            [(cell.id, cell.source) for cell in student_markdown],
            [(cell.id, cell.source) for cell in solved_markdown],
        )

    def test_codigo_resolvido_simples(self) -> None:
        notebook = self._read(SOLVED)
        code = self._cells(notebook, "code")
        forbidden_names = {"df", "x", "tmp", "aa"}

        for cell in code:
            self.assertNotIn(";", cell.source)
            tree = ast.parse(cell.source)
            self.assertFalse(
                any(
                    isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Lambda))
                    for node in ast.walk(tree)
                )
            )
            self.assertFalse(
                any(
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Call)
                    for node in ast.walk(tree)
                )
            )
            assigned = {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
            }
            self.assertTrue(forbidden_names.isdisjoint(assigned))
            imports = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            self.assertTrue(imports.issubset({"pandas"}))

    def test_cada_celula_resolvida_comeca_com_um_comentario(self) -> None:
        notebook = self._read(SOLVED)
        code = self._cells(notebook, "code")

        for cell in code:
            lines = [line.strip() for line in cell.source.splitlines()]
            comments = [line for line in lines if line.startswith("# ")]
            self.assertTrue(lines[0].startswith("# "))
            self.assertEqual(len(comments), 1)

    def test_saidas_resolvidas(self) -> None:
        notebook = self._read(SOLVED)
        code = self._cells(notebook, "code")
        no_output = {0, 6, 14, 15}

        for index, cell in enumerate(code):
            expected = 0 if index in no_output else 1
            self.assertEqual(len(cell.outputs), expected)

        self.assertEqual(code[1].outputs[0].output_type, "stream")
        info = self._output_text(code[1].outputs[0])
        for column in (
            "studyName",
            "Individual ID",
            "Species",
            "Island",
            "Body Mass (g)",
        ):
            self.assertIn(column, info)

        scalar_text = "\n".join(
            self._output_text(cell.outputs[0])
            for index, cell in enumerate(code)
            if index not in no_output and index not in {16, 17}
        )
        for expected in (
            "342",
            "2700.0",
            "6300.0",
            "94",
            "4201.754385964912",
            "4177.5",
            "344",
            "30",
            "pinguim",
            "registro de um pinguim",
        ):
            self.assertIn(expected, scalar_text)

        random_counts = self._output_text(code[16].outputs[0])
        convenience_counts = self._output_text(code[17].outputs[0])
        self.assertIn("Gentoo penguin", random_counts)
        self.assertIn("Adelie Penguin", random_counts)
        self.assertIn("Chinstrap penguin", random_counts)
        self.assertIn("12", random_counts)
        self.assertIn("6", random_counts)
        self.assertIn("Adelie Penguin", convenience_counts)
        self.assertIn("30", convenience_counts)


if __name__ == "__main__":
    unittest.main()
