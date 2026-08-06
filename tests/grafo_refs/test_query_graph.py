import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.query_graph import query_by_content, query_by_topic


GRAPH = {
    "metadados": {
        "cobertura": {
            "estado": "parcial",
            "conteudos_concluidos": ["01.01", "01.03"],
            "conteudos_pendentes": ["02.01"],
        }
    },
    "nos": [
        {"id": "fonte-a", "tipo": "fonte", "titulo": "Fonte A"},
        {
            "id": "secao-a",
            "tipo": "secao",
            "numero_impresso": "1.2",
            "titulo": "Medidas de posição",
            "pagina_pdf_inicio": 12,
            "pagina_pdf_fim": 15,
        },
        {"id": "conteudo-01-01", "tipo": "conteudo_curricular", "codigo": "01.01"},
        {"id": "conteudo-01-02", "tipo": "conteudo_curricular", "codigo": "01.02"},
        {"id": "conteudo-01-03", "tipo": "conteudo_curricular", "codigo": "01.03"},
        {"id": "conteudo-02-01", "tipo": "conteudo_curricular", "codigo": "02.01"},
        {"id": "topico-media", "tipo": "topico", "nome": "Média"},
    ],
    "relacoes": [
        {"origem": "fonte-a", "tipo": "contem", "destino": "secao-a"},
        {"origem": "secao-a", "tipo": "corresponde_a", "destino": "conteudo-01-03"},
        {"origem": "secao-a", "tipo": "aborda", "destino": "topico-media"},
    ],
}


class QueryGraphTests(unittest.TestCase):
    def test_returns_pending_state_without_results_for_unmapped_content(self):
        """Catches treating an unmapped curriculum content as absent from the corpus."""
        result = query_by_content(GRAPH, "02.01")

        self.assertEqual(result["estado"], "pendente")
        self.assertEqual(result["resultados"], [])

    def test_returns_pending_state_for_known_content_absent_from_coverage_lists(self):
        """Catches classifying a known but uncovered curriculum code as unknown."""
        result = query_by_content(GRAPH, "01.02")

        self.assertEqual(result, {"estado": "pendente", "resultados": []})

    def test_returns_only_real_references_for_completed_content(self):
        """Catches fabricated results or loss of source and page location."""
        result = query_by_content(GRAPH, "01.03")

        self.assertEqual(result["estado"], "concluido")
        self.assertEqual(
            result["resultados"],
            [
                {
                    "id": "secao-a",
                    "tipo": "secao",
                    "numero_impresso": "1.2",
                    "titulo": "Medidas de posição",
                    "pagina_pdf_inicio": 12,
                    "pagina_pdf_fim": 15,
                    "fontes": [{"id": "fonte-a", "titulo": "Fonte A"}],
                }
            ],
        )

    def test_returns_real_references_for_topic_in_stable_order(self):
        """Catches topic queries that omit source context or derive unsupported matches."""
        self.assertEqual(
            query_by_topic(GRAPH, "topico-media"),
            [
                {
                    "id": "secao-a",
                    "tipo": "secao",
                    "numero_impresso": "1.2",
                    "titulo": "Medidas de posição",
                    "pagina_pdf_inicio": 12,
                    "pagina_pdf_fim": 15,
                    "fontes": [{"id": "fonte-a", "titulo": "Fonte A"}],
                }
            ],
        )

    def test_cli_returns_exit_2_for_pending_content(self):
        """Catches the CLI reporting a pending content as a successful empty query."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            graph_path = Path(temporary_directory) / "grafo.json"
            graph_path.write_text(json.dumps(GRAPH), encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, "scripts/grafo_refs/query_graph.py", str(graph_path), "--content", "02.01"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "conteúdo ainda não mapeado: 02.01\n")
        self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
