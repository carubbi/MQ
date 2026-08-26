import copy
import tempfile
import unittest
from pathlib import Path

from scripts.aulas.manifesto import dump_manifest, load_manifest, validate_manifest
from tests.aulas.fixtures import GRAPH, VALID_MANIFEST, approved_manifest


class ManifestValidationTests(unittest.TestCase):
    def test_accepts_approved_contract_1_1_manifest(self):
        self.assertEqual(
            [],
            validate_manifest(approved_manifest(), GRAPH, require_approved=True),
        )

    def test_rejects_contract_1_0(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["versao_contrato"] = "1.0"

        findings = validate_manifest(manifest, GRAPH)

        self.assertTrue(
            any("'1.1' was expected" in finding for finding in findings),
            findings,
        )

    def test_rejects_missing_time_plan(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        del manifest["planejamento_tempo"]

        findings = validate_manifest(manifest, GRAPH)

        self.assertTrue(
            any(
                "'planejamento_tempo' is a required property" in finding
                for finding in findings
            ),
            findings,
        )

    def test_rejects_cycle_without_temporal_metadata(self):
        manifest = approved_manifest()
        del manifest["ciclos"][0]["complexidade"]
        del manifest["ciclos"][0]["duracao_minima_minutos"]
        del manifest["ciclos"][0]["justificativa_particao"]

        findings = validate_manifest(manifest, GRAPH)

        self.assertTrue(
            any("'complexidade' is a required property" in item for item in findings)
        )
        self.assertTrue(
            any(
                "'duracao_minima_minutos' is a required property" in item
                for item in findings
            )
        )
        self.assertTrue(
            any(
                "'justificativa_particao' is a required property" in item
                for item in findings
            )
        )

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
