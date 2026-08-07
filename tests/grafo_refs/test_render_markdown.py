import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.build_graph import DEFAULT_CURATED_DIRECTORY, build_graph
from scripts.grafo_refs.render_markdown import render_markdown


GRAPH = {
    "metadados": {
        "cobertura": {
            "estado": "parcial",
            "criterio": "conteudo_curricular",
            "conteudos_concluidos": ["01.01", "01.03"],
            "conteudos_pendentes": ["02.01", "99.99"],
            "fontes_inventariadas": 1,
        }
    },
    "nos": [
        {"id": "fonte-a", "tipo": "fonte", "titulo": "Fonte A", "tipo_fonte": "livro"},
        {
            "id": "secao-a",
            "tipo": "secao",
            "numero_impresso": "1.2",
            "titulo": "Medidas de posição",
            "pagina_pdf_inicio": 12,
            "pagina_pdf_fim": 15,
        },
        {
            "id": "item-fora",
            "tipo": "questao",
            "numero_impresso": "7",
            "pagina_pdf": 18,
            "pertinencia_t199": "fora_do_escopo",
        },
        {
            "id": "conteudo-01-01",
            "tipo": "conteudo_curricular",
            "codigo": "01.01",
            "unidade": "I",
            "nome": "Fundamentos estatísticos",
        },
        {
            "id": "conteudo-01-02",
            "tipo": "conteudo_curricular",
            "codigo": "01.02",
            "unidade": "I",
            "nome": "Conteúdo curricular omitido da cobertura",
        },
        {
            "id": "conteudo-01-03",
            "tipo": "conteudo_curricular",
            "codigo": "01.03",
            "unidade": "I",
            "nome": "Análise univariada",
        },
        {
            "id": "conteudo-02-01",
            "tipo": "conteudo_curricular",
            "codigo": "02.01",
            "unidade": "I",
            "nome": "Conteúdo ainda não mapeado",
        },
        {"id": "topico-media", "tipo": "topico", "nome": "Média"},
    ],
    "relacoes": [
        {"origem": "fonte-a", "tipo": "contem", "destino": "secao-a"},
        {"origem": "fonte-a", "tipo": "contem", "destino": "item-fora"},
        {"origem": "secao-a", "tipo": "corresponde_a", "destino": "conteudo-01-03"},
        {"origem": "secao-a", "tipo": "aborda", "destino": "topico-media"},
    ],
}


class RenderMarkdownTests(unittest.TestCase):
    def test_complete_graph_has_no_partial_notice_and_no_pending_contents(self):
        """Catches a completed graph being rendered with partial-coverage copy."""
        rendered = render_markdown(
            build_graph("2026-08-07", DEFAULT_CURATED_DIRECTORY)
        )

        self.assertTrue(rendered.startswith("# Grafo de referências da T199\n\n"))
        self.assertNotIn("Cobertura parcial", rendered)
        self.assertIn("## Conteúdos pendentes\n\n- nenhum conteúdo pendente", rendered)

    def test_starts_with_partial_coverage_notice_and_is_deterministic(self):
        """Catches an output that hides partial coverage or depends on iteration order."""
        rendered = render_markdown(GRAPH)

        self.assertTrue(
            rendered.startswith(
                "# Grafo de referências da T199\n\n"
                "> **Cobertura parcial:** esta versão mapeia somente os conteúdos `01.01` a\n"
                "> `01.04`. Ausência de resultados para outros conteúdos não indica ausência\n"
                "> de referências no corpus.\n"
            )
        )
        self.assertEqual(rendered, render_markdown(GRAPH))

    def test_includes_required_indexes_and_non_exhaustive_out_of_scope_notice(self):
        """Catches a human view that omits discoverability indexes or overclaims coverage."""
        rendered = render_markdown(GRAPH)

        for heading in (
            "## Cobertura do corpus",
            "## Conteúdos concluídos",
            "## Conteúdos pendentes",
            "## Índice por fonte",
            "## Índice por conteúdo da Unidade I",
            "## Índice por tópico",
            "## Itens examinados fora do escopo",
        ):
            self.assertIn(heading, rendered)
        self.assertIn("não é exaustiva", rendered)
        self.assertIn("$12$–$15$", rendered)
        self.assertNotIn("\\(", rendered)

    def test_distinguishes_pending_coverage_from_completed_content_without_references(self):
        """Catches rendering a pending content as a completed empty result."""
        rendered = render_markdown(GRAPH)

        self.assertIn("- `02.01` — ainda não mapeado", rendered)
        self.assertIn("### `01.01` — Fundamentos estatísticos\n- nenhuma referência curada", rendered)

    def test_content_index_includes_only_completed_coverage(self):
        """Catches pending curriculum content leaking into the curated content index."""
        rendered = render_markdown(GRAPH)

        self.assertIn("### `01.01` — Fundamentos estatísticos", rendered)
        self.assertIn("### `01.03` — Análise univariada", rendered)
        self.assertNotIn("### `02.01`", rendered)

    def test_lists_known_content_omitted_from_coverage_as_pending_outside_curated_index(self):
        """Catches known uncovered content disappearing from the pending section."""
        rendered = render_markdown(GRAPH)

        self.assertIn("- `01.02` — ainda não mapeado", rendered)
        self.assertLess(rendered.index("- `01.02` — ainda não mapeado"), rendered.index("- `02.01` — ainda não mapeado"))
        self.assertNotIn("### `01.02`", rendered)
        self.assertNotIn("- `99.99` — ainda não mapeado", rendered)

    def test_source_index_follows_pdf_page_order_instead_of_lexicographic_ids(self):
        graph = json.loads(json.dumps(GRAPH))
        graph["nos"].extend(
            [
                {
                    "id": "fonte-a-cap-15",
                    "tipo": "capitulo",
                    "numero_impresso": "15",
                    "titulo": "Capítulo posterior",
                    "pagina_pdf_inicio": 150,
                    "pagina_pdf_fim": 160,
                },
                {
                    "id": "fonte-a-cap-2",
                    "tipo": "capitulo",
                    "numero_impresso": "2",
                    "titulo": "Capítulo anterior",
                    "pagina_pdf_inicio": 20,
                    "pagina_pdf_fim": 30,
                },
            ]
        )
        graph["relacoes"].extend(
            [
                {"origem": "fonte-a", "tipo": "contem", "destino": "fonte-a-cap-15"},
                {"origem": "fonte-a", "tipo": "contem", "destino": "fonte-a-cap-2"},
            ]
        )

        rendered = render_markdown(graph)

        self.assertLess(
            rendered.index("capitulo 2 — Capítulo anterior"),
            rendered.index("capitulo 15 — Capítulo posterior"),
        )

    def test_source_index_uses_natural_numbering_on_the_same_page(self):
        graph = json.loads(json.dumps(GRAPH))
        graph["nos"].extend(
            [
                {
                    "id": "fonte-a-item-100",
                    "tipo": "questao",
                    "numero_impresso": "100",
                    "pagina_pdf": 20,
                    "pertinencia_t199": "direta",
                },
                {
                    "id": "fonte-a-item-70",
                    "tipo": "questao",
                    "numero_impresso": "70",
                    "pagina_pdf": 20,
                    "pertinencia_t199": "direta",
                },
            ]
        )
        graph["relacoes"].extend(
            [
                {"origem": "fonte-a", "tipo": "contem", "destino": "fonte-a-item-100"},
                {"origem": "fonte-a", "tipo": "contem", "destino": "fonte-a-item-70"},
            ]
        )

        rendered = render_markdown(graph)
        source_index = rendered.split("## Índice por fonte", 1)[1].split(
            "## Índice por conteúdo da Unidade I", 1
        )[0]

        self.assertLess(
            source_index.index("questao 70"),
            source_index.index("questao 100"),
        )

    def test_cli_renders_markdown_when_executed_as_a_script(self):
        """Catches a direct CLI execution that cannot import the local package."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            graph_path = directory / "grafo.json"
            output_path = directory / "grafo.md"
            graph_path.write_text(json.dumps(GRAPH), encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, "scripts/grafo_refs/render_markdown.py", str(graph_path), str(output_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            rendered = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(rendered.startswith("# Grafo de referências da T199\n"))


if __name__ == "__main__":
    unittest.main()
