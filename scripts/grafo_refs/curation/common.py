"""Construtores e utilitários compartilhados para curadoria editorial."""

import json
import re
from pathlib import Path

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.extract_pdf import extract_pdf
from scripts.grafo_refs.model import slug_id


DATA_DIRECTORY = REPOSITORY_ROOT / "scripts/grafo_refs/data"
CONTRACT_PATH = DATA_DIRECTORY / "contrato_publicado_unidade_i.json"
MIGRATIONS_PATH = DATA_DIRECTORY / "migracoes_estrutura_unidade_i.json"


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
    """Extrai sempre do PDF canônico; tmp nunca participa da geração."""
    del source
    return extract_pdf(pdf_path)


def finalize_source(source: str, nodes: list[dict]) -> list[dict]:
    """Aplica contrato curricular e migrações estruturais auditáveis."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    migrations = json.loads(MIGRATIONS_PATH.read_text(encoding="utf-8"))[
        "migracoes"
    ]
    contract_nodes = {
        node_id: frozen
        for node_id, frozen in contract["nos"].items()
        if node_id.startswith(f"{source}-") and frozen["tipo"] != "fonte"
    }
    parents = {}
    topics = {}
    contents = {}
    precedence = {}
    for origin, relation_type, destination in contract["relacoes"]:
        if relation_type == "contem" and destination in contract_nodes:
            parents[destination] = origin
        elif relation_type == "aborda" and origin in contract_nodes:
            topics.setdefault(origin, []).append(destination)
        elif relation_type == "corresponde_a" and origin in contract_nodes:
            contents.setdefault(origin, []).append(destination)
        elif relation_type == "precede" and origin in contract_nodes:
            precedence.setdefault(origin, []).append(destination)

    field_migrations = {
        (migration["id"], migration["campo"]): migration["para"]
        for migration in migrations
        if migration["tipo"] == "campo"
    }
    parent_migrations = {
        migration["destino"]: migration["origem_para"]
        for migration in migrations
        if migration["tipo"] == "relacao"
        and migration["relacao"] == "contem"
    }

    finalized = []
    for node in nodes:
        node_id = node["id"]
        finalized_node = node.copy()
        if node_id in contract_nodes:
            frozen = contract_nodes[node_id]
            for key in (
                "pagina_pdf",
                "pagina_pdf_inicio",
                "pagina_pdf_fim",
            ):
                if key in frozen:
                    finalized_node[key] = frozen[key]
            if node_id in parents:
                finalized_node["pai"] = parents[node_id]
            finalized_node["topicos"] = topics.get(node_id, [])
            finalized_node["conteudos"] = contents.get(node_id, [])
            if finalized_node["tipo"] in {
                "secao",
                "questao",
                "exercicio",
                "exemplo",
            }:
                finalized_node["pertinencia_t199"] = "direta"
            if node_id in precedence:
                finalized_node["precede_publicados"] = precedence[node_id]

        for key in (
            "pagina_pdf",
            "pagina_pdf_inicio",
            "pagina_pdf_fim",
        ):
            migrated = field_migrations.get((node_id, key))
            if migrated is not None:
                finalized_node[key] = migrated
        if node_id in parent_migrations:
            finalized_node["pai"] = parent_migrations[node_id]
        finalized.append(finalized_node)

    missing = sorted(set(contract_nodes) - {node["id"] for node in finalized})
    if missing:
        raise ValueError(
            f"nós publicados não reconstruídos por {source}: {missing}"
        )
    return _enclose_children(finalized)


def _enclose_children(nodes: list[dict]) -> list[dict]:
    """Amplia pais editoriais até conter todos os descendentes diretos."""
    by_id = {node["id"]: node for node in nodes}
    changed = True
    while changed:
        changed = False
        for child in nodes:
            parent = by_id.get(child.get("pai"))
            if parent is None or "pagina_pdf_fim" not in parent:
                continue
            child_end = child.get(
                "pagina_pdf",
                child.get("pagina_pdf_fim"),
            )
            if child_end is not None and child_end > parent["pagina_pdf_fim"]:
                parent["pagina_pdf_fim"] = child_end
                changed = True
    return nodes


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
    return nodes


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
