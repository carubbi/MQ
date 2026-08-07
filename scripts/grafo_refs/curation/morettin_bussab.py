"""Estrutura editorial verificada de Morettin e Bussab (2010)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import marker_numbered_nodes


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
    return marker_numbered_nodes(
        "morettin-bussab-2010",
        PDF_PATH,
        chapter_pattern=r"^Capítulo (\d+)$",
        section_pattern=r"^(\d+\.\d+)\s+",
        terminal_page=511,
        chapter_titles=CHAPTER_TITLES,
    )
