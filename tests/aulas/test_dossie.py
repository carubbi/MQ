import copy
import unittest

from scripts.aulas.dossie import render_dossier
from tests.aulas.fixtures import VALID_MANIFEST, approved_manifest


class DossierRenderingTests(unittest.TestCase):
    def test_renders_time_plan_as_list(self):
        rendered = render_dossier(VALID_MANIFEST)

        self.assertIn("## Planejamento temporal", rendered)
        self.assertIn("- **Abertura:** 5 minutos", rendered)
        self.assertIn("- **Fechamento:** 10 minutos", rendered)
        self.assertIn("- **Disponível para ciclos:** 85 minutos", rendered)

    def test_renders_empty_cycle_selection_explicitly(self):
        rendered = render_dossier(VALID_MANIFEST)

        self.assertIn("## Ciclos conceituais", rendered)
        self.assertIn("Ciclos ainda não definidos.", rendered)

    def test_renders_approved_cycles_as_nested_lists(self):
        rendered = render_dossier(approved_manifest())

        self.assertIn("### ciclo-01 — População e amostra", rendered)
        self.assertIn("- **Tópicos:** `topico-populacao`", rendered)
        self.assertIn("- **Complexidade:** moderada", rendered)
        self.assertIn("- **Duração mínima:** 20 minutos", rendered)
        self.assertIn("- **Aplicação no notebook:**", rendered)
        self.assertIn(
            "  - **Pergunta:** Qual população sustenta a conclusão pretendida?",
            rendered,
        )
        self.assertNotIn("| Ciclo |", rendered)

    def test_renders_scope_topics_references_and_evidence(self):
        rendered = render_dossier(VALID_MANIFEST)

        self.assertTrue(rendered.startswith("# Dossiê de curadoria — u1_a02\n"))
        self.assertIn("## Escopo do encontro", rendered)
        self.assertIn("## Tópicos candidatos", rendered)
        self.assertIn("### População — pendente", rendered)
        self.assertIn("`secao-populacao`", rendered)
        self.assertIn("Definição de população e amostra.", rendered)
        self.assertIn("N para população e n para amostra.", rendered)

    def test_rendering_is_deterministic_and_does_not_mutate_manifest(self):
        manifest = copy.deepcopy(VALID_MANIFEST)
        before = copy.deepcopy(manifest)

        self.assertEqual(render_dossier(manifest), render_dossier(manifest))
        self.assertEqual(before, manifest)

    def test_dossier_contains_no_editable_selection_controls(self):
        rendered = render_dossier(VALID_MANIFEST)

        self.assertNotIn("[ ]", rendered)
        self.assertNotIn("[x]", rendered.casefold())

    def test_renders_references_as_readable_lists_instead_of_tables(self):
        rendered = render_dossier(VALID_MANIFEST)

        self.assertIn("1. **`secao-populacao`**", rendered)
        self.assertIn("   - **Fonte:** `fonte-a`", rendered)
        self.assertIn("   - **Cobertura:** Definição de população e amostra.", rendered)
        self.assertNotIn("| Referência |", rendered)


if __name__ == "__main__":
    unittest.main()
