"""Construtores e utilitários compartilhados para curadoria editorial."""

import json
import re
from pathlib import Path

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.extract_pdf import extract_pdf
from scripts.grafo_refs.model import slug_id


DATA_DIRECTORY = REPOSITORY_ROOT / "scripts/grafo_refs/data"
CURATED_DIRECTORY = DATA_DIRECTORY / "curadorias"
CONTRACT_PATH = DATA_DIRECTORY / "contrato_publicado_unidade_i.json"
EXTRACTION_DIRECTORY = REPOSITORY_ROOT / "tmp/grafo_refs"


def chapter(
    source: str, number: str, title: str, start: int, end: int
) -> dict:
    return {
        "id": f"{source}-cap-{number.replace('.', '-')}",
        "tipo": "capitulo",
        "numero_impresso": number,
        "titulo": title,
        "pagina_pdf_inicio": start,
        "pagina_pdf_fim": end,
        "pai": source,
    }


def section(
    source: str,
    number: str,
    title: str,
    start: int,
    end: int,
    parent: str,
    topics: list[str],
    contents: list[str],
    *,
    pertinence: str = "direta",
) -> dict:
    return {
        "id": f"{source}-sec-{number.replace('.', '-')}",
        "tipo": "secao",
        "numero_impresso": number,
        "titulo": title.replace("\x00", "").strip(),
        "pagina_pdf_inicio": start,
        "pagina_pdf_fim": end,
        "pai": parent,
        "pertinencia_t199": pertinence,
        "topicos": topics,
        "conteudos": contents,
    }


def item(
    source: str,
    number: str,
    page: int,
    parent: str,
    topics: list[str],
    contents: list[str],
    *,
    item_type: str,
    pertinence: str = "direta",
) -> dict:
    stable_number = number.lower().replace(".", "-").replace("_", "-")
    return {
        "id": f"{source}-{item_type}-{stable_number}",
        "tipo": item_type,
        "numero_impresso": number,
        "pagina_pdf": page,
        "pai": parent,
        "pertinencia_t199": pertinence,
        "topicos": topics,
        "conteudos": contents,
    }


def extract_sequential_numbered_items(
    extracted: dict,
    *,
    start_page: int,
    end_page: int,
    first_number: int,
    last_number: int,
) -> list[tuple[int, int]]:
    """Localiza uma sequência editorial e ignora números internos às questões."""
    expected = first_number
    items = []
    pattern = re.compile(r"(?m)^\s*(\d{1,4})\.\s")
    for page in extracted["paginas"]:
        page_number = page["pagina_pdf"]
        if not start_page <= page_number <= end_page:
            continue
        for match in pattern.finditer(page["texto"]):
            number = int(match.group(1))
            if number == expected:
                items.append((number, page_number))
                expected += 1
                if expected > last_number:
                    return items
    raise ValueError(
        f"sequência incompleta: esperado {expected}, limite {last_number}"
    )


def load_extraction(source: str, pdf_path: Path) -> dict:
    """Usa o extrato auditável quando presente e o PDF canônico como fallback."""
    extracted_path = EXTRACTION_DIRECTORY / f"{source}.extract.json"
    if extracted_path.exists():
        return json.loads(extracted_path.read_text(encoding="utf-8"))
    return extract_pdf(pdf_path)


def merge_published_nodes(source: str, nodes: list[dict]) -> list[dict]:
    """Sobrepõe apenas os nós congelados no contrato publicado da Unidade I."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    published_ids = {
        node_id
        for node_id in contract["nos"]
        if node_id.startswith(f"{source}-")
    }
    current_path = CURATED_DIRECTORY / f"{source}.json"
    current_nodes = json.loads(current_path.read_text(encoding="utf-8"))
    published = {
        node["id"]: node
        for node in current_nodes
        if node["id"] in published_ids
    }
    published_precedence = {}
    for origin, relation_type, destination in contract["relacoes"]:
        if (
            relation_type == "precede"
            and origin in published_ids
            and destination in published_ids
        ):
            published_precedence.setdefault(origin, []).append(destination)

    merged = []
    seen = set()
    for node in nodes:
        node_id = node["id"]
        merged_node = published.get(node_id, node).copy()
        if node_id in published_precedence:
            merged_node["precede_publicados"] = published_precedence[node_id]
        merged.append(merged_node)
        seen.add(node_id)
    for node_id, node in published.items():
        if node_id not in seen:
            merged_node = node.copy()
            if node_id in published_precedence:
                merged_node["precede_publicados"] = published_precedence[
                    node_id
                ]
            merged.append(merged_node)
    return merged


def numbered_editorial_nodes(
    source: str,
    chapters: list[tuple[str, str, int]],
    sections: list[tuple[str, str, int]],
    *,
    terminal_page: int,
) -> list[dict]:
    """Constrói intervalos e hierarquia de capítulos/seções numerados."""
    chapter_ends = {}
    for index, (number, _title, start) in enumerate(chapters):
        next_start = (
            chapters[index + 1][2]
            if index + 1 < len(chapters)
            else terminal_page + 1
        )
        chapter_ends[number] = max(start, next_start - 1)

    nodes = [
        chapter(source, number, title, start, chapter_ends[number])
        for number, title, start in chapters
    ]
    section_numbers = {number for number, _title, _start in sections}
    for index, (number, title, start) in enumerate(sections):
        chapter_number = number.split(".")[0]
        depth = number.count(".")
        end = chapter_ends[chapter_number]
        for following_number, _following_title, following_start in sections[
            index + 1 :
        ]:
            if following_number.split(".")[0] != chapter_number:
                break
            if following_number.count(".") <= depth:
                end = max(start, following_start - 1)
                break

        parent_number = number.rsplit(".", 1)[0] if "." in number else ""
        if parent_number in section_numbers:
            parent = f"{source}-sec-{parent_number.replace('.', '-')}"
        else:
            parent = f"{source}-cap-{chapter_number}"
        nodes.append(
            section(
                source,
                number,
                title,
                start,
                end,
                parent,
                [],
                [],
                pertinence="indireta",
            )
        )
    return merge_published_nodes(source, nodes)


def marker_numbered_nodes(
    source: str,
    pdf_path: Path,
    *,
    chapter_pattern: str,
    section_pattern: str,
    terminal_page: int,
    chapter_titles: dict[str, str] | None = None,
    include_introductions: bool = False,
) -> list[dict]:
    """Converte marcadores numerados confiáveis em estrutura editorial."""
    chapters = []
    sections = []
    current_chapter = None
    for marker in load_extraction(source, pdf_path)["marcadores"]:
        title = marker["titulo"].replace("\x00", "").strip()
        chapter_match = re.match(chapter_pattern, title)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            chapter_title = (
                chapter_titles[current_chapter]
                if chapter_titles
                else title[chapter_match.end() :].strip(" :")
            )
            chapters.append(
                (current_chapter, chapter_title, marker["pagina_pdf"])
            )
            continue

        section_match = re.match(section_pattern, title)
        if section_match:
            number = section_match.group(1)
            sections.append(
                (number, title[section_match.end() :].strip(), marker["pagina_pdf"])
            )
        elif (
            include_introductions
            and current_chapter
            and title == "Introduction"
        ):
            sections.append(
                (
                    f"{current_chapter}.0",
                    title,
                    marker["pagina_pdf"],
                )
            )

    return numbered_editorial_nodes(
        source,
        chapters,
        sections,
        terminal_page=terminal_page,
    )


def unnumbered_section(
    source: str,
    identifier: str,
    title: str,
    start: int,
    end: int,
    parent: str,
) -> dict:
    """Representa seção formal sem fabricar um número impresso."""
    return {
        "id": f"{source}-sec-{identifier}",
        "tipo": "secao",
        "numero_impresso": "s.n.",
        "titulo": title.replace("\x00", "").strip(),
        "pagina_pdf_inicio": start,
        "pagina_pdf_fim": end,
        "pai": parent,
        "pertinencia_t199": "indireta",
        "topicos": [],
        "conteudos": [],
    }
