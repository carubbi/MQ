"""Contrato do par de notebooks integrais da Aula 2."""

from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[2]
STUDENT = ROOT / "notebooks/u1_a02.ipynb"
SOLVED = ROOT / "notebooks/resolvidos/u1_a02.ipynb"

TITLE = "# Aula 2 — Fundamentos estatísticos e investigação com dados"
SECTIONS = (
    "## 3. Pergunta estatística e preparação dos dados",
    "## 4. Investigação estatística e variabilidade",
    "## 5. População, amostra, representatividade e vieses",
    "## 6. Descrição, inferência e alcance das conclusões",
    "## 7. Síntese",
    "## 8. Estudo e exercícios",
    "## 9. Referências",
)


class NotebookAula2IntegralTest(unittest.TestCase):
    def _read(self, path: Path):
        self.assertTrue(path.is_file(), f"arquivo ausente: {path}")
        return nbformat.read(path, as_version=4)

    @staticmethod
    def _cells(notebook, cell_type: str):
        return [cell for cell in notebook.cells if cell.cell_type == cell_type]

    @staticmethod
    def _markdown(notebook) -> str:
        return "\n".join(
            cell.source
            for cell in notebook.cells
            if cell.cell_type == "markdown"
        )

    def test_estrutura_compartilhada_sem_ciclos(self) -> None:
        student = self._read(STUDENT)
        solved = self._read(SOLVED)

        self.assertEqual(len(student.cells), 58)
        self.assertEqual(len(solved.cells), 58)
        self.assertEqual(
            [(cell.id, cell.cell_type) for cell in student.cells],
            [(cell.id, cell.cell_type) for cell in solved.cells],
        )
        for notebook in (student, solved):
            markdown = self._markdown(notebook)
            self.assertIn(TITLE, markdown)
            self.assertIn("## 1. Objetivos de aprendizagem", markdown)
            self.assertIn("## 2. Agenda", markdown)
            for section in SECTIONS:
                self.assertIn(section, markdown)
            self.assertNotRegex(markdown, r"(?i)\bciclo(?:s)? didático")
            self.assertNotRegex(markdown, r"(?m)^## Ciclo \d+")

    def test_roteiro_de_sala_nao_executado(self) -> None:
        notebook = self._read(STUDENT)
        code = self._cells(notebook, "code")

        self.assertEqual(len(code), 16)
        self.assertTrue(all(cell.source.strip() for cell in code))
        self.assertTrue(all(cell.execution_count is None for cell in code))
        self.assertTrue(all(cell.outputs == [] for cell in code))
        self.assertNotIn("**Resposta:**", self._markdown(notebook))
        for cell in code:
            ast.parse(cell.source)

    def test_resolucao_executada_sem_erros(self) -> None:
        notebook = self._read(SOLVED)
        code = self._cells(notebook, "code")

        self.assertEqual(len(code), 16)
        self.assertEqual(
            [cell.execution_count for cell in code],
            list(range(1, 17)),
        )
        self.assertFalse(
            any(
                output.output_type == "error"
                for cell in code
                for output in cell.outputs
            )
        )
        for cell in code:
            self.assertTrue(cell.source.lstrip().startswith("# "))
            ast.parse(cell.source)

    def test_figuras_locais_existem(self) -> None:
        for path in (STUDENT, SOLVED):
            notebook = self._read(path)
            markdown = self._markdown(notebook)
            sources = re.findall(r"!\[[^]]*\]\(([^)]+)\)", markdown)
            local_sources = [
                source
                for source in sources
                if not source.startswith(("http://", "https://"))
            ]
            self.assertEqual(len(local_sources), 2)
            for source in local_sources:
                self.assertTrue(
                    (path.parent / source).resolve().is_file(),
                    f"imagem ausente em {path.name}: {source}",
                )


if __name__ == "__main__":
    unittest.main()
