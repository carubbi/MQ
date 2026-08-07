"""Consultas reproduzíveis sobre o grafo canônico de referências."""

import argparse
import json
from collections import defaultdict
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GRAPH = REPOSITORY_ROOT / "prof/refs/mapas/grafo_referencias.json"
REFERENCE_FIELDS = (
    "id",
    "tipo",
    "numero_impresso",
    "titulo",
    "nome",
    "pagina_pdf",
    "pagina_pdf_inicio",
    "pagina_pdf_fim",
    "pagina_impressa",
    "pagina_impressa_inicio",
    "pertinencia_t199",
)


def _nodes_by_id(graph: dict) -> dict[str, dict]:
    return {
        node["id"]: node
        for node in graph.get("nos", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }


def _parents_by_child(graph: dict) -> dict[str, list[str]]:
    parents = defaultdict(list)
    for edge in graph.get("relacoes", []):
        if isinstance(edge, dict) and edge.get("tipo") == "contem":
            origin = edge.get("origem")
            destination = edge.get("destino")
            if isinstance(origin, str) and isinstance(destination, str):
                parents[destination].append(origin)
    return parents


def _source_context(node_id: str, nodes_by_id: dict[str, dict], parents: dict[str, list[str]]) -> list[dict]:
    """Retorna todas as fontes ancestrais de uma referência, em ordem estável."""
    pending = list(parents.get(node_id, []))
    visited = set()
    sources = []
    while pending:
        ancestor_id = pending.pop()
        if ancestor_id in visited:
            continue
        visited.add(ancestor_id)
        ancestor = nodes_by_id.get(ancestor_id)
        if ancestor is None:
            continue
        if ancestor.get("tipo") == "fonte":
            source = {"id": ancestor_id}
            if "titulo" in ancestor:
                source["titulo"] = ancestor["titulo"]
            sources.append(source)
        pending.extend(parents.get(ancestor_id, []))
    return sorted(sources, key=lambda source: (source.get("titulo", ""), source["id"]))


def _reference(node_id: str, nodes_by_id: dict[str, dict], parents: dict[str, list[str]]) -> dict:
    node = nodes_by_id[node_id]
    result = {field: node[field] for field in REFERENCE_FIELDS if field in node}
    result["fontes"] = _source_context(node_id, nodes_by_id, parents)
    return result


def _references_for_relation(graph: dict, relation_type: str, destination_id: str) -> list[dict]:
    nodes_by_id = _nodes_by_id(graph)
    parents = _parents_by_child(graph)
    matching_ids = {
        edge.get("origem")
        for edge in graph.get("relacoes", [])
        if isinstance(edge, dict)
        and edge.get("tipo") == relation_type
        and edge.get("destino") == destination_id
        and edge.get("origem") in nodes_by_id
    }
    return sorted(
        (_reference(node_id, nodes_by_id, parents) for node_id in matching_ids),
        key=lambda reference: (reference.get("tipo", ""), reference.get("id", "")),
    )


def _coverage_codes(graph: dict, key: str) -> set[str]:
    coverage = graph.get("metadados", {}).get("cobertura", {})
    values = coverage.get(key, []) if isinstance(coverage, dict) else []
    return {value for value in values if isinstance(value, str)}


def query_by_content(graph: dict, code: str) -> dict:
    """Consulta referências de um conteúdo, sem confundir pendência com ausência."""
    completed = _coverage_codes(graph, "conteudos_concluidos")
    content = next(
        (
            node
            for node in _nodes_by_id(graph).values()
            if node.get("tipo") == "conteudo_curricular" and node.get("codigo") == code
        ),
        None,
    )
    if content is None:
        return {"estado": "desconhecido", "resultados": []}
    if code in completed:
        return {
            "estado": "concluido",
            "resultados": _references_for_relation(graph, "corresponde_a", content["id"]),
        }
    return {"estado": "pendente", "resultados": []}


def query_by_topic(graph: dict, topic_id: str) -> list[dict]:
    """Retorna somente referências explicitamente ligadas ao tópico solicitado."""
    return _references_for_relation(graph, "aborda", topic_id)


def _read_graph(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Consulta o grafo de referências da T199.")
    parser.add_argument("graph", nargs="?", type=Path, default=DEFAULT_GRAPH)
    query_group = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument("--content", metavar="CODE")
    query_group.add_argument("--topic", metavar="TOPIC_ID")
    arguments = parser.parse_args()
    graph = _read_graph(arguments.graph)

    if arguments.content is not None:
        result = query_by_content(graph, arguments.content)
        if result["estado"] == "pendente":
            print(f"conteúdo ainda não mapeado: {arguments.content}")
            raise SystemExit(2)
    else:
        result = query_by_topic(graph, arguments.topic)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
