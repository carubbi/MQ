import copy
import tempfile
import unittest
from pathlib import Path

from scripts.aulas.manifesto import dump_manifest, load_manifest, validate_manifest
from tests.aulas.fixtures import GRAPH, VALID_MANIFEST, approved_manifest


class ManifestValidationTests(unittest.TestCase):
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

    def test_rejects_legacy_cycles_field(self):
        manifest = approved_manifest()
        manifest["ciclos"] = []

        findings = validate_manifest(manifest, GRAPH)
        self.assertTrue(any("Additional properties" in item for item in findings))

    def test_allows_selected_topic_without_cycle_during_selection(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["topicos"][0]["estado"] = "selecionado"
        reference = manifest["topicos"][0]["referencias"][0]
        reference["estado"] = "selecionada"
        reference["papeis"] = ["fundamentacao"]

        self.assertEqual([], validate_manifest(manifest, GRAPH))

    def test_accepts_approved_manifest_without_cycles(self):
        self.assertEqual(
            [],
            validate_manifest(approved_manifest(), GRAPH, require_approved=True),
        )

    def test_rejects_contract_1_1(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["versao_contrato"] = "1.1"

        findings = validate_manifest(manifest, GRAPH)

        self.assertTrue(
            any("'2.0' was expected" in finding for finding in findings),
            findings,
        )

    def test_approved_manifest_requires_student_resources(self):
        manifest = approved_manifest()
        del manifest["recursos_discentes"]

        findings = validate_manifest(manifest, GRAPH, require_approved=True)

        self.assertTrue(
            any(
                "'recursos_discentes' is a required property" in finding
                for finding in findings
            ),
            findings,
        )

    def test_selection_manifest_may_omit_student_resources(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        del manifest["recursos_discentes"]

        self.assertEqual([], validate_manifest(manifest, GRAPH))

    def test_accepts_empty_student_resource_lists(self):
        manifest = approved_manifest()
        manifest["recursos_discentes"] = {
            "materiais_didaticos": [],
            "exercicios_indicados": [],
        }

        self.assertEqual(
            [],
            validate_manifest(manifest, GRAPH, require_approved=True),
        )

    def test_rejects_unknown_student_resource(self):
        manifest = approved_manifest()
        manifest["recursos_discentes"]["materiais_didaticos"] = [
            {"id": "ausente"}
        ]

        self.assertIn(
            "recurso discente desconhecido: ausente",
            validate_manifest(manifest, GRAPH),
        )

    def test_rejects_resource_type_in_wrong_list(self):
        manifest = approved_manifest()
        manifest["recursos_discentes"]["materiais_didaticos"] = [
            {"id": "questao-populacao"}
        ]

        self.assertIn(
            "recurso questao-populacao do tipo questao é inválido em "
            "materiais_didaticos",
            validate_manifest(manifest, GRAPH),
        )

    def test_rejects_material_type_in_exercise_list(self):
        manifest = approved_manifest()
        manifest["recursos_discentes"]["exercicios_indicados"] = [
            {"id": "secao-populacao"}
        ]

        self.assertIn(
            "recurso secao-populacao do tipo secao é inválido em "
            "exercicios_indicados",
            validate_manifest(manifest, GRAPH),
        )

    def test_accepts_chapter_related_through_contained_section(self):
        self.assertEqual([], validate_manifest(approved_manifest(), GRAPH))

    def test_rejects_resource_without_pages(self):
        graph = copy.deepcopy(GRAPH)
        chapter = next(
            node
            for node in graph["nos"]
            if node["id"] == "capitulo-fundamentos"
        )
        del chapter["pagina_pdf_inicio"]
        del chapter["pagina_pdf_fim"]

        self.assertIn(
            "recurso capitulo-fundamentos não possui páginas verificáveis",
            validate_manifest(approved_manifest(), graph),
        )

    def test_rejects_resource_without_source_ancestor(self):
        graph = copy.deepcopy(GRAPH)
        graph["relacoes"] = [
            edge
            for edge in graph["relacoes"]
            if not (
                edge["origem"] == "fonte-a"
                and edge["tipo"] == "contem"
                and edge["destino"] == "capitulo-fundamentos"
            )
        ]

        self.assertIn(
            "recurso capitulo-fundamentos não pertence a uma fonte",
            validate_manifest(approved_manifest(), graph),
        )

    def test_rejects_resource_unrelated_to_selected_topics(self):
        graph = copy.deepcopy(GRAPH)
        graph["relacoes"] = [
            edge
            for edge in graph["relacoes"]
            if not (
                edge["origem"] == "questao-populacao"
                and edge["tipo"] == "aborda"
            )
        ]

        self.assertIn(
            "recurso questao-populacao não aborda tópico selecionado da aula",
            validate_manifest(approved_manifest(), graph),
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

    def test_invalid_time_plan_is_reported_without_semantic_crash(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        manifest["planejamento_tempo"] = "inválido"

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
