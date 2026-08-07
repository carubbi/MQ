"""Estrutura editorial verificada de Montgomery (2018)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    finalize_source,
    marker_numbered_nodes,
)


PDF_PATH = (
    REPOSITORY_ROOT
    / "prof/refs/livros/Montgomery 2018 Applied Statistics and Probability for Engineers.pdf"
)


def build_nodes() -> list[dict]:
    source = "montgomery-2018"
    nodes = marker_numbered_nodes(
        source,
        PDF_PATH,
        chapter_pattern=r"^Chapter (\d+):",
        section_pattern=r"^(\d+\.\d+(?:\.\d+)?)\s+",
        terminal_page=500,
    )
    apply_curricular_mappings(
        nodes,
        {
            f"{source}-sec-2-1-1": (
                ["topico-experimento-aleatorio"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-1-2": (
                ["topico-espaco-amostral"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-1-3": (
                ["topico-evento"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-3": (
                ["topico-experimento-aleatorio"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-4": (
                ["topico-regra-da-adicao"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-5": (
                ["topico-probabilidade-condicional"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-6": (
                ["topico-regra-do-produto", "topico-probabilidade-total"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-7": (
                ["topico-independencia"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-8": (
                ["topico-teorema-de-bayes"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-2-9": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-variavel-aleatoria-continua",
                ],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-3-1": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-funcao-de-probabilidade",
                ],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-3-2": (
                ["topico-funcao-distribuicao-acumulada"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-3-3": (
                ["topico-esperanca", "topico-variancia"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-4-1": (
                [
                    "topico-variavel-aleatoria-continua",
                    "topico-funcao-densidade",
                ],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-4-2": (
                ["topico-funcao-distribuicao-acumulada"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-4-3": (
                ["topico-esperanca", "topico-variancia"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-3-5": (
                ["topico-distribuicao-binomial"],
                ["conteudo-02-03"],
            ),
            f"{source}-sec-3-8": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{source}-sec-4-4": (
                ["topico-distribuicao-uniforme"],
                ["conteudo-02-04"],
            ),
            f"{source}-sec-4-5": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
            f"{source}-sec-4-7": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
            f"{source}-sec-6-7": (
                [
                    "topico-grafico-qq",
                    "topico-diagnostico-do-modelo",
                    "topico-distribuicao-normal",
                ],
                ["conteudo-02-04"],
            ),
        },
    )
    return finalize_source(
        source,
        nodes,
    )
