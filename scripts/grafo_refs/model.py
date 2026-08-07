"""Transformações do modelo canônico do grafo de referências."""

import re
import unicodedata


ITEM_TYPES = {"questao", "exercicio", "exemplo"}
ITEM_FIELDS = (
    "id",
    "tipo",
    "numero_impresso",
    "pagina_pdf",
    "pagina_impressa",
    "pertinencia_t199",
)


CANONICAL_FIELDS_BY_TYPE = {
    "fonte": (
        "id",
        "tipo",
        "tipo_fonte",
        "titulo",
        "arquivo",
        "paginas_pdf",
        "idioma",
        "hash_sha256",
    ),
    "capitulo": (
        "id",
        "tipo",
        "numero_impresso",
        "titulo",
        "pagina_pdf_inicio",
        "pagina_pdf_fim",
        "pagina_impressa_inicio",
    ),
    "secao": (
        "id",
        "tipo",
        "numero_impresso",
        "titulo",
        "pagina_pdf_inicio",
        "pagina_pdf_fim",
        "pagina_impressa_inicio",
        "pertinencia_t199",
    ),
    **{item_type: ITEM_FIELDS for item_type in ITEM_TYPES},
    "topico": ("id", "tipo", "nome"),
    "conteudo_curricular": ("id", "tipo", "codigo", "unidade", "nome"),
}


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
    explicit_precedence = []
    sibling_groups = {}

    for curated_node in nodes:
        try:
            allowed_fields = CANONICAL_FIELDS_BY_TYPE[curated_node["tipo"]]
        except KeyError as error:
            raise ValueError("tipo de nó curado desconhecido") from error

        node = {
            field: curated_node[field]
            for field in allowed_fields
            if field in curated_node
        }
        parent_id = curated_node.get("pai", source_id)
        topics = curated_node.get("topicos", [])
        contents = curated_node.get("conteudos", [])
        explicit_precedence.extend(
            {
                "origem": node["id"],
                "tipo": "precede",
                "destino": destination,
            }
            for destination in curated_node.get("precede_publicados", [])
        )
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

    edges.extend(explicit_precedence)
    unique_edges = {
        (edge["origem"], edge["tipo"], edge["destino"]): edge
        for edge in edges
    }
    return canonical_nodes, list(unique_edges.values())
