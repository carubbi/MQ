"""Validação conjunta dos notebooks canônicos de sala e resolvido."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import nbformat
from nbformat import NotebookNode

from scripts.aulas.estrutura import validate_structure


def extract_header(path: Path) -> str:
    """Extrai o único bloco HTML do arquivo de cabeçalho canônico."""
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```html\n(.*?)\n```", text, re.DOTALL)
    if len(blocks) != 1:
        raise ValueError("o cabeçalho deve conter exatamente um bloco HTML")
    return blocks[0]


def load_notebook(path: Path) -> tuple[NotebookNode, str]:
    """Carrega um notebook e calcula o hash dos mesmos bytes lidos."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    notebook = nbformat.reads(raw.decode("utf-8"), as_version=4)
    return notebook, digest


def _markdown(notebook: NotebookNode) -> str:
    return "\n\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )


def _normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def extract_section(markdown: str, title: str) -> str:
    """Extrai o conteúdo de uma seção H2 numerada pelo título exato."""
    match = re.search(
        rf"(?ms)^##\s+\d+\.\s+{re.escape(title)}\s*$\n"
        rf"(?P<text>.*?)(?=^##\s+\d+\.|\Z)",
        markdown,
    )
    return "" if match is None else _normalize(match.group("text"))


def heading_hierarchy(markdown: str) -> list[str]:
    """Retorna a hierarquia H1–H3 na ordem em que aparece."""
    return [
        line.rstrip()
        for line in markdown.splitlines()
        if re.fullmatch(r"#{1,3}\s+\S.*", line.rstrip())
    ]


def _identity_findings(
    role: str,
    notebook: NotebookNode,
    header: str,
    expected_title: str,
) -> list[str]:
    findings: list[str] = []
    if not notebook.cells:
        return [f"notebook {role} não contém células"]
    first = notebook.cells[0]
    if first.cell_type != "markdown" or first.source != header:
        findings.append(f"cabeçalho do notebook {role} diverge do canônico")
    if len(notebook.cells) < 2:
        findings.append(f"notebook {role} não contém título")
    else:
        second = notebook.cells[1]
        lines = second.source.splitlines() if second.cell_type == "markdown" else []
        if not lines or lines[0] != expected_title:
            findings.append(f"título do notebook {role} diverge do manifesto")
    return findings


def _execution_findings(role: str, notebook: NotebookNode) -> list[str]:
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    findings: list[str] = []
    if role == "sala":
        if any(cell.execution_count is not None for cell in code_cells):
            findings.append("roteiro de sala deve permanecer sem contagens de execução")
        if any(cell.outputs for cell in code_cells):
            findings.append("roteiro de sala deve permanecer sem outputs")
        return findings

    counts = [cell.execution_count for cell in code_cells]
    expected = list(range(1, len(code_cells) + 1))
    if counts != expected:
        findings.append(
            f"contagens de execução divergentes: {counts}; esperadas {expected}"
        )
    for cell in code_cells:
        if any(output.output_type == "error" for output in cell.outputs):
            findings.append(f"célula {cell.id} contém output de erro")
    return findings


def _editorial_findings(
    role: str,
    notebook_markdown: str,
    structure_body: str,
) -> list[str]:
    findings: list[str] = []
    for title, label in (
        ("Objetivos de aprendizagem", "objetivos"),
        ("Agenda", "agenda"),
    ):
        expected = extract_section(structure_body, title)
        observed = extract_section(notebook_markdown, title)
        if observed != expected:
            findings.append(f"{label} do notebook {role} divergem da estrutura")
    if heading_hierarchy(notebook_markdown) != heading_hierarchy(structure_body):
        findings.append(f"hierarquia do notebook {role} diverge da estrutura")
    return findings


def validate_notebook_pair(
    *,
    manifest: dict,
    structure_metadata: dict,
    structure_body: str,
    header: str,
    room_notebook: NotebookNode,
    room_sha256: str,
    solved_notebook: NotebookNode,
    solved_sha256: str,
    repository_root: Path,
) -> list[str]:
    """Valida conjuntamente identidade, conteúdo e execução dos dois papéis."""
    findings = validate_structure(
        structure_metadata,
        structure_body,
        manifest,
        repository_root,
    )
    state = structure_metadata.get("estado")
    if state not in {"aprovada", "publicada"}:
        findings.append("estrutura deve estar aprovada ou publicada")

    lesson = manifest.get("aula")
    if not isinstance(lesson, dict):
        return findings
    expected_title = f"# Aula {lesson.get('numero')} — {lesson.get('titulo')}"
    room_markdown = _markdown(room_notebook)
    solved_markdown = _markdown(solved_notebook)

    findings.extend(
        _identity_findings("de sala", room_notebook, header, expected_title)
    )
    findings.extend(
        _identity_findings("resolvido", solved_notebook, header, expected_title)
    )
    findings.extend(_editorial_findings("de sala", room_markdown, structure_body))
    findings.extend(
        _editorial_findings("resolvido", solved_markdown, structure_body)
    )
    if heading_hierarchy(room_markdown) != heading_hierarchy(solved_markdown):
        findings.append("hierarquias dos notebooks divergem entre os papéis")

    findings.extend(_execution_findings("sala", room_notebook))
    findings.extend(_execution_findings("resolvido", solved_notebook))

    markdown_lesson = repository_root / "aulas" / f"{lesson.get('id')}.md"
    if markdown_lesson.exists():
        findings.append(
            f"artefato incompatível com notebook_integral: {markdown_lesson}"
        )

    if state == "publicada":
        notebooks = structure_metadata.get("notebooks", {})
        expected_hashes = {
            "sala": notebooks.get("sala", {}).get("sha256"),
            "resolvido": notebooks.get("resolvido", {}).get("sha256"),
        }
        observed_hashes = {"sala": room_sha256, "resolvido": solved_sha256}
        for role in ("sala", "resolvido"):
            if expected_hashes[role] != observed_hashes[role]:
                findings.append(f"hash do notebook de {role} diverge da publicação")
    return findings
