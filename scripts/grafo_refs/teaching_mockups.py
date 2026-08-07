"""Criação e validação dos mockups de aulas e notebooks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CONTENT_RE = re.compile(r"\b\d{2}\.\d{2}\b")
TOPICS_RE = re.compile(r"^- \*\*Tópicos:\*\* (.+)$", re.MULTILINE)
AULA_RE = re.compile(
    r"\A#[^\n]+\n\n"
    r"- \*\*Disciplina:\*\* [^\n]+\n"
    r"- \*\*Unidade:\*\* [^\n]+\n"
    r"- \*\*Semana:\*\* [^\n]+\n"
    r"- \*\*Data:\*\* [^\n]+\n"
    r"- \*\*Conteúdos formais:\*\* [^\n]+\n"
    r"- \*\*Tópicos:\*\* [^\n]+\n"
    r"- \*\*Resultado de aprendizagem:\*\* [^\n]+\n\n"
    r"---\n?\Z"
)


def _known_values(graph: dict) -> tuple[set[str], set[str]]:
    contents = {
        node["codigo"]
        for node in graph["nos"]
        if node.get("tipo") == "conteudo_curricular"
    }
    topics = {
        node["nome"]
        for node in graph["nos"]
        if node.get("tipo") == "topico"
    }
    return contents, topics


def validate_aula_mockup(path: Path, graph: dict) -> list[str]:
    """Retorna os achados estruturais e curriculares de um mockup de aula."""
    source = path.read_text(encoding="utf-8")
    findings: list[str] = []

    if AULA_RE.fullmatch(source) is None:
        findings.append("conteúdo adicional no mockup")

    known_contents, known_topics = _known_values(graph)
    for code in sorted(set(CONTENT_RE.findall(source)) - known_contents):
        findings.append(f"conteúdo curricular desconhecido: {code}")

    topic_match = TOPICS_RE.search(source)
    if topic_match is not None:
        topics = {
            item.strip().strip("`")
            for item in topic_match.group(1).split(";")
            if item.strip()
        }
        for topic in sorted(topics - known_topics):
            findings.append(f"tópico desconhecido: {topic}")

    return findings


def build_notebook_mockup(head_text: str) -> dict:
    """Constrói um notebook não executável com apenas o cabeçalho institucional."""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "head-unifor",
                "metadata": {},
                "source": head_text.splitlines(keepends=True),
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def validate_notebook_mockup(path: Path, head_text: str) -> list[str]:
    """Retorna os achados estruturais de um notebook-mockup."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    findings: list[str] = []

    if len(cells) != 1 or cells[0].get("cell_type") != "markdown":
        findings.append("mockup deve conter uma única célula Markdown")

    if (
        len(cells) != 1
        or "".join(cells[0].get("source", [])) != head_text
    ):
        findings.append("cabeçalho do notebook divergente")

    return findings


def _create_notebooks(paths: list[Path], head_text: str) -> list[str]:
    existing = [path for path in paths if path.exists()]
    if existing:
        return [f"{path}: arquivo já existe" for path in existing]

    notebook = build_notebook_mockup(head_text)
    serialized = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(serialized, encoding="utf-8")
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path)
    parser.add_argument("--head", type=Path)
    parser.add_argument("--aula", type=Path, action="append", default=[])
    parser.add_argument("--notebook", type=Path, action="append", default=[])
    parser.add_argument(
        "--create-notebook",
        type=Path,
        action="append",
        default=[],
    )
    arguments = parser.parse_args()

    if not (
        arguments.aula
        or arguments.notebook
        or arguments.create_notebook
    ):
        parser.error("informe ao menos um recurso")
    if arguments.aula and arguments.graph is None:
        parser.error("--graph é obrigatório para validar aulas")
    if (
        arguments.notebook or arguments.create_notebook
    ) and arguments.head is None:
        parser.error("--head é obrigatório para notebooks")

    head_text = (
        arguments.head.read_text(encoding="utf-8")
        if arguments.head is not None
        else ""
    )
    findings: list[str] = []

    if arguments.create_notebook:
        findings.extend(
            _create_notebooks(arguments.create_notebook, head_text)
        )

    if arguments.aula:
        graph = json.loads(arguments.graph.read_text(encoding="utf-8"))
        for path in arguments.aula:
            for finding in validate_aula_mockup(path, graph):
                findings.append(f"{path}: {finding}")

    for path in arguments.notebook:
        for finding in validate_notebook_mockup(path, head_text):
            findings.append(f"{path}: {finding}")

    for finding in findings:
        print(finding, file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
