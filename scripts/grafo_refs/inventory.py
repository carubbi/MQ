"""Inventário reproduzível das fontes PDF do grafo de referências."""

import argparse
import hashlib
import json
from pathlib import Path

import fitz


DEFAULT_MANIFEST = Path("scripts/grafo_refs/data/fontes.json")
HASH_BLOCK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    """Calcula SHA-256 sem carregar todo o PDF na memória."""
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for block in iter(lambda: source_file.read(HASH_BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory_sources(manifest_path: Path, root: Path) -> list[dict]:
    """Acrescenta contagem de páginas e hash às fontes de um manifesto."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    inventory = []
    for source in manifest:
        pdf_path = root / source["arquivo"]
        with fitz.open(pdf_path) as document:
            page_count = document.page_count
        inventory.append(
            {
                **source,
                "paginas_pdf": page_count,
                "hash_sha256": sha256_file(pdf_path),
            }
        )
    return inventory


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventa as fontes PDF do grafo.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    arguments = parser.parse_args()

    inventory = inventory_sources(arguments.manifest, Path.cwd())
    print(json.dumps(inventory, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
