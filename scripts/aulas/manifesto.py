"""Carregamento e validação dos manifestos privados de curadoria."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from scripts.aulas.grafo import (
    graph_indexes,
    node_and_descendant_ids,
    page_interval,
    source_ancestors,
)


SCHEMA_PATH = Path(__file__).with_name("schema_selecao.json")
REFERENCE_TYPES = {"secao", "exemplo", "exercicio", "questao"}
ACTIVITY_NODE_TYPES = {
    "exercicio": "exercicio",
    "questao": "questao",
    "exemplo_aplicado": "exemplo",
}
STUDENT_RESOURCE_TYPES = {
    "materiais_didaticos": {"capitulo", "secao", "exemplo"},
    "exercicios_indicados": {"exercicio", "questao"},
}


def load_manifest(path: Path) -> dict:
    """Carrega um manifesto YAML cujo nível superior deve ser um objeto."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifesto deve ser um objeto YAML")
    return value


def dump_manifest(manifest: dict) -> str:
    """Serializa o manifesto de modo legível e com ordem preservada."""
    return yaml.safe_dump(
        manifest,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )


def _schema_findings(manifest: dict) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema: {error.message}"
        for error in sorted(
            validator.iter_errors(manifest),
            key=lambda error: (list(error.absolute_path), error.message),
        )
    ]


def _cycle_findings(manifest: dict) -> list[str]:
    findings: list[str] = []
    lesson_duration = manifest.get("aula", {}).get("duracao_minutos")
    timing = manifest.get("planejamento_tempo", {})
    if not isinstance(timing, dict):
        return findings
    opening = timing.get("abertura_minutos")
    closing = timing.get("fechamento_minutos")
    cycles = manifest.get("ciclos", [])

    if not all(
        isinstance(value, int)
        for value in (lesson_duration, opening, closing)
    ):
        return findings

    available = lesson_duration - opening - closing
    if available <= 0:
        findings.append(
            "planejamento temporal não deixa minutos disponíveis para ciclos"
        )

    durations = [
        cycle.get("duracao_minima_minutos")
        for cycle in cycles
        if isinstance(cycle, dict)
    ]
    if all(isinstance(value, int) for value in durations):
        required = sum(durations)
        if available > 0 and required > available:
            findings.append(
                f"duração mínima dos ciclos ({required} min) excede "
                f"o tempo disponível ({available} min)"
            )

    topic_states = {
        topic.get("id"): topic.get("estado")
        for topic in manifest.get("topicos", [])
        if isinstance(topic, dict) and isinstance(topic.get("id"), str)
    }
    cycle_topics: list[str] = []
    for cycle in cycles:
        if not isinstance(cycle, dict):
            continue
        cycle_id = cycle.get("id")
        for topic_id in cycle.get("topicos", []):
            cycle_topics.append(topic_id)
            if topic_id not in topic_states:
                findings.append(
                    f"ciclo {cycle_id} contém tópico desconhecido: {topic_id}"
                )
            elif topic_states[topic_id] != "selecionado":
                findings.append(
                    f"ciclo {cycle_id} contém tópico não selecionado: {topic_id}"
                )
        notebook_cycle = cycle.get("aplicacao_notebook", {}).get(
            "ciclo_notebook"
        )
        if isinstance(cycle_id, str) and isinstance(notebook_cycle, str):
            if notebook_cycle != cycle_id:
                findings.append(
                    f"aplicação do ciclo {cycle_id} aponta para {notebook_cycle}"
                )

    counts = Counter(cycle_topics)
    for topic_id, count in counts.items():
        if count > 1:
            findings.append(
                f"tópico selecionado aparece em mais de um ciclo: {topic_id}"
            )
    if manifest.get("estado") == "aprovado":
        for topic_id, state in topic_states.items():
            if state == "selecionado" and counts[topic_id] == 0:
                findings.append(
                    f"tópico selecionado ausente dos ciclos: {topic_id}"
                )
    return findings


def _student_resource_findings(
    manifest: dict,
    nodes: dict[str, dict],
    relations: dict[str, set[tuple[str, str]]],
    formal_ids: set[str],
) -> list[str]:
    findings: list[str] = []
    selected_topic_ids = {
        topic.get("id")
        for topic in manifest.get("topicos", [])
        if isinstance(topic, dict) and topic.get("estado") == "selecionado"
    }
    resources = manifest.get("recursos_discentes", {})
    if not isinstance(resources, dict):
        return findings

    for list_name, accepted_types in STUDENT_RESOURCE_TYPES.items():
        for entry in resources.get(list_name, []):
            if not isinstance(entry, dict):
                continue
            resource_id = entry.get("id")
            node = nodes.get(resource_id)
            if node is None:
                findings.append(f"recurso discente desconhecido: {resource_id}")
                continue
            node_type = node.get("tipo")
            if node_type not in accepted_types:
                findings.append(
                    f"recurso {resource_id} do tipo {node_type} é inválido "
                    f"em {list_name}"
                )
                continue
            candidates = (
                node_and_descendant_ids(resource_id, relations["contem"])
                if list_name == "materiais_didaticos"
                else {resource_id}
            )
            start, end = page_interval(node)
            if not all(isinstance(value, int) for value in (start, end)):
                findings.append(
                    f"recurso {resource_id} não possui páginas verificáveis"
                )
            if not source_ancestors(resource_id, nodes, relations["contem"]):
                findings.append(f"recurso {resource_id} não pertence a uma fonte")
            if formal_ids and not any(
                (candidate_id, content_id) in relations["corresponde_a"]
                for candidate_id in candidates
                for content_id in formal_ids
            ):
                findings.append(
                    f"recurso {resource_id} não corresponde aos conteúdos da aula"
                )
            if selected_topic_ids and not any(
                (candidate_id, topic_id) in relations["aborda"]
                for candidate_id in candidates
                for topic_id in selected_topic_ids
            ):
                findings.append(
                    f"recurso {resource_id} não aborda tópico selecionado da aula"
                )
    return findings


def _activity_findings(manifest: dict, nodes: dict[str, dict]) -> list[str]:
    findings: list[str] = []
    for cycle in manifest.get("ciclos", []):
        if not isinstance(cycle, dict):
            continue
        cycle_id = cycle.get("id")
        activity = cycle.get("atividade_resolvida")
        if not isinstance(cycle_id, str) or not isinstance(activity, dict):
            continue

        reference_id = activity.get("referencia_id")
        reference_node = nodes.get(reference_id)
        if reference_node is None:
            findings.append(
                f"atividade resolvida do ciclo {cycle_id} referencia "
                f"desconhecida: {reference_id}"
            )
            continue

        origin_type = activity.get("tipo_origem")
        expected_node_type = ACTIVITY_NODE_TYPES.get(origin_type)
        node_type = reference_node.get("tipo")
        if expected_node_type is not None and node_type != expected_node_type:
            findings.append(
                f"atividade resolvida do ciclo {cycle_id} declara {origin_type}, "
                f"mas a referência {reference_id} é do tipo {node_type}"
            )

        pages = activity.get("paginas_pdf")
        if isinstance(pages, dict):
            selected_start = pages.get("inicio")
            selected_end = pages.get("fim")
            node_start, node_end = page_interval(reference_node)
            if (
                all(
                    isinstance(value, int)
                    for value in (
                        selected_start,
                        selected_end,
                        node_start,
                        node_end,
                    )
                )
                and not node_start <= selected_start <= selected_end <= node_end
            ):
                findings.append(
                    "páginas da atividade resolvida fora do intervalo de "
                    f"{reference_id}: {selected_start}-{selected_end}"
                )

        exception_justification = activity.get("justificativa_excecao")
        if origin_type == "exemplo_aplicado" and not (
            isinstance(exception_justification, str)
            and exception_justification.strip()
        ):
            findings.append(
                f"atividade resolvida do ciclo {cycle_id} do tipo "
                "exemplo_aplicado exige justificativa_excecao não vazia"
            )
        elif origin_type in {"exercicio", "questao"} and (
            exception_justification is not None
        ):
            findings.append(
                f"atividade resolvida do ciclo {cycle_id} do tipo {origin_type} "
                "deve ter justificativa_excecao nula"
            )

        selected_topic_ids = set(cycle.get("topicos", []))
        is_selected_exercise = any(
            topic.get("id") in selected_topic_ids
            and any(
                reference.get("id") == reference_id
                and reference.get("estado") == "selecionada"
                and "exercicio" in reference.get("papeis", [])
                for reference in topic.get("referencias", [])
                if isinstance(reference, dict)
            )
            for topic in manifest.get("topicos", [])
            if isinstance(topic, dict)
        )
        if not is_selected_exercise:
            findings.append(
                f"atividade resolvida do ciclo {cycle_id} não está selecionada "
                "com papel exercicio em tópico do ciclo"
            )
    return findings


def _semantic_findings(
    manifest: dict,
    graph: dict,
    *,
    require_approved: bool,
) -> list[str]:
    findings: list[str] = []
    nodes, relations = graph_indexes(graph)
    content_ids = {
        node["codigo"]: node_id
        for node_id, node in nodes.items()
        if node.get("tipo") == "conteudo_curricular"
        and isinstance(node.get("codigo"), str)
    }
    formal_codes = manifest.get("aula", {}).get("conteudos_formais", [])
    formal_ids = {content_ids.get(code) for code in formal_codes}
    formal_ids.discard(None)

    if require_approved and manifest.get("estado") != "aprovado":
        findings.append("manifesto ainda não aprovado")

    for topic in manifest.get("topicos", []):
        if not isinstance(topic, dict):
            continue
        topic_id = topic.get("id")
        topic_node = nodes.get(topic_id)
        if topic_node is None or topic_node.get("tipo") != "topico":
            findings.append(f"tópico desconhecido: {topic_id}")

        topic_state = topic.get("estado")
        if manifest.get("estado") == "aprovado" and topic_state == "pendente":
            findings.append(f"manifesto aprovado contém tópico pendente: {topic_id}")

        selected_roles: set[str] = set()
        for reference in topic.get("referencias", []):
            if not isinstance(reference, dict):
                continue
            reference_id = reference.get("id")
            reference_node = nodes.get(reference_id)
            if reference_node is None or reference_node.get("tipo") not in REFERENCE_TYPES:
                findings.append(f"referência desconhecida ou inválida: {reference_id}")
                continue

            if (reference_id, topic_id) not in relations["aborda"]:
                findings.append(
                    f"referência {reference_id} não aborda {topic_id}"
                )
            if formal_ids and not any(
                (reference_id, content_id) in relations["corresponde_a"]
                for content_id in formal_ids
            ):
                findings.append(
                    f"referência {reference_id} não corresponde aos conteúdos da aula"
                )

            source_id = reference.get("fonte_id")
            if source_id not in source_ancestors(
                reference_id,
                nodes,
                relations["contem"],
            ):
                findings.append(
                    f"fonte {source_id} não contém a referência {reference_id}"
                )

            pages = reference.get("paginas_pdf", {})
            selected_start = pages.get("inicio")
            selected_end = pages.get("fim")
            node_start, node_end = page_interval(reference_node)
            if (
                all(
                    isinstance(value, int)
                    for value in (
                        selected_start,
                        selected_end,
                        node_start,
                        node_end,
                    )
                )
                and not node_start <= selected_start <= selected_end <= node_end
            ):
                findings.append(
                    f"páginas fora do intervalo de {reference_id}: "
                    f"{selected_start}-{selected_end}"
                )

            reference_state = reference.get("estado")
            if manifest.get("estado") == "aprovado" and reference_state == "pendente":
                findings.append(
                    f"manifesto aprovado contém referência pendente: {reference_id}"
                )
            if reference_state == "selecionada":
                selected_roles.update(reference.get("papeis", []))

        if topic_state == "selecionado" and "fundamentacao" not in selected_roles:
            findings.append(
                f"tópico selecionado sem referência de fundamentação: {topic_id}"
            )

    if manifest.get("estado") == "aprovado" and not manifest.get("ciclos"):
        findings.append("manifesto aprovado deve definir ao menos um ciclo")
    findings.extend(
        _student_resource_findings(
            manifest,
            nodes,
            relations,
            formal_ids,
        )
    )
    findings.extend(_activity_findings(manifest, nodes))
    findings.extend(_cycle_findings(manifest))
    return findings


def validate_manifest(
    manifest: dict,
    graph: dict,
    *,
    require_approved: bool = False,
) -> list[str]:
    """Retorna achados estruturais e semânticos sem alterar as entradas."""
    findings = _schema_findings(manifest)
    if not (
        isinstance(manifest, dict)
        and isinstance(manifest.get("aula"), dict)
        and isinstance(manifest.get("topicos"), list)
    ):
        return findings
    findings.extend(
        _semantic_findings(
            manifest,
            graph,
            require_approved=require_approved,
        )
    )
    return findings
