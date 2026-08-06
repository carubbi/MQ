"""Transformações do modelo canônico do grafo de referências."""

import re
import unicodedata


def slug_id(value: str) -> str:
    """Normaliza texto em um identificador ASCII estável."""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")


def flatten_curated_source(
    source_id: str, nodes: list[dict]
) -> tuple[list[dict], list[dict]]:
    """Transforma campos de curadoria em nós e relações canônicos."""
    canonical_nodes = []
    edges = []
    sibling_groups = {}

    for curated_node in nodes:
        node = curated_node.copy()
        parent_id = node.pop("pai", source_id)
        topics = node.pop("topicos", [])
        contents = node.pop("conteudos", [])
        node_id = node["id"]

        canonical_nodes.append(node)
        edges.append({"origem": parent_id, "tipo": "contem", "destino": node_id})
        sibling_groups.setdefault(parent_id, []).append(node_id)
        edges.extend(
            {"origem": node_id, "tipo": "aborda", "destino": topic_id}
            for topic_id in topics
        )
        edges.extend(
            {
                "origem": node_id,
                "tipo": "corresponde_a",
                "destino": content_id,
            }
            for content_id in contents
        )

    for siblings in sibling_groups.values():
        edges.extend(
            {"origem": current, "tipo": "precede", "destino": following}
            for current, following in zip(siblings, siblings[1:])
        )

    return canonical_nodes, edges
