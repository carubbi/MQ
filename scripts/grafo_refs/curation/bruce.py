"""Estrutura editorial verificada de Estatística Prática."""

from collections import Counter

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    apply_curricular_mappings,
    chapter,
    load_extraction,
    finalize_source,
    unnumbered_section,
)
from scripts.grafo_refs.model import slug_id


SOURCE = "estatistica-pratica-cd"
PDF_PATH = (
    REPOSITORY_ROOT
    / "prof/refs/livros/Estatistica-pratica-para-cientistas-de-dados.pdf"
)
PARATEXT_TITLES = {"Leitura Adicional", "Resumo"}
PUBLISHED_SECTION_NUMBERS = {
    "elementos-de-dados-estruturados": "1.1",
    "dados-retangulares": "1.2",
    "quadros-de-dados-e-indices": "1.3",
    "estimativas-de-localizacao": "1.4",
    "estimativas-de-variabilidade": "1.5",
    "explorando-a-distribuicao-de-dados": "1.6",
    "explorando-dados-binarios-e-categoricos": "1.7",
    "correlacao": "1.8",
    "graficos-de-dispersao": "1.9",
    "explorando-duas-ou-mais-variaveis": "1.10",
}


def build_nodes() -> list[dict]:
    markers = load_extraction(SOURCE, PDF_PATH)["marcadores"]
    chapter_markers = [marker for marker in markers if marker["nivel"] == 2]
    nodes = []
    for index, marker in enumerate(chapter_markers):
        start = marker["pagina_pdf"]
        end = (
            chapter_markers[index + 1]["pagina_pdf"] - 1
            if index + 1 < len(chapter_markers)
            else 351
        )
        nodes.append(
            chapter(
                SOURCE,
                str(index + 1),
                marker["titulo"].strip(),
                start,
                end,
            )
        )

    chapter_number = 0
    active_major_section = None
    occurrences = Counter()
    editorial_markers = [
        marker
        for marker in markers
        if marker["nivel"] in {2, 3}
        and marker["titulo"].replace("\x00", "").strip()
        not in PARATEXT_TITLES
    ]
    for index, marker in enumerate(editorial_markers):
        title = marker["titulo"].replace("\x00", "").strip()
        if marker["nivel"] == 2:
            chapter_number += 1
            active_major_section = None
            continue

        title_slug = slug_id(title)
        occurrences[(chapter_number, title_slug)] += 1
        published_number = PUBLISHED_SECTION_NUMBERS.get(title_slug)
        if published_number:
            identifier = published_number.replace(".", "-")
            active_major_section = f"{SOURCE}-sec-{identifier}"
        else:
            identifier = f"{chapter_number}-{title_slug}"
            if occurrences[(chapter_number, title_slug)] > 1:
                identifier += f"-{occurrences[(chapter_number, title_slug)]}"

        end = nodes[chapter_number - 1]["pagina_pdf_fim"]
        for following in editorial_markers[index + 1 :]:
            if following["nivel"] in {2, 3}:
                end = max(
                    marker["pagina_pdf"],
                    following["pagina_pdf"] - 1,
                )
                break
        parent = f"{SOURCE}-cap-{chapter_number}"
        if (
            chapter_number == 1
            and not published_number
            and active_major_section is not None
        ):
            parent = active_major_section
        nodes.append(
            unnumbered_section(
                SOURCE,
                identifier,
                title,
                marker["pagina_pdf"],
                end,
                parent,
            )
        )
    apply_curricular_mappings(
        nodes,
        {
            f"{SOURCE}-sec-2-distribuicao-normal": (
                ["topico-distribuicao-normal"],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-sec-2-normal-padrao-e-graficos-qq": (
                [
                    "topico-distribuicao-normal",
                    "topico-padronizacao",
                    "topico-grafico-qq",
                    "topico-diagnostico-do-modelo",
                ],
                ["conteudo-02-04"],
            ),
            f"{SOURCE}-sec-2-distribuicao-binomial": (
                ["topico-distribuicao-binomial"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-sec-2-distribuicoes-poisson": (
                ["topico-distribuicao-poisson"],
                ["conteudo-02-03"],
            ),
            f"{SOURCE}-sec-2-distribuicao-exponencial": (
                ["topico-distribuicao-exponencial"],
                ["conteudo-02-04"],
            ),
        },
    )
    return finalize_source(SOURCE, nodes)
