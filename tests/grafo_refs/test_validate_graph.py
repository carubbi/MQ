import copy
import json
import unittest
from pathlib import Path

from scripts.grafo_refs.build_graph import build_graph
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

    def test_rejects_curricular_relationship_to_pending_content(self):
        """Catches partial graphs that claim a pending curriculum mapping."""
        errors = self.errors_for(
            lambda graph: graph["relacoes"].append(
                {"origem": "topico-amostra", "tipo": "corresponde_a", "destino": "conteudo-02-01"}
            )
        )
        self.assert_has_error(errors, "conteúdo pendente")

    def test_rejects_curricular_relationship_without_curriculum_content(self):
        """Catches corresponde_a relations that do not target a completed content."""
        errors = self.errors_for(
            lambda graph: graph["relacoes"].append(
                {"origem": "topico-amostra", "tipo": "corresponde_a", "destino": "topico-populacao"}
            )
        )
        self.assert_has_error(errors, "conteúdo curricular concluído")

    def test_rejects_hybrid_pedagogical_item(self):
        """Catches an item that combines concluded and pending curriculum content."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-q-hibrida",
                    "tipo": "item_pedagogico",
                    "subtipo": "questao",
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

        self.assert_has_error(self.errors_for(mutate), "item híbrido")

    def test_rejects_pedagogical_item_without_pertinence(self):
        """Catches an item whose pertinence to T199 was not classified."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-q-sem-pertinencia",
                    "tipo": "item_pedagogico",
                    "subtipo": "questao",
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

        self.assert_has_error(self.errors_for(mutate), "item pedagógico sem pertinência")

    def test_rejects_long_textual_field_on_pedagogical_item(self):
        """Catches fields that could store a long pedagogical statement."""
        def mutate(graph):
            graph["nos"].append(
                {
                    "id": "barbetta-2010-q-texto-longo",
                    "tipo": "item_pedagogico",
                    "subtipo": "questao",
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

        self.assert_has_error(self.errors_for(mutate), "campo textual longo em item pedagógico")

    def test_rejects_a_source_derived_from_a_summary(self):
        """Catches an auxiliary Markdown-summary path presented as a PDF source."""
        def mutate(graph):
            source = next(node for node in graph["nos"] if node["id"] == "barbetta-2010")
            source["arquivo"] = "prof/refs/livros/sumarios/barbetta.md"

        self.assert_has_error(self.errors_for(mutate), "fonte derivada de livros/sumarios/")

    def test_rejects_noncanonical_partial_coverage(self):
        """Catches a coverage declaration that no longer matches the approved slice."""
        errors = self.errors_for(
            lambda graph: graph["metadados"]["cobertura"].update({"fontes_inventariadas": 8})
        )
        self.assert_has_error(errors, "cobertura parcial não corresponde")

    def test_warns_when_coverage_is_missing(self):
        """Catches graphs that omit the required partial-coverage declaration."""
        errors = self.errors_for(lambda graph: graph["metadados"].pop("cobertura"))
        self.assert_has_error(errors, "aviso: cobertura ausente")


if __name__ == "__main__":
    unittest.main()
