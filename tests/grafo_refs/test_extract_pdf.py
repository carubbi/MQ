import unittest
from pathlib import Path
import tempfile

import fitz

from scripts.grafo_refs.extract_pdf import extract_pdf, search_pages


class ExtractPdfTests(unittest.TestCase):
    def test_extract_pdf_preserves_one_based_pages_and_bookmarks(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "sample.pdf"
            document = fitz.open()
            first_page = document.new_page()
            first_page.insert_text((72, 72), "Introdução")
            second_page = document.new_page()
            second_page.insert_text((72, 72), "A MEDIANA é resistente.")
            document.set_toc([[1, "Capítulo", 1]])
            document.save(pdf_path)
            document.close()

            extracted = extract_pdf(pdf_path)

        self.assertEqual(extracted["paginas"][0]["pagina_pdf"], 1)
        self.assertEqual(extracted["marcadores"][0]["pagina_pdf"], 1)
        self.assertEqual(search_pages(extracted, ["mediana"]), [2])

    def test_search_pages_ignores_case_and_diacritics(self):
        extracted = {
            "paginas": [
                {"pagina_pdf": 1, "texto": "Média aritmética"},
                {"pagina_pdf": 2, "texto": "Mediana"},
            ],
            "marcadores": [],
        }

        self.assertEqual(search_pages(extracted, ["media aritmetica"]), [1])
