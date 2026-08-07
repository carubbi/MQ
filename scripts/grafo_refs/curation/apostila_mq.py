"""Estrutura editorial verificada da apostila de Métodos Quantitativos."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    extract_sequential_numbered_items,
    item,
    load_extraction,
    merge_published_nodes,
    numbered_editorial_nodes,
)


SOURCE = "apostila-mq"
PDF_PATH = REPOSITORY_ROOT / "mat/apostila/apostila_mq.pdf"
CHAPTERS = [
    ("1", "Conceitos Básicos em Estatística", 8),
    ("2", "Estudos dos Dados Estatísticos", 11),
    ("3", "Distribuição de Frequências", 22),
    ("4", "Medidas de Posição", 27),
    ("5", "Medidas de Dispersão", 49),
    ("6", "Medidas de Assimetria e Curtose", 58),
    ("7", "Índices e Indicadores", 62),
    ("8", "Probabilidade", 74),
    ("9", "Variáveis Aleatórias Unidimensionais", 90),
    ("10", "Distribuições Discretas de Probabilidade", 96),
    ("11", "Distribuição Normal", 105),
    ("12", "Amostragem", 117),
    ("13", "Distribuições Amostrais", 125),
    ("14", "Estimação", 130),
    ("15", "Análise de Correlação e Regressão", 148),
    ("16", "Critérios de arredondamentos", 164),
    ("17", "Exercícios Propostos", 168),
]
SECTIONS = [
    ("1.1", "Divisão da Estatística", 8),
    ("1.2", "Conceitos Fundamentais", 8),
    ("1.3", "Fases do Método Estatístico", 10),
    ("2.1", "Séries Estatísticas", 11),
    ("2.2", "Apresentação Tabular e Gráfica", 12),
    ("2.2.1", "Apresentação Tabular", 12),
    ("2.2.2", "Apresentação Gráfica", 14),
    ("3.1", "Distribuição de Frequências para Dados Discretos", 23),
    ("3.2", "Distribuição de Frequências para Dados Contínuos", 24),
    ("4", "Medidas de Posição", 27),
    ("4.1", "Pequenos Conjuntos de Dados", 27),
    ("4.2", "Grandes conjuntos de dados: Discretos", 30),
    ("4.3", "Grandes conjuntos de dados: Contínuos", 32),
    ("4.4", "Medidas Separatrizes", 35),
    ("4.5", "Interpolação Linear", 42),
    ("4.6", "Outras Medidas de Posição", 44),
    ("5", "Medidas de Dispersão", 49),
    ("5.1", "Pequenos Conjuntos de dados", 49),
    ("5.2", "Grandes conjuntos de dados: Discretos", 53),
    ("5.3", "Grandes conjuntos de dados: Contínuos", 55),
    ("6.1", "Medidas de Assimetria", 58),
    ("6.2", "Medidas de Curtose", 59),
    ("7.1", "Valor Absoluto e Valor Relativo", 62),
    ("7.2", "Coeficientes", 63),
    ("7.3", "Índices", 63),
    ("7.4", "Indicadores de Desempenho", 69),
    ("8.1", "Conceitos iniciais", 74),
    ("8.2", "Operações com Eventos Aleatórios", 75),
    ("8.3", "Medida de Probabilidade", 78),
    ("8.4", "Teorema da Soma", 79),
    ("8.5", "Eventos Dependentes", 82),
    ("8.6", "Probabilidade Condicional", 82),
    ("8.7", "Teorema do Produto ou Regra do Produto", 83),
    ("8.8", "Eventos Independentes", 83),
    ("8.8.1", "Teorema do Produto ou Regra do Produto", 83),
    ("8.9", "Teorema de Bayes", 86),
    ("9.1", "Variáveis Aleatórias Discretas", 90),
    ("9.2", "Variáveis Aleatórias Contínuas", 92),
    ("9.3", "Propriedades da Esperança e da Variância", 94),
    ("10.1", "Distribuição Binomial", 96),
    ("10.2", "Distribuição de Poisson", 99),
    ("10.3", "Distribuição de Poisson como Aproximação da Binomial", 101),
    ("10.4", "Distribuição Hipergeométrica", 102),
    ("11.1", "Aproximação da Binomial pela Normal", 114),
    ("11.2", "Combinação Linear de Normais Independentes", 115),
    ("12.1", "Conceitos Fundamentais em Amostragem", 117),
    ("12.2", "Tipos de Amostragem", 119),
    ("12.3", "Uso do Excel na amostragem", 124),
    ("13.1", "Distribuição Amostral da Média", 125),
    ("13.2", "O Teorema do Limite Central", 125),
    ("13.3", "Distribuição Amostral da Proporção", 127),
    ("14.1", "Conceitos Fundamentais em estimação", 130),
    ("14.2", "Estimativa Pontual", 132),
    ("14.3", "Estimativa Intervalar ou Intervalo de Confiança para uma Amostra", 132),
    ("14.4", "Amostragem para População Finita", 140),
    ("14.5", "Estimativa Intervalar ou Intervalo de Confiança para Duas Amostras", 143),
    ("15.1", "Gráfico de dispersão", 148),
    ("15.2", "Coeficiente de Correlação de Pearson (Rxy)", 149),
    ("15.3", "Regressão Linear Simples", 150),
    ("15.4", "Regressão Linear Simples com Excel", 162),
    ("17.1", "Análise Descritiva", 168),
    ("17.2", "Introdução ao Estudo dos indicadores", 173),
    ("17.3", "Probabilidade", 174),
    ("17.4", "Variáveis Aleatórias", 177),
    ("17.5", "Distribuições Discretas", 180),
    ("17.6", "Distribuições Contínuas", 183),
    ("17.7", "Distribuição Normal", 183),
    ("17.8", "Distribuições Amostrais", 187),
    ("17.9", "Amostragem e Estimação", 188),
    ("17.10", "Análise de Correlação e Regressão", 191),
]
EXERCISE_PARENTS = (
    (1, 27, "17.1"),
    (28, 29, "17.2"),
    (30, 54, "17.3"),
    (55, 72, "17.4"),
    (73, 99, "17.5"),
    (100, 131, "17.7"),
    (132, 135, "17.8"),
    (136, 153, "17.9"),
    (154, 162, "17.10"),
)


def _exercise_parent(number: int) -> str:
    for first, last, section_number in EXERCISE_PARENTS:
        if first <= number <= last:
            return f"{SOURCE}-sec-{section_number.replace('.', '-')}"
    raise ValueError(f"exercício sem bloco editorial: {number}")


def build_nodes() -> list[dict]:
    nodes = numbered_editorial_nodes(
        SOURCE,
        CHAPTERS,
        SECTIONS,
        terminal_page=193,
    )
    nodes = [node for node in nodes if node["tipo"] not in {"exercicio", "questao"}]
    for node in nodes:
        if node["id"] in {
            "apostila-mq-sec-14-2",
            "apostila-mq-sec-14-3",
            "apostila-mq-sec-14-4",
            "apostila-mq-sec-14-5",
        }:
            node["numero_impresso"] = node["numero_impresso"].replace("14.", "13.")

    extracted = load_extraction(SOURCE, PDF_PATH)
    for number, page in extract_sequential_numbered_items(
        extracted,
        start_page=168,
        end_page=193,
        first_number=1,
        last_number=162,
    ):
        nodes.append(
            item(
                SOURCE,
                str(number),
                page,
                _exercise_parent(number),
                [],
                [],
                item_type="exercicio",
                pertinence="indireta",
            )
        )
    return merge_published_nodes(SOURCE, nodes)
