"""Validação estrutural dos recursos didáticos em Markdown."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


AULA_HEADINGS = (
    "## Pergunta orientadora",
    "## Conceitos e definições",
    "## Notação e formulação matemática",
    "## Exemplo proposto",
    "## Resolução do exemplo",
    "## Aplicação ou discussão em sala",
    "## Erros comuns e cuidados interpretativos",
    "## Síntese",
    "## Estudo e exercícios",
    "## Referências",
)

ROTEIRO_HEADINGS = (
    "## 1. Identificação",
    "## 2. Resultado de aprendizagem",
    "## 3. Contexto e pergunta-problema",
    "## 4. Preparação conceitual",
    "## 5. Dados, entradas e dependências",
    "## 6. Antecipação conceitual antes do cálculo ou da execução",
    "## 8. Sequência funcional do futuro notebook",
    "## 9. Verificação e contraste",
    "## 10. Evidência de aprendizagem",
    "## 11. Síntese e limitações",
    "## 12. Estudo, exercícios e referências",
    "## 13. Critérios para implementação futura",
)

CONTENT_RE = re.compile(r"\b\d{2}\.\d{2}\b")
TOPICS_RE = re.compile(r"^- \*\*Tópicos:\*\* (.+)$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN_LATEX = ("\\(", "\\)", "\\[", "\\]")
FORBIDDEN_MARKERS = ("TODO", "TBD")
THEORETICAL_DATASET_TERMS = {
    "palmer penguins": "Palmer Penguins",
    "penguins_raw.csv": "penguins_raw.csv",
    "penguins.csv": "penguins.csv",
}
FORBIDDEN_MARP_RE = re.compile(
    r"^(?:marp|theme|paginate|math):\s*",
    re.MULTILINE | re.IGNORECASE,
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


def _broken_links(path: Path, text: str) -> list[str]:
    findings = []
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = (path.parent / target.split("#", 1)[0]).resolve()
        if not target_path.exists():
            findings.append(f"link local quebrado: {target}")
    return findings


def validate_resource(
    path: Path,
    kind: str,
    graph: dict,
    text: str | None = None,
) -> list[str]:
    """Retorna achados de validação; uma lista vazia representa sucesso."""
    if kind not in {"aula", "roteiro"}:
        raise ValueError(f"tipo de recurso inválido: {kind}")

    source = path.read_text(encoding="utf-8") if text is None else text
    findings: list[str] = []
    headings = AULA_HEADINGS if kind == "aula" else ROTEIRO_HEADINGS

    for heading in headings:
        if heading not in source:
            findings.append(f"seção ausente: {heading}")

    if kind == "aula" and "\n---\n" not in source:
        findings.append("separador editorial ausente")
    if kind == "roteiro" and "não executável" not in source:
        findings.append("estado não executável ausente")
    if FORBIDDEN_MARP_RE.search(source):
        findings.append("diretiva Marp proibida")
    if any(delimiter in source for delimiter in FORBIDDEN_LATEX):
        findings.append("delimitador LaTeX proibido")

    for marker in FORBIDDEN_MARKERS:
        if re.search(rf"\b{marker}\b", source):
            findings.append(f"marcador incompleto proibido: {marker}")

    known_contents, known_topics = _known_values(graph)
    codes = set(CONTENT_RE.findall(source))
    if not codes:
        findings.append("conteúdo formal ausente")
    for code in sorted(codes - known_contents):
        findings.append(f"conteúdo curricular desconhecido: {code}")

    topic_match = TOPICS_RE.search(source)
    if topic_match is None:
        findings.append("tópicos ausentes")
    else:
        topics = {
            item.strip().strip("`")
            for item in topic_match.group(1).split(";")
            if item.strip()
        }
        for topic in sorted(topics - known_topics):
            findings.append(f"tópico desconhecido: {topic}")

    if "escovedo" in source.casefold():
        findings.append("referência Escovedo proibida")

    if kind == "aula":
        normalized_source = source.casefold()
        for term, label in THEORETICAL_DATASET_TERMS.items():
            if term in normalized_source:
                findings.append(
                    f"conjunto didático específico em slides teóricos: {label}"
                )

    findings.extend(_broken_links(path, source))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--aula", type=Path, action="append", default=[])
    parser.add_argument("--roteiro", type=Path, action="append", default=[])
    arguments = parser.parse_args()

    if not arguments.aula and not arguments.roteiro:
        parser.error("informe ao menos um recurso")

    graph = json.loads(arguments.graph.read_text(encoding="utf-8"))
    all_findings = []
    for kind, paths in (
        ("aula", arguments.aula),
        ("roteiro", arguments.roteiro),
    ):
        for path in paths:
            for finding in validate_resource(path, kind, graph):
                all_findings.append(f"{path}: {finding}")

    for finding in all_findings:
        print(finding)
    return 1 if all_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
