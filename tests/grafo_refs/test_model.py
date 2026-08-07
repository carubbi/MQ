import unittest

from scripts.grafo_refs.model import flatten_curated_source, slug_id


class ModelTests(unittest.TestCase):
    def test_slug_id_is_ascii_and_stable(self):
        self.assertEqual(slug_id("Análise bivariada"), "analise-bivariada")

    def test_flatten_builds_structural_and_curricular_edges(self):
        curated = [
            {
                "id": "livro-x-cap-01",
                "tipo": "capitulo",
                "numero_impresso": "1",
                "titulo": "Dados",
                "pagina_pdf_inicio": 1,
                "pagina_pdf_fim": 4,
                "pai": "livro-x",
            },
            {
                "id": "livro-x-sec-01-01",
                "tipo": "secao",
                "numero_impresso": "1.1",
                "titulo": "População e amostra",
                "pagina_pdf_inicio": 2,
                "pagina_pdf_fim": 4,
                "pai": "livro-x-cap-01",
                "pertinencia_t199": "direta",
                "topicos": ["topico-populacao", "topico-amostra"],
                "conteudos": ["conteudo-01-01"],
            },
        ]
        nodes, edges = flatten_curated_source("livro-x", curated)

        self.assertFalse(any("pai" in node for node in nodes))
        self.assertFalse(any("topicos" in node for node in nodes))
        self.assertFalse(any("conteudos" in node for node in nodes))
        self.assertIn(
            {
                "origem": "livro-x-sec-01-01",
                "tipo": "corresponde_a",
                "destino": "conteudo-01-01",
            },
            edges,
        )
        self.assertIn(
            {
                "origem": "livro-x-cap-01",
                "tipo": "contem",
                "destino": "livro-x-sec-01-01",
            },
            edges,
        )
        self.assertIn(
            {
                "origem": "livro-x-sec-01-01",
                "tipo": "aborda",
                "destino": "topico-populacao",
            },
            edges,
        )

    def test_flatten_discards_prohibited_and_free_text_fields(self):
        curated = [
            {
                "id": "livro-x-sec-01-01",
                "tipo": "secao",
                "numero_impresso": "1.1",
                "titulo": "População e amostra",
                "pagina_pdf_inicio": 2,
                "pagina_pdf_fim": 4,
                "pai": "livro-x",
                "pertinencia_t199": "direta",
                "dificuldade": "alta",
                "observacao": "revisar",
                "enunciado": "Texto completo que não pertence ao grafo.",
                "solucao": "Solução que não pertence ao grafo.",
                "imagem": "pagina-2.png",
                "substituto_livre": "não permitido",
            }
        ]

        nodes, _ = flatten_curated_source("livro-x", curated)

        self.assertEqual(
            nodes,
            [
                {
                    "id": "livro-x-sec-01-01",
                    "tipo": "secao",
                    "numero_impresso": "1.1",
                    "titulo": "População e amostra",
                    "pagina_pdf_inicio": 2,
                    "pagina_pdf_fim": 4,
                    "pertinencia_t199": "direta",
                }
            ],
        )

    def test_flatten_preserves_concrete_item_type_without_legacy_subtype(self):
        """Catches reintroducing the generic pedagogical-item representation."""
        curated = [
            {
                "id": "livro-x-q-01",
                "tipo": "questao",
                "subtipo": "questao",
                "numero_impresso": "1",
                "pagina_pdf": 3,
                "pertinencia_t199": "direta",
            }
        ]

        nodes, _ = flatten_curated_source("livro-x", curated)

        self.assertEqual(
            nodes,
            [
                {
                    "id": "livro-x-q-01",
                    "tipo": "questao",
                    "numero_impresso": "1",
                    "pagina_pdf": 3,
                    "pertinencia_t199": "direta",
                }
            ],
        )

    def test_flatten_precedes_consecutive_siblings(self):
        curated = [
            {"id": "livro-x-cap-01", "tipo": "capitulo", "pai": "livro-x"},
            {"id": "livro-x-cap-02", "tipo": "capitulo", "pai": "livro-x"},
        ]

        _, edges = flatten_curated_source("livro-x", curated)

        self.assertIn(
            {
                "origem": "livro-x-cap-01",
                "tipo": "precede",
                "destino": "livro-x-cap-02",
            },
            edges,
        )
