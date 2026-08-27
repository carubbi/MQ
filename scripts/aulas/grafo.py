"""Índices e travessias compartilhados do grafo de referências."""

from __future__ import annotations

from collections import defaultdict


def graph_indexes(
    graph: dict,
) -> tuple[dict[str, dict], dict[str, set[tuple[str, str]]]]:
    """Indexa nós e relações válidas sem alterar o grafo recebido."""
    nodes = {
        node["id"]: node
        for node in graph.get("nos", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    relations: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for edge in graph.get("relacoes", []):
        if not isinstance(edge, dict):
            continue
        values = (edge.get("tipo"), edge.get("origem"), edge.get("destino"))
        if all(isinstance(value, str) for value in values):
            relation_type, origin, destination = values
            relations[relation_type].add((origin, destination))
    return nodes, relations


def source_ancestors(
    node_id: str,
    nodes: dict[str, dict],
    contains: set[tuple[str, str]],
) -> set[str]:
    """Retorna as fontes ancestrais de um nó pela relação ``contem``."""
    parents: dict[str, set[str]] = defaultdict(set)
    for parent, child in contains:
        parents[child].add(parent)
    found: set[str] = set()
    pending = list(parents.get(node_id, set()))
    visited: set[str] = set()
    while pending:
        ancestor_id = pending.pop()
        if ancestor_id in visited:
            continue
        visited.add(ancestor_id)
        if nodes.get(ancestor_id, {}).get("tipo") == "fonte":
            found.add(ancestor_id)
        pending.extend(parents.get(ancestor_id, set()))
    return found


def node_and_descendant_ids(
    node_id: str,
    contains: set[tuple[str, str]],
) -> set[str]:
    """Retorna um nó e todos os seus descendentes pela relação ``contem``."""
    children: dict[str, set[str]] = defaultdict(set)
    for parent, child in contains:
        children[parent].add(child)
    found = {node_id}
    pending = list(children.get(node_id, set()))
    while pending:
        descendant_id = pending.pop()
        if descendant_id in found:
            continue
        found.add(descendant_id)
        pending.extend(children.get(descendant_id, set()))
    return found


def page_interval(node: dict) -> tuple[int | None, int | None]:
    """Obtém o intervalo de páginas de um nó concreto do grafo."""
    if isinstance(node.get("pagina_pdf"), int):
        return node["pagina_pdf"], node["pagina_pdf"]
    return node.get("pagina_pdf_inicio"), node.get("pagina_pdf_fim")
