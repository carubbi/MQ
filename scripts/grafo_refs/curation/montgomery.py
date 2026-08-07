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
            f"{source}-sec-7-1": (
                ["topico-estatistica-inferencial", "topico-estimacao-pontual"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-7-2": (
                [
                    "topico-distribuicao-amostral",
                    "topico-teorema-central-do-limite",
                    "topico-erro-padrao",
                    "topico-tamanho-amostral",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-7-3-3": (
                ["topico-estimacao-pontual", "topico-erro-padrao"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-8-1-1": (
                ["topico-intervalo-de-confianca", "topico-margem-de-erro"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-8-1-5": (
                ["topico-intervalo-de-confianca", "topico-margem-de-erro"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-8-2-1": (
                ["topico-intervalo-de-confianca"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-8-2-2": (
                ["topico-intervalo-de-confianca", "topico-margem-de-erro"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-8-4": (
                [
                    "topico-estimacao-pontual",
                    "topico-intervalo-de-confianca",
                    "topico-margem-de-erro",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-8-5": (
                ["topico-intervalo-de-confianca", "topico-margem-de-erro"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-9-1-1": (
                ["topico-hipotese-nula", "topico-hipotese-alternativa"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-1-2": (
                [
                    "topico-hipotese-nula",
                    "topico-hipotese-alternativa",
                    "topico-nivel-de-significancia",
                    "topico-erro-tipo-i",
                    "topico-erro-tipo-ii",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-1-3": (
                ["topico-hipotese-alternativa"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-1-4": (
                ["topico-nivel-de-significancia", "topico-valor-p"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-1-5": (
                ["topico-intervalo-de-confianca", "topico-valor-p"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-1-6": (
                [
                    "topico-hipotese-nula",
                    "topico-hipotese-alternativa",
                    "topico-nivel-de-significancia",
                    "topico-valor-p",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-2-1": (
                ["topico-teste-para-media"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-3-1": (
                ["topico-teste-para-media"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-9-5-1": (
                ["topico-teste-para-proporcao"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-11-2": (
                [
                    "topico-regressao-linear-simples",
                    "topico-minimos-quadrados",
                    "topico-residuo",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-11-3": (
                ["topico-regressao-linear-simples", "topico-minimos-quadrados"],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-11-4-1": (
                [
                    "topico-regressao-linear-simples",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-valor-p",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-11-5-1": (
                [
                    "topico-inferencia-sobre-coeficientes",
                    "topico-intervalo-de-confianca",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-11-7-1": (
                [
                    "topico-residuo",
                    "topico-diagnostico-do-modelo",
                    "topico-grafico-qq",
                    "topico-valor-discrepante",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-11-7-2": (
                ["topico-coeficiente-de-determinacao"],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-1-1": (
                ["topico-regressao-linear-multipla"],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-1-2": (
                ["topico-regressao-linear-multipla", "topico-minimos-quadrados"],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-2-2": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-valor-p",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-3-1": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-intervalo-de-confianca",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-5-1": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-residuo",
                    "topico-diagnostico-do-modelo",
                    "topico-grafico-qq",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-5-2": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-diagnostico-do-modelo",
                    "topico-valor-discrepante",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-6-2": (
                ["topico-regressao-linear-multipla", "topico-variavel-indicadora"],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-12-6-4": (
                ["topico-regressao-linear-multipla", "topico-diagnostico-do-modelo"],
                ["conteudo-03-04"],
            ),
        },
    )
    return finalize_source(
        source,
        nodes,
    )
