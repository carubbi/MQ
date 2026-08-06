"""Renderiza a visão humana, determinística, do grafo de referências."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.grafo_refs.query_graph import _nodes_by_id, _parents_by_child, _reference, query_by_content, query_by_topic


PARTIAL_COVERAGE_NOTICE = (
    "# Grafo de referências da T199\n\n"
    "> **Cobertura parcial:** esta versão mapeia somente os conteúdos `01.01` a\n"
    "> `01.04`. Ausência de resultados para outros conteúdos não indica ausência\n"
    "> de referências no corpus.\n"
)


def _coverage(graph: dict) -> dict:
    metadata = graph.get("metadados", {})
    coverage = metadata.get("cobertura", {}) if isinstance(metadata, dict) else {}
    return coverage if isinstance(coverage, dict) else {}


def _node_label(node: dict) -> str:
    kind = node.get("tipo", "referência")
    number = node.get("numero_impresso")
    title = node.get("titulo") or node.get("nome")
    parts = [kind]
    if number is not None:
        parts.append(str(number))
    if title:
        parts.append(f"— {title}")
    return " ".join(parts)


def _page_label(node: dict) -> str:
    if "pagina_pdf" in node:
        return f"página ${node['pagina_pdf']}$"
    start = node.get("pagina_pdf_inicio")
    end = node.get("pagina_pdf_fim")
    if start is None:
        return ""
    if end is None or start == end:
        return f"página ${start}$"
    return f"páginas ${start}$–${end}$"


def _reference_label(reference: dict) -> str:
    label = _node_label(reference)
    pages = _page_label(reference)
    sources = reference.get("fontes", [])
    source_label = ", ".join(source.get("titulo", source["id"]) for source in sources)
    details = "; ".join(detail for detail in (pages, source_label) if detail)
    return f"{label} ({details})" if details else label


def _descendants_by_source(graph: dict) -> dict[str, list[dict]]:
    nodes_by_id = _nodes_by_id(graph)
    parents = _parents_by_child(graph)
    grouped = defaultdict(list)
    for node_id, node in nodes_by_id.items():
        if node.get("tipo") in {"fonte", "topico", "conteudo_curricular"}:
            continue
        for source in _reference(node_id, nodes_by_id, parents)["fontes"]:
            grouped[source["id"]].append(node)
    return {
        source_id: sorted(nodes, key=lambda node: (node.get("tipo", ""), node.get("id", "")))
        for source_id, nodes in grouped.items()
    }


def _content_nodes(graph: dict) -> list[dict]:
    return sorted(
        (
            node
            for node in _nodes_by_id(graph).values()
            if node.get("tipo") == "conteudo_curricular"
        ),
        key=lambda node: node.get("codigo", ""),
    )


def render_markdown(graph: dict) -> str:
    """Deriva Markdown estável do JSON, sem acrescentar relações inexistentes."""
    coverage = _coverage(graph)
    nodes_by_id = _nodes_by_id(graph)
    lines = [PARTIAL_COVERAGE_NOTICE.rstrip(), "", "## Cobertura do corpus", ""]
    lines.extend(
        [
            f"- Estado: {coverage.get('estado', 'não declarado')}",
            f"- Critério: {coverage.get('criterio', 'não declarado')}",
            f"- Fontes inventariadas: {coverage.get('fontes_inventariadas', 'não declarado')}",
            "",
            "## Conteúdos concluídos",
            "",
        ]
    )
    completed = sorted(coverage.get("conteudos_concluidos", []))
    lines.extend(
        f"- `{code}`" + (f" — {node['nome']}" if (node := next((item for item in _content_nodes(graph) if item.get("codigo") == code), None)) and node.get("nome") else "")
        for code in completed
    )
    lines.extend(["", "## Conteúdos pendentes", ""])
    lines.extend(f"- `{code}`" for code in sorted(coverage.get("conteudos_pendentes", [])))

    lines.extend(["", "## Índice por fonte", ""])
    descendants = _descendants_by_source(graph)
    sources = sorted(
        (node for node in nodes_by_id.values() if node.get("tipo") == "fonte"),
        key=lambda node: (node.get("titulo", ""), node["id"]),
    )
    for source in sources:
        source_type = f" ({source['tipo_fonte']})" if source.get("tipo_fonte") else ""
        lines.append(f"- {source.get('titulo', source['id'])}{source_type}")
        items = descendants.get(source["id"], [])
        lines.extend(f"  - {_node_label(item)}" + (f" — {_page_label(item)}" if _page_label(item) else "") for item in items)
        if not items:
            lines.append("  - nenhum item curado nesta cobertura")

    lines.extend(["", "## Índice por conteúdo da Unidade I", ""])
    for content in (node for node in _content_nodes(graph) if node.get("unidade") == "I"):
        lines.append(f"### `{content.get('codigo', content['id'])}` — {content.get('nome', '')}".rstrip())
        results = query_by_content(graph, content.get("codigo", ""))["resultados"]
        lines.extend(f"- {_reference_label(result)}" for result in results)
        if not results:
            lines.append("- nenhuma referência curada")
        lines.append("")

    lines.extend(["## Índice por tópico", ""])
    topics = sorted(
        (node for node in nodes_by_id.values() if node.get("tipo") == "topico"),
        key=lambda node: (node.get("nome", ""), node["id"]),
    )
    for topic in topics:
        lines.append(f"### {topic.get('nome', topic['id'])}")
        results = query_by_topic(graph, topic["id"])
        lines.extend(f"- {_reference_label(result)}" for result in results)
        if not results:
            lines.append("- nenhuma referência curada")
        lines.append("")

    lines.extend(["## Itens examinados fora do escopo", "", "Esta lista não é exaustiva: inclui apenas itens efetivamente examinados durante esta cobertura parcial.", ""])
    outside_items = sorted(
        (
            node
            for node in nodes_by_id.values()
            if node.get("tipo") == "item_pedagogico" and node.get("pertinencia_t199") == "fora_do_escopo"
        ),
        key=lambda node: node["id"],
    )
    parents = _parents_by_child(graph)
    lines.extend(f"- {_reference_label(_reference(node['id'], nodes_by_id, parents))}" for node in outside_items)
    if not outside_items:
        lines.append("- nenhum item examinado registrado")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Renderiza o Markdown do grafo de referências.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    graph = json.loads(arguments.input.read_text(encoding="utf-8"))
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(render_markdown(graph), encoding="utf-8")


if __name__ == "__main__":
    main()
