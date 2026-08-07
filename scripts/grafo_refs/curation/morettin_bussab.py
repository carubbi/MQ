"""Estrutura editorial verificada de Morettin e Bussab (2010)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    finalize_source,
    marker_numbered_nodes,
    section,
)


PDF_PATH = (
    REPOSITORY_ROOT
    / "prof/refs/livros/P. A. Morettin, W. de O. Bussab - Estatística Básica-Saraiva (2010).pdf"
)
CHAPTER_TITLES = {
    "1": "Preliminares",
    "2": "Resumo de dados",
    "3": "Medidas-resumo",
    "4": "Análise bidimensional",
    "5": "Probabilidade",
    "6": "Variáveis aleatórias discretas",
    "7": "Variáveis aleatórias contínuas",
    "8": "Variáveis aleatórias multidimensionais",
    "9": "Simulação",
    "10": "Noções de amostragem",
    "11": "Estimação",
    "12": "Testes de hipóteses",
    "13": "Inferência para duas populações",
    "14": "Análise de aderência e associação",
    "15": "Inferência para várias populações",
    "16": "Regressão linear simples",
}


def build_nodes() -> list[dict]:
    source = "morettin-bussab-2010"
    nodes = marker_numbered_nodes(
        source,
        PDF_PATH,
        chapter_pattern=r"^Capítulo (\d+)$",
        section_pattern=r"^(\d+\.\d+)\s+",
        terminal_page=511,
        chapter_titles=CHAPTER_TITLES,
    )
    nodes.extend(
        [
            section(
                source,
                "2.3.1",
                "Gráficos para variáveis qualitativas",
                32,
                32,
                f"{source}-sec-2-3",
                [],
                [],
            ),
            section(
                source,
                "2.3.2",
                "Gráficos para variáveis quantitativas",
                33,
                36,
                f"{source}-sec-2-3",
                [],
                [],
            ),
        ]
    )
    apply_curricular_mappings(
        nodes,
        {
            f"{source}-sec-5-1": (
                [
                    "topico-experimento-aleatorio",
                    "topico-espaco-amostral",
                    "topico-evento",
                ],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-5-2": (
                ["topico-evento", "topico-regra-da-adicao"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-5-3": (
                [
                    "topico-probabilidade-condicional",
                    "topico-regra-do-produto",
                    "topico-independencia",
                ],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-5-4": (
                ["topico-probabilidade-total", "topico-teorema-de-bayes"],
                ["conteudo-02-01"],
            ),
            f"{source}-sec-6-2": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-funcao-de-probabilidade",
                ],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-6-3": (
                ["topico-esperanca", "topico-variancia"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-6-5": (
                ["topico-funcao-distribuicao-acumulada"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-6-6": (
                [
                    "topico-distribuicao-binomial",
                    "topico-distribuicao-poisson",
                ],
                ["conteudo-02-03"],
            ),
            f"{source}-sec-7-1": (
                [
                    "topico-variavel-aleatoria-continua",
                    "topico-funcao-densidade",
                ],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-7-2": (
                ["topico-esperanca", "topico-variancia"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-7-3": (
                ["topico-funcao-distribuicao-acumulada"],
                ["conteudo-02-02"],
            ),
            f"{source}-sec-6-7": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{source}-sec-7-4": (
                [
                    "topico-distribuicao-uniforme",
                    "topico-distribuicao-normal",
                    "topico-distribuicao-exponencial",
                    "topico-padronizacao",
                ],
                ["conteudo-02-04"],
            ),
        },
    )
    return finalize_source(source, nodes)
