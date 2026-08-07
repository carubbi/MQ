"""Estrutura editorial verificada de Pinheiro et al. (2009)."""

from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    finalize_source,
    item,
    numbered_editorial_nodes,
)


SOURCE = "pinheiro-2009"
CHAPTERS = [
    ("1", "Análise exploratória para uma variável", 18),
    ("2", "Estudando a relação entre duas variáveis", 59),
    ("3", "Introdução ao cálculo de probabilidades", 87),
    ("4", "Variáveis aleatórias", 112),
    ("5", "Variáveis aleatórias multidimensionais", 151),
    ("6", "Amostragem: uma ponte entre probabilidade e inferência", 172),
    ("7", "Estimação de parâmetros", 192),
    ("8", "Testes de hipótese", 229),
]
SECTIONS = [
    ("1.1", "Introdução", 20),
    ("1.2", "População e Amostra", 22),
    ("1.3", "Tipologia das Variáveis", 24),
    ("1.4", "Distribuições de Freqüências - Tabelas e Gráficos", 27),
    ("1.5", "Medidas de Centralidade para Variáveis Quantitativas", 35),
    ("1.6", "Medidas de Dispersão para Variáveis Quantitativas", 37),
    ("1.7", "O Conceito de Resistência de uma Medida", 43),
    ("1.8", "Identificação de Discrepâncias em Variáveis Quantitativas", 44),
    ("1.9", "Box Plot para Variáveis Quantitativas", 46),
    ("2.1", "Relação entre Variáveis Qualitativas - Tabelas de Contingência", 60),
    ("2.2", "Correlação entre Variáveis Quantitativas", 66),
    ("2.3", "O Ajuste da Reta de Regressão por Mínimos Quadrados", 72),
    ("3.1", "Alguns Conceitos Fundamentais", 89),
    ("3.2", "Propriedades Básicas da Probabilidade", 92),
    ("3.3", "Probabilidade Condicional e Independência de Eventos", 93),
    ("3.4", "Somar ou Multiplicar Probabilidades?", 97),
    ("4.1", "Introdução", 114),
    ("4.2", "Tipos de Variáveis Aleatórias", 115),
    ("4.3", "O Caso Discreto", 116),
    ("4.4", "O Caso Contínuo", 128),
    ("4.5", "A Distribuição Normal", 137),
    ("5.1", "O Caso de Duas Variáveis Aleatórias Discretas", 153),
    ("5.2", "Independência de Variáveis Aleatórias", 158),
    ("5.3", "Propriedades das Medidas de Centralidade, de Dispersão e de Interdependência", 161),
    ("6.1", "O Teorema Central do Limite", 174),
    ("6.2", "Aproximação da Binomial pela Normal", 180),
    ("6.3", "Amostragem Aleatória Simples", 182),
    ("6.4", "Amostral versus Populacional", 184),
    ("6.5", "A Abordagem dos Problemas Reais Através da Inferência Estatística", 185),
    ("7.1", "Parâmetro, Estimador e Estimativa", 194),
    ("7.2", "Estimador Pontual da Média Populacional", 196),
    ("7.3", "Estimação Pontual da Variância e do Desvio-padrão Populacionais", 202),
    ("7.4", "Estimação Pontual da Proporção Populacional", 204),
    ("7.5", "Viés, Variância e Erro Quadrático Médio de um Estimador", 208),
    ("7.6", "As Versões Amostral e Populacional de Vários Conceitos", 212),
    ("7.7", "Estimação por Intervalo", 212),
    ("8.1", "Conceitos Básicos", 231),
    ("8.2", "Esclarecendo Melhor Alguns Conceitos", 233),
    ("8.3", "Rotina para Obtenção do Critério de Decisão", 237),
    ("8.4", "Teste para a Média Populacional", 238),
    ("8.5", "O Conceito de Nível Crítico", 241),
    ("8.6", "O Poder do Teste", 244),
    ("8.7", "Teste para Proporções", 246),
    ("8.8", "Testes para Comparação de Duas Médias", 249),
    ("8.9", "Testes para Comparação de Várias Médias", 257),
    ("8.10", "Testando a Independência entre Duas Variáveis", 265),
]


def build_nodes() -> list[dict]:
    nodes = numbered_editorial_nodes(
        SOURCE,
        CHAPTERS,
        SECTIONS,
        terminal_page=281,
    )
    for number, page, parent in [
        ("1.4_P", 55, f"{SOURCE}-cap-1"),
        ("1.5_P", 55, f"{SOURCE}-cap-1"),
        ("1.7_P", 56, f"{SOURCE}-cap-1"),
        ("2.1_P", 81, f"{SOURCE}-cap-2"),
        ("2.2_P", 82, f"{SOURCE}-cap-2"),
        ("2.5_P", 83, f"{SOURCE}-cap-2"),
        ("2.7_P", 85, f"{SOURCE}-cap-2"),
    ]:
        nodes.append(
            item(
                SOURCE,
                number,
                page,
                parent,
                [],
                [],
                item_type="exercicio",
            )
        )
    for number, page, parent in [
        ("3.8_P", 111, f"{SOURCE}-cap-3"),
        ("3.9_P", 111, f"{SOURCE}-cap-3"),
        ("3.10_P", 111, f"{SOURCE}-cap-3"),
        ("4.3_P", 148, f"{SOURCE}-cap-4"),
        ("4.6_P", 149, f"{SOURCE}-cap-4"),
        ("4.7_P", 149, f"{SOURCE}-cap-4"),
        ("4.8_P", 149, f"{SOURCE}-cap-4"),
        ("4.9_P", 149, f"{SOURCE}-cap-4"),
    ]:
        nodes.append(
            item(
                SOURCE,
                number,
                page,
                parent,
                [],
                [],
                item_type="exercicio",
            )
        )
    apply_curricular_mappings(
        nodes,
        {
            f"{SOURCE}-sec-3-1": (
                [
                    "topico-experimento-aleatorio",
                    "topico-espaco-amostral",
                    "topico-evento",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-3-2": (
                ["topico-evento", "topico-regra-da-adicao"],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-3-3": (
                [
                    "topico-probabilidade-condicional",
                    "topico-regra-do-produto",
                    "topico-independencia",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-3-4": (
                [
                    "topico-regra-da-adicao",
                    "topico-regra-do-produto",
                    "topico-probabilidade-total",
                    "topico-teorema-de-bayes",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-4-2": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-variavel-aleatoria-continua",
                ],
                ["conteudo-02-02"],
            ),
            f"{SOURCE}-sec-4-3": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-funcao-de-probabilidade",
                    "topico-funcao-distribuicao-acumulada",
                    "topico-esperanca",
                    "topico-variancia",
                ],
                ["conteudo-02-02"],
            ),
            f"{SOURCE}-sec-4-4": (
                [
                    "topico-variavel-aleatoria-continua",
                    "topico-funcao-densidade",
                    "topico-funcao-distribuicao-acumulada",
                    "topico-esperanca",
                    "topico-variancia",
                    "topico-distribuicao-uniforme",
                    "topico-distribuicao-exponencial",
                ],
                ["conteudo-02-02", "conteudo-02-04"],
            ),
            f"{SOURCE}-sec-4-5": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-3-8-p": (
                [
                    "topico-probabilidade-condicional",
                    "topico-probabilidade-total",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-exercicio-3-9-p": (
                [
                    "topico-probabilidade-condicional",
                    "topico-probabilidade-total",
                    "topico-teorema-de-bayes",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-exercicio-3-10-p": (
                [
                    "topico-probabilidade-condicional",
                    "topico-probabilidade-total",
                    "topico-teorema-de-bayes",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-exercicio-4-3-p": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-funcao-de-probabilidade",
                    "topico-esperanca",
                    "topico-variancia",
                ],
                ["conteudo-02-02"],
            ),
            f"{SOURCE}-exercicio-4-6-p": (
                ["topico-distribuicao-binomial"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-exercicio-4-7-p": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-exercicio-4-8-p": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-4-9-p": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
        },
    )
    return finalize_source(SOURCE, nodes)
