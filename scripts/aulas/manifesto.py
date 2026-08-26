"""Carregamento e validação dos manifestos privados de curadoria."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = Path(__file__).with_name("schema_selecao.json")
REFERENCE_TYPES = {"secao", "exemplo", "exercicio", "questao"}


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


def _graph_indexes(graph: dict) -> tuple[dict[str, dict], dict[str, set[tuple[str, str]]]]:
    nodes = {
        node["id"]: node
        for node in graph.get("nos", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    relations: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for edge in graph.get("relacoes", []):
        if not isinstance(edge, dict):
            continue
        relation_type = edge.get("tipo")
        origin = edge.get("origem")
        destination = edge.get("destino")
        if all(isinstance(value, str) for value in (relation_type, origin, destination)):
            relations[relation_type].add((origin, destination))
    return nodes, relations


def _source_ancestors(
    node_id: str,
    nodes: dict[str, dict],
    contains: set[tuple[str, str]],
) -> set[str]:
    parents: dict[str, set[str]] = defaultdict(set)
    for parent, child in contains:
        parents[child].add(parent)
    ancestors: set[str] = set()
    pending = list(parents.get(node_id, set()))
    visited: set[str] = set()
    while pending:
        ancestor_id = pending.pop()
        if ancestor_id in visited:
            continue
        visited.add(ancestor_id)
        ancestor = nodes.get(ancestor_id, {})
        if ancestor.get("tipo") == "fonte":
            ancestors.add(ancestor_id)
        pending.extend(parents.get(ancestor_id, set()))
    return ancestors


def _page_interval(node: dict) -> tuple[int | None, int | None]:
    if isinstance(node.get("pagina_pdf"), int):
        return node["pagina_pdf"], node["pagina_pdf"]
    return node.get("pagina_pdf_inicio"), node.get("pagina_pdf_fim")


def _semantic_findings(
    manifest: dict,
    graph: dict,
    *,
    require_approved: bool,
) -> list[str]:
    findings: list[str] = []
    nodes, relations = _graph_indexes(graph)
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
            if source_id not in _source_ancestors(
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
            node_start, node_end = _page_interval(reference_node)
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
