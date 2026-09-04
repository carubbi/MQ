"""Interface de linha de comando para validar e renderizar curadorias."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.aulas.dossie import render_dossier
from scripts.aulas.estrutura import (
    approve_structure,
    dump_structure,
    load_structure,
    mark_published,
    validate_structure,
)
from scripts.aulas.manifesto import load_manifest, validate_manifest
from scripts.aulas.notebooks import (
    extract_header,
    load_notebook,
    validate_notebook_pair,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validar", help="validar um manifesto")
    validate.add_argument("--manifesto", type=Path, required=True)
    validate.add_argument("--grafo", type=Path, required=True)
    validate.add_argument("--exigir-aprovado", action="store_true")

    render = commands.add_parser("renderizar", help="renderizar um dossiê")
    render.add_argument("--manifesto", type=Path, required=True)
    render.add_argument("--grafo", type=Path, required=True)
    render.add_argument("--saida", type=Path, required=True)

    for name, help_text in (
        ("validar-estrutura", "validar um contrato editorial"),
        ("aprovar-estrutura", "registrar a aprovação editorial"),
        ("validar-notebooks", "validar conjuntamente os notebooks canônicos"),
        ("registrar-publicacao", "registrar a publicação lógica dos notebooks"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--manifesto", type=Path, required=True)
        command.add_argument("--grafo", type=Path, required=True)
        command.add_argument("--estrutura", type=Path, required=True)
        command.add_argument("--raiz-repositorio", type=Path, required=True)
        if name == "aprovar-estrutura":
            command.add_argument("--aprovado-em", required=True)
        if name in {"validar-notebooks", "registrar-publicacao"}:
            command.add_argument("--cabecalho", type=Path, required=True)
        if name == "registrar-publicacao":
            command.add_argument("--publicado-em", required=True)
    return parser


def _load_graph(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("grafo deve ser um objeto JSON")
    return value


def _report(findings: list[str]) -> int:
    for finding in findings:
        print(finding, file=sys.stderr)
    return 1


def _load_curation(manifest_path: Path, graph_path: Path) -> tuple[dict, dict]:
    manifest = load_manifest(manifest_path)
    graph = _load_graph(graph_path)
    findings = validate_manifest(manifest, graph, require_approved=True)
    if findings:
        raise ValueError("\n".join(findings))
    return manifest, graph


def _write_structure(path: Path, metadata: dict, body: str) -> None:
    path.write_text(dump_structure(metadata, body), encoding="utf-8")


def _load_pair(manifest: dict, repository_root: Path):
    lesson_id = manifest["aula"]["id"]
    room_path = repository_root / "notebooks" / f"{lesson_id}.ipynb"
    solved_path = (
        repository_root / "notebooks" / "resolvidos" / f"{lesson_id}.ipynb"
    )
    room, room_hash = load_notebook(room_path)
    solved, solved_hash = load_notebook(solved_path)
    return room, room_hash, solved, solved_hash


def _pair_findings(arguments, manifest: dict, metadata: dict, body: str):
    room, room_hash, solved, solved_hash = _load_pair(
        manifest,
        arguments.raiz_repositorio,
    )
    header = extract_header(arguments.cabecalho)
    findings = validate_notebook_pair(
        manifest=manifest,
        structure_metadata=metadata,
        structure_body=body,
        header=header,
        room_notebook=room,
        room_sha256=room_hash,
        solved_notebook=solved,
        solved_sha256=solved_hash,
        repository_root=arguments.raiz_repositorio,
    )
    return (
        findings,
        {"sala": room_hash, "resolvido": solved_hash},
        room,
        solved,
        header,
    )


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command in {
            "validar-estrutura",
            "aprovar-estrutura",
            "validar-notebooks",
            "registrar-publicacao",
        }:
            manifest, _ = _load_curation(arguments.manifesto, arguments.grafo)
            metadata, body = load_structure(arguments.estrutura)

            if arguments.command == "validar-estrutura":
                findings = validate_structure(
                    metadata,
                    body,
                    manifest,
                    arguments.raiz_repositorio,
                )
                if findings:
                    return _report(findings)
                print("estrutura válida")
                return 0

            if arguments.command == "aprovar-estrutura":
                findings = validate_structure(
                    metadata,
                    body,
                    manifest,
                    arguments.raiz_repositorio,
                )
                if findings:
                    return _report(findings)
                approved = approve_structure(metadata, body, arguments.aprovado_em)
                findings = validate_structure(
                    approved,
                    body,
                    manifest,
                    arguments.raiz_repositorio,
                )
                if findings:
                    return _report(findings)
                _write_structure(arguments.estrutura, approved, body)
                print("estrutura aprovada")
                return 0

            findings, hashes, room, solved, header = _pair_findings(
                arguments,
                manifest,
                metadata,
                body,
            )
            if findings:
                return _report(findings)
            if arguments.command == "validar-notebooks":
                print("notebooks válidos")
                return 0

            published = mark_published(
                metadata,
                body,
                hashes,
                arguments.publicado_em,
            )
            findings = validate_notebook_pair(
                manifest=manifest,
                structure_metadata=published,
                structure_body=body,
                header=header,
                room_notebook=room,
                room_sha256=hashes["sala"],
                solved_notebook=solved,
                solved_sha256=hashes["resolvido"],
                repository_root=arguments.raiz_repositorio,
            )
            if findings:
                return _report(findings)
            _write_structure(arguments.estrutura, published, body)
            print("publicação registrada")
            return 0

        manifest = load_manifest(arguments.manifesto)
        graph = _load_graph(arguments.grafo)
        findings = validate_manifest(
            manifest,
            graph,
            require_approved=(
                arguments.command == "validar" and arguments.exigir_aprovado
            ),
        )
        if findings:
            return _report(findings)
        if arguments.command == "renderizar":
            arguments.saida.parent.mkdir(parents=True, exist_ok=True)
            arguments.saida.write_text(
                render_dossier(manifest, graph),
                encoding="utf-8",
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
