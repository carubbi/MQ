import unittest

from scripts.grafo_refs.build_graph import (
    DEFAULT_CURATED_DIRECTORY,
    build_graph,
)
from scripts.grafo_refs.query_graph import query_by_topic


UNIT_II = ("02.01", "02.02", "02.03", "02.04")
EXPECTED_ORIGINS = {
    "02.01": {
        "apostila-mq-sec-8-1",
        "apostila-mq-sec-8-2",
        "apostila-mq-sec-8-3",
        "apostila-mq-sec-8-4",
        "apostila-mq-sec-8-5",
        "apostila-mq-sec-8-6",
        "apostila-mq-sec-8-7",
        "apostila-mq-sec-8-8",
        "apostila-mq-sec-8-8-1",
        "apostila-mq-sec-8-9",
        "barbetta-2010-sec-4-1",
        "barbetta-2010-sec-4-2",
        "barbetta-2010-sec-4-3",
        "barbetta-2010-sec-4-4",
        "barbetta-2010-sec-4-5",
        "montgomery-2018-sec-2-1-1",
        "montgomery-2018-sec-2-1-2",
        "montgomery-2018-sec-2-1-3",
        "montgomery-2018-sec-2-3",
        "montgomery-2018-sec-2-4",
        "montgomery-2018-sec-2-5",
        "montgomery-2018-sec-2-6",
        "montgomery-2018-sec-2-7",
        "montgomery-2018-sec-2-8",
        "morettin-bussab-2010-sec-5-1",
        "morettin-bussab-2010-sec-5-2",
        "morettin-bussab-2010-sec-5-3",
        "morettin-bussab-2010-sec-5-4",
        "navidi-2024-sec-2-1",
        "navidi-2024-sec-2-3",
        "pinheiro-2009-exercicio-3-10-p",
        "pinheiro-2009-exercicio-3-8-p",
        "pinheiro-2009-exercicio-3-9-p",
        "pinheiro-2009-sec-3-1",
        "pinheiro-2009-sec-3-2",
        "pinheiro-2009-sec-3-3",
        "pinheiro-2009-sec-3-4",
    },
    "02.02": {
        "apostila-mq-sec-9-1",
        "apostila-mq-sec-9-2",
        "apostila-mq-sec-9-3",
        "barbetta-2010-exercicio-5-1",
        "barbetta-2010-exercicio-6-1",
        "barbetta-2010-sec-5-1",
        "barbetta-2010-sec-6-1",
        "montgomery-2018-sec-2-9",
        "montgomery-2018-sec-3-1",
        "montgomery-2018-sec-3-2",
        "montgomery-2018-sec-3-3",
        "montgomery-2018-sec-4-1",
        "montgomery-2018-sec-4-2",
        "montgomery-2018-sec-4-3",
        "morettin-bussab-2010-sec-6-2",
        "morettin-bussab-2010-sec-6-3",
        "morettin-bussab-2010-sec-6-5",
        "morettin-bussab-2010-sec-7-1",
        "morettin-bussab-2010-sec-7-2",
        "morettin-bussab-2010-sec-7-3",
        "navidi-2024-sec-2-4",
        "pinheiro-2009-exercicio-4-3-p",
        "pinheiro-2009-sec-4-2",
        "pinheiro-2009-sec-4-3",
        "pinheiro-2009-sec-4-4",
    },
    "02.03": {
        "apostila-mq-sec-10-1",
        "apostila-mq-sec-10-2",
        "banco-questoes-2026-2-sec-5-1-1",
        "banco-questoes-2026-2-sec-5-1-2",
        "barbetta-2010-exercicio-5-11",
        "barbetta-2010-exercicio-5-7",
        "barbetta-2010-sec-5-2",
        "estatistica-pratica-cd-sec-2-distribuicao-binomial",
        "estatistica-pratica-cd-sec-2-distribuicoes-poisson",
        "montgomery-2018-sec-3-5",
        "montgomery-2018-sec-3-8",
        "morettin-bussab-2010-sec-6-6",
        "morettin-bussab-2010-sec-6-7",
        "navidi-2024-sec-4-2",
        "navidi-2024-sec-4-3",
        "pinheiro-2009-exercicio-4-6-p",
        "pinheiro-2009-exercicio-4-7-p",
    },
    "02.04": {
        "apostila-mq-sec-17-7",
        "banco-questoes-2026-2-sec-5-2-1",
        "banco-questoes-2026-2-sec-5-2-2",
        "banco-questoes-2026-2-sec-5-2-4",
        "barbetta-2010-exercicio-6-1",
        "barbetta-2010-exercicio-6-13",
        "barbetta-2010-exercicio-6-17",
        "barbetta-2010-exercicio-6-2",
        "barbetta-2010-exercicio-6-6",
        "barbetta-2010-exercicio-6-8",
        "barbetta-2010-sec-6-2",
        "barbetta-2010-sec-6-4",
        "estatistica-pratica-cd-sec-2-distribuicao-exponencial",
        "estatistica-pratica-cd-sec-2-distribuicao-normal",
        "estatistica-pratica-cd-sec-2-normal-padrao-e-graficos-qq",
        "montgomery-2018-sec-4-4",
        "montgomery-2018-sec-4-5",
        "montgomery-2018-sec-4-7",
        "montgomery-2018-sec-6-7",
        "morettin-bussab-2010-sec-7-4",
        "navidi-2024-sec-4-10",
        "navidi-2024-sec-4-5",
        "navidi-2024-sec-4-7",
        "navidi-2024-sec-4-8",
        "pinheiro-2009-exercicio-4-8-p",
        "pinheiro-2009-exercicio-4-9-p",
        "pinheiro-2009-sec-4-4",
        "pinheiro-2009-sec-4-5",
    },
}
REQUIRED_TOPICS = {
    "02.01": {
        "topico-experimento-aleatorio",
        "topico-espaco-amostral",
        "topico-evento",
        "topico-regra-da-adicao",
        "topico-regra-do-produto",
        "topico-probabilidade-condicional",
        "topico-independencia",
        "topico-probabilidade-total",
        "topico-teorema-de-bayes",
    },
    "02.02": {
        "topico-variavel-aleatoria-discreta",
        "topico-variavel-aleatoria-continua",
        "topico-funcao-de-probabilidade",
        "topico-funcao-densidade",
        "topico-funcao-distribuicao-acumulada",
        "topico-esperanca",
        "topico-variancia",
    },
    "02.03": {
        "topico-distribuicao-binomial",
        "topico-distribuicao-poisson",
    },
    "02.04": {
        "topico-distribuicao-uniforme",
        "topico-distribuicao-exponencial",
        "topico-distribuicao-normal",
        "topico-padronizacao",
        "topico-grafico-qq",
        "topico-diagnostico-do-modelo",
    },
}
EXPECTED_EXERCISES = {
    "barbetta-2010-exercicio-5-1": (126, {"02.02"}),
    "barbetta-2010-exercicio-5-7": (132, {"02.03"}),
    "barbetta-2010-exercicio-5-11": (137, {"02.03"}),
    "barbetta-2010-exercicio-6-1": (147, {"02.02", "02.04"}),
    "barbetta-2010-exercicio-6-2": (147, {"02.04"}),
    "barbetta-2010-exercicio-6-6": (153, {"02.04"}),
    "barbetta-2010-exercicio-6-8": (159, {"02.04"}),
    "barbetta-2010-exercicio-6-13": (167, {"02.04"}),
    "barbetta-2010-exercicio-6-17": (168, {"02.04"}),
    "pinheiro-2009-exercicio-3-8-p": (111, {"02.01"}),
    "pinheiro-2009-exercicio-3-9-p": (111, {"02.01"}),
    "pinheiro-2009-exercicio-3-10-p": (111, {"02.01"}),
    "pinheiro-2009-exercicio-4-3-p": (148, {"02.02"}),
    "pinheiro-2009-exercicio-4-6-p": (149, {"02.03"}),
    "pinheiro-2009-exercicio-4-7-p": (149, {"02.03"}),
    "pinheiro-2009-exercicio-4-8-p": (149, {"02.04"}),
    "pinheiro-2009-exercicio-4-9-p": (149, {"02.04"}),
}
OUT_OF_SCOPE_DISTRIBUTION_SECTIONS = {
    "apostila-mq-sec-10-4",
    "banco-questoes-2026-2-sec-5-1-3",
    "banco-questoes-2026-2-sec-5-1-4",
    "banco-questoes-2026-2-sec-5-1-5",
    "banco-questoes-2026-2-sec-5-1-6",
    "banco-questoes-2026-2-sec-5-1-7",
    "banco-questoes-2026-2-sec-5-2-3",
    "banco-questoes-2026-2-sec-5-2-5",
    "banco-questoes-2026-2-sec-5-2-6",
    "banco-questoes-2026-2-sec-5-2-7",
    "estatistica-pratica-cd-sec-2-distribuicao-weibull",
    "montgomery-2018-sec-3-6",
    "montgomery-2018-sec-3-7",
    "montgomery-2018-sec-4-8",
    "montgomery-2018-sec-4-9",
    "montgomery-2018-sec-4-10",
    "montgomery-2018-sec-4-11",
    "navidi-2024-sec-4-6",
}


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
        """Catches replacement, loss, or expansion of a reviewed origin."""
        for code, expected_origins in EXPECTED_ORIGINS.items():
            with self.subTest(code=code):
                self.assertEqual(
                    curricular_origins(self.graph, code),
                    expected_origins,
                )

    def test_every_required_topic_is_supported_by_the_same_content_origins(self):
        """Catches global topic matches unrelated to the reviewed content."""
        edges = {
            (edge["origem"], edge["tipo"], edge["destino"])
            for edge in self.graph["relacoes"]
        }
        for code, required_topics in REQUIRED_TOPICS.items():
            origins = curricular_origins(self.graph, code)
            actual_topics = {
                destination
                for origin, relation_type, destination in edges
                if relation_type == "aborda" and origin in origins
            }
            with self.subTest(code=code):
                self.assertTrue(
                    required_topics.issubset(actual_topics),
                    required_topics - actual_topics,
                )
                self.assertTrue(
                    all(
                        any(
                            relation_type == "aborda"
                            and origin == reference
                            and destination in required_topics
                            for origin, relation_type, destination in edges
                        )
                        for reference in origins
                    )
                )

    def test_apostila_topics_match_the_pdf_localizers_exactly(self):
        """Catches reintroducing unsupported CDF relations in chapter 9."""
        expected = {
            "apostila-mq-sec-9-1": {
                "topico-variavel-aleatoria-discreta",
                "topico-funcao-de-probabilidade",
                "topico-esperanca",
                "topico-variancia",
            },
            "apostila-mq-sec-9-2": {
                "topico-variavel-aleatoria-continua",
                "topico-funcao-densidade",
                "topico-esperanca",
                "topico-variancia",
            },
        }
        for origin, expected_topics in expected.items():
            with self.subTest(origin=origin):
                self.assertEqual(
                    {
                        edge["destino"]
                        for edge in self.graph["relacoes"]
                        if edge["origem"] == origin
                        and edge["tipo"] == "aborda"
                    },
                    expected_topics,
                )

    def test_selected_exercises_preserve_ids_pages_and_contents(self):
        """Catches loss or relocation of any PDF-confirmed exercise."""
        nodes = {node["id"]: node for node in self.graph["nos"]}
        contents = {
            node["id"]: node["codigo"]
            for node in self.graph["nos"]
            if node.get("tipo") == "conteudo_curricular"
        }
        actual_item_ids = set()
        for item_id, (page, expected_contents) in EXPECTED_EXERCISES.items():
            node = nodes[item_id]
            actual_item_ids.add(item_id)
            with self.subTest(item_id=item_id):
                self.assertEqual(node["tipo"], "exercicio")
                self.assertEqual(node["pagina_pdf"], page)
                self.assertEqual(
                    {
                        contents[edge["destino"]]
                        for edge in self.graph["relacoes"]
                        if edge["origem"] == item_id
                        and edge["tipo"] == "corresponde_a"
                    },
                    expected_contents,
                )
        selected = {
            node["id"]
            for node in self.graph["nos"]
            if node.get("tipo") == "exercicio"
            and (
                node["id"].startswith("barbetta-2010-exercicio-5-")
                or node["id"].startswith("barbetta-2010-exercicio-6-")
                or node["id"].startswith("pinheiro-2009-exercicio-3-")
                or node["id"].startswith("pinheiro-2009-exercicio-4-")
            )
            and any(
                edge["origem"] == node["id"]
                and edge["tipo"] == "corresponde_a"
                and contents.get(edge["destino"], "").startswith("02.")
                for edge in self.graph["relacoes"]
            )
        }
        self.assertEqual(selected, actual_item_ids)

    def test_unplanned_distributions_have_no_direct_curricular_mapping(self):
        """Catches convenience mappings outside the teaching project."""
        curricular_edges = {
            edge["origem"]
            for edge in self.graph["relacoes"]
            if edge["tipo"] == "corresponde_a"
            and edge["destino"].startswith("conteudo-02-")
        }
        self.assertTrue(
            OUT_OF_SCOPE_DISTRIBUTION_SECTIONS.isdisjoint(curricular_edges)
        )

    def test_qq_is_a_diagnostic_topic_not_a_curricular_content(self):
        """Catches promoting Q-Q to an independent curricular content."""
        qq_references = {
            result["id"]
            for result in query_by_topic(self.graph, "topico-grafico-qq")
        }
        self.assertGreater(len(qq_references), 0)
        normal_origins = curricular_origins(self.graph, "02.04")
        self.assertTrue(qq_references.intersection(normal_origins))
        self.assertFalse(
            any(
                node.get("tipo") == "conteudo_curricular"
                and "q-q" in node.get("nome", "").lower()
                for node in self.graph["nos"]
            )
        )

    def test_coverage_remains_partial_until_the_integral_gate(self):
        """Catches premature promotion before Units II and III are complete."""
        coverage = self.graph["metadados"]["cobertura"]
        self.assertEqual(coverage["estado"], "parcial")
        self.assertEqual(
            coverage["conteudos_concluidos"],
            ["01.01", "01.02", "01.03", "01.04"],
        )
        self.assertEqual(
            coverage["conteudos_pendentes"],
            list(UNIT_II + ("03.01", "03.02", "03.03", "03.04")),
        )


if __name__ == "__main__":
    unittest.main()
