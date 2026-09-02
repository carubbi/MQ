import copy
import unittest

from scripts.aulas.dossie import render_dossier
from tests.aulas.fixtures import GRAPH, VALID_MANIFEST, approved_manifest


class DossierRenderingTests(unittest.TestCase):
    def test_renders_time_plan_as_list(self):
        rendered = render_dossier(VALID_MANIFEST, GRAPH)

        self.assertIn("## Planejamento temporal", rendered)
        self.assertIn("- **Abertura:** 5 minutos", rendered)
        self.assertIn("- **Fechamento:** 10 minutos", rendered)
        self.assertIn("- **Disponível para desenvolvimento:** 85 minutos", rendered)
        self.assertNotIn("Ciclos conceituais", rendered)
        self.assertNotIn("Aplicação no notebook", rendered)
        self.assertNotIn("ciclo-01", rendered)

    def test_renders_scope_topics_references_and_evidence(self):
        rendered = render_dossier(VALID_MANIFEST, GRAPH)

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

        self.assertEqual(
            render_dossier(manifest, GRAPH),
            render_dossier(manifest, GRAPH),
        )
        self.assertEqual(before, manifest)

    def test_dossier_contains_no_editable_selection_controls(self):
        rendered = render_dossier(VALID_MANIFEST, GRAPH)

        self.assertNotIn("[ ]", rendered)
        self.assertNotIn("[x]", rendered.casefold())

    def test_renders_references_as_readable_lists_instead_of_tables(self):
        rendered = render_dossier(VALID_MANIFEST, GRAPH)

        self.assertIn("1. **`secao-populacao`**", rendered)
        self.assertIn("   - **Fonte:** `fonte-a`", rendered)
        self.assertIn("   - **Cobertura:** Definição de população e amostra.", rendered)
        self.assertNotIn("| Referência |", rendered)

    def test_renders_student_resources_as_ordered_readable_lists(self):
        rendered = render_dossier(approved_manifest(), GRAPH)

        self.assertIn("## Recursos discentes", rendered)
        self.assertIn("### Materiais didáticos", rendered)
        self.assertIn("1. **`capitulo-fundamentos`**", rendered)
        self.assertIn("- **Fonte:** `fonte-a`", rendered)
        self.assertIn("- **Páginas PDF:** 10–13", rendered)
        self.assertIn("### Exercícios indicados", rendered)
        self.assertIn("1. **`questao-populacao`**", rendered)
        self.assertNotIn("| Recurso |", rendered)

    def test_omits_empty_student_resource_subsection(self):
        manifest = approved_manifest()
        manifest["recursos_discentes"]["exercicios_indicados"] = []

        rendered = render_dossier(manifest, GRAPH)

        self.assertIn("### Materiais didáticos", rendered)
        self.assertNotIn("### Exercícios indicados", rendered)


if __name__ == "__main__":
    unittest.main()
