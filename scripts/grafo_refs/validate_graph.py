"""Valida regras semânticas do grafo além do JSON Schema."""

import argparse
import json
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator


COMPLETED_CONTENTS = {"01.01", "01.02", "01.03", "01.04"}
PENDING_CONTENTS = {"02.01", "02.02", "02.03", "02.04", "03.01", "03.02", "03.03", "03.04"}
EXPECTED_COVERAGE = {
    "estado": "parcial",
    "criterio": "conteudo_curricular",
    "conteudos_concluidos": ["01.01", "01.02", "01.03", "01.04"],
    "conteudos_pendentes": ["02.01", "02.02", "02.03", "02.04", "03.01", "03.02", "03.03", "03.04"],
    "fontes_inventariadas": 9,
}
PROHIBITED_KEYS = {"dificuldade", "observacao"}
MANIFEST_PATH = Path("scripts/grafo_refs/data/fontes.json")


def _walk_keys(value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield key
            yield from _walk_keys(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from _walk_keys(nested_value)


def _source_ancestors(node_id: str, parents: dict[str, list[str]], nodes_by_id: dict) -> list[dict]:
    sources = []
    pending = list(parents.get(node_id, []))
    seen = set()
    while pending:
        ancestor_id = pending.pop()
        if ancestor_id in seen:
            continue
        seen.add(ancestor_id)
        ancestor = nodes_by_id.get(ancestor_id)
        if ancestor is None:
            continue
        if ancestor.get("tipo") == "fonte":
            sources.append(ancestor)
        pending.extend(parents.get(ancestor_id, []))
    return sources


def _schema_errors(graph: dict, schema: dict) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"schema: {error.message}"
        for error in sorted(validator.iter_errors(graph), key=lambda error: (list(error.absolute_path), error.message))
    ]


def _manifest_source_pairs(root: Path) -> set[tuple[str, str]] | None:
    """Lê os pares canônicos de ID e arquivo, sem interromper a validação."""
    try:
        manifest = json.loads((root / MANIFEST_PATH).read_text(encoding="utf-8"))
    except (OSError, TypeError, json.JSONDecodeError):
        return None
    if not isinstance(manifest, list):
        return None
    return {
        (source["id"], source["arquivo"])
        for source in manifest
        if isinstance(source, dict)
        and isinstance(source.get("id"), str)
        and isinstance(source.get("arquivo"), str)
    }


def validate_graph(graph: dict, schema: dict, root: Path) -> list[str]:
    """Retorna erros de estrutura e de significado, sem alterar o grafo."""
    errors = _schema_errors(graph, schema)
    errors.extend(f"chave proibida: {key}" for key in _walk_keys(graph) if key in PROHIBITED_KEYS)

    metadata = graph.get("metadados", {}) if isinstance(graph, dict) else {}
    coverage = metadata.get("cobertura") if isinstance(metadata, dict) else None
    if coverage is None:
        errors.append("aviso: cobertura ausente")
    elif coverage != EXPECTED_COVERAGE:
        errors.append("cobertura parcial não corresponde ao recorte canônico")

    nodes = graph.get("nos", []) if isinstance(graph, dict) else []
    edges = graph.get("relacoes", []) if isinstance(graph, dict) else []
    nodes = nodes if isinstance(nodes, list) else []
    edges = edges if isinstance(edges, list) else []
    nodes_by_id = {}
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            continue
        node_id = node["id"]
        if node_id in nodes_by_id:
            errors.append(f"ID duplicado: {node_id}")
        else:
            nodes_by_id[node_id] = node

    source_nodes = [node for node in nodes_by_id.values() if node.get("tipo") == "fonte"]
    if len(source_nodes) != 9:
        errors.append(f"fontes inventariadas devem ser 9, recebido {len(source_nodes)}")
    expected_source_pairs = _manifest_source_pairs(root)
    if expected_source_pairs is None:
        errors.append("manifesto canônico de fontes indisponível")
    else:
        source_pairs = {
            (source["id"], source["arquivo"])
            for source in source_nodes
            if isinstance(source.get("arquivo"), str)
        }
        if source_pairs != expected_source_pairs:
            errors.append("fontes inventariadas não correspondem ao manifesto canônico")
    for source in source_nodes:
        arquivo = source.get("arquivo")
        if isinstance(arquivo, str) and "livros/sumarios/" in arquivo.replace("\\", "/").lower():
            errors.append(f"fonte derivada de livros/sumarios/: {source['id']}")

    parents = defaultdict(list)
    curriculum_by_id = {
        node_id: node.get("codigo")
        for node_id, node in nodes_by_id.items()
        if node.get("tipo") == "conteudo_curricular" and isinstance(node.get("codigo"), str)
    }
    curricular_edges_by_origin = defaultdict(set)
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        origin = edge.get("origem")
        destination = edge.get("destino")
        if not isinstance(origin, str) or not isinstance(destination, str):
            errors.append(f"aresta com extremos inválidos: {origin} -> {destination}")
            continue
        if origin not in nodes_by_id or destination not in nodes_by_id:
            errors.append(f"aresta órfã: {origin} -> {destination}")
            continue
        if edge.get("tipo") == "contem":
            parents[destination].append(origin)
        if edge.get("tipo") == "corresponde_a":
            code = curriculum_by_id.get(destination)
            if code is not None:
                curricular_edges_by_origin[origin].add(code)
            if code not in COMPLETED_CONTENTS:
                if code in PENDING_CONTENTS:
                    errors.append(f"correspondência curricular para conteúdo pendente: {code}")
                else:
                    errors.append(
                        "correspondência curricular sem conteúdo curricular concluído: "
                        f"{destination}"
                    )

    for node_id, node in nodes_by_id.items():
        if node.get("tipo") == "item_pedagogico":
            if "pertinencia_t199" not in node:
                errors.append(f"item pedagógico sem pertinência: {node_id}")
            for key, value in node.items():
                if key not in {"titulo", "nome"} and isinstance(value, str) and len(value) > 240:
                    errors.append(f"campo textual longo em item pedagógico: {node_id}.{key}")
            contents = curricular_edges_by_origin[node_id]
            if contents & COMPLETED_CONTENTS and contents & PENDING_CONTENTS:
                errors.append(f"item híbrido depende de conteúdo pendente: {node_id}")

        page_start = node.get("pagina_pdf_inicio")
        page_end = node.get("pagina_pdf_fim")
        if isinstance(page_start, int) and isinstance(page_end, int) and page_start > page_end:
            errors.append(f"intervalo de páginas invertido: {node_id}")
        page_values = [
            value
            for key, value in node.items()
            if key in {"pagina_pdf", "pagina_pdf_inicio", "pagina_pdf_fim"} and isinstance(value, int)
        ]
        if not page_values:
            continue
        sources = _source_ancestors(node_id, parents, nodes_by_id)
        if not sources:
            errors.append(f"nó paginado sem fonte ancestral: {node_id}")
            continue
        for source in sources:
            page_count = source.get("paginas_pdf")
            if not isinstance(page_count, int) or isinstance(page_count, bool):
                errors.append(f"fonte sem paginas_pdf válido: {source['id']}")
                continue
            if any(page > page_count for page in page_values):
                errors.append(f"página fora do PDF de {source['id']}: {node_id}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida um grafo de referências.")
    parser.add_argument("graph", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("prof/refs/mapas/schema_grafo_referencias.json"),
    )
    arguments = parser.parse_args()
    graph = json.loads(arguments.graph.read_text(encoding="utf-8"))
    schema = json.loads(arguments.schema.read_text(encoding="utf-8"))
    errors = validate_graph(graph, schema, Path.cwd())
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
