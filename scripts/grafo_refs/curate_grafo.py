"""Agrega e escreve as curadorias verificadas do grafo."""

import argparse
import json
from pathlib import Path

from scripts.grafo_refs.build_graph import DEFAULT_CURATED_DIRECTORY
from scripts.grafo_refs.curation import (
    apostila_mq,
    banco_questoes,
    barbetta,
    bruce,
    montgomery,
    morettin_bussab,
    navidi,
    pinheiro,
)


def build_curations() -> dict[str, list[dict]]:
    """Reúne as oito curadorias editoriais; Escovedo permanece sem nós."""
    return {
        "apostila-mq": apostila_mq.build_nodes(),
        "banco-questoes-2026-2": banco_questoes.build_nodes(),
        "barbetta-2010": barbetta.build_nodes(),
        "estatistica-pratica-cd": bruce.build_nodes(),
        "montgomery-2018": montgomery.build_nodes(),
        "morettin-bussab-2010": morettin_bussab.build_nodes(),
        "navidi-2024": navidi.build_nodes(),
        "pinheiro-2009": pinheiro.build_nodes(),
    }


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
