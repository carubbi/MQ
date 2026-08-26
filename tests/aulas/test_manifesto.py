import copy
import tempfile
import unittest
from pathlib import Path

from scripts.aulas.manifesto import dump_manifest, load_manifest, validate_manifest
from tests.aulas.fixtures import GRAPH, VALID_MANIFEST


class ManifestValidationTests(unittest.TestCase):
    def test_accepts_complete_manifest_in_selection(self):
        self.assertEqual([], validate_manifest(VALID_MANIFEST, GRAPH))

    def test_rejects_unknown_topic(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["topicos"][0]["id"] = "topico-inexistente"

        self.assertIn(
            "tópico desconhecido: topico-inexistente",
            validate_manifest(manifest, GRAPH),
        )

    def test_rejects_reference_without_explicit_topic_relation(self):
        graph = copy.deepcopy(GRAPH)
        graph["relacoes"] = [
            edge for edge in graph["relacoes"] if edge["tipo"] != "aborda"
        ]

        self.assertIn(
            "referência secao-populacao não aborda topico-populacao",
            validate_manifest(VALID_MANIFEST, graph),
        )

    def test_rejects_pages_outside_reference_interval(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        reference = manifest["topicos"][0]["referencias"][0]
        reference["paginas_pdf"]["fim"] = 13

        self.assertIn(
            "páginas fora do intervalo de secao-populacao: 10-13",
            validate_manifest(manifest, GRAPH),
        )

    def test_approved_manifest_rejects_pending_decisions(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["estado"] = "aprovado"

        self.assertIn(
            "manifesto aprovado contém tópico pendente: topico-populacao",
            validate_manifest(manifest, GRAPH, require_approved=True),
        )

    def test_selected_topic_requires_fundamentation_reference(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["estado"] = "aprovado"
        topic = manifest["topicos"][0]
        topic["estado"] = "selecionado"
        reference = topic["referencias"][0]
        reference["estado"] = "selecionada"
        reference["papeis"] = ["complementar"]

        self.assertIn(
            "tópico selecionado sem referência de fundamentação: "
            "topico-populacao",
            validate_manifest(manifest, GRAPH, require_approved=True),
        )

    def test_structural_error_is_reported_without_semantic_crash(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["aula"] = "inválida"

        findings = validate_manifest(manifest, GRAPH)

        self.assertTrue(any(item.startswith("schema: ") for item in findings))


class ManifestSerializationTests(unittest.TestCase):
    def test_dump_and_load_preserve_manifest(self):
        serialized = dump_manifest(VALID_MANIFEST)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "selecao.yaml"
            path.write_text(serialized, encoding="utf-8")

            self.assertEqual(VALID_MANIFEST, load_manifest(path))

    def test_load_rejects_non_mapping_yaml(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "selecao.yaml"
            path.write_text("- item\n", encoding="utf-8")

            with self.assertRaisesRegex(
                ValueError,
                "manifesto deve ser um objeto YAML",
            ):
                load_manifest(path)


if __name__ == "__main__":
    unittest.main()
