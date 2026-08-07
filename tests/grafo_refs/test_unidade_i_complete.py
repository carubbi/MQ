import json
import unittest
from pathlib import Path

from scripts.grafo_refs.build_graph import (
    DEFAULT_CURATED_DIRECTORY,
    REPOSITORY_ROOT,
    build_graph,
)
from scripts.grafo_refs.curation.common import extract_sequential_numbered_items
from scripts.grafo_refs.extract_pdf import extract_pdf
from scripts.grafo_refs.query_graph import query_by_content


MAPPED_SOURCES = {
    "apostila-mq",
    "banco-questoes-2026-2",
    "barbetta-2010",
    "estatistica-pratica-cd",
    "montgomery-2018",
    "morettin-bussab-2010",
    "navidi-2024",
    "pinheiro-2009",
}
ITEM_TYPES = {"questao", "exercicio", "exemplo"}
CONTRACT_PATH = (
    REPOSITORY_ROOT / "scripts/grafo_refs/data/contrato_publicado_unidade_i.json"
)
MIGRATIONS_PATH = (
    REPOSITORY_ROOT
    / "scripts/grafo_refs/data/migracoes_estrutura_unidade_i.json"
)


def load_published_contract(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_ancestors(graph: dict, node_id: str) -> set[str]:
    nodes = {node["id"]: node for node in graph["nos"]}
    parents = {}
    for edge in graph["relacoes"]:
        if edge["tipo"] == "contem":
            parents.setdefault(edge["destino"], set()).add(edge["origem"])

    sources = set()
    pending = list(parents.get(node_id, set()))
    visited = set()
    while pending:
        ancestor_id = pending.pop()
        if ancestor_id in visited:
            continue
        visited.add(ancestor_id)
        if nodes[ancestor_id]["tipo"] == "fonte":
            sources.add(ancestor_id)
        pending.extend(parents.get(ancestor_id, set()))
    return sources


class UnidadeICompleteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph("2026-08-06", DEFAULT_CURATED_DIRECTORY)

    def test_every_unidade_i_content_has_real_references(self):
        for code in ("01.01", "01.02", "01.03", "01.04"):
            with self.subTest(code=code):
                result = query_by_content(self.graph, code)
                self.assertEqual(result["estado"], "concluido")
                self.assertGreater(len(result["resultados"]), 0)

    def test_preserves_the_published_unidade_i_contract(self):
        contract = load_published_contract(CONTRACT_PATH)
        migrations = json.loads(MIGRATIONS_PATH.read_text(encoding="utf-8"))
        graph_nodes = {node["id"]: node for node in self.graph["nos"]}
        self.assertEqual(contract["versao"], 2)
        self.assertTrue(set(contract["nos"]).issubset(graph_nodes))

        for node_id, expected in contract["nos"].items():
            actual = graph_nodes[node_id]
            self.assertEqual(actual["tipo"], expected["tipo"])

        actual_edges = {
            (edge["origem"], edge["tipo"], edge["destino"])
            for edge in self.graph["relacoes"]
        }
        contract_edges = {tuple(edge) for edge in contract["relacoes"]}
        for relation_type in {"aborda", "corresponde_a"}:
            self.assertEqual(
                {
                    edge
                    for edge in actual_edges
                    if edge[1] == relation_type
                },
                {
                    edge
                    for edge in contract_edges
                    if edge[1] == relation_type
                },
            )

        actual_field_migrations = set()
        for node_id, expected in contract["nos"].items():
            actual = graph_nodes[node_id]
            for field in {
                "pagina_pdf",
                "pagina_pdf_inicio",
                "pagina_pdf_fim",
            }:
                if field in expected and actual.get(field) != expected[field]:
                    actual_field_migrations.add(
                        (
                            node_id,
                            field,
                            expected[field],
                            actual.get(field),
                        )
                    )
        declared_field_migrations = {
            (
                migration["id"],
                migration["campo"],
                migration["de"],
                migration["para"],
            )
            for migration in migrations["migracoes"]
            if migration["tipo"] == "campo"
        }
        self.assertEqual(
            actual_field_migrations,
            declared_field_migrations,
        )

        contract_parents = {
            destination: origin
            for origin, relation_type, destination in contract_edges
            if relation_type == "contem"
        }
        actual_parents = {
            destination: origin
            for origin, relation_type, destination in actual_edges
            if relation_type == "contem"
            and destination in contract["nos"]
        }
        actual_parent_migrations = {
            (destination, contract_parent, actual_parents[destination])
            for destination, contract_parent in contract_parents.items()
            if actual_parents[destination] != contract_parent
        }
        declared_parent_migrations = {
            (
                migration["destino"],
                migration["origem_de"],
                migration["origem_para"],
            )
            for migration in migrations["migracoes"]
            if migration["tipo"] == "relacao"
            and migration["relacao"] == "contem"
        }
        self.assertEqual(
            actual_parent_migrations,
            declared_parent_migrations,
        )

        contract_precedence = {
            edge for edge in contract_edges if edge[1] == "precede"
        }
        published_ids = set(contract["nos"])
        actual_precedence = {
            edge
            for edge in actual_edges
            if edge[1] == "precede"
            and edge[0] in published_ids
            and edge[2] in published_ids
        }
        declared_precedence_migrations = {
            (
                migration["origem_de"],
                "precede",
                migration["destino"],
                migration["origem_para"],
            )
            for migration in migrations["migracoes"]
            if migration["tipo"] == "relacao"
            and migration["relacao"] == "precede"
        }
        self.assertEqual(
            (
                contract_precedence - actual_precedence,
                actual_precedence - contract_precedence,
            ),
            (
                {
                    (origin_from, "precede", destination)
                    for origin_from, _, destination, _origin_to
                    in declared_precedence_migrations
                },
                {
                    (origin_to, "precede", destination)
                    for _origin_from, _, destination, origin_to
                    in declared_precedence_migrations
                },
            ),
        )

    def test_expected_sources_are_mapped_without_escovedo(self):
        curricular_origins = {
            edge["origem"]
            for edge in self.graph["relacoes"]
            if edge["tipo"] == "corresponde_a"
        }
        mapped_sources = set()
        for origin in curricular_origins:
            mapped_sources.update(_source_ancestors(self.graph, origin))

        self.assertEqual(mapped_sources, MAPPED_SOURCES)
        self.assertNotIn("introducao-estatistica-cd", mapped_sources)

    def test_public_question_sources_have_individual_items(self):
        nodes = self.graph["nos"]
        for source_id in ("apostila-mq", "banco-questoes-2026-2"):
            with self.subTest(source_id=source_id):
                item_ids = {
                    node["id"]
                    for node in nodes
                    if node["tipo"] in ITEM_TYPES
                    and source_id in _source_ancestors(self.graph, node["id"])
                }
                self.assertGreater(len(item_ids), 0)

    def test_graph_uses_only_concrete_item_types(self):
        """Catches regressions to the generic item type or subtype field."""
        item_nodes = [
            node for node in self.graph["nos"] if node["tipo"] in ITEM_TYPES
        ]

        self.assertEqual(len(item_nodes), 432)
        self.assertTrue(all("subtipo" not in node for node in self.graph["nos"]))
        self.assertNotIn(
            "subtipos_item_pedagogico",
            self.graph["vocabularios"],
        )

    def test_formal_leaf_sections_are_not_hidden_by_aggregate_nodes(self):
        node_ids = {node["id"] for node in self.graph["nos"]}

        self.assertTrue(
            {
                "apostila-mq-sec-4-4",
                "banco-questoes-2026-2-sec-1-3-2-3",
                "montgomery-2018-sec-1-1-2",
                "morettin-bussab-2010-sec-4-9",
            }.issubset(node_ids)
        )

    def test_subsections_preserve_the_editorial_hierarchy(self):
        edges = {
            (edge["origem"], edge["tipo"], edge["destino"])
            for edge in self.graph["relacoes"]
        }

        self.assertTrue(
            {
                (
                    "barbetta-2010-sec-2-2",
                    "contem",
                    "barbetta-2010-sec-2-2-1",
                ),
                (
                    "morettin-bussab-2010-sec-2-3",
                    "contem",
                    "morettin-bussab-2010-sec-2-3-1",
                ),
            }.issubset(edges)
        )

    def test_mixed_chapters_keep_full_editorial_identity(self):
        nodes = {node["id"]: node for node in self.graph["nos"]}
        edges = {
            (edge["origem"], edge["tipo"], edge["destino"])
            for edge in self.graph["relacoes"]
        }

        self.assertEqual(
            nodes["apostila-mq-cap-15"]["titulo"],
            "Análise de Correlação e Regressão",
        )
        self.assertEqual(nodes["apostila-mq-cap-15"]["pagina_pdf_fim"], 163)
        self.assertIn(
            ("apostila-mq-cap-17", "contem", "apostila-mq-sec-17-1"),
            edges,
        )
        self.assertEqual(nodes["barbetta-2010-cap-11"]["pagina_pdf_fim"], 350)
        self.assertEqual(nodes["pinheiro-2009-cap-2"]["pagina_pdf_fim"], 86)
        self.assertEqual(nodes["pinheiro-2009-cap-3"]["pagina_pdf_inicio"], 87)


class CurateUnidadeITests(unittest.TestCase):
    def test_extracts_bank_questions_without_table_number_false_positives(self):
        extracted = extract_pdf(
            REPOSITORY_ROOT / "mat/apostila/banco_questoes_provas_2026_2.pdf"
        )

        items = extract_sequential_numbered_items(
            extracted,
            start_page=7,
            end_page=94,
            first_number=1,
            last_number=259,
        )

        self.assertEqual(len(items), 259)
        self.assertEqual(items[0], (1, 7))
        self.assertEqual(items[120], (121, 54))
        self.assertEqual(items[-1], (259, 94))


if __name__ == "__main__":
    unittest.main()
