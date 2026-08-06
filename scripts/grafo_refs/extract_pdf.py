"""Extração local de texto, marcadores e páginas renderizadas de PDFs."""

import argparse
import json
import unicodedata
from pathlib import Path

import fitz


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPOSITORY_ROOT / "scripts/grafo_refs/data/fontes.json"
EXTRACTION_DIRECTORY = REPOSITORY_ROOT / "tmp/grafo_refs"
RENDER_DIRECTORY = REPOSITORY_ROOT / "tmp/pdfs/grafo_refs"


def extract_pdf(pdf_path: Path) -> dict:
    """Extrai texto por página e marcadores, sempre numerando páginas em base 1."""
    with fitz.open(pdf_path) as document:
        pages = [
            {"pagina_pdf": page_number, "texto": page.get_text()}
            for page_number, page in enumerate(document, start=1)
        ]
        bookmarks = [
            {"nivel": level, "titulo": title, "pagina_pdf": page_number}
            for level, title, page_number in document.get_toc(simple=True)
        ]
    return {"paginas": pages, "marcadores": bookmarks}


def _search_normalized(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(
        character for character in normalized if not unicodedata.combining(character)
    ).casefold()


def search_pages(extracted: dict, terms: list[str]) -> list[int]:
    """Localiza páginas que incluem todos os termos, sem caixa ou diacríticos."""
    normalized_terms = [
        normalized for term in terms if (normalized := _search_normalized(term).strip())
    ]
    if not normalized_terms:
        return []
    return [
        page["pagina_pdf"]
        for page in extracted["paginas"]
        if all(normalized in _search_normalized(page["texto"]) for normalized in normalized_terms)
    ]


def render_pages(pdf_path: Path, source_id: str, page_numbers: list[int]) -> list[Path]:
    """Renderiza páginas PDF base 1 como PNGs intermediários locais."""
    RENDER_DIRECTORY.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    with fitz.open(pdf_path) as document:
        for page_number in page_numbers:
            if not 1 <= page_number <= document.page_count:
                raise ValueError(f"página PDF inválida: {page_number}")
            output_path = RENDER_DIRECTORY / f"{source_id}-pagina-{page_number:04d}.png"
            document[page_number - 1].get_pixmap(matrix=fitz.Matrix(2, 2)).save(output_path)
            rendered_paths.append(output_path)
    return rendered_paths


def _source_for_id(source_id: str, manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for source in manifest:
        if source["id"] == source_id:
            return source
    raise ValueError(f"fonte não encontrada no manifesto: {source_id}")


def _parse_render_pages(value: str) -> list[int]:
    try:
        return [int(page.strip()) for page in value.split(",") if page.strip()]
    except ValueError as error:
        raise argparse.ArgumentTypeError("--render usa páginas como 1,5,10") from error


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrai uma fonte PDF do grafo.")
    parser.add_argument("source_id")
    parser.add_argument("--search", action="append", default=[], metavar="TERMO")
    parser.add_argument("--render", type=_parse_render_pages, metavar="PAGINAS")
    arguments = parser.parse_args()

    source = _source_for_id(arguments.source_id, DEFAULT_MANIFEST)
    pdf_path = REPOSITORY_ROOT / source["arquivo"]
    extracted = extract_pdf(pdf_path)
    EXTRACTION_DIRECTORY.mkdir(parents=True, exist_ok=True)
    extraction_path = EXTRACTION_DIRECTORY / f"{source['id']}.extract.json"
    extraction_path.write_text(
        json.dumps(extracted, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    rendered = []
    if arguments.render is not None:
        rendered = [
            str(path.relative_to(REPOSITORY_ROOT))
            for path in render_pages(pdf_path, source["id"], arguments.render)
        ]
    result = {
        "fonte": source["id"],
        "extracao": str(extraction_path.relative_to(REPOSITORY_ROOT)),
        "paginas_encontradas": search_pages(extracted, arguments.search)
        if arguments.search
        else [],
        "renders": rendered,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
