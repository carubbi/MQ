import json
import unittest
from collections import defaultdict

from scripts.grafo_refs.build_graph import (
    DEFAULT_CURATED_DIRECTORY,
    REPOSITORY_ROOT,
    build_graph,
)


EXPECTED_STRUCTURE = (
    REPOSITORY_ROOT
    / "scripts/grafo_refs/data/estrutura_editorial_esperada.json"
)
STRUCTURE_MIGRATIONS = (
    REPOSITORY_ROOT
    / "scripts/grafo_refs/data/migracoes_estrutura_unidade_i.json"
)
ESCOVEDO_ID = "introducao-estatistica-cd"


class EditorialCompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph("2026-08-07", DEFAULT_CURATED_DIRECTORY)

    def test_every_expected_editorial_node_is_present(self):
        """Catches any structural divergence from the PDF-verified manifest."""
        expected = json.loads(EXPECTED_STRUCTURE.read_text(encoding="utf-8"))
        nodes = {node["id"]: node for node in self.graph["nos"]}
        parents = {
            edge["destino"]: edge["origem"]
            for edge in self.graph["relacoes"]
            if edge["tipo"] == "contem"
        }

        for source_id, structure in expected.items():
            with self.subTest(source_id=source_id):
                expected_nodes = structure["nos"]
                actual_ids = {
                    node_id
                    for node_id in nodes
                    if node_id.startswith(f"{source_id}-")
                    and nodes[node_id]["tipo"] in {"capitulo", "secao"}
                }
                self.assertEqual(actual_ids, set(expected_nodes))
                for node_id, expected_node in expected_nodes.items():
                    actual = nodes[node_id]
                    self.assertEqual(
                        {
                            "tipo": actual["tipo"],
                            "pai": parents[node_id],
                            "pagina_pdf_inicio": actual["pagina_pdf_inicio"],
                            "pagina_pdf_fim": actual["pagina_pdf_fim"],
                        },
                        expected_node,
                    )

    def test_escovedo_has_no_descendants(self):
        """Catches accidental editorial or curricular curation of Escovedo."""
        children = {
            edge["destino"]
            for edge in self.graph["relacoes"]
            if edge["tipo"] == "contem"
            and edge["origem"] == ESCOVEDO_ID
        }

        self.assertEqual(children, set())

    def test_apostila_exercises_are_individualized_after_27(self):
        """Catches any missing, duplicate, or extra apostila exercise."""
        exercise_ids = {
            node["id"]
            for node in self.graph["nos"]
            if node["tipo"] == "exercicio"
            and node["id"].startswith("apostila-mq-exercicio-")
        }

        self.assertEqual(
            exercise_ids,
            {f"apostila-mq-exercicio-{number}" for number in range(1, 163)},
        )

    def test_known_structural_errors_are_migrated_to_pdf_evidence(self):
        """Catches reintroduction of reviewed structural errors."""
        nodes = {node["id"]: node for node in self.graph["nos"]}
        parents = {
            edge["destino"]: edge["origem"]
            for edge in self.graph["relacoes"]
            if edge["tipo"] == "contem"
        }

        self.assertEqual(
            (
                nodes["banco-questoes-2026-2-cap-1"]["pagina_pdf_inicio"],
                nodes["banco-questoes-2026-2-cap-1"]["pagina_pdf_fim"],
            ),
            (7, 87),
        )
        self.assertEqual(
            (
                nodes["banco-questoes-2026-2-cap-2"]["pagina_pdf_inicio"],
                nodes["banco-questoes-2026-2-cap-2"]["pagina_pdf_fim"],
            ),
            (88, 94),
        )
        self.assertEqual(
            parents["banco-questoes-2026-2-sec-3-1"],
            "banco-questoes-2026-2-cap-2",
        )
        self.assertEqual(
            nodes["montgomery-2018-cap-6"]["pagina_pdf_fim"],
            165,
        )
        self.assertEqual(
            (
                nodes["pinheiro-2009-cap-2"]["pagina_pdf_inicio"],
                nodes["pinheiro-2009-cap-2"]["pagina_pdf_fim"],
                nodes["pinheiro-2009-cap-3"]["pagina_pdf_inicio"],
            ),
            (59, 86, 87),
        )

    def test_structural_migrations_are_declared(self):
        """Catches Unit I structural changes without an audit record."""
        migrations = json.loads(
            STRUCTURE_MIGRATIONS.read_text(encoding="utf-8")
        )

        self.assertEqual(migrations["versao"], 1)
        self.assertGreater(len(migrations["migracoes"]), 0)
        for migration in migrations["migracoes"]:
            self.assertIn(migration["tipo"], {"campo", "relacao"})
            evidence = migration["evidencia"]
            self.assertIn("arquivo_pdf", evidence)
            self.assertIn("pagina_pdf", evidence)
            self.assertIn("justificativa", evidence)

    def test_editorial_hierarchy_has_valid_intervals_and_overlaps(self):
        """Catches descendants outside parents and multi-page sibling overlap."""
        nodes = {node["id"]: node for node in self.graph["nos"]}
        children = defaultdict(list)
        for edge in self.graph["relacoes"]:
            if edge["tipo"] == "contem":
                children[edge["origem"]].append(edge["destino"])

        for parent_id, child_ids in children.items():
            parent = nodes[parent_id]
            if "pagina_pdf_inicio" not in parent:
                continue
            for child_id in child_ids:
                child = nodes[child_id]
                child_start = child.get(
                    "pagina_pdf",
                    child.get("pagina_pdf_inicio"),
                )
                child_end = child.get(
                    "pagina_pdf",
                    child.get("pagina_pdf_fim"),
                )
                self.assertGreaterEqual(
                    child_start,
                    parent["pagina_pdf_inicio"],
                    child_id,
                )
                self.assertLessEqual(
                    child_end,
                    parent["pagina_pdf_fim"],
                    child_id,
                )

            editorial = [
                nodes[child_id]
                for child_id in child_ids
                if nodes[child_id]["tipo"] in {"capitulo", "secao"}
            ]
            for index, left in enumerate(editorial):
                for right in editorial[index + 1 :]:
                    overlap = (
                        min(
                            left["pagina_pdf_fim"],
                            right["pagina_pdf_fim"],
                        )
                        - max(
                            left["pagina_pdf_inicio"],
                            right["pagina_pdf_inicio"],
                        )
                        + 1
                    )
                    self.assertLessEqual(
                        overlap,
                        1,
                        f"{left['id']} x {right['id']}",
                    )


if __name__ == "__main__":
    unittest.main()
