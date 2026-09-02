"""Carregamento e validação dos manifestos privados de curadoria."""

from __future__ import annotations

import json
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


def _time_findings(manifest: dict) -> list[str]:
    lesson_duration = manifest.get("aula", {}).get("duracao_minutos")
    timing = manifest.get("planejamento_tempo", {})
    if not isinstance(timing, dict):
        return []
    opening = timing.get("abertura_minutos")
    closing = timing.get("fechamento_minutos")
    if not all(
        isinstance(value, int)
        for value in (lesson_duration, opening, closing)
    ):
        return []
    if lesson_duration - opening - closing <= 0:
        return [
            "planejamento temporal não deixa minutos para desenvolvimento"
        ]
    return []


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

    findings.extend(
        _student_resource_findings(
            manifest,
            nodes,
            relations,
            formal_ids,
        )
    )
    findings.extend(_time_findings(manifest))
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
