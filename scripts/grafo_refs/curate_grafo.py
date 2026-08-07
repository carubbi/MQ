"""Agrega e escreve as curadorias verificadas do grafo."""

import argparse
import json
from pathlib import Path

from scripts.grafo_refs.build_graph import DEFAULT_CURATED_DIRECTORY
from scripts.grafo_refs.curation import unidade_i_legada


def build_curations() -> dict[str, list[dict]]:
    """Reúne as curadorias disponíveis, atualmente as oito da Unidade I."""
    return unidade_i_legada.build_curations()


def write_curations(
    output_directory: Path = DEFAULT_CURATED_DIRECTORY,
) -> None:
    """Escreve um JSON determinístico por fonte."""
    output_directory.mkdir(parents=True, exist_ok=True)
    for source_id, nodes in build_curations().items():
        (output_directory / f"{source_id}.json").write_text(
            json.dumps(nodes, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera as curadorias do grafo.")
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=DEFAULT_CURATED_DIRECTORY,
    )
    arguments = parser.parse_args()
    write_curations(arguments.output_directory)


if __name__ == "__main__":
    main()
