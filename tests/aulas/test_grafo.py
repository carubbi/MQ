import unittest

from scripts.aulas.grafo import (
    graph_indexes,
    node_and_descendant_ids,
    page_interval,
    source_ancestors,
)
from tests.aulas.fixtures import GRAPH


class GraphHelpersTests(unittest.TestCase):
    def test_traverses_containment_in_both_directions_needed_by_curation(self):
        nodes, relations = graph_indexes(GRAPH)

        self.assertEqual(
            {
                "capitulo-fundamentos",
                "secao-populacao",
                "questao-populacao",
            },
            node_and_descendant_ids(
                "capitulo-fundamentos",
                relations["contem"],
            ),
        )
        self.assertEqual(
            {"fonte-a"},
            source_ancestors(
                "secao-populacao",
                nodes,
                relations["contem"],
            ),
        )

    def test_reads_single_page_and_interval_nodes(self):
        nodes, _ = graph_indexes(GRAPH)

        self.assertEqual((10, 12), page_interval(nodes["secao-populacao"]))
        self.assertEqual((13, 13), page_interval(nodes["questao-populacao"]))


if __name__ == "__main__":
    unittest.main()
