"""Estrutura editorial verificada de Navidi (2024)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    finalize_source,
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
            f"{source}-sec-4-10": (
                [
                    "topico-distribuicao-normal",
                    "topico-grafico-qq",
                    "topico-diagnostico-do-modelo",
                ],
                ["conteudo-02-04"],
            ),
        },
    )
    return finalize_source(
        source,
        nodes,
    )
