import unittest

from scripts.grafo_refs.build_graph import (
    DEFAULT_CURATED_DIRECTORY,
    build_graph,
)
from scripts.grafo_refs.query_graph import query_by_topic


UNIT_II = ("02.01", "02.02", "02.03", "02.04")


def curricular_origins(graph: dict, code: str) -> set[str]:
    content_id = next(
        node["id"]
        for node in graph["nos"]
        if node.get("tipo") == "conteudo_curricular"
        and node.get("codigo") == code
    )
    return {
        edge["origem"]
        for edge in graph["relacoes"]
        if edge.get("tipo") == "corresponde_a"
        and edge.get("destino") == content_id
    }


class UnidadeIICompleteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph("2026-08-07", DEFAULT_CURATED_DIRECTORY)

    def test_every_unidade_ii_content_has_real_references(self):
        """Catches a curricular content left without a direct reference."""
        for code in UNIT_II:
            with self.subTest(code=code):
                self.assertGreater(
                    len(curricular_origins(self.graph, code)),
                    0,
                )

    def test_required_unidade_ii_topics_have_references(self):
        """Catches a required topic left without an explicit source relation."""
        for topic_id in (
            "topico-probabilidade-condicional",
            "topico-teorema-de-bayes",
            "topico-variavel-aleatoria-discreta",
            "topico-distribuicao-binomial",
            "topico-distribuicao-poisson",
            "topico-distribuicao-uniforme",
            "topico-distribuicao-exponencial",
            "topico-distribuicao-normal",
        ):
            with self.subTest(topic_id=topic_id):
                self.assertGreater(
                    len(query_by_topic(self.graph, topic_id)),
                    0,
                )


if __name__ == "__main__":
    unittest.main()
