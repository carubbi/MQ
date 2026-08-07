"""Constrói o grafo canônico de referências da T199."""

import argparse
import json
from pathlib import Path

from scripts.grafo_refs.inventory import inventory_sources
from scripts.grafo_refs.model import flatten_curated_source


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = REPOSITORY_ROOT / "scripts/grafo_refs/data"
DEFAULT_CURATED_DIRECTORY = DATA_DIRECTORY / "curadorias"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "prof/refs/mapas/grafo_referencias.json"
COMPLETED_CONTENTS = ["01.01", "01.02", "01.03", "01.04"]
PENDING_CONTENTS = ["02.01", "02.02", "02.03", "02.04", "03.01", "03.02", "03.03", "03.04"]
VOCABULARIES = {
    "tipos_no": [
        "fonte",
        "capitulo",
        "secao",
        "questao",
        "exercicio",
        "exemplo",
        "topico",
        "conteudo_curricular",
    ],
    "tipos_relacao": ["contem", "aborda", "corresponde_a", "precede"],
    "pertinencias_t199": ["direta", "indireta", "fora_do_escopo"],
}


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_curated_sources(curated_dir: Path) -> tuple[list[dict], list[dict]]:
    nodes = []
    edges = []
    if not curated_dir.exists():
        return nodes, edges

    for curated_path in sorted(curated_dir.glob("*.json")):
        curated_nodes = _read_json(curated_path)
        if not isinstance(curated_nodes, list):
            raise ValueError(f"curadoria deve ser uma lista: {curated_path}")
        source_nodes, source_edges = flatten_curated_source(curated_path.stem, curated_nodes)
        nodes.extend(source_nodes)
        edges.extend(source_edges)
    return nodes, edges


def build_graph(generated_on: str, curated_dir: Path) -> dict:
    """Monta o grafo parcial, de modo independente da ordem de arquivos."""
    sources = inventory_sources(DATA_DIRECTORY / "fontes.json", REPOSITORY_ROOT)
    source_nodes = [{"id": source["id"], "tipo": "fonte", **{key: value for key, value in source.items() if key != "id"}} for source in sources]
    contents = _read_json(DATA_DIRECTORY / "conteudos_t199.json")
    topics = _read_json(DATA_DIRECTORY / "topicos_unidade_i.json")
    curated_nodes, curated_edges = _load_curated_sources(curated_dir)
    nodes = source_nodes + contents + topics + curated_nodes

    return {
        "metadados": {
            "versao_esquema": "1.1",
            "data_geracao": generated_on,
            "semestre_referencia": "2026.2",
            "cobertura": {
                "estado": "parcial",
                "criterio": "conteudo_curricular",
                "conteudos_concluidos": COMPLETED_CONTENTS,
                "conteudos_pendentes": PENDING_CONTENTS,
                "fontes_inventariadas": 9,
            },
        },
        "vocabularios": VOCABULARIES,
        "nos": sorted(nodes, key=lambda node: (node["tipo"], node["id"])),
        "relacoes": sorted(curated_edges, key=lambda edge: (edge["origem"], edge["tipo"], edge["destino"])),
    }


def write_graph(graph: dict, output_path: Path) -> None:
    """Escreve JSON canônico legível e estável."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Constrói o grafo parcial de referências.")
    parser.add_argument("--generated-on", required=True, help="Data de geração em YYYY-MM-DD.")
    parser.add_argument("--curated-dir", type=Path, default=DEFAULT_CURATED_DIRECTORY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    write_graph(build_graph(arguments.generated_on, arguments.curated_dir), arguments.output)


if __name__ == "__main__":
    main()
