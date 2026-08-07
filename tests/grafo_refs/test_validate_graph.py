import copy
import json
import unittest
from pathlib import Path

from scripts.grafo_refs.build_graph import DEFAULT_CURATED_DIRECTORY, build_graph
from scripts.grafo_refs.validate_graph import validate_graph


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "prof/refs/mapas/schema_grafo_referencias.json"


class ValidateGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.graph = build_graph("2026-08-06", REPOSITORY_ROOT / "tmp/absent-curations")

    def errors_for(self, mutate):
        graph = copy.deepcopy(self.graph)
        mutate(graph)
        return validate_graph(graph, self.schema, REPOSITORY_ROOT)

    def assert_has_error(self, errors, expected):
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_a_child_outside_its_direct_parent_interval(self):
        """Catches a section or item extending beyond its direct parent."""
        def mutate(graph):
            graph["nos"].extend(
                [
                    {
                        "id": "capitulo-a",
                        "tipo": "capitulo",
                        "pagina_pdf_inicio": 2,
                        "pagina_pdf_fim": 5,
                    },
                    {
                        "id": "secao-a",
                        "tipo": "secao",
                        "pagina_pdf_inicio": 4,
                        "pagina_pdf_fim": 6,
                        "pertinencia_t199": "indireta",
                    },
                ]
            )
            graph["relacoes"].extend(
                [
                    {
                        "origem": "barbetta-2010",
                        "tipo": "contem",
                        "destino": "capitulo-a",
                    },
                    {
                        "origem": "capitulo-a",
                        "tipo": "contem",
                        "destino": "secao-a",
                    },
                ]
            )

        errors = self.errors_for(mutate)

        self.assert_has_error(
            errors,
            "filho fora do intervalo do pai: capitulo-a -> secao-a",
        )

    def test_rejects_multi_page_overlap_between_editorial_siblings(self):
        """Catches sibling chapters or sections with a multi-page overlap."""
        def mutate(graph):
            graph["nos"].extend(
                [
                    {
                        "id": "capitulo-a",
                        "tipo": "capitulo",
                        "pagina_pdf_inicio": 2,
                        "pagina_pdf_fim": 8,
                    },
                    {
                        "id": "capitulo-b",
                        "tipo": "capitulo",
                        "pagina_pdf_inicio": 7,
                        "pagina_pdf_fim": 10,
                    },
                ]
            )
            graph["relacoes"].extend(
                [
                    {
                        "origem": "barbetta-2010",
                        "tipo": "contem",
                        "destino": "capitulo-a",
                    },
                    {
                        "origem": "barbetta-2010",
                        "tipo": "contem",
                        "destino": "capitulo-b",
                    },
                ]
            )

        errors = self.errors_for(mutate)

        self.assert_has_error(
            errors,
            "sobreposição editorial inválida: capitulo-a x capitulo-b",
        )

    def test_rejects_duplicate_node_ids(self):
        """Catches duplicate canonical identifiers."""
        errors = self.errors_for(lambda graph: graph["nos"].append(copy.deepcopy(graph["nos"][0])))
        self.assert_has_error(errors, "ID duplicado")

    def test_rejects_an_orphan_edge(self):
        """Catches a relation whose destination is not a node."""
        errors = self.errors_for(
            lambda graph: graph["relacoes"].append(
                {"origem": "conteudo-01-01", "tipo": "precede", "destino": "nao-existe"}
            )
        )
        self.assert_has_error(errors, "aresta órfã")

    def test_rejects_a_page_after_its_ancestral_pdf(self):
        """Catches page locations outside the containing source."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-cap-fora",
                    "tipo": "capitulo",
                    "numero_impresso": "99",
                    "titulo": "Fora do PDF",
                    "pagina_pdf_inicio": 413,
                    "pagina_pdf_fim": 413,
                }
            )
            graph["relacoes"].append(
                {"origem": "barbetta-2010", "tipo": "contem", "destino": "barbetta-2010-cap-fora"}
            )

        self.assert_has_error(self.errors_for(mutate), "fora do PDF")

    def test_rejects_a_reversed_pdf_page_interval(self):
        """Catches an editorial interval whose end precedes its beginning."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-cap-invertido",
                    "tipo": "capitulo",
                    "numero_impresso": "98",
                    "titulo": "Intervalo invertido",
                    "pagina_pdf_inicio": 3,
                    "pagina_pdf_fim": 2,
                }
            )
            graph["relacoes"].append(
                {"origem": "barbetta-2010", "tipo": "contem", "destino": "barbetta-2010-cap-invertido"}
            )

        self.assert_has_error(self.errors_for(mutate), "intervalo de páginas invertido")

    def test_rejects_prohibited_keys_recursively(self):
        """Catches forbidden review metadata even below arbitrary dictionaries."""
        for prohibited_key in ("dificuldade", "observacao"):
            with self.subTest(prohibited_key=prohibited_key):
                errors = self.errors_for(
                    lambda graph, key=prohibited_key: graph["metadados"].update({"aninhado": {key: "x"}})
                )
                self.assert_has_error(errors, f"chave proibida: {prohibited_key}")

    def test_rejects_a_complete_graph_with_an_uncovered_content(self):
        """Catches loss of the last reference for any completed curriculum code."""
        graph = build_graph("2026-08-06", DEFAULT_CURATED_DIRECTORY)
        graph["relacoes"] = [
            edge
            for edge in graph["relacoes"]
            if not (
                edge["tipo"] == "corresponde_a"
                and edge["destino"] == "conteudo-03-04"
            )
        ]
        errors = validate_graph(graph, self.schema, REPOSITORY_ROOT)
        self.assert_has_error(errors, "conteúdo concluído sem referência: 03.04")

    def test_rejects_curricular_relationship_without_curriculum_content(self):
        """Catches corresponde_a relations that do not target a completed content."""
        errors = self.errors_for(
            lambda graph: graph["relacoes"].append(
                {"origem": "topico-amostra", "tipo": "corresponde_a", "destino": "topico-populacao"}
            )
        )
        self.assert_has_error(errors, "conteúdo curricular concluído")

    def test_permits_an_item_with_multiple_completed_contents(self):
        """Catches obsolete hybrid-item rejection after integral promotion."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-q-hibrida",
                    "tipo": "questao",
                    "numero_impresso": "1",
                    "pagina_pdf": 1,
                    "pertinencia_t199": "direta",
                }
            )
            graph["relacoes"].extend(
                [
                    {"origem": "barbetta-2010", "tipo": "contem", "destino": "barbetta-2010-q-hibrida"},
                    {"origem": "barbetta-2010-q-hibrida", "tipo": "corresponde_a", "destino": "conteudo-01-01"},
                    {"origem": "barbetta-2010-q-hibrida", "tipo": "corresponde_a", "destino": "conteudo-02-01"},
                ]
            )

        self.assertFalse(
            any("item híbrido" in error for error in self.errors_for(mutate))
        )

    def test_rejects_concrete_item_without_pertinence(self):
        """Catches a concrete item whose pertinence to T199 was not classified."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-q-sem-pertinencia",
                    "tipo": "questao",
                    "numero_impresso": "2",
                    "pagina_pdf": 1,
                }
            )
            graph["relacoes"].append(
                {
                    "origem": "barbetta-2010",
                    "tipo": "contem",
                    "destino": "barbetta-2010-q-sem-pertinencia",
                }
            )

        self.assert_has_error(self.errors_for(mutate), "item sem pertinência")

    def test_rejects_long_textual_field_on_concrete_item(self):
        """Catches fields that could store a long item statement."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-q-texto-longo",
                    "tipo": "questao",
                    "numero_impresso": "x" * 241,
                    "pagina_pdf": 1,
                    "pertinencia_t199": "direta",
                }
            )
            graph["relacoes"].append(
                {
                    "origem": "barbetta-2010",
                    "tipo": "contem",
                    "destino": "barbetta-2010-q-texto-longo",
                }
            )

        self.assert_has_error(self.errors_for(mutate), "campo textual longo em item")

    def test_rejects_a_source_derived_from_a_summary(self):
        """Catches an auxiliary Markdown-summary path presented as a PDF source."""
        def mutate(graph):
            source = next(node for node in graph["nos"] if node["id"] == "barbetta-2010")
            source["arquivo"] = "prof/refs/livros/sumarios/barbetta.md"

        self.assert_has_error(self.errors_for(mutate), "fonte derivada de livros/sumarios/")

    def test_returns_errors_when_ancestral_source_lacks_page_count(self):
        """Catches malformed sources without aborting semantic page validation."""
        def mutate(graph):
            source = next(node for node in graph["nos"] if node["id"] == "barbetta-2010")
            source.pop("paginas_pdf")
            graph["nos"].append(
                {
                    "id": "barbetta-2010-cap-sem-total",
                    "tipo": "capitulo",
                    "numero_impresso": "1",
                    "titulo": "Sem total de páginas",
                    "pagina_pdf_inicio": 1,
                    "pagina_pdf_fim": 1,
                }
            )
            graph["relacoes"].append(
                {
                    "origem": "barbetta-2010",
                    "tipo": "contem",
                    "destino": "barbetta-2010-cap-sem-total",
                }
            )

        errors = self.errors_for(mutate)
        self.assertIsInstance(errors, list)
        self.assert_has_error(errors, "paginas_pdf")

    def test_returns_errors_when_source_path_is_not_text(self):
        """Catches malformed source paths without calling string methods on them."""
        def mutate(graph):
            source = next(node for node in graph["nos"] if node["id"] == "barbetta-2010")
            source["arquivo"] = 123

        errors = self.errors_for(mutate)
        self.assertIsInstance(errors, list)
        self.assert_has_error(errors, "schema:")

    def test_returns_errors_when_node_id_has_invalid_type(self):
        """Catches an unhashable node ID without aborting duplicate-ID validation."""
        errors = self.errors_for(
            lambda graph: graph["nos"].append({"id": [], "tipo": "topico", "nome": "Inválido"})
        )
        self.assertIsInstance(errors, list)
        self.assert_has_error(errors, "schema:")

    def test_returns_errors_when_edge_endpoint_has_invalid_type(self):
        """Catches an unhashable edge endpoint without aborting orphan-edge validation."""
        errors = self.errors_for(
            lambda graph: graph["relacoes"].append(
                {"origem": [], "tipo": "contem", "destino": "conteudo-01-01"}
            )
        )
        self.assertIsInstance(errors, list)
        self.assert_has_error(errors, "is not of type 'string'")

    def test_returns_errors_when_curriculum_code_has_invalid_type(self):
        """Catches an unhashable curriculum code without aborting scope validation."""
        def mutate(graph):
            content = next(node for node in graph["nos"] if node["id"] == "conteudo-01-01")
            content["codigo"] = []
            graph["relacoes"].append(
                {"origem": "topico-amostra", "tipo": "corresponde_a", "destino": "conteudo-01-01"}
            )

        errors = self.errors_for(mutate)
        self.assertIsInstance(errors, list)
        self.assert_has_error(errors, "schema:")

    def test_rejects_nine_sources_that_do_not_match_the_manifest(self):
        """Catches a nine-source graph with an impostor replacing a canonical source."""
        def mutate(graph):
            source = next(node for node in graph["nos"] if node["id"] == "barbetta-2010")
            source["id"] = "fonte-impostora"
            source["arquivo"] = "prof/refs/livros/fonte-impostora.pdf"

        self.assert_has_error(self.errors_for(mutate), "fontes inventariadas não correspondem ao manifesto")

    def test_rejects_noncanonical_complete_coverage(self):
        """Catches a coverage declaration that no longer matches the approved graph."""
        errors = self.errors_for(
            lambda graph: graph["metadados"]["cobertura"].update({"fontes_inventariadas": 8})
        )
        self.assert_has_error(errors, "cobertura integral não corresponde")

    def test_warns_when_coverage_is_missing(self):
        """Catches graphs that omit the required integral-coverage declaration."""
        errors = self.errors_for(lambda graph: graph["metadados"].pop("cobertura"))
        self.assert_has_error(errors, "aviso: cobertura ausente")


if __name__ == "__main__":
    unittest.main()
