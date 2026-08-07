import json
import unittest

from scripts.grafo_refs.build_graph import (
    DEFAULT_CURATED_DIRECTORY,
    REPOSITORY_ROOT,
    build_graph,
)


EXPECTED_STRUCTURE = (
    REPOSITORY_ROOT
    / "scripts/grafo_refs/data/estrutura_editorial_esperada.json"
)
ESCOVEDO_ID = "introducao-estatistica-cd"


class EditorialCompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph("2026-08-07", DEFAULT_CURATED_DIRECTORY)

    def test_every_expected_editorial_node_is_present(self):
        """Catches omission of any chapter or formal section verified in the PDFs."""
        expected = json.loads(EXPECTED_STRUCTURE.read_text(encoding="utf-8"))
        node_ids = {node["id"] for node in self.graph["nos"]}

        for source_id, structure in expected.items():
            with self.subTest(source_id=source_id):
                required = set(structure["capitulos"]) | set(
                    structure["secoes"]
                )
                missing = sorted(required - node_ids)
                self.assertEqual(missing, [])

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
        """Catches regression to the partial exercise extraction of Unit I."""
        node_ids = {node["id"] for node in self.graph["nos"]}

        self.assertIn("apostila-mq-exercicio-28", node_ids)
        self.assertIn("apostila-mq-exercicio-162", node_ids)


if __name__ == "__main__":
    unittest.main()
