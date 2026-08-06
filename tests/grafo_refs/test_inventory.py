import json
import tempfile
import unittest
from pathlib import Path

import fitz

from scripts.grafo_refs.inventory import inventory_sources


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPOSITORY_ROOT / "scripts/grafo_refs/data/fontes.json"


class InventoryTests(unittest.TestCase):
    def test_inventory_reports_page_count_and_sha256_for_a_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf_path = root / "sample.pdf"
            document = fitz.open()
            document.new_page()
            document.new_page()
            document.save(pdf_path)
            document.close()
            manifest_path = root / "fontes.json"
            manifest_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "sample",
                            "tipo_fonte": "apostila",
                            "titulo": "Sample",
                            "arquivo": "sample.pdf",
                            "idioma": "en",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            inventory = inventory_sources(manifest_path, root)

        self.assertEqual(inventory[0]["paginas_pdf"], 2)
        self.assertRegex(inventory[0]["hash_sha256"], r"^[0-9a-f]{64}$")

    def test_manifest_has_nine_unique_ids_and_existing_paths(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(len(manifest), 9)
        self.assertEqual(len({source["id"] for source in manifest}), 9)
        self.assertTrue(
            all((REPOSITORY_ROOT / source["arquivo"]).is_file() for source in manifest)
        )
