"""Testes do contrato editorial privado das aulas em notebook."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from scripts.aulas.estrutura import (
    approve_structure,
    content_sha256,
    dump_structure,
    load_structure,
    mark_published,
    semantic_sha256,
    validate_structure,
)


def manifest() -> dict:
    return {
        "versao_contrato": "2.0",
        "estado": "aprovado",
        "aula": {
            "id": "u1_a05",
            "semestre": "2026-2",
            "numero": 5,
            "duracao_minutos": 100,
            "titulo": "Tipos, qualidade e pré-processamento básico",
        },
    }


def structure_body() -> str:
    return (
        "# Aula 5 — Tipos, qualidade e pré-processamento básico\n\n"
        "## 1. Objetivos de aprendizagem\n\n"
        "Ao final da aula, o aluno será capaz de:\n\n"
        "- classificar variáveis.\n\n"
        "## 2. Agenda\n\n"
        "1. Conteúdo — 95 min\n"
        "2. Estudo e exercícios — 5 min\n\n"
        "## 3. Conteúdo\n\n"
        "### 3.1 Conceito\n\n"
        "**Abordagem didática:** partir de um exemplo.\n\n"
        "**Aplicação prevista:** classificar uma variável.\n\n"
        "**Evidência esperada:** justificativa escrita.\n\n"
        "**Tópico curricular:** `topico-teste`.\n\n"
        "**Referências:** `referencia-teste`.\n\n"
        "## 4. Estudo e exercícios\n\n"
        "## 5. Referências\n"
    )


def structure_metadata() -> dict:
    return {
        "versao_contrato": "1.0",
        "estado": "em_elaboracao",
        "aula_id": "u1_a05",
        "semestre": "2026-2",
        "modo_publicacao": "notebook_integral",
        "origem": {
            "manifesto": ".interno/prof/aulas/2026-2/u1_a05/selecao.yaml",
            "manifesto_sha256": semantic_sha256(manifest()),
        },
        "aprovacao": {
            "estrutura_em": None,
            "publicacao_em": None,
            "conteudo_sha256": None,
        },
        "notebooks": {
            "sala": {"caminho": "notebooks/u1_a05.ipynb", "sha256": None},
            "resolvido": {
                "caminho": "notebooks/resolvidos/u1_a05.ipynb",
                "sha256": None,
            },
        },
    }


class StructureSerializationTest(unittest.TestCase):
    def test_hash_semantico_independe_da_ordem_das_chaves(self) -> None:
        self.assertEqual(
            semantic_sha256({"b": 2, "a": 1}),
            semantic_sha256({"a": 1, "b": 2}),
        )

    def test_dump_e_load_preservam_metadados_e_corpo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "estrutura.md"
            metadata = structure_metadata()
            body = structure_body()
            path.write_text(dump_structure(metadata, body), encoding="utf-8")
            loaded_metadata, loaded_body = load_structure(path)

        self.assertEqual(loaded_metadata, metadata)
        self.assertEqual(loaded_body, body)
        self.assertEqual(len(content_sha256(body)), 64)

    def test_load_rejeita_arquivo_sem_front_matter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "estrutura.md"
            path.write_text("# Sem contrato\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "front matter"):
                load_structure(path)


class StructureValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = manifest()
        self.metadata = structure_metadata()
        self.body = structure_body()
        self.root = Path("/repositorio-simulado")

    def validate(self, metadata: dict | None = None, body: str | None = None) -> list[str]:
        return validate_structure(
            self.metadata if metadata is None else metadata,
            self.body if body is None else body,
            self.manifest,
            self.root,
        )

    def assert_finding(self, text: str, findings: list[str]) -> None:
        self.assertTrue(
            any(text in finding for finding in findings),
            f"esperava achado contendo {text!r}; obtidos: {findings}",
        )

    def test_aceita_estrutura_em_elaboracao_valida(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_rejeita_estado_desatualizada(self) -> None:
        self.metadata["estado"] = "desatualizada"
        self.assert_finding("schema", self.validate())

    def test_em_elaboracao_rejeita_campos_de_aprovacao(self) -> None:
        self.metadata["aprovacao"]["conteudo_sha256"] = "0" * 64
        self.assert_finding("em_elaboracao", self.validate())

    def test_rejeita_manifesto_nao_aprovado(self) -> None:
        self.manifest["estado"] = "em_selecao"
        self.assert_finding("manifesto deve estar aprovado", self.validate())

    def test_rejeita_hash_semantico_do_manifesto_divergente(self) -> None:
        self.metadata["origem"]["manifesto_sha256"] = "0" * 64
        self.assert_finding("manifesto diverge", self.validate())

    def test_rejeita_identidade_e_caminhos_nao_canonicos(self) -> None:
        self.metadata["aula_id"] = "u1_a06"
        self.metadata["notebooks"]["sala"]["caminho"] = "outro.ipynb"
        findings = self.validate()
        self.assert_finding("aula_id diverge", findings)
        self.assert_finding("caminho canônico do notebook de sala", findings)

    def test_rejeita_titulo_objetivos_e_agenda_invalidos(self) -> None:
        body = self.body.replace("# Aula 5", "# Aula 6")
        body = body.replace("- classificar variáveis.", "classificar variáveis.")
        body = body.replace("Conteúdo — 95 min", "Conteúdo — 90 min")
        findings = self.validate(body=body)
        self.assert_finding("título", findings)
        self.assert_finding("Objetivos", findings)
        self.assert_finding("Agenda totaliza 95 minutos", findings)

    def test_rejeita_secao_substantiva_sem_abordagem(self) -> None:
        body = self.body.replace("**Abordagem didática:** partir de um exemplo.\n\n", "")
        self.assert_finding("Abordagem didática", self.validate(body=body))

    def test_aprovada_rejeita_corpo_modificado(self) -> None:
        approved = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        self.assert_finding(
            "conteúdo aprovado diverge",
            self.validate(approved, self.body + "\nMudança\n"),
        )


class StructureTransitionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata = structure_metadata()
        self.body = structure_body()

    def test_aprovar_nao_muta_entrada(self) -> None:
        before = copy.deepcopy(self.metadata)
        approved = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        self.assertEqual(self.metadata, before)
        self.assertEqual(approved["estado"], "aprovada")
        self.assertEqual(approved["aprovacao"]["conteudo_sha256"], content_sha256(self.body))

    def test_aprovar_exige_em_elaboracao(self) -> None:
        self.metadata["estado"] = "aprovada"
        with self.assertRaisesRegex(ValueError, "em_elaboracao"):
            approve_structure(self.metadata, self.body, "2026-09-04T14:00:00-03:00")

    def test_publicar_nao_muta_entrada_e_registra_hashes(self) -> None:
        approved = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        before = copy.deepcopy(approved)
        published = mark_published(
            approved,
            self.body,
            {"sala": "0" * 64, "resolvido": "1" * 64},
            "2026-09-04T18:00:00-03:00",
        )
        self.assertEqual(approved, before)
        self.assertEqual(published["estado"], "publicada")
        self.assertEqual(published["notebooks"]["sala"]["sha256"], "0" * 64)
        self.assertEqual(published["notebooks"]["resolvido"]["sha256"], "1" * 64)

    def test_publicar_exige_aprovada_e_corpo_inalterado(self) -> None:
        with self.assertRaisesRegex(ValueError, "aprovada"):
            mark_published(
                self.metadata,
                self.body,
                {"sala": "0" * 64, "resolvido": "1" * 64},
                "2026-09-04T18:00:00-03:00",
            )
        approved = approve_structure(
            self.metadata,
            self.body,
            "2026-09-04T14:00:00-03:00",
        )
        with self.assertRaisesRegex(ValueError, "conteúdo"):
            mark_published(
                approved,
                self.body + "\nMudança\n",
                {"sala": "0" * 64, "resolvido": "1" * 64},
                "2026-09-04T18:00:00-03:00",
            )


if __name__ == "__main__":
    unittest.main()
