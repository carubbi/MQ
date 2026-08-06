import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "prof/refs/mapas/schema_grafo_referencias.json"
)


def valid_graph():
    return {
        "metadados": {
            "versao_esquema": "1.0",
            "data_geracao": "2026-08-06",
            "semestre_referencia": "2026.2",
            "cobertura": {
                "estado": "parcial",
                "criterio": "conteudo_curricular",
                "conteudos_concluidos": ["01.01", "01.02", "01.03", "01.04"],
                "conteudos_pendentes": [
                    "02.01",
                    "02.02",
                    "02.03",
                    "02.04",
                    "03.01",
                    "03.02",
                    "03.03",
                    "03.04",
                ],
                "fontes_inventariadas": 9,
            },
        },
        "vocabularios": {
            "tipos_no": [
                "fonte",
                "capitulo",
                "secao",
                "item_pedagogico",
                "topico",
                "conteudo_curricular",
            ],
            "subtipos_item_pedagogico": ["questao", "exercicio", "exemplo"],
            "tipos_relacao": ["contem", "aborda", "corresponde_a", "precede"],
            "pertinencias_t199": ["direta", "indireta", "fora_do_escopo"],
        },
        "nos": [
            {
                "id": "fonte-x",
                "tipo": "fonte",
                "tipo_fonte": "livro",
                "titulo": "Fonte X",
                "arquivo": "prof/refs/livros/fonte-x.pdf",
                "paginas_pdf": 4,
                "idioma": "pt-BR",
                "hash_sha256": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
            },
            {
                "id": "fonte-x-cap-01",
                "tipo": "capitulo",
                "numero_impresso": "1",
                "titulo": "Capítulo 1",
                "pagina_pdf_inicio": 1,
                "pagina_pdf_fim": 2,
            },
            {
                "id": "fonte-x-sec-01-01",
                "tipo": "secao",
                "numero_impresso": "1.1",
                "titulo": "Seção 1.1",
                "pagina_pdf_inicio": 1,
                "pagina_pdf_fim": 2,
                "pertinencia_t199": "direta",
            },
            {
                "id": "fonte-x-q-01",
                "tipo": "item_pedagogico",
                "subtipo": "questao",
                "numero_impresso": "1",
                "pagina_pdf": 2,
                "pertinencia_t199": "direta",
            },
            {"id": "topico-dados", "tipo": "topico", "nome": "Dados"},
            {
                "id": "conteudo-01-01",
                "tipo": "conteudo_curricular",
                "codigo": "01.01",
                "unidade": "I",
                "nome": "Fundamentos estatísticos",
            },
        ],
        "relacoes": [
            {"origem": "fonte-x", "tipo": "contem", "destino": "fonte-x-cap-01"},
            {
                "origem": "fonte-x-sec-01-01",
                "tipo": "aborda",
                "destino": "topico-dados",
            },
            {
                "origem": "fonte-x-sec-01-01",
                "tipo": "corresponde_a",
                "destino": "conteudo-01-01",
            },
            {
                "origem": "fonte-x-cap-01",
                "tipo": "precede",
                "destino": "fonte-x-sec-01-01",
            },
        ],
    }


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open(encoding="utf-8") as schema_file:
            cls.validator = Draft202012Validator(json.load(schema_file))

    def assert_valid(self, graph):
        self.assertEqual(list(self.validator.iter_errors(graph)), [])

    def assert_invalid(self, graph):
        self.assertNotEqual(list(self.validator.iter_errors(graph)), [])

    def test_accepts_a_minimal_graph_with_declared_partial_coverage(self):
        self.assert_valid(valid_graph())

    def test_rejects_difficulty_on_a_canonical_node(self):
        graph = valid_graph()
        graph["nos"][2]["dificuldade"] = "alta"

        self.assert_invalid(graph)

    def test_rejects_observacao_on_a_canonical_node(self):
        graph = valid_graph()
        graph["nos"][2]["observacao"] = "verificar"

        self.assert_invalid(graph)

    def test_rejects_page_zero(self):
        graph = valid_graph()
        graph["nos"][1]["pagina_pdf_inicio"] = 0

        self.assert_invalid(graph)

    def test_requires_coverage(self):
        graph = valid_graph()
        del graph["metadados"]["cobertura"]

        self.assert_invalid(graph)

    def test_rejects_invalid_completed_curriculum_content(self):
        graph = valid_graph()
        graph["metadados"]["cobertura"]["conteudos_concluidos"] = ["04.01"]

        self.assert_invalid(graph)

    def test_requires_unique_completed_and_pending_contents(self):
        graph = valid_graph()
        graph["metadados"]["cobertura"]["conteudos_pendentes"].append("02.01")

        self.assert_invalid(graph)

    def test_requires_complete_canonical_vocabulary_lists(self):
        for vocabulary_name in valid_graph()["vocabularios"]:
            with self.subTest(vocabulary_name=vocabulary_name):
                graph = valid_graph()
                graph["vocabularios"][vocabulary_name].pop()

                self.assert_invalid(graph)
