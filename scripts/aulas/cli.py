"""Interface de linha de comando para validar e renderizar curadorias."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.aulas.dossie import render_dossier
from scripts.aulas.manifesto import load_manifest, validate_manifest


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


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
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
                render_dossier(manifest),
                encoding="utf-8",
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
