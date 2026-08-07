"""Estrutura editorial verificada de Montgomery (2018)."""

from scripts.grafo_refs.build_graph import REPOSITORY_ROOT
from scripts.grafo_refs.curation.common import (
    finalize_source,
    marker_numbered_nodes,
)


PDF_PATH = (
    REPOSITORY_ROOT
    / "prof/refs/livros/Montgomery 2018 Applied Statistics and Probability for Engineers.pdf"
)


def build_nodes() -> list[dict]:
    source = "montgomery-2018"
    return finalize_source(
        source,
        marker_numbered_nodes(
            source,
            PDF_PATH,
            chapter_pattern=r"^Chapter (\d+):",
            section_pattern=r"^(\d+\.\d+(?:\.\d+)?)\s+",
            terminal_page=500,
        ),
    )
