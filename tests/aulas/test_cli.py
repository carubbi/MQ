import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import nbformat

from scripts.aulas.estrutura import (
    approve_structure,
    dump_structure,
    semantic_sha256,
)
from scripts.aulas.manifesto import dump_manifest
from tests.aulas.fixtures import GRAPH, VALID_MANIFEST, approved_manifest


class LessonCurationCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)
        self.manifest_path = self.directory / "selecao.yaml"
        self.graph_path = self.directory / "grafo.json"
        self.dossier_path = self.directory / "artefatos" / "dossie.md"
        self.manifest_path.write_text(
            dump_manifest(VALID_MANIFEST),
            encoding="utf-8",
        )
        self.graph_path.write_text(
            json.dumps(GRAPH, ensure_ascii=False),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "scripts.aulas.cli", *arguments],
            cwd=Path(__file__).resolve().parents[2],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_render_command_writes_only_dossier(self):
        before = self.manifest_path.read_bytes()

        completed = self.run_cli(
            "renderizar",
            "--manifesto",
            str(self.manifest_path),
            "--grafo",
            str(self.graph_path),
            "--saida",
            str(self.dossier_path),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertTrue(
            self.dossier_path.read_text(encoding="utf-8").startswith(
                "# Dossiê de curadoria — u1_a02"
            )
        )
        self.assertIn(
            "## Planejamento temporal",
            self.dossier_path.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "## Recursos discentes",
            self.dossier_path.read_text(encoding="utf-8"),
        )
        self.assertEqual(before, self.manifest_path.read_bytes())

    def test_validate_command_reports_semantic_errors_without_writing(self):
        invalid_manifest = copy.deepcopy(VALID_MANIFEST)
        invalid_manifest["topicos"][0]["id"] = "topico-inexistente"
        self.manifest_path.write_text(
            dump_manifest(invalid_manifest),
            encoding="utf-8",
        )
        before = self.manifest_path.read_bytes()

        completed = self.run_cli(
            "validar",
            "--manifesto",
            str(self.manifest_path),
            "--grafo",
            str(self.graph_path),
        )

        self.assertEqual(1, completed.returncode)
        self.assertIn("tópico desconhecido", completed.stderr)
        self.assertEqual(before, self.manifest_path.read_bytes())
        self.assertFalse(self.dossier_path.exists())


class EditorialLifecycleCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.manifest = approved_manifest()
        self.manifest_path = self.root / "selecao.yaml"
        self.graph_path = self.root / "grafo.json"
        self.structure_path = self.root / "estrutura.md"
        self.header_path = self.root / "cabecalho.md"
        self.manifest_path.write_text(
            dump_manifest(self.manifest),
            encoding="utf-8",
        )
        self.graph_path.write_text(
            json.dumps(GRAPH, ensure_ascii=False),
            encoding="utf-8",
        )
        self.header_path.write_text(
            "```html\n<header>\n```\n",
            encoding="utf-8",
        )
        lesson = self.manifest["aula"]
        self.body = (
            f"# Aula {lesson['numero']} — {lesson['titulo']}\n\n"
            "## 1. Objetivos de aprendizagem\n\n"
            "Ao final da aula, o aluno será capaz de:\n\n"
            "- interpretar dados.\n\n"
            "## 2. Agenda\n\n"
            "1. Conteúdo — 100 min\n\n"
            "## 3. Conteúdo\n\n"
            "**Abordagem didática:** exemplo orientado.\n"
        )
        self.metadata = {
            "versao_contrato": "1.0",
            "estado": "em_elaboracao",
            "aula_id": lesson["id"],
            "semestre": lesson["semestre"],
            "modo_publicacao": "notebook_integral",
            "origem": {
                "manifesto": (
                    f".interno/prof/aulas/{lesson['semestre']}/"
                    f"{lesson['id']}/selecao.yaml"
                ),
                "manifesto_sha256": semantic_sha256(self.manifest),
            },
            "aprovacao": {
                "estrutura_em": None,
                "publicacao_em": None,
                "conteudo_sha256": None,
            },
            "notebooks": {
                "sala": {
                    "caminho": f"notebooks/{lesson['id']}.ipynb",
                    "sha256": None,
                },
                "resolvido": {
                    "caminho": f"notebooks/resolvidos/{lesson['id']}.ipynb",
                    "sha256": None,
                },
            },
        }
        self.structure_path.write_text(
            dump_structure(self.metadata, self.body),
            encoding="utf-8",
        )
        self._write_notebooks()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def _write_notebooks(self) -> None:
        lesson = self.manifest["aula"]
        markdown = (
            f"# Aula {lesson['numero']} — {lesson['titulo']}\n\n"
            "## 1. Objetivos de aprendizagem\n\n"
            "Ao final da aula, o aluno será capaz de:\n\n"
            "- interpretar dados.\n\n"
            "## 2. Agenda\n\n"
            "1. Conteúdo — 100 min\n\n"
            "## 3. Conteúdo\n\n"
            "Texto discente."
        )
        room = nbformat.v4.new_notebook(
            cells=[
                nbformat.v4.new_markdown_cell("<header>", id="cabecalho"),
                nbformat.v4.new_markdown_cell(markdown, id="conteudo"),
                nbformat.v4.new_code_cell(
                    "# Exibe um valor\nvalor = 2\nvalor",
                    id="codigo",
                    execution_count=None,
                    outputs=[],
                ),
            ]
        )
        solved = nbformat.from_dict(json.loads(nbformat.writes(room)))
        solved.cells[2].execution_count = 1
        solved.cells[2].outputs = [
            nbformat.v4.new_output(
                "execute_result",
                data={"text/plain": "2"},
                execution_count=1,
            )
        ]
        room_path = self.root / self.metadata["notebooks"]["sala"]["caminho"]
        solved_path = self.root / self.metadata["notebooks"]["resolvido"]["caminho"]
        room_path.parent.mkdir(parents=True)
        solved_path.parent.mkdir(parents=True)
        nbformat.write(room, room_path)
        nbformat.write(solved, solved_path)

    def run_cli(self, command: str, *extra: str) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable,
            "-m",
            "scripts.aulas.cli",
            command,
            "--manifesto",
            str(self.manifest_path),
            "--grafo",
            str(self.graph_path),
            "--estrutura",
            str(self.structure_path),
            "--raiz-repositorio",
            str(self.root),
            *extra,
        ]
        return subprocess.run(
            arguments,
            cwd=Path(__file__).resolve().parents[2],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_validar_estrutura_aceita_contrato_em_elaboracao(self) -> None:
        completed = self.run_cli("validar-estrutura")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "estrutura válida\n")

    def test_aprovar_estrutura_atualiza_somente_contrato_valido(self) -> None:
        completed = self.run_cli(
            "aprovar-estrutura",
            "--aprovado-em",
            "2026-09-04T14:00:00-03:00",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        text = self.structure_path.read_text(encoding="utf-8")
        self.assertIn("estado: aprovada", text)
        self.assertIn("estrutura aprovada\n", completed.stdout)

    def test_aprovar_estrutura_preserva_arquivo_invalido(self) -> None:
        self.structure_path.write_text("inválido\n", encoding="utf-8")
        before = self.structure_path.read_bytes()
        completed = self.run_cli(
            "aprovar-estrutura",
            "--aprovado-em",
            "2026-09-04T14:00:00-03:00",
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(self.structure_path.read_bytes(), before)

    def test_validar_notebooks_aceita_par_canonico(self) -> None:
        self.metadata = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        self.structure_path.write_text(
            dump_structure(self.metadata, self.body),
            encoding="utf-8",
        )
        completed = self.run_cli(
            "validar-notebooks",
            "--cabecalho",
            str(self.header_path),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "notebooks válidos\n")

    def test_registrar_publicacao_registra_hashes(self) -> None:
        self.metadata = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        self.structure_path.write_text(
            dump_structure(self.metadata, self.body),
            encoding="utf-8",
        )
        completed = self.run_cli(
            "registrar-publicacao",
            "--cabecalho",
            str(self.header_path),
            "--publicado-em",
            "2026-09-04T18:00:00-03:00",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        text = self.structure_path.read_text(encoding="utf-8")
        self.assertIn("estado: publicada", text)
        self.assertNotIn("sha256: null", text)
        self.assertEqual(completed.stdout, "publicação registrada\n")

    def test_registrar_publicacao_preserva_estrutura_se_par_invalido(self) -> None:
        self.metadata = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        self.structure_path.write_text(
            dump_structure(self.metadata, self.body),
            encoding="utf-8",
        )
        room_path = self.root / self.metadata["notebooks"]["sala"]["caminho"]
        room = nbformat.read(room_path, as_version=4)
        room.cells[2].execution_count = 1
        nbformat.write(room, room_path)
        before = self.structure_path.read_bytes()
        completed = self.run_cli(
            "registrar-publicacao",
            "--cabecalho",
            str(self.header_path),
            "--publicado-em",
            "2026-09-04T18:00:00-03:00",
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(self.structure_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
