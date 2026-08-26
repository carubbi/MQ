"""Renderiza o dossiê legível a partir do manifesto canônico."""

from __future__ import annotations


def _text_list(values: list[str]) -> str:
    return "; ".join(values) if values else "Nenhum."


def _render_scope(scope: dict) -> list[str]:
    return [
        "### Incluídos",
        "",
        _text_list(scope["incluidos"]),
        "",
        "### Excluídos",
        "",
        _text_list(scope["excluidos"]),
        "",
        "### Reservados para aulas posteriores",
        "",
        _text_list(scope["reservados"]),
    ]


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
        f"- **Disponível para ciclos:** {available} minutos",
    ]


def _render_cycles(cycles: list[dict]) -> list[str]:
    lines = ["## Ciclos conceituais", ""]
    if not cycles:
        return [*lines, "Ciclos ainda não definidos."]
    for cycle in cycles:
        application = cycle["aplicacao_notebook"]
        topics = ", ".join(
            f"`{topic_id}`" for topic_id in cycle["topicos"]
        )
        lines.extend(
            [
                f"### {cycle['id']} — {cycle['titulo']}",
                "",
                f"- **Tópicos:** {topics}",
                f"- **Complexidade:** {cycle['complexidade']}",
                (
                    "- **Duração mínima:** "
                    f"{cycle['duracao_minima_minutos']} minutos"
                ),
                (
                    "- **Justificativa da partição:** "
                    f"{cycle['justificativa_particao']}"
                ),
                "- **Aplicação no notebook:**",
                f"  - **Objetivo:** {application['objetivo']}",
                f"  - **Pergunta:** {application['pergunta']}",
                f"  - **Contraste:** {application['contraste']}",
                f"  - **Evidência:** {application['evidencia']}",
                f"  - **Ciclo:** `{application['ciclo_notebook']}`",
                f"  - **Caminho:** `{application['caminho']}`",
                "",
            ]
        )
    return lines


def _render_topic(topic: dict) -> list[str]:
    compatibility = topic["compatibilizacao"]
    lines = [
        f"### {topic['nome']} — {topic['estado']}",
        "",
        f"- **ID:** `{topic['id']}`",
        f"- **Classificação:** {topic['classificacao']}",
        f"- **Profundidade:** {topic['profundidade']}",
        f"- **Subassuntos:** {_text_list(topic['subassuntos'])}",
        f"- **Divergências:** {_text_list(topic['divergencias'])}",
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


def render_dossier(manifest: dict) -> str:
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
    lines.extend([""])
    lines.extend(_render_cycles(manifest["ciclos"]))
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
