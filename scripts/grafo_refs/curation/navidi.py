"""Estrutura editorial verificada de Navidi (2024)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import marker_numbered_nodes


PDF_PATH = (
    REPOSITORY_ROOT
    / "prof/refs/livros/Navidi 2024 Statistics for Engineers and Scientists.pdf"
)


def build_nodes() -> list[dict]:
    return marker_numbered_nodes(
        "navidi-2024",
        PDF_PATH,
        chapter_pattern=r"^Chapter (\d+)\s+",
        section_pattern=r"^(\d+\.\d+)\s+",
        terminal_page=838,
        include_introductions=True,
    )
