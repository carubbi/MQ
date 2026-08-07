"""Construtores compartilhados para nós de curadoria."""

import re


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
