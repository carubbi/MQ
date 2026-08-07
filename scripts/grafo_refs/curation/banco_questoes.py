"""Estrutura editorial e questões verificadas do banco 2026.2."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    extract_sequential_numbered_items,
    item,
    load_extraction,
    finalize_source,
    numbered_editorial_nodes,
)


SOURCE = "banco-questoes-2026-2"
PDF_PATH = REPOSITORY_ROOT / "mat/apostila/banco_questoes_provas_2026_2.pdf"
CHAPTERS = [
    ("1", "Análise Descritiva", 7),
    ("2", "Momentos, Assimetria e Curtose", 88),
    ("3", "Probabilidade", 95),
    ("4", "Variáveis Aleatórias", 148),
    ("5", "Modelos Probabilísticos", 177),
    ("6", "Distribuições Amostrais", 251),
    ("7", "Amostragem", 261),
    ("8", "Estimação", 275),
    ("9", "Correlação e Regressão", 303),
    ("10", "Testes de Significância", 413),
    ("11", "ENADE", 432),
]
SECTIONS = [
    ("1.1", "Conceitos e Classificação", 7),
    ("1.1.2", "Variáveis", 8),
    ("1.1.3", "Séries Estatísticas: Elementos e Classificação", 11),
    ("1.2", "Tabela de Dupla Entrada", 13),
    ("1.3", "Gráficos", 15),
    ("1.3.1", "Análise Gráfica", 16),
    ("1.3.2", "Gráficos Especiais", 18),
    ("1.3.2.1", "Histograma", 18),
    ("1.3.2.2", "Gráfico de Tendência", 20),
    ("1.3.2.3", "Box Plot", 22),
    ("1.3.2.4", "Gráfico de Pareto", 29),
    ("1.3.2.5", "Fluxo de Processo", 33),
    ("2.1", "Medidas de Posição para Dados Agrupados e Não Agrupados", 34),
    ("2.2", "Propriedades das Medidas de Posição e Dispersão", 74),
    ("2.3", "Medidas Separatrizes", 82),
    ("2.4", "Médias Geométrica, Harmônica, Ponderada e Quadrática", 84),
    ("2.4.1", "Média Geométrica", 84),
    ("2.4.2", "Média Harmônica", 84),
    ("2.4.3", "Média Ponderada", 85),
    ("2.4.4", "Média Quadrática", 87),
    ("3.1", "Momentos", 88),
    ("3.2", "Assimetria", 89),
    ("3.3", "Curtose", 92),
    ("5.1", "Modelos Discretos", 177),
    ("5.1.1", "Distribuição Binomial", 177),
    ("5.1.2", "Distribuição de Poisson", 184),
    ("5.1.3", "Distribuição Hipergeométrica", 192),
    ("5.1.4", "Distribuição Geométrica", 199),
    ("5.1.5", "Distribuição Binomial Negativa", 202),
    ("5.1.6", "Distribuição Uniforme Discreta", 205),
    ("5.1.7", "Distribuição Multinomial", 206),
    ("5.2", "Modelos Contínuos", 209),
    ("5.2.1", "Distribuição Normal", 209),
    ("5.2.2", "Distribuição Exponencial Negativa", 224),
    ("5.2.3", "Distribuição Beta", 233),
    ("5.2.4", "Distribuição Uniforme Contínua", 235),
    ("5.2.5", "Distribuição Gama", 243),
    ("5.2.6", "Distribuição Weibull", 245),
    ("5.2.7", "Distribuição LogNormal", 247),
    ("6.1", "Distribuição Amostral da Média", 251),
    ("6.2", "Distribuição Amostral da Proporção", 257),
    ("6.3", "Distribuição Amostral da Variância", 259),
    ("8.1", "Intervalo de Confiança para Média", 275),
    ("8.2", "Intervalo de Confiança para Proporção", 290),
    ("8.3", "Intervalo de Confiança para Variância", 299),
    ("9.1", "Regressão Simples", 303),
    ("9.2", "Regressão Múltipla", 372),
    ("10.1", "Teste de Significância para Média", 413),
    ("10.2", "Teste de Significância para Proporção", 422),
    ("10.3", "Teste de Significância para Variância", 428),
]


def build_nodes() -> list[dict]:
    nodes = numbered_editorial_nodes(
        SOURCE,
        CHAPTERS,
        SECTIONS,
        terminal_page=470,
    )
    nodes = [node for node in nodes if node["tipo"] != "questao"]
    extracted = load_extraction(SOURCE, PDF_PATH)
    for number, page in extract_sequential_numbered_items(
        extracted,
        start_page=7,
        end_page=94,
        first_number=1,
        last_number=259,
    ):
        nodes.append(
            item(
                SOURCE,
                str(number),
                page,
                f"{SOURCE}-cap-1",
                [],
                [],
                item_type="questao",
                pertinence="indireta",
            )
        )
    apply_curricular_mappings(
        nodes,
        {
            f"{SOURCE}-sec-5-1-1": (
                ["topico-distribuicao-binomial"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-sec-5-1-2": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-sec-5-2-1": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-sec-5-2-2": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-sec-5-2-4": (
                ["topico-distribuicao-uniforme"],
                ["conteudo-02-04"],
            ),
        },
    )
    return finalize_source(SOURCE, nodes)
