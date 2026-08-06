import json
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.build_graph import build_graph, write_graph


COMPLETED = ["01.01", "01.02", "01.03", "01.04"]
PENDING = ["02.01", "02.02", "02.03", "02.04", "03.01", "03.02", "03.03", "03.04"]


class BuildGraphTests(unittest.TestCase):
    def test_builds_the_declared_partial_coverage_deterministically(self):
        """Catches a build that changes coverage, inventory, or ordering."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            curated_dir = Path(temporary_directory)
            (curated_dir / "barbetta-2010.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "barbetta-2010-sec-01-01",
                            "tipo": "secao",
                            "numero_impresso": "1.1",
                            "titulo": "Dados estatísticos",
                            "pagina_pdf_inicio": 2,
                            "pagina_pdf_fim": 3,
                            "pertinencia_t199": "direta",
                            "topicos": ["topico-populacao"],
                            "conteudos": ["conteudo-01-01"],
                        }
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            build_a = build_graph("2026-08-06", curated_dir)
            build_b = build_graph("2026-08-06", curated_dir)

        coverage = build_a["metadados"]["cobertura"]
        source_nodes = [node for node in build_a["nos"] if node["tipo"] == "fonte"]
        self.assertEqual(coverage["estado"], "parcial")
        self.assertEqual(coverage["conteudos_concluidos"], COMPLETED)
        self.assertEqual(coverage["conteudos_pendentes"], PENDING)
        self.assertEqual(len(source_nodes), 9)
        self.assertEqual(build_a, build_b)
        self.assertIn(
            {"origem": "barbetta-2010-sec-01-01", "tipo": "corresponde_a", "destino": "conteudo-01-01"},
            build_a["relacoes"],
        )
        self.assertEqual(build_a["nos"], sorted(build_a["nos"], key=lambda node: (node["tipo"], node["id"])))
        self.assertEqual(
            build_a["relacoes"],
            sorted(build_a["relacoes"], key=lambda edge: (edge["origem"], edge["tipo"], edge["destino"])),
        )

    def test_writes_utf8_json_with_a_final_newline(self):
        """Catches graph output that is not reproducible UTF-8 JSON."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "grafo.json"
            write_graph(
                {"nome": "Média"},
                output_path,
            )

            self.assertEqual(
                output_path.read_bytes(),
                b'{\n  "nome": "M\xc3\xa9dia"\n}\n',
            )


if __name__ == "__main__":
    unittest.main()
