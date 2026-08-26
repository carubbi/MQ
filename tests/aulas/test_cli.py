import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.aulas.manifesto import dump_manifest
from tests.aulas.fixtures import GRAPH, VALID_MANIFEST


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


if __name__ == "__main__":
    unittest.main()
