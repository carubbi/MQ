"""Estrutura editorial verificada de Navidi (2024)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    finalize_source,
    item,
    marker_numbered_nodes,
)


PDF_PATH = (
    REPOSITORY_ROOT
    / "prof/refs/livros/Navidi 2024 Statistics for Engineers and Scientists.pdf"
)


def build_nodes() -> list[dict]:
    source = "navidi-2024"
    nodes = marker_numbered_nodes(
        source,
        PDF_PATH,
        chapter_pattern=r"^Chapter (\d+)\s+",
        section_pattern=r"^(\d+\.\d+)\s+",
        terminal_page=838,
        include_introductions=True,
    )
    nodes.extend(
        [
            item(
                source,
                "1.1",
                26,
                f"{source}-sec-1-1",
                [],
                [],
                item_type="exemplo",
            ),
            item(
                source,
                "2",
                34,
                f"{source}-sec-1-1",
                [],
                [],
                item_type="exercicio",
                identifier="1-1-2",
            ),
        ]
    )
    apply_curricular_mappings(
        nodes,
        {
            f"{source}-sec-2-1": (
                [
                    "topico-experimento-aleatorio",
                    "topico-espaco-amostral",
                    "topico-evento",
                    "topico-regra-da-adicao",
                ],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-3": (
                [
                    "topico-probabilidade-condicional",
                    "topico-regra-do-produto",
                    "topico-independencia",
                    "topico-probabilidade-total",
                    "topico-teorema-de-bayes",
                ],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-4": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-variavel-aleatoria-continua",
                    "topico-funcao-de-probabilidade",
                    "topico-funcao-densidade",
                    "topico-funcao-distribuicao-acumulada",
                    "topico-esperanca",
                    "topico-variancia",
                ],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-4-2": (
                ["topico-distribuicao-binomial"],
                ["conteudo-02-03"],
            ),
            f"{source}-sec-4-3": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{source}-sec-4-5": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
            f"{source}-sec-4-7": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
            f"{source}-sec-4-8": (
                ["topico-distribuicao-uniforme"],
                ["conteudo-02-04"],
            ),
            f"{source}-sec-4-10": (
                [
                    "topico-distribuicao-normal",
                    "topico-grafico-qq",
                    "topico-diagnostico-do-modelo",
                ],
                ["conteudo-02-04"],
            ),
            f"{source}-exemplo-1-1": (
                [
                    "topico-populacao",
                    "topico-amostra",
                    "topico-amostragem",
                    "topico-representatividade",
                    "topico-amostragem-aleatoria-simples",
                ],
                ["conteudo-03-01"],
            ),
            f"{source}-exercicio-1-1-2": (
                [
                    "topico-amostragem",
                    "topico-representatividade",
                    "topico-amostragem-por-conveniencia",
                ],
                ["conteudo-03-01"],
            ),
            f"{source}-sec-4-9": (
                ["topico-estimacao-pontual"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-4-11": (
                [
                    "topico-distribuicao-amostral",
                    "topico-teorema-central-do-limite",
                    "topico-erro-padrao",
                    "topico-tamanho-amostral",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-5-1": (
                [
                    "topico-estimacao-pontual",
                    "topico-intervalo-de-confianca",
                    "topico-margem-de-erro",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-5-2": (
                [
                    "topico-estimacao-pontual",
                    "topico-intervalo-de-confianca",
                    "topico-margem-de-erro",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-5-3": (
                [
                    "topico-estimacao-pontual",
                    "topico-intervalo-de-confianca",
                    "topico-margem-de-erro",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-6-1": (
                [
                    "topico-hipotese-nula",
                    "topico-hipotese-alternativa",
                    "topico-nivel-de-significancia",
                    "topico-valor-p",
                    "topico-teste-para-media",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-6-2": (
                [
                    "topico-nivel-de-significancia",
                    "topico-valor-p",
                    "topico-erro-tipo-i",
                    "topico-erro-tipo-ii",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-6-3": (
                ["topico-teste-para-media"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-6-4": (
                ["topico-teste-para-proporcao"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-6-11": (
                [
                    "topico-hipotese-nula",
                    "topico-hipotese-alternativa",
                    "topico-nivel-de-significancia",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-6-12": (
                ["topico-erro-tipo-ii", "topico-poder-do-teste"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-7-2": (
                [
                    "topico-regressao-linear-simples",
                    "topico-minimos-quadrados",
                    "topico-coeficiente-de-determinacao",
                    "topico-residuo",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-7-3": (
                [
                    "topico-regressao-linear-simples",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-intervalo-de-confianca",
                    "topico-valor-p",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-7-4": (
                [
                    "topico-residuo",
                    "topico-diagnostico-do-modelo",
                    "topico-grafico-qq",
                    "topico-valor-discrepante",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-8-1": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-minimos-quadrados",
                    "topico-coeficiente-de-determinacao",
                    "topico-coeficiente-de-determinacao-ajustado",
                    "topico-residuo",
                    "topico-inferencia-sobre-coeficientes",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-8-2": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-diagnostico-do-modelo",
                ],
                ["conteudo-03-04"],
            ),
        },
    )
    return finalize_source(
        source,
        nodes,
    )
