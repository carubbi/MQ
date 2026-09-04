"""Contrato editorial privado para aulas publicadas como notebook integral."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = Path(__file__).with_name("schema_estrutura.json")
FRONT_MATTER = re.compile(
    r"\A---\n(?P<yaml>.*?)\n---\n(?P<body>.*)\Z",
    re.DOTALL,
)
AGENDA_ITEM = re.compile(r"^(?P<number>\d+)\.\s+.+\s+—\s+(?P<minutes>\d+)\s+min$")
SECTION = re.compile(r"(?m)^##\s+\d+\.\s+(?P<title>.+?)\s*$")


def semantic_sha256(value: object) -> str:
    """Calcula SHA-256 de uma representação JSON canônica."""
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def content_sha256(body: str) -> str:
    """Calcula SHA-256 do corpo Markdown exato."""
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_structure(path: Path) -> tuple[dict, str]:
    """Carrega front matter e corpo de um contrato editorial."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.fullmatch(text)
    if match is None:
        raise ValueError("estrutura deve conter front matter YAML delimitado por ---")
    metadata = yaml.safe_load(match.group("yaml"))
    if not isinstance(metadata, dict):
        raise ValueError("front matter de estrutura deve ser um objeto YAML")
    return metadata, match.group("body")


def dump_structure(metadata: dict, body: str) -> str:
    """Serializa o contrato editorial sem alterar o corpo Markdown."""
    serialized = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )
    return f"---\n{serialized}---\n{body}"


def _schema_findings(metadata: dict) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema: {error.message}"
        for error in sorted(
            validator.iter_errors(metadata),
            key=lambda error: (list(error.absolute_path), error.message),
        )
    ]


def _state_findings(metadata: dict, body: str) -> list[str]:
    state = metadata.get("estado")
    approval = metadata.get("aprovacao")
    notebooks = metadata.get("notebooks")
    if not isinstance(approval, dict) or not isinstance(notebooks, dict):
        return []
    room = notebooks.get("sala")
    solved = notebooks.get("resolvido")
    if not isinstance(room, dict) or not isinstance(solved, dict):
        return []

    structure_at = approval.get("estrutura_em")
    publication_at = approval.get("publicacao_em")
    approved_hash = approval.get("conteudo_sha256")
    room_hash = room.get("sha256")
    solved_hash = solved.get("sha256")
    findings: list[str] = []

    if state == "em_elaboracao":
        values = (structure_at, publication_at, approved_hash, room_hash, solved_hash)
        if any(value is not None for value in values):
            findings.append("estado em_elaboracao exige campos de aprovação e hashes nulos")
    elif state == "aprovada":
        if structure_at is None or approved_hash is None:
            findings.append("estado aprovada exige data e hash do conteúdo")
        if publication_at is not None or room_hash is not None or solved_hash is not None:
            findings.append("estado aprovada exige publicação e hashes dos notebooks nulos")
    elif state == "publicada":
        if any(
            value is None
            for value in (
                structure_at,
                publication_at,
                approved_hash,
                room_hash,
                solved_hash,
            )
        ):
            findings.append("estado publicada exige datas e todos os hashes")

    if state in {"aprovada", "publicada"} and approved_hash is not None:
        if approved_hash != content_sha256(body):
            findings.append("conteúdo aprovado diverge do hash registrado")
    return findings


def _body_findings(body: str, manifest: dict) -> list[str]:
    lesson = manifest.get("aula", {})
    if not isinstance(lesson, dict):
        return []
    findings: list[str] = []
    expected_title = f"# Aula {lesson.get('numero')} — {lesson.get('titulo')}"
    if not body.startswith(f"{expected_title}\n"):
        findings.append("título da estrutura diverge do manifesto")

    objectives = re.search(
        r"(?ms)^##\s+\d+\.\s+Objetivos de aprendizagem\s*$\n"
        r"(?P<text>.*?)(?=^##\s+\d+\.|\Z)",
        body,
    )
    if (
        objectives is None
        or "Ao final da aula, o aluno será capaz de:" not in objectives.group("text")
        or re.search(r"(?m)^-\s+\S", objectives.group("text")) is None
    ):
        findings.append("Objetivos de aprendizagem ausentes ou sem enunciados")

    agenda = re.search(
        r"(?ms)^##\s+\d+\.\s+Agenda\s*$\n"
        r"(?P<text>.*?)(?=^##\s+\d+\.|\Z)",
        body,
    )
    if agenda is None:
        findings.append("Agenda ausente na estrutura")
    else:
        lines = [
            line.strip()
            for line in agenda.group("text").splitlines()
            if re.match(r"^\d+\.\s+", line.strip())
        ]
        matches = [AGENDA_ITEM.fullmatch(line) for line in lines]
        if not lines or any(match is None for match in matches):
            findings.append("formato dos itens da Agenda deve ser N. Seção — X min")
        else:
            numbers = [int(match.group("number")) for match in matches if match]
            if numbers != list(range(1, len(numbers) + 1)):
                findings.append("numeração dos itens da Agenda deve ser sequencial")
            total = sum(int(match.group("minutes")) for match in matches if match)
            duration = lesson.get("duracao_minutos")
            if isinstance(duration, int) and total != duration:
                findings.append(
                    f"Agenda totaliza {total} minutos; esperados {duration} minutos"
                )

    matches = list(SECTION.finditer(body))
    for index, match in enumerate(matches):
        title = match.group("title").strip()
        if title in {
            "Objetivos de aprendizagem",
            "Agenda",
            "Estudo e exercícios",
            "Referências",
        }:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        section_text = body[match.end() : end]
        if "**Abordagem didática:**" not in section_text:
            findings.append(f"seção {title} não informa Abordagem didática")
    return findings


def validate_structure(
    metadata: dict,
    body: str,
    manifest: dict,
    repository_root: Path,
) -> list[str]:
    """Valida contrato, identidade, integridade e conteúdo editorial mínimo."""
    del repository_root
    findings = _schema_findings(metadata)
    if not isinstance(manifest, dict):
        return [*findings, "manifesto deve ser um objeto"]
    lesson = manifest.get("aula")
    if not isinstance(lesson, dict):
        return [*findings, "aula do manifesto deve ser um objeto"]

    if manifest.get("estado") != "aprovado":
        findings.append("manifesto deve estar aprovado")

    lesson_id = lesson.get("id")
    semester = lesson.get("semestre")
    if metadata.get("aula_id") != lesson_id:
        findings.append("aula_id diverge do manifesto")
    if metadata.get("semestre") != semester:
        findings.append("semestre diverge do manifesto")

    origin = metadata.get("origem")
    if isinstance(origin, dict):
        expected_manifest = f".interno/prof/aulas/{semester}/{lesson_id}/selecao.yaml"
        if origin.get("manifesto") != expected_manifest:
            findings.append("caminho canônico do manifesto divergente")
        if origin.get("manifesto_sha256") != semantic_sha256(manifest):
            findings.append("manifesto diverge do hash semântico registrado")

    notebooks = metadata.get("notebooks")
    if isinstance(notebooks, dict):
        expected_paths = {
            "sala": f"notebooks/{lesson_id}.ipynb",
            "resolvido": f"notebooks/resolvidos/{lesson_id}.ipynb",
        }
        for role, expected in expected_paths.items():
            entry = notebooks.get(role)
            if isinstance(entry, dict) and entry.get("caminho") != expected:
                findings.append(f"caminho canônico do notebook de {role} divergente")

    findings.extend(_state_findings(metadata, body))
    findings.extend(_body_findings(body, manifest))
    return findings


def approve_structure(metadata: dict, body: str, approved_at: str) -> dict:
    """Retorna metadados aprovados sem mutar a entrada."""
    if metadata.get("estado") != "em_elaboracao":
        raise ValueError("aprovação exige estado em_elaboracao")
    approved = copy.deepcopy(metadata)
    approved["estado"] = "aprovada"
    approved["aprovacao"]["estrutura_em"] = approved_at
    approved["aprovacao"]["conteudo_sha256"] = content_sha256(body)
    return approved


def mark_published(
    metadata: dict,
    body: str,
    notebook_hashes: dict[str, str],
    published_at: str,
) -> dict:
    """Retorna metadados publicados após conferir o corpo aprovado."""
    if metadata.get("estado") != "aprovada":
        raise ValueError("publicação exige estrutura aprovada")
    if metadata.get("aprovacao", {}).get("conteudo_sha256") != content_sha256(body):
        raise ValueError("conteúdo da estrutura mudou após a aprovação")
    published = copy.deepcopy(metadata)
    published["estado"] = "publicada"
    published["aprovacao"]["publicacao_em"] = published_at
    for role in ("sala", "resolvido"):
        published["notebooks"][role]["sha256"] = notebook_hashes[role]
    return published
