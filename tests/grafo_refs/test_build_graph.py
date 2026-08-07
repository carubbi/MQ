import json
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.build_graph import build_graph, write_graph
from scripts.grafo_refs.curate_grafo import build_curations, write_curations


COMPLETED = ["01.01", "01.02", "01.03", "01.04"]
PENDING = ["02.01", "02.02", "02.03", "02.04", "03.01", "03.02", "03.03", "03.04"]
TOPICS_PATH = (
    Path(__file__).resolve().parents[2]
    / "scripts/grafo_refs/data/topicos_t199.json"
)
CURATIONS_DIRECTORY = TOPICS_PATH.parent / "curadorias"
CURATED_SOURCES = (
    "apostila-mq",
    "banco-questoes-2026-2",
    "barbetta-2010",
    "estatistica-pratica-cd",
    "montgomery-2018",
    "morettin-bussab-2010",
    "navidi-2024",
    "pinheiro-2009",
)
CANONICAL_TOPIC_IDS = {
    "topico-amostra",
    "topico-amostragem",
    "topico-amostragem-aleatoria-simples",
    "topico-amostragem-estratificada",
    "topico-amostragem-por-conglomerados",
    "topico-amostragem-por-conveniencia",
    "topico-amostragem-sistematica",
    "topico-amplitude",
    "topico-assimetria",
    "topico-associacao",
    "topico-boxplot",
    "topico-coeficiente-de-determinacao",
    "topico-coeficiente-de-determinacao-ajustado",
    "topico-coeficiente-de-variacao",
    "topico-correlacao-linear",
    "topico-covariancia",
    "topico-desvio-padrao",
    "topico-diagnostico-do-modelo",
    "topico-distribuicao-amostral",
    "topico-distribuicao-binomial",
    "topico-distribuicao-exponencial",
    "topico-distribuicao-normal",
    "topico-distribuicao-poisson",
    "topico-distribuicao-uniforme",
    "topico-erro-padrao",
    "topico-erro-tipo-i",
    "topico-erro-tipo-ii",
    "topico-espaco-amostral",
    "topico-esperanca",
    "topico-estatistica-descritiva",
    "topico-estatistica-inferencial",
    "topico-estimacao-pontual",
    "topico-evento",
    "topico-experimento-aleatorio",
    "topico-frequencia",
    "topico-funcao-de-probabilidade",
    "topico-funcao-densidade",
    "topico-funcao-distribuicao-acumulada",
    "topico-grafico",
    "topico-grafico-qq",
    "topico-hipotese-alternativa",
    "topico-hipotese-nula",
    "topico-importacao-de-dados",
    "topico-independencia",
    "topico-inferencia-sobre-coeficientes",
    "topico-intervalo-de-confianca",
    "topico-intervalo-interquartil",
    "topico-investigacao-estatistica",
    "topico-margem-de-erro",
    "topico-media",
    "topico-mediana",
    "topico-minimos-quadrados",
    "topico-moda",
    "topico-nivel-de-significancia",
    "topico-padronizacao",
    "topico-poder-do-teste",
    "topico-populacao",
    "topico-pre-processamento",
    "topico-probabilidade-condicional",
    "topico-probabilidade-total",
    "topico-quantil",
    "topico-regra-da-adicao",
    "topico-regra-do-produto",
    "topico-regressao-linear-multipla",
    "topico-regressao-linear-simples",
    "topico-representatividade",
    "topico-residuo",
    "topico-tabela",
    "topico-tabela-de-contingencia",
    "topico-tamanho-amostral",
    "topico-teorema-central-do-limite",
    "topico-teorema-de-bayes",
    "topico-teste-para-media",
    "topico-teste-para-proporcao",
    "topico-tipos-de-variaveis",
    "topico-unidade-de-analise",
    "topico-valor-discrepante",
    "topico-valor-p",
    "topico-variancia",
    "topico-variavel-aleatoria-continua",
    "topico-variavel-aleatoria-discreta",
    "topico-variavel-indicadora",
}


def _published_curations() -> dict[str, list[dict]]:
    return {
        source: json.loads(
            (CURATIONS_DIRECTORY / f"{source}.json").read_text(
                encoding="utf-8"
            )
        )
        for source in CURATED_SOURCES
    }


class BuildGraphTests(unittest.TestCase):
    def test_integral_topic_vocabulary_has_the_exact_canonical_ids(self):
        """Catches any missing, extra, or colliding canonical topic ID."""
        topics = json.loads(TOPICS_PATH.read_text(encoding="utf-8"))
        ids = [topic["id"] for topic in topics]

        self.assertEqual(len(ids), 82)
        self.assertEqual(set(ids), CANONICAL_TOPIC_IDS)

    def test_general_curator_preserves_all_published_curations(self):
        """Catches any generated node that diverges from published curation."""
        self.assertEqual(build_curations(), _published_curations())

    def test_general_curator_writes_the_published_files_deterministically(self):
        """Catches missing, extra, or bytewise-different curation outputs."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory)
            write_curations(output_directory)

            self.assertEqual(
                {path.name for path in output_directory.glob("*.json")},
                {f"{source}.json" for source in CURATED_SOURCES},
            )
            for source in CURATED_SOURCES:
                with self.subTest(source=source):
                    self.assertEqual(
                        (output_directory / f"{source}.json").read_bytes(),
                        (CURATIONS_DIRECTORY / f"{source}.json").read_bytes(),
                    )

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
