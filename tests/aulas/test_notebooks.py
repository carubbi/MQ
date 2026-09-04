"""Testes da validação conjunta dos notebooks de sala e resolvido."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import nbformat

from scripts.aulas.estrutura import approve_structure, mark_published
from scripts.aulas.notebooks import load_notebook, validate_notebook_pair
from tests.aulas.test_estrutura import manifest, structure_body, structure_metadata


def notebook_markdown() -> str:
    return (
        "# Aula 5 — Tipos, qualidade e pré-processamento básico\n\n"
        "## 1. Objetivos de aprendizagem\n\n"
        "Ao final da aula, o aluno será capaz de:\n\n"
        "- classificar variáveis.\n\n"
        "## 2. Agenda\n\n"
        "1. Conteúdo — 95 min\n"
        "2. Estudo e exercícios — 5 min\n\n"
        "## 3. Conteúdo\n\n"
        "### 3.1 Conceito\n\n"
        "Texto discente.\n\n"
        "## 4. Estudo e exercícios\n\n"
        "Atividades.\n\n"
        "## 5. Referências\n\n"
        "Referência."
    )


def room_notebook(header: str):
    return nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell(header, id="cabecalho"),
            nbformat.v4.new_markdown_cell(notebook_markdown(), id="conteudo"),
            nbformat.v4.new_code_cell(
                "# Exibe um valor\nvalor = 2\nvalor",
                id="codigo",
                execution_count=None,
                outputs=[],
            ),
        ]
    )


def solved_notebook(header: str):
    notebook = room_notebook(header)
    notebook.cells[2].execution_count = 1
    notebook.cells[2].outputs = [
        nbformat.v4.new_output(
            "execute_result",
            data={"text/plain": "2"},
            execution_count=1,
        )
    ]
    return notebook


class NotebookLoadTest(unittest.TestCase):
    def test_carrega_notebook_e_hash_dos_mesmos_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notebook.ipynb"
            nbformat.write(room_notebook("<header>"), path)
            loaded, digest = load_notebook(path)
            expected = __import__("hashlib").sha256(path.read_bytes()).hexdigest()

        self.assertEqual(loaded.cells[0].source, "<header>")
        self.assertEqual(digest, expected)


class NotebookPairValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.root_directory.name)
        self.manifest = manifest()
        self.body = structure_body()
        self.metadata = approve_structure(
            structure_metadata(),
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        self.header = "<header>"
        self.room = room_notebook(self.header)
        self.solved = solved_notebook(self.header)
        self.room_hash = "0" * 64
        self.solved_hash = "1" * 64

    def tearDown(self) -> None:
        self.root_directory.cleanup()

    def validate(self) -> list[str]:
        return validate_notebook_pair(
            manifest=self.manifest,
            structure_metadata=self.metadata,
            structure_body=self.body,
            header=self.header,
            room_notebook=self.room,
            room_sha256=self.room_hash,
            solved_notebook=self.solved,
            solved_sha256=self.solved_hash,
            repository_root=self.root,
        )

    def assert_finding(self, text: str) -> None:
        findings = self.validate()
        self.assertTrue(
            any(text in finding for finding in findings),
            f"esperava achado contendo {text!r}; obtidos: {findings}",
        )

    def test_aceita_par_valido(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_exige_estrutura_aprovada(self) -> None:
        self.metadata = structure_metadata()
        self.assert_finding("aprovada ou publicada")

    def test_rejeita_cabecalho_e_titulo_divergentes(self) -> None:
        self.room.cells[0].source = "<outro>"
        self.solved.cells[1].source = self.solved.cells[1].source.replace(
            "# Aula 5", "# Aula 6"
        )
        findings = self.validate()
        self.assertTrue(any("cabeçalho" in finding for finding in findings))
        self.assertTrue(any("título" in finding for finding in findings))

    def test_rejeita_objetivos_divergentes(self) -> None:
        self.room.cells[1].source = self.room.cells[1].source.replace(
            "- classificar variáveis.", "- descrever variáveis."
        )
        self.assert_finding("objetivos do notebook de sala")

    def test_rejeita_agenda_divergente(self) -> None:
        self.solved.cells[1].source = self.solved.cells[1].source.replace(
            "Conteúdo — 95 min", "Conteúdo — 90 min"
        )
        self.assert_finding("agenda do notebook resolvido")

    def test_rejeita_hierarquia_divergente(self) -> None:
        self.room.cells[1].source = self.room.cells[1].source.replace(
            "## 3. Conteúdo", "## 3. Outro conteúdo"
        )
        self.assert_finding("hierarquia do notebook de sala")

    def test_rejeita_estrutura_diferente_entre_os_papeis(self) -> None:
        self.solved.cells[1].source = self.solved.cells[1].source.replace(
            "### 3.1 Conceito", "### 3.2 Conceito"
        )
        self.assert_finding("hierarquias dos notebooks divergem")

    def test_rejeita_roteiro_com_execucao_ou_output(self) -> None:
        self.room.cells[2].execution_count = 1
        self.room.cells[2].outputs = [
            nbformat.v4.new_output("stream", name="stdout", text="2\n")
        ]
        findings = self.validate()
        self.assertTrue(any("sem contagens" in finding for finding in findings))
        self.assertTrue(any("sem outputs" in finding for finding in findings))

    def test_rejeita_resolucao_sem_execucao_sequencial(self) -> None:
        self.solved.cells[2].execution_count = None
        self.assert_finding("contagens de execução")

    def test_rejeita_output_de_erro(self) -> None:
        self.solved.cells[2].outputs = [
            nbformat.v4.new_output(
                "error",
                ename="ValueError",
                evalue="falhou",
                traceback=[],
            )
        ]
        self.assert_finding("output de erro")

    def test_rejeita_markdown_publico_no_modo_integral(self) -> None:
        path = self.root / "aulas" / "u1_a05.md"
        path.parent.mkdir(parents=True)
        path.write_text("legado", encoding="utf-8")
        self.assert_finding("artefato incompatível")

    def test_publicada_rejeita_hash_divergente(self) -> None:
        self.metadata = mark_published(
            self.metadata,
            self.body,
            {"sala": "a" * 64, "resolvido": self.solved_hash},
            "2026-09-04T18:00:00-03:00",
        )
        self.assert_finding("hash do notebook de sala")


if __name__ == "__main__":
    unittest.main()
