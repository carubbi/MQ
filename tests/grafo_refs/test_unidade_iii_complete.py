import json
import unittest
import unicodedata

from scripts.grafo_refs.build_graph import (
    DEFAULT_CURATED_DIRECTORY,
    REPOSITORY_ROOT,
    build_graph,
)


UNIT_III = ("03.01", "03.02", "03.03", "03.04")
CONTRACT_PATH = (
    REPOSITORY_ROOT / "scripts/grafo_refs/data/contrato_unidade_iii.json"
)

REQUIRED_TOPICS = {
    "03.01": {
        "topico-populacao",
        "topico-amostra",
        "topico-amostragem",
        "topico-amostragem-aleatoria-simples",
        "topico-amostragem-estratificada",
        "topico-amostragem-sistematica",
        "topico-amostragem-por-conglomerados",
        "topico-amostragem-por-conveniencia",
        "topico-representatividade",
    },
    "03.02": {
        "topico-distribuicao-amostral",
        "topico-teorema-central-do-limite",
        "topico-erro-padrao",
        "topico-estimacao-pontual",
        "topico-intervalo-de-confianca",
        "topico-margem-de-erro",
        "topico-tamanho-amostral",
    },
    "03.03": {
        "topico-hipotese-nula",
        "topico-hipotese-alternativa",
        "topico-nivel-de-significancia",
        "topico-valor-p",
        "topico-teste-para-media",
        "topico-teste-para-proporcao",
        "topico-erro-tipo-i",
        "topico-erro-tipo-ii",
        "topico-poder-do-teste",
    },
    "03.04": {
        "topico-regressao-linear-simples",
        "topico-regressao-linear-multipla",
        "topico-minimos-quadrados",
        "topico-inferencia-sobre-coeficientes",
        "topico-coeficiente-de-determinacao",
        "topico-coeficiente-de-determinacao-ajustado",
        "topico-residuo",
        "topico-diagnostico-do-modelo",
        "topico-variavel-indicadora",
        "topico-valor-p",
    },
}

OUT_OF_SCOPE_ORIGINS = {
    "apostila-mq-sec-14-4",
    "apostila-mq-sec-14-5",
    "barbetta-2010-sec-7-4",
    "barbetta-2010-sec-9-2",
    "barbetta-2010-sec-9-3",
    "barbetta-2010-sec-9-7",
    "barbetta-2010-sec-9-8",
    "barbetta-2010-cap-10",
    "estatistica-pratica-cd-sec-3-anova",
    "estatistica-pratica-cd-sec-3-anova-bidirecional",
    "estatistica-pratica-cd-sec-3-potencia-e-tamanho-de-amostra",
    "montgomery-2018-cap-10",
    "montgomery-2018-sec-8-1-2",
    "montgomery-2018-sec-9-9",
    "morettin-bussab-2010-cap-13",
    "navidi-2024-sec-8-3",
    "pinheiro-2009-sec-8-8",
}
AUTOMATIC_SELECTION_ORIGINS = {
    "estatistica-pratica-cd-sec-4-selecao-de-modelo-e-regressao-passo-a-passo",
    "montgomery-2018-sec-12-6-3",
    "navidi-2024-sec-8-3",
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


class UnidadeIIICompleteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph("2026-08-07", DEFAULT_CURATED_DIRECTORY)
        cls.edges = {
            (edge["origem"], edge["tipo"], edge["destino"])
            for edge in cls.graph["relacoes"]
        }
        cls.contract = json.loads(
            CONTRACT_PATH.read_text(encoding="utf-8")
        )

    def test_every_unidade_iii_content_has_real_references(self):
        """Catches replacement, loss, or expansion of a reviewed origin."""
        for code, expected_origins in self.contract[
            "origens_por_conteudo"
        ].items():
            with self.subTest(code=code):
                self.assertEqual(
                    curricular_origins(self.graph, code),
                    set(expected_origins),
                )

    def test_every_reviewed_origin_preserves_its_exact_topics(self):
        """Catches unsupported topics or loss of a PDF-reviewed relation."""
        for origin, expected_topics in self.contract[
            "topicos_por_origem"
        ].items():
            with self.subTest(origin=origin):
                self.assertEqual(
                    {
                        destination
                        for edge_origin, relation_type, destination in self.edges
                        if relation_type == "aborda"
                        and edge_origin == origin
                    },
                    set(expected_topics),
                )

    def test_every_required_topic_is_supported_by_its_content_origins(self):
        """Catches global topic matches unrelated to a Unit III mapping."""
        for code, required_topics in REQUIRED_TOPICS.items():
            origins = curricular_origins(self.graph, code)
            actual_topics = {
                destination
                for origin, relation_type, destination in self.edges
                if relation_type == "aborda" and origin in origins
            }
            with self.subTest(code=code):
                self.assertTrue(
                    required_topics.issubset(actual_topics),
                    required_topics - actual_topics,
                )

    def test_unidade_iii_excludes_topics_outside_the_teaching_scope(self):
        """Catches mappings for unplanned sampling and inferential methods."""
        unit_iii_origins = set().union(
            *(curricular_origins(self.graph, code) for code in UNIT_III)
        )
        self.assertTrue(
            OUT_OF_SCOPE_ORIGINS.isdisjoint(unit_iii_origins)
        )

    def test_aic_and_bic_cannot_be_used_for_unidade_iii_predictor_choice(self):
        """Protects the decision to choose X before examining model results."""
        regression_origins = curricular_origins(self.graph, "03.04")
        regression_topics = {
            destination
            for origin, relation_type, destination in self.edges
            if relation_type == "aborda" and origin in regression_origins
        }
        regression_names = {
            node["nome"].lower()
            for node in self.graph["nos"]
            if node["id"] in regression_topics
        }
        self.assertFalse(
            any("aic" in name or "bic" in name for name in regression_names)
        )
        self.assertTrue(
            AUTOMATIC_SELECTION_ORIGINS.isdisjoint(regression_origins)
        )
        nodes = {node["id"]: node for node in self.graph["nos"]}
        prohibited_fragments = {
            "aic",
            "bic",
            "model selection",
            "selection of variables",
            "variable selection",
            "automatic selection",
            "automatic variable selection",
            "stepwise",
            "selecao de modelo",
            "selecao de variaveis",
            "selecao automatica",
            "passo a passo",
        }
        for origin in regression_origins:
            searchable = unicodedata.normalize(
                "NFKD",
                " ".join(
                    (
                        origin,
                        nodes[origin].get("titulo", ""),
                    )
                ),
            ).encode("ascii", "ignore").decode("ascii").lower()
            with self.subTest(origin=origin):
                self.assertFalse(
                    any(
                        fragment in searchable
                        for fragment in prohibited_fragments
                    )
                )


if __name__ == "__main__":
    unittest.main()
