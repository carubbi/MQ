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
            f"{source}-sec-10-2": (
                ["topico-populacao", "topico-amostra", "topico-representatividade"],
                ["conteudo-03-01"],
            ),
            f"{source}-sec-10-4": (
                ["topico-amostragem", "topico-representatividade"],
                ["conteudo-03-01"],
            ),
            f"{source}-sec-10-5": (
                ["topico-amostragem", "topico-amostragem-aleatoria-simples"],
                ["conteudo-03-01"],
            ),
            f"{source}-sec-10-6": (
                ["topico-estimacao-pontual"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-10-7": (
                ["topico-distribuicao-amostral"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-10-8": (
                [
                    "topico-distribuicao-amostral",
                    "topico-teorema-central-do-limite",
                    "topico-erro-padrao",
                    "topico-tamanho-amostral",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-10-9": (
                [
                    "topico-distribuicao-amostral",
                    "topico-erro-padrao",
                    "topico-tamanho-amostral",
                ],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-11-1": (
                ["topico-estatistica-inferencial", "topico-estimacao-pontual"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-11-6": (
                ["topico-intervalo-de-confianca", "topico-margem-de-erro"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-11-7": (
                ["topico-estimacao-pontual", "topico-erro-padrao"],
                ["conteudo-03-02"],
            ),
            f"{source}-sec-12-3": (
                [
                    "topico-hipotese-nula",
                    "topico-hipotese-alternativa",
                    "topico-nivel-de-significancia",
                    "topico-erro-tipo-i",
                    "topico-erro-tipo-ii",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-12-4": (
                [
                    "topico-hipotese-nula",
                    "topico-hipotese-alternativa",
                    "topico-nivel-de-significancia",
                ],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-12-5": (
                ["topico-teste-para-media"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-12-6": (
                ["topico-teste-para-proporcao"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-12-7": (
                ["topico-erro-tipo-ii", "topico-poder-do-teste"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-12-8": (
                ["topico-nivel-de-significancia", "topico-valor-p"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-12-10": (
                ["topico-teste-para-media"],
                ["conteudo-03-03"],
            ),
            f"{source}-sec-16-2": (
                [
                    "topico-regressao-linear-simples",
                    "topico-minimos-quadrados",
                    "topico-residuo",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-16-3": (
                [
                    "topico-regressao-linear-simples",
                    "topico-coeficiente-de-determinacao",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-valor-p",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-16-4": (
                [
                    "topico-regressao-linear-simples",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-intervalo-de-confianca",
                ],
                ["conteudo-03-04"],
            ),
            f"{source}-sec-16-5": (
                [
                    "topico-residuo",
                    "topico-diagnostico-do-modelo",
                    "topico-grafico-qq",
                    "topico-valor-discrepante",
                ],
                ["conteudo-03-04"],
            ),
        },
    )
    return finalize_source(source, nodes)
