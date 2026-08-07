"""Preserva as oito curadorias verificadas da Unidade I."""

import json

from scripts.grafo_refs.build_graph import (
    REPOSITORY_ROOT,
)
from scripts.grafo_refs.curation.common import (
    chapter as make_chapter,
    extract_sequential_numbered_items,
    item,
    section,
)


EXTRACTION_DIRECTORY = REPOSITORY_ROOT / "tmp/grafo_refs"


def _bank_curated() -> list[dict]:
    source = "banco-questoes-2026-2"
    chapter_id = f"{source}-cap-1"
    nodes = [make_chapter(source, "1", "Análise Descritiva", 7, 94)]
    sections = [
        ("1.1", "Conceitos e classificação", 7, 12,
         ["topico-investigacao-estatistica", "topico-tipos-de-variaveis"],
         ["conteudo-01-01", "conteudo-01-02"]),
        ("1.2", "Tabela de dupla entrada", 13, 14,
         ["topico-tabela", "topico-tabela-de-contingencia"],
         ["conteudo-01-02", "conteudo-01-04"]),
        ("1.3", "Gráficos", 15, 33,
         ["topico-grafico", "topico-frequencia", "topico-boxplot"],
         ["conteudo-01-02", "conteudo-01-03"]),
        ("2.1", "Medidas de posição para dados agrupados e não agrupados", 34, 73,
         ["topico-media", "topico-mediana", "topico-moda", "topico-variancia", "topico-desvio-padrao"],
         ["conteudo-01-03"]),
        ("2.2", "Propriedades das medidas de posição e dispersão", 74, 81,
         ["topico-media", "topico-variancia", "topico-desvio-padrao", "topico-coeficiente-de-variacao"],
         ["conteudo-01-03"]),
        ("2.3", "Medidas separatrizes", 82, 83,
         ["topico-mediana", "topico-quantil", "topico-intervalo-interquartil"],
         ["conteudo-01-03"]),
        ("2.4", "Médias geométrica, harmônica, ponderada e quadrática", 84, 87,
         ["topico-media"], ["conteudo-01-03"]),
        ("3.1", "Momentos", 88, 88,
         ["topico-media", "topico-variancia"], ["conteudo-01-03"]),
        ("3.2", "Assimetria", 89, 91,
         ["topico-assimetria"], ["conteudo-01-03"]),
        ("3.3", "Curtose", 92, 94,
         ["topico-assimetria"], ["conteudo-01-03"]),
    ]
    for number, title, start, end, topics, contents in sections:
        nodes.append(
            section(source, number, title, start, end, chapter_id, topics, contents)
        )
    leaf_sections = [
        ("1.1.2", "Variáveis", 8, 10, "1.1",
         ["topico-tipos-de-variaveis"], ["conteudo-01-02"]),
        ("1.1.3", "Séries estatísticas: elementos e classificação", 11, 12, "1.1",
         ["topico-tabela", "topico-tipos-de-variaveis"], ["conteudo-01-02"]),
        ("1.3.1", "Análise gráfica", 16, 17, "1.3",
         ["topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("1.3.2", "Gráficos especiais", 18, 33, "1.3",
         ["topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("1.3.2.1", "Histograma", 18, 19, "1.3.2",
         ["topico-frequencia", "topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("1.3.2.2", "Gráfico de tendência", 20, 21, "1.3.2",
         ["topico-grafico"], ["conteudo-01-02"]),
        ("1.3.2.3", "Box plot", 22, 28, "1.3.2",
         ["topico-boxplot", "topico-valor-discrepante"], ["conteudo-01-03"]),
        ("1.3.2.4", "Gráfico de Pareto", 29, 32, "1.3.2",
         ["topico-frequencia", "topico-grafico"], ["conteudo-01-02"]),
        ("1.3.2.5", "Fluxo de processo", 33, 33, "1.3.2",
         ["topico-grafico"], ["conteudo-01-02"]),
        ("2.4.1", "Média geométrica", 84, 84, "2.4",
         ["topico-media"], ["conteudo-01-03"]),
        ("2.4.2", "Média harmônica", 84, 84, "2.4",
         ["topico-media"], ["conteudo-01-03"]),
        ("2.4.3", "Média ponderada", 85, 86, "2.4",
         ["topico-media"], ["conteudo-01-03"]),
        ("2.4.4", "Média quadrática", 87, 87, "2.4",
         ["topico-media"], ["conteudo-01-03"]),
    ]
    for number, title, start, end, parent, topics, contents in leaf_sections:
        nodes.append(
            section(
                source,
                number,
                title,
                start,
                end,
                f"{source}-sec-{parent.replace('.', '-')}",
                topics,
                contents,
            )
        )

    extracted = json.loads(
        (EXTRACTION_DIRECTORY / f"{source}.extract.json").read_text(
            encoding="utf-8"
        )
    )
    for number, page in extract_sequential_numbered_items(
        extracted,
        start_page=7,
        end_page=94,
        first_number=1,
        last_number=259,
    ):
        if number <= 6:
            parent = f"{source}-sec-1-1"
            topics = ["topico-investigacao-estatistica", "topico-populacao", "topico-amostra"]
            contents = ["conteudo-01-01"]
        elif number <= 24:
            parent = f"{source}-sec-1-1"
            topics = ["topico-tipos-de-variaveis", "topico-tabela"]
            contents = ["conteudo-01-02"]
        elif number <= 32:
            parent = f"{source}-sec-1-2"
            topics = ["topico-tabela", "topico-tabela-de-contingencia", "topico-associacao"]
            contents = ["conteudo-01-02", "conteudo-01-04"]
        elif number <= 73:
            parent = f"{source}-sec-1-3"
            topics = ["topico-grafico", "topico-frequencia", "topico-boxplot"]
            contents = ["conteudo-01-02", "conteudo-01-03"]
        elif number <= 168:
            parent = f"{source}-sec-2-1"
            topics = ["topico-media", "topico-mediana", "topico-moda", "topico-desvio-padrao"]
            contents = ["conteudo-01-03"]
        elif number <= 198:
            parent = f"{source}-sec-2-2"
            topics = ["topico-media", "topico-variancia", "topico-coeficiente-de-variacao"]
            contents = ["conteudo-01-03"]
        elif number <= 210:
            parent = f"{source}-sec-2-3"
            topics = ["topico-quantil", "topico-intervalo-interquartil"]
            contents = ["conteudo-01-03"]
        elif number <= 234:
            parent = f"{source}-sec-2-4"
            topics = ["topico-media"]
            contents = ["conteudo-01-03"]
        elif number <= 237:
            parent = f"{source}-sec-3-1"
            topics = ["topico-media", "topico-variancia"]
            contents = ["conteudo-01-03"]
        elif number <= 249:
            parent = f"{source}-sec-3-2"
            topics = ["topico-assimetria"]
            contents = ["conteudo-01-03"]
        else:
            parent = f"{source}-sec-3-3"
            topics = ["topico-assimetria"]
            contents = ["conteudo-01-03"]
        nodes.append(
            item(
                source,
                str(number),
                page,
                parent,
                topics,
                contents,
                item_type="questao",
            )
        )
    return nodes


def _apostila_curated() -> list[dict]:
    source = "apostila-mq"
    chapter_specs = [
        ("1", "Conceitos básicos em Estatística", 8, 10),
        ("2", "Estudos dos dados estatísticos", 11, 21),
        ("3", "Distribuição de frequências", 22, 26),
        ("4", "Medidas de posição", 27, 48),
        ("5", "Medidas de dispersão", 49, 57),
        ("6", "Medidas de assimetria e curtose", 58, 61),
        ("15", "Análise de Correlação e Regressão", 148, 163),
        ("17", "Exercícios Propostos", 168, 193),
    ]
    nodes = [
        make_chapter(source, number, title, start, end)
        for number, title, start, end in chapter_specs
    ]
    section_specs = [
        ("1.1", "Divisão da Estatística", 8, 8, "1",
         ["topico-estatistica-descritiva", "topico-estatistica-inferencial"], ["conteudo-01-01"]),
        ("1.2", "Conceitos fundamentais", 8, 9, "1",
         ["topico-populacao", "topico-amostra", "topico-unidade-de-analise"], ["conteudo-01-01"]),
        ("1.3", "Fases do método estatístico", 10, 10, "1",
         ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("2.1", "Séries estatísticas", 11, 11, "2",
         ["topico-tipos-de-variaveis", "topico-tabela"], ["conteudo-01-02"]),
        ("2.2", "Apresentação tabular e gráfica", 12, 21, "2",
         ["topico-tabela", "topico-grafico"], ["conteudo-01-02"]),
        ("3.1", "Distribuição de frequências para dados discretos", 23, 23, "3",
         ["topico-frequencia", "topico-tabela"], ["conteudo-01-02"]),
        ("3.2", "Distribuição de frequências para dados contínuos", 24, 26, "3",
         ["topico-frequencia", "topico-grafico"], ["conteudo-01-02"]),
        ("4", "Medidas de posição", 27, 48, "4",
         ["topico-media", "topico-mediana", "topico-moda", "topico-quantil"], ["conteudo-01-03"]),
        ("5", "Medidas de dispersão", 49, 57, "5",
         ["topico-amplitude", "topico-variancia", "topico-desvio-padrao", "topico-coeficiente-de-variacao"], ["conteudo-01-03"]),
        ("6.1", "Medidas de assimetria", 58, 58, "6",
         ["topico-assimetria"], ["conteudo-01-03"]),
        ("6.2", "Medidas de curtose", 59, 61, "6",
         ["topico-assimetria"], ["conteudo-01-03"]),
        ("15.1", "Gráfico de dispersão", 148, 148, "15",
         ["topico-grafico", "topico-associacao"], ["conteudo-01-04"]),
        ("15.2", "Coeficiente de correlação de Pearson", 149, 149, "15",
         ["topico-correlacao-linear", "topico-covariancia"], ["conteudo-01-04"]),
        ("17.1", "Análise Descritiva", 168, 173, "17",
         ["topico-estatistica-descritiva"], ["conteudo-01-01", "conteudo-01-02", "conteudo-01-03", "conteudo-01-04"]),
    ]
    for number, title, start, end, chapter, topics, contents in section_specs:
        nodes.append(
            section(
                source,
                number,
                title,
                start,
                end,
                f"{source}-cap-{chapter.replace('.', '-')}",
                topics,
                contents,
            )
        )
    leaf_sections = [
        ("2.2.1", "Apresentação tabular", 12, 13, "2.2",
         ["topico-tabela"], ["conteudo-01-02"]),
        ("2.2.2", "Apresentação gráfica", 14, 21, "2.2",
         ["topico-grafico"], ["conteudo-01-02"]),
        ("4.1", "Pequenos conjuntos de dados", 27, 29, "4",
         ["topico-media", "topico-mediana", "topico-moda"], ["conteudo-01-03"]),
        ("4.2", "Grandes conjuntos de dados: discretos", 30, 31, "4",
         ["topico-media", "topico-mediana", "topico-moda"], ["conteudo-01-03"]),
        ("4.3", "Grandes conjuntos de dados: contínuos", 32, 34, "4",
         ["topico-media", "topico-mediana", "topico-moda"], ["conteudo-01-03"]),
        ("4.4", "Medidas separatrizes", 35, 41, "4",
         ["topico-quantil", "topico-mediana"], ["conteudo-01-03"]),
        ("4.5", "Interpolação linear", 42, 43, "4",
         ["topico-quantil"], ["conteudo-01-03"]),
        ("4.6", "Outras medidas de posição", 44, 48, "4",
         ["topico-media"], ["conteudo-01-03"]),
        ("5.1", "Pequenos conjuntos de dados", 49, 52, "5",
         ["topico-amplitude", "topico-variancia", "topico-desvio-padrao"], ["conteudo-01-03"]),
        ("5.2", "Grandes conjuntos de dados: discretos", 53, 54, "5",
         ["topico-variancia", "topico-desvio-padrao", "topico-coeficiente-de-variacao"], ["conteudo-01-03"]),
        ("5.3", "Grandes conjuntos de dados: contínuos", 55, 57, "5",
         ["topico-variancia", "topico-desvio-padrao", "topico-coeficiente-de-variacao"], ["conteudo-01-03"]),
    ]
    for number, title, start, end, parent, topics, contents in leaf_sections:
        nodes.append(
            section(
                source,
                number,
                title,
                start,
                end,
                f"{source}-sec-{parent.replace('.', '-')}",
                topics,
                contents,
            )
        )

    extracted = json.loads(
        (EXTRACTION_DIRECTORY / f"{source}.extract.json").read_text(
            encoding="utf-8"
        )
    )
    for number, page in extract_sequential_numbered_items(
        extracted,
        start_page=168,
        end_page=173,
        first_number=1,
        last_number=27,
    ):
        if number <= 6:
            topics = ["topico-investigacao-estatistica", "topico-tipos-de-variaveis", "topico-tabela"]
            contents = ["conteudo-01-01", "conteudo-01-02"]
        elif number == 7:
            topics = ["topico-tabela-de-contingencia", "topico-associacao"]
            contents = ["conteudo-01-04"]
        elif number == 21:
            topics = ["topico-media", "topico-coeficiente-de-variacao", "topico-associacao"]
            contents = ["conteudo-01-03", "conteudo-01-04"]
        else:
            topics = ["topico-media", "topico-mediana", "topico-variancia", "topico-desvio-padrao"]
            contents = ["conteudo-01-03"]
        nodes.append(
            item(
                source,
                str(number),
                page,
                f"{source}-sec-17-1",
                topics,
                contents,
                item_type="exercicio",
            )
        )
    return nodes


def _barbetta_curated() -> list[dict]:
    source = "barbetta-2010"
    chapters = [
        ("1", "Introdução", 12, 23),
        ("2", "O planejamento de uma pesquisa", 24, 50),
        ("3", "Análise exploratória de dados", 51, 91),
        ("11", "Correlação e regressão", 317, 350),
    ]
    nodes = [make_chapter(source, *chapter) for chapter in chapters]
    sections = [
        ("1.1", "A estatística", 12, 12, "1", ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.2", "Pesquisas, dados, variabilidade e estatística", 13, 13, "1", ["topico-investigacao-estatistica", "topico-representatividade"], ["conteudo-01-01"]),
        ("1.3", "A estatística na engenharia", 14, 14, "1", ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.4", "A estatística e a informática", 15, 15, "1", ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.5", "Modelos", 16, 17, "1", ["topico-estatistica-descritiva", "topico-estatistica-inferencial"], ["conteudo-01-01"]),
        ("1.6", "Conceitos básicos", 18, 23, "1", ["topico-populacao", "topico-amostra", "topico-variancia", "topico-desvio-padrao"], ["conteudo-01-01"]),
        ("2.1", "Aspectos gerais", 24, 24, "2", ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("2.2", "Pesquisas de levantamento", 25, 33, "2", ["topico-amostragem", "topico-representatividade"], ["conteudo-01-01"]),
        ("2.3", "Planejamento de experimentos", 34, 50, "2", ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("3.1", "Dados e variáveis", 52, 53, "3", ["topico-tipos-de-variaveis"], ["conteudo-01-02"]),
        ("3.2", "Análise de variáveis qualitativas", 54, 58, "3", ["topico-frequencia", "topico-tabela", "topico-grafico"], ["conteudo-01-02"]),
        ("3.3", "Análise de variáveis quantitativas", 59, 68, "3", ["topico-frequencia", "topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("3.4", "Medidas descritivas", 69, 83, "3", ["topico-media", "topico-mediana", "topico-variancia", "topico-desvio-padrao", "topico-boxplot"], ["conteudo-01-03"]),
        ("3.5", "Observações ao longo do tempo", 84, 84, "3", ["topico-grafico"], ["conteudo-01-02"]),
        ("3.6", "Análise exploratória com apoio do computador", 85, 85, "3", ["topico-pre-processamento", "topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("3.7", "Orientação geral", 86, 91, "3", ["topico-estatistica-descritiva", "topico-associacao"], ["conteudo-01-03", "conteudo-01-04"]),
        ("11.1", "Correlação", 317, 318, "11", ["topico-associacao", "topico-grafico"], ["conteudo-01-04"]),
        ("11.2", "Coeficiente de correlação linear de Pearson", 319, 324, "11", ["topico-correlacao-linear", "topico-covariancia"], ["conteudo-01-04"]),
    ]
    for number, title, start, end, chapter, topics, contents in sections:
        nodes.append(section(source, number, title, start, end, f"{source}-cap-{chapter}", topics, contents))
    nodes.extend([
        section(
            source,
            "2.2.1",
            "Procedimentos de amostragem",
            25,
            31,
            f"{source}-sec-2-2",
            ["topico-amostragem", "topico-representatividade"],
            ["conteudo-01-01"],
        ),
        section(
            source,
            "2.2.2",
            "Tamanho da amostra",
            32,
            33,
            f"{source}-sec-2-2",
            ["topico-amostragem", "topico-representatividade"],
            ["conteudo-01-01"],
        ),
    ])
    nodes.extend([
        item(source, "1.2", 23, f"{source}-cap-1", ["topico-populacao", "topico-amostra", "topico-amostragem"], ["conteudo-01-01"], item_type="exercicio"),
        item(source, "2.7", 34, f"{source}-cap-2", ["topico-amostragem", "topico-representatividade"], ["conteudo-01-01"], item_type="exercicio"),
        item(source, "3.4", 87, f"{source}-cap-3", ["topico-media", "topico-desvio-padrao", "topico-frequencia"], ["conteudo-01-03"], item_type="exercicio"),
        item(source, "3.8", 88, f"{source}-cap-3", ["topico-tipos-de-variaveis", "topico-frequencia", "topico-grafico"], ["conteudo-01-02"], item_type="exercicio"),
    ])
    return nodes


def _morettin_curated() -> list[dict]:
    source = "morettin-bussab-2010"
    chapters = [
        ("1", "Preliminares", 18, 25),
        ("2", "Resumo de dados", 26, 51),
        ("3", "Medidas-resumo", 52, 84),
        ("4", "Análise bidimensional", 85, 119),
    ]
    nodes = [make_chapter(source, *chapter) for chapter in chapters]
    sections = [
        ("1.1", "Introdução", 18, 18, "1", ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.2", "Modelos", 18, 18, "1", ["topico-estatistica-descritiva", "topico-estatistica-inferencial"], ["conteudo-01-01"]),
        ("1.3", "Técnicas computacionais", 19, 19, "1", ["topico-importacao-de-dados", "topico-pre-processamento"], ["conteudo-01-02"]),
        ("1.4", "Métodos gráficos", 20, 20, "1", ["topico-grafico"], ["conteudo-01-02"]),
        ("1.5", "Conjuntos de dados", 21, 21, "1", ["topico-unidade-de-analise", "topico-tipos-de-variaveis"], ["conteudo-01-01", "conteudo-01-02"]),
        ("2.1", "Tipos de variáveis", 26, 27, "2", ["topico-tipos-de-variaveis"], ["conteudo-01-02"]),
        ("2.2", "Distribuições de frequências", 28, 31, "2", ["topico-frequencia", "topico-tabela"], ["conteudo-01-02"]),
        ("2.3", "Gráficos", 32, 36, "2", ["topico-grafico"], ["conteudo-01-02"]),
        ("2.4", "Ramo-e-folhas", 37, 39, "2", ["topico-grafico", "topico-frequencia"], ["conteudo-01-02"]),
        ("2.5", "Exemplos computacionais", 40, 42, "2", ["topico-importacao-de-dados", "topico-grafico"], ["conteudo-01-02"]),
        ("2.6", "Problemas e complementos", 43, 51, "2", ["topico-tipos-de-variaveis", "topico-frequencia", "topico-grafico"], ["conteudo-01-02"]),
        ("3.1", "Medidas de posição", 52, 53, "3", ["topico-media", "topico-mediana", "topico-moda"], ["conteudo-01-03"]),
        ("3.2", "Medidas de dispersão", 54, 57, "3", ["topico-amplitude", "topico-variancia", "topico-desvio-padrao", "topico-coeficiente-de-variacao"], ["conteudo-01-03"]),
        ("3.3", "Quantis empíricos", 58, 63, "3", ["topico-quantil", "topico-intervalo-interquartil"], ["conteudo-01-03"]),
        ("3.4", "Box plots", 64, 67, "3", ["topico-boxplot", "topico-valor-discrepante"], ["conteudo-01-03"]),
        ("3.5", "Gráficos de simetria", 68, 68, "3", ["topico-assimetria", "topico-grafico"], ["conteudo-01-03"]),
        ("3.6", "Transformações", 69, 70, "3", ["topico-pre-processamento"], ["conteudo-01-03"]),
        ("3.7", "Exemplos computacionais", 71, 72, "3", ["topico-grafico", "topico-boxplot"], ["conteudo-01-03"]),
        ("3.8", "Problemas e complementos", 73, 84, "3", ["topico-media", "topico-variancia", "topico-boxplot"], ["conteudo-01-03"]),
        ("4.1", "Introdução", 85, 86, "4", ["topico-associacao"], ["conteudo-01-04"]),
        ("4.2", "Variáveis qualitativas", 87, 89, "4", ["topico-tabela-de-contingencia"], ["conteudo-01-04"]),
        ("4.3", "Associação entre variáveis qualitativas", 90, 92, "4", ["topico-associacao", "topico-tabela-de-contingencia"], ["conteudo-01-04"]),
        ("4.4", "Medidas de associação entre variáveis qualitativas", 93, 96, "4", ["topico-associacao"], ["conteudo-01-04"]),
        ("4.5", "Associação entre variáveis quantitativas", 97, 102, "4", ["topico-covariancia", "topico-correlacao-linear"], ["conteudo-01-04"]),
        ("4.6", "Associação entre variáveis qualitativas e quantitativas", 103, 106, "4", ["topico-associacao"], ["conteudo-01-04"]),
        ("4.7", "Gráficos q x q", 107, 108, "4", ["topico-grafico", "topico-associacao"], ["conteudo-01-04"]),
        ("4.8", "Exemplos computacionais", 109, 110, "4", ["topico-associacao", "topico-grafico"], ["conteudo-01-04"]),
        ("4.9", "Problemas e complementos", 111, 119, "4", ["topico-associacao", "topico-correlacao-linear"], ["conteudo-01-04"]),
    ]
    for number, title, start, end, chapter, topics, contents in sections:
        nodes.append(section(source, number, title, start, end, f"{source}-cap-{chapter}", topics, contents))
    nodes.extend([
        section(
            source,
            "2.3.1",
            "Gráficos para variáveis qualitativas",
            32,
            32,
            f"{source}-sec-2-3",
            ["topico-grafico", "topico-tipos-de-variaveis"],
            ["conteudo-01-02"],
        ),
        section(
            source,
            "2.3.2",
            "Gráficos para variáveis quantitativas",
            33,
            36,
            f"{source}-sec-2-3",
            ["topico-grafico", "topico-tipos-de-variaveis"],
            ["conteudo-01-02", "conteudo-01-03"],
        ),
    ])
    return nodes


def _pinheiro_curated() -> list[dict]:
    source = "pinheiro-2009"
    nodes = [
        make_chapter(source, "1", "Análise exploratória para uma variável", 20, 59),
        make_chapter(source, "2", "Estudando a relação entre duas variáveis", 60, 91),
    ]
    sections = [
        ("1.1", "Introdução", 20, 21, "1", ["topico-estatistica-descritiva"], ["conteudo-01-01"]),
        ("1.2", "População e amostra", 22, 23, "1", ["topico-populacao", "topico-amostra"], ["conteudo-01-01"]),
        ("1.3", "Tipologia das variáveis", 24, 26, "1", ["topico-tipos-de-variaveis"], ["conteudo-01-02"]),
        ("1.4", "Distribuições de frequências - tabelas e gráficos", 27, 34, "1", ["topico-frequencia", "topico-tabela", "topico-grafico"], ["conteudo-01-02"]),
        ("1.5", "Medidas de centralidade para variáveis quantitativas", 35, 36, "1", ["topico-media", "topico-mediana", "topico-moda"], ["conteudo-01-03"]),
        ("1.6", "Medidas de dispersão para variáveis quantitativas", 37, 42, "1", ["topico-amplitude", "topico-variancia", "topico-desvio-padrao", "topico-coeficiente-de-variacao"], ["conteudo-01-03"]),
        ("1.7", "O conceito de resistência de uma medida", 43, 43, "1", ["topico-mediana", "topico-intervalo-interquartil"], ["conteudo-01-03"]),
        ("1.8", "Identificação de discrepâncias em variáveis quantitativas", 44, 45, "1", ["topico-valor-discrepante"], ["conteudo-01-03"]),
        ("1.9", "Box plot para variáveis quantitativas", 46, 59, "1", ["topico-boxplot", "topico-valor-discrepante"], ["conteudo-01-03"]),
        ("2.1", "Relação entre variáveis qualitativas - tabelas de contingência", 60, 65, "2", ["topico-tabela-de-contingencia", "topico-associacao"], ["conteudo-01-04"]),
        ("2.2", "Correlação entre variáveis quantitativas", 66, 71, "2", ["topico-covariancia", "topico-correlacao-linear"], ["conteudo-01-04"]),
    ]
    for number, title, start, end, chapter, topics, contents in sections:
        nodes.append(section(source, number, title, start, end, f"{source}-cap-{chapter}", topics, contents))
    selected = [
        ("1.4_P", 55, "1", ["topico-intervalo-interquartil", "topico-valor-discrepante"], ["conteudo-01-03"]),
        ("1.5_P", 55, "1", ["topico-frequencia", "topico-grafico"], ["conteudo-01-02"]),
        ("1.7_P", 56, "1", ["topico-media", "topico-variancia", "topico-desvio-padrao"], ["conteudo-01-03"]),
        ("2.1_P", 81, "2", ["topico-tabela-de-contingencia", "topico-associacao"], ["conteudo-01-04"]),
        ("2.2_P", 82, "2", ["topico-tabela-de-contingencia", "topico-associacao"], ["conteudo-01-04"]),
        ("2.5_P", 83, "2", ["topico-correlacao-linear", "topico-valor-discrepante"], ["conteudo-01-04"]),
        ("2.7_P", 85, "2", ["topico-correlacao-linear", "topico-associacao"], ["conteudo-01-04"]),
    ]
    for number, page, chapter, topics, contents in selected:
        nodes.append(item(source, number, page, f"{source}-cap-{chapter}", topics, contents, item_type="exercicio"))
    return nodes


def _bruce_curated() -> list[dict]:
    source = "estatistica-pratica-cd"
    chapter_id = f"{source}-cap-1"
    nodes = [make_chapter(source, "1", "Análise Exploratória de Dados", 22, 70)]
    sections = [
        ("1.1", "Elementos de dados estruturados", 23, 26, ["topico-tipos-de-variaveis", "topico-unidade-de-analise"], ["conteudo-01-02"]),
        ("1.2", "Dados retangulares", 27, 28, ["topico-tabela", "topico-importacao-de-dados"], ["conteudo-01-02"]),
        ("1.3", "Quadros de dados e índices", 29, 30, ["topico-tabela", "topico-importacao-de-dados"], ["conteudo-01-02"]),
        ("1.4", "Estimativas de localização", 31, 37, ["topico-media", "topico-mediana"], ["conteudo-01-03"]),
        ("1.5", "Estimativas de variabilidade", 38, 44, ["topico-variancia", "topico-desvio-padrao", "topico-quantil", "topico-intervalo-interquartil"], ["conteudo-01-03"]),
        ("1.6", "Explorando a distribuição de dados", 45, 50, ["topico-frequencia", "topico-boxplot", "topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("1.7", "Explorando dados binários e categóricos", 51, 54, ["topico-moda", "topico-tabela", "topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("1.8", "Correlação", 55, 58, ["topico-correlacao-linear", "topico-covariancia"], ["conteudo-01-04"]),
        ("1.9", "Gráficos de dispersão", 59, 60, ["topico-grafico", "topico-associacao"], ["conteudo-01-04"]),
        ("1.10", "Explorando duas ou mais variáveis", 61, 69, ["topico-tabela-de-contingencia", "topico-associacao", "topico-grafico"], ["conteudo-01-04"]),
    ]
    for number, title, start, end, topics, contents in sections:
        nodes.append(section(source, number, title, start, end, chapter_id, topics, contents))
    return nodes


def _montgomery_curated() -> list[dict]:
    source = "montgomery-2018"
    nodes = [
        make_chapter(source, "1", "The Role of Statistics in Engineering", 19, 34),
        make_chapter(source, "6", "Descriptive Statistics", 144, 161),
    ]
    sections = [
        ("1.1", "The Engineering Method and Statistical Thinking", 20, 23, "1", ["topico-investigacao-estatistica", "topico-populacao", "topico-amostra"], ["conteudo-01-01"]),
        ("1.2", "Collecting Engineering Data", 23, 29, "1", ["topico-investigacao-estatistica", "topico-representatividade"], ["conteudo-01-01"]),
        ("1.3", "Mechanistic and Empirical Models", 30, 32, "1", ["topico-estatistica-descritiva", "topico-estatistica-inferencial"], ["conteudo-01-01"]),
        ("6.1", "Numerical Summaries of Data", 145, 148, "6", ["topico-media", "topico-mediana", "topico-variancia", "topico-desvio-padrao"], ["conteudo-01-03"]),
        ("6.2", "Stem-and-Leaf Diagrams", 149, 152, "6", ["topico-frequencia", "topico-grafico"], ["conteudo-01-02"]),
        ("6.3", "Frequency Distributions and Histograms", 153, 156, "6", ["topico-frequencia", "topico-grafico"], ["conteudo-01-02", "conteudo-01-03"]),
        ("6.4", "Box Plots", 157, 157, "6", ["topico-boxplot", "topico-valor-discrepante"], ["conteudo-01-03"]),
        ("6.5", "Time Sequence Plots", 158, 159, "6", ["topico-grafico"], ["conteudo-01-02"]),
        ("6.6", "Scatter Diagrams", 160, 161, "6", ["topico-grafico", "topico-associacao"], ["conteudo-01-04"]),
    ]
    for number, title, start, end, chapter, topics, contents in sections:
        nodes.append(section(source, number, title, start, end, f"{source}-cap-{chapter}", topics, contents))
    leaf_sections = [
        ("1.1.1", "Variability", 21, 22, "1.1",
         ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.1.2", "Populations and Samples", 23, 23, "1.1",
         ["topico-populacao", "topico-amostra"], ["conteudo-01-01"]),
        ("1.2.1", "Basic Principles", 23, 23, "1.2",
         ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.2.2", "Retrospective Study", 23, 23, "1.2",
         ["topico-investigacao-estatistica", "topico-representatividade"], ["conteudo-01-01"]),
        ("1.2.3", "Observational Study", 24, 24, "1.2",
         ["topico-investigacao-estatistica", "topico-representatividade"], ["conteudo-01-01"]),
        ("1.2.4", "Designed Experiments", 24, 26, "1.2",
         ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.2.5", "Observing Processes Over Time", 27, 29, "1.2",
         ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
    ]
    for number, title, start, end, parent, topics, contents in leaf_sections:
        nodes.append(
            section(
                source,
                number,
                title,
                start,
                end,
                f"{source}-sec-{parent.replace('.', '-')}",
                topics,
                contents,
            )
        )
    return nodes


def _navidi_curated() -> list[dict]:
    source = "navidi-2024"
    chapter_id = f"{source}-cap-1"
    nodes = [make_chapter(source, "1", "Sampling and Descriptive Statistics", 23, 69)]
    sections = [
        ("1.0", "Introduction", 23, 24, ["topico-investigacao-estatistica"], ["conteudo-01-01"]),
        ("1.1", "Sampling", 25, 34, ["topico-populacao", "topico-amostra", "topico-amostragem", "topico-representatividade"], ["conteudo-01-01"]),
        ("1.2", "Summary Statistics", 35, 46, ["topico-media", "topico-mediana", "topico-variancia", "topico-desvio-padrao", "topico-quantil"], ["conteudo-01-03"]),
        ("1.3", "Graphical Summaries", 47, 69, ["topico-frequencia", "topico-grafico", "topico-boxplot", "topico-associacao"], ["conteudo-01-02", "conteudo-01-03", "conteudo-01-04"]),
    ]
    for number, title, start, end, topics, contents in sections:
        nodes.append(section(source, number, title, start, end, chapter_id, topics, contents))
    return nodes


def build_curations() -> dict[str, list[dict]]:
    """Retorna as oito curadorias usadas na Unidade I; Escovedo fica sem mapa."""
    return {
        "apostila-mq": _apostila_curated(),
        "banco-questoes-2026-2": _bank_curated(),
        "barbetta-2010": _barbetta_curated(),
        "estatistica-pratica-cd": _bruce_curated(),
        "montgomery-2018": _montgomery_curated(),
        "morettin-bussab-2010": _morettin_curated(),
        "navidi-2024": _navidi_curated(),
        "pinheiro-2009": _pinheiro_curated(),
    }
