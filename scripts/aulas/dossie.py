"""Renderiza o dossiê legível a partir do manifesto canônico."""

from __future__ import annotations

from scripts.aulas.grafo import graph_indexes, page_interval, source_ancestors


def _markdown_items(values: list[str], *, indentation: str = "") -> list[str]:
    items = values or ["Nenhum."]
    return [f"{indentation}- {value}" for value in items]


def _render_scope(scope: dict) -> list[str]:
    lines: list[str] = []
    for title, key in (
        ("Incluídos", "incluidos"),
        ("Excluídos", "excluidos"),
        ("Reservados para aulas posteriores", "reservados"),
    ):
        lines.extend([f"### {title}", ""])
        lines.extend(_markdown_items(scope[key]))
        lines.extend([""])
    return lines[:-1]


def _render_time_plan(manifest: dict) -> list[str]:
    lesson_minutes = manifest["aula"]["duracao_minutos"]
    timing = manifest["planejamento_tempo"]
    opening = timing["abertura_minutos"]
    closing = timing["fechamento_minutos"]
    available = lesson_minutes - opening - closing
    return [
        "## Planejamento temporal",
        "",
        f"- **Duração da aula:** {lesson_minutes} minutos",
        f"- **Abertura:** {opening} minutos",
        f"- **Fechamento:** {closing} minutos",
        f"- **Disponível para desenvolvimento:** {available} minutos",
    ]


def _render_topic(topic: dict) -> list[str]:
    compatibility = topic["compatibilizacao"]
    lines = [
        f"### {topic['nome']} — {topic['estado']}",
        "",
        f"- **ID:** `{topic['id']}`",
        f"- **Classificação:** {topic['classificacao']}",
        f"- **Profundidade:** {topic['profundidade']}",
        "- **Subassuntos:**",
        *_markdown_items(topic["subassuntos"], indentation="  "),
        "- **Divergências:**",
        *_markdown_items(topic["divergencias"], indentation="  "),
        (
            "- **Compatibilização:** "
            f"{compatibility['convencao']} — {compatibility['observacao']}"
        ),
        "",
    ]
    for index, reference in enumerate(topic["referencias"], start=1):
        pages = reference["paginas_pdf"]
        roles = ", ".join(reference["papeis"]) or "—"
        marker = f"{index}."
        indentation = " " * (len(marker) + 1)
        lines.extend(
            [
                f"{marker} **`{reference['id']}`**",
                f"{indentation}- **Fonte:** `{reference['fonte_id']}`",
                f"{indentation}- **Estado:** {reference['estado']}",
                f"{indentation}- **Papéis:** {roles}",
                (
                    f"{indentation}- **Páginas PDF:** "
                    f"{pages['inicio']}–{pages['fim']}"
                ),
                f"{indentation}- **Cobertura:** {reference['cobertura']}",
                f"{indentation}- **Notação:** {reference['notacao']}",
                "",
            ]
        )
    return lines


def _page_label(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}–{end}"


def _render_resource_list(
    title: str,
    entries: list[dict],
    nodes: dict[str, dict],
    contains: set[tuple[str, str]],
) -> list[str]:
    if not entries:
        return []
    lines = [f"### {title}", ""]
    for index, entry in enumerate(entries, start=1):
        resource_id = entry["id"]
        node = nodes[resource_id]
        start, end = page_interval(node)
        source_ids = sorted(source_ancestors(resource_id, nodes, contains))
        number = node.get("numero_impresso")
        label = node.get("titulo") or (
            f"Item {number}" if number else resource_id
        )
        lines.extend(
            [
                f"{index}. **`{resource_id}`** — {label}",
                f"   - **Fonte:** `{source_ids[0]}`",
                f"   - **Tipo:** {node['tipo']}",
                f"   - **Páginas PDF:** {_page_label(start, end)}",
                "",
            ]
        )
    return lines


def _render_student_resources(manifest: dict, graph: dict) -> list[str]:
    resources = manifest.get("recursos_discentes", {})
    materials = resources.get("materiais_didaticos", [])
    exercises = resources.get("exercicios_indicados", [])
    if not materials and not exercises:
        return []
    nodes, relations = graph_indexes(graph)
    lines = ["## Recursos discentes", ""]
    lines.extend(
        _render_resource_list(
            "Materiais didáticos",
            materials,
            nodes,
            relations["contem"],
        )
    )
    lines.extend(
        _render_resource_list(
            "Exercícios indicados",
            exercises,
            nodes,
            relations["contem"],
        )
    )
    return lines


def render_dossier(manifest: dict, graph: dict) -> str:
    """Produz Markdown determinístico sem alterar o manifesto recebido."""
    lesson = manifest["aula"]
    lines = [
        f"# Dossiê de curadoria — {lesson['id']}",
        "",
        f"- **Título:** {lesson['titulo']}",
        f"- **Data:** {lesson['data']}",
        f"- **Duração:** {lesson['duracao_minutos']} minutos",
        f"- **Conteúdos formais:** {', '.join(lesson['conteudos_formais'])}",
        f"- **Estado:** {manifest['estado']}",
        "",
        "## Escopo do encontro",
        "",
    ]
    lines.extend(_render_scope(manifest["escopo"]))
    lines.extend([""])
    lines.extend(_render_time_plan(manifest))
    resources = _render_student_resources(manifest, graph)
    if resources:
        lines.extend([""])
        lines.extend(resources)
    lines.extend(["", "## Tópicos candidatos", ""])
    for topic in manifest["topicos"]:
        lines.extend(_render_topic(topic))
    lines.extend(
        [
            "---",
            "",
            "Este dossiê é derivado de `selecao.yaml`; registre decisões somente no YAML.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
