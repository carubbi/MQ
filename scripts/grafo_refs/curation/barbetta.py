"""Estrutura editorial verificada de Barbetta, Reis e Bornia (2010)."""

from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    finalize_source,
    item,
    numbered_editorial_nodes,
)


SOURCE = "barbetta-2010"
CHAPTERS = [
    ("1", "Introdução", 12),
    ("2", "O planejamento de uma pesquisa", 24),
    ("3", "Análise exploratória de dados", 51),
    ("4", "Probabilidade", 92),
    ("5", "Variáveis aleatórias discretas", 117),
    ("6", "Variáveis aleatórias contínuas", 141),
    ("7", "Distribuições amostrais e estimação de parâmetros", 170),
    ("8", "Testes de hipóteses", 199),
    ("9", "Comparação entre tratamentos", 233),
    ("10", "Testes não paramétricos", 274),
    ("11", "Correlação e regressão", 317),
]
SECTIONS = [
    ("1.1", "A estatística", 12),
    ("1.2", "Pesquisas, dados, variabilidade e estatística", 13),
    ("1.3", "A estatística na engenharia", 14),
    ("1.4", "A estatística e a informática", 15),
    ("1.5", "Modelos", 16),
    ("1.6", "Conceitos básicos", 18),
    ("2.1", "Aspectos gerais", 24),
    ("2.2", "Pesquisas de levantamento", 25),
    ("2.2.1", "Procedimentos de amostragem", 25),
    ("2.2.2", "Tamanho da amostra", 32),
    ("2.3", "Planejamento de experimentos", 34),
    ("3.1", "Dados e variáveis", 52),
    ("3.2", "Análise de variáveis qualitativas", 54),
    ("3.3", "Análise de variáveis quantitativas", 59),
    ("3.4", "Medidas descritivas", 69),
    ("3.5", "Observações ao longo do tempo", 84),
    ("3.6", "Análise exploratória com apoio do computador", 85),
    ("3.7", "Orientação geral", 86),
    ("4.1", "Espaço amostral e eventos", 94),
    ("4.2", "Definições de probabilidade", 97),
    ("4.3", "Probabilidade condicional e independência", 103),
    ("4.4", "Teorema da probabilidade total", 111),
    ("4.5", "Teorema de Bayes", 113),
    ("5.1", "Variável aleatória", 117),
    ("5.2", "Principais distribuições discretas", 127),
    ("6.1", "Caracterização de uma variável aleatória contínua", 141),
    ("6.2", "Principais modelos contínuos", 148),
    ("6.3", "A normal como limite de outras distribuições", 160),
    ("6.4", "Gráfico de probabilidade normal", 165),
    ("7.1", "Parâmetros e estatísticas", 170),
    ("7.2", "Distribuições amostrais", 175),
    ("7.3", "Estimação de parâmetros", 180),
    ("7.4", "Tamanho de amostra", 193),
    ("8.1", "As hipóteses", 199),
    ("8.2", "Conceitos básicos", 202),
    ("8.3", "Tipos de erro", 206),
    ("8.4", "Abordagem clássica", 207),
    ("8.5", "Testes unilaterais e bilaterais", 209),
    ("8.6", "Aplicação de testes estatísticos", 212),
    ("8.7", "Teste para proporção", 213),
    ("8.8", "Teste para média", 218),
    ("8.9", "Teste para variância", 223),
    ("8.10", "Poder de um teste e tamanho da amostra", 225),
    ("9.1", "Amostras independentes e em blocos", 233),
    ("9.2", "Teste t para duas amostras pareadas", 236),
    ("9.3", "Teste t para duas amostras independentes", 239),
    ("9.4", "Tamanho das amostras", 243),
    ("9.5", "Teste F para duas variâncias", 248),
    ("9.6", "Comparação de várias médias", 249),
    ("9.7", "Anova em projetos fatoriais", 259),
    ("9.8", "Anova em projetos do tipo 2k", 264),
    ("10.1", "Testes de aderência", 275),
    ("10.2", "Análise de associação", 288),
    ("10.3", "Testes para duas populações", 294),
    ("11.1", "Correlação", 317),
    ("11.2", "Coeficiente de correlação linear de Pearson", 319),
    ("11.3", "Regressão linear simples", 325),
    ("11.4", "Introdução à regressão múltipla", 347),
]


def build_nodes() -> list[dict]:
    nodes = numbered_editorial_nodes(
        SOURCE,
        CHAPTERS,
        SECTIONS,
        terminal_page=350,
    )
    for number, page, parent in [
        ("1.2", 23, f"{SOURCE}-cap-1"),
        ("2.7", 34, f"{SOURCE}-cap-2"),
        ("3.4", 87, f"{SOURCE}-cap-3"),
        ("3.8", 88, f"{SOURCE}-cap-3"),
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
    for number, identifier, page, parent in [
        ("1", "5-1", 126, f"{SOURCE}-sec-5-1"),
        ("7", "5-7", 132, f"{SOURCE}-sec-5-2"),
        ("11", "5-11", 137, f"{SOURCE}-sec-5-2"),
        ("1", "6-1", 147, f"{SOURCE}-sec-6-1"),
        ("2", "6-2", 147, f"{SOURCE}-sec-6-1"),
        ("6", "6-6", 153, f"{SOURCE}-sec-6-2"),
        ("8", "6-8", 159, f"{SOURCE}-sec-6-2"),
        ("13", "6-13", 167, f"{SOURCE}-cap-6"),
        ("17", "6-17", 168, f"{SOURCE}-cap-6"),
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
                identifier=identifier,
            )
        )
    apply_curricular_mappings(
        nodes,
        {
            f"{SOURCE}-sec-4-1": (
                [
                    "topico-experimento-aleatorio",
                    "topico-espaco-amostral",
                    "topico-evento",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-4-2": (
                ["topico-evento", "topico-regra-da-adicao"],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-4-3": (
                [
                    "topico-probabilidade-condicional",
                    "topico-regra-do-produto",
                    "topico-independencia",
                ],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-4-4": (
                ["topico-probabilidade-total"],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-4-5": (
                ["topico-teorema-de-bayes"],
                ["conteudo-02-01"],
            ),
            f"{SOURCE}-sec-5-1": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-funcao-de-probabilidade",
                    "topico-funcao-distribuicao-acumulada",
                    "topico-esperanca",
                    "topico-variancia",
                ],
                ["conteudo-02-02"],
            ),
            f"{SOURCE}-sec-5-2": (
                [
                    "topico-distribuicao-binomial",
                    "topico-distribuicao-poisson",
                ],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-sec-6-1": (
                [
                    "topico-variavel-aleatoria-continua",
                    "topico-funcao-densidade",
                    "topico-funcao-distribuicao-acumulada",
                    "topico-esperanca",
                    "topico-variancia",
                ],
                ["conteudo-02-02"],
            ),
            f"{SOURCE}-sec-6-2": (
                [
                    "topico-distribuicao-uniforme",
                    "topico-distribuicao-exponencial",
                    "topico-distribuicao-normal",
                    "topico-padronizacao",
                ],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-sec-6-4": (
                [
                    "topico-distribuicao-normal",
                    "topico-grafico-qq",
                    "topico-diagnostico-do-modelo",
                ],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-5-1": (
                [
                    "topico-variavel-aleatoria-discreta",
                    "topico-funcao-de-probabilidade",
                ],
                ["conteudo-02-02"],
            ),
            f"{SOURCE}-exercicio-5-7": (
                ["topico-distribuicao-binomial"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-exercicio-5-11": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-exercicio-6-1": (
                [
                    "topico-variavel-aleatoria-continua",
                    "topico-funcao-densidade",
                    "topico-funcao-distribuicao-acumulada",
                    "topico-esperanca",
                    "topico-variancia",
                    "topico-distribuicao-uniforme",
                ],
                ["conteudo-02-02", "conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-6-2": (
                [
                    "topico-funcao-densidade",
                    "topico-distribuicao-uniforme",
                    "topico-esperanca",
                    "topico-variancia",
                ],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-6-6": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-6-8": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-6-13": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-exercicio-6-17": (
                ["topico-distribuicao-normal", "topico-padronizacao"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-sec-2-2-1": (
                [
                    "topico-amostragem",
                    "topico-amostragem-aleatoria-simples",
                    "topico-amostragem-estratificada",
                    "topico-amostragem-sistematica",
                    "topico-amostragem-por-conglomerados",
                    "topico-amostragem-por-conveniencia",
                    "topico-representatividade",
                ],
                ["conteudo-03-01"],
            ),
            f"{SOURCE}-sec-7-1": (
                ["topico-estimacao-pontual"],
                ["conteudo-03-02"],
            ),
            f"{SOURCE}-sec-7-2": (
                ["topico-distribuicao-amostral", "topico-erro-padrao"],
                ["conteudo-03-02"],
            ),
            f"{SOURCE}-sec-7-3": (
                [
                    "topico-estimacao-pontual",
                    "topico-intervalo-de-confianca",
                    "topico-margem-de-erro",
                ],
                ["conteudo-03-02"],
            ),
            f"{SOURCE}-sec-8-1": (
                ["topico-hipotese-nula", "topico-hipotese-alternativa"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-8-2": (
                ["topico-nivel-de-significancia", "topico-valor-p"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-8-3": (
                ["topico-erro-tipo-i", "topico-erro-tipo-ii"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-8-5": (
                ["topico-hipotese-nula", "topico-hipotese-alternativa"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-8-7": (
                ["topico-teste-para-proporcao"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-8-8": (
                ["topico-teste-para-media"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-8-10": (
                ["topico-poder-do-teste"],
                ["conteudo-03-03"],
            ),
            f"{SOURCE}-sec-11-3": (
                [
                    "topico-regressao-linear-simples",
                    "topico-minimos-quadrados",
                    "topico-coeficiente-de-determinacao",
                    "topico-coeficiente-de-determinacao-ajustado",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-residuo",
                    "topico-diagnostico-do-modelo",
                ],
                ["conteudo-03-04"],
            ),
            f"{SOURCE}-sec-11-4": (
                [
                    "topico-regressao-linear-multipla",
                    "topico-variavel-indicadora",
                    "topico-inferencia-sobre-coeficientes",
                    "topico-residuo",
                ],
                ["conteudo-03-04"],
            ),
        },
    )
    return finalize_source(SOURCE, nodes)
