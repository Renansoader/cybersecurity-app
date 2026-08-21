"""Pegada digital em metadados de documento — so em arquivos locais proprios."""
import sys
from pathlib import Path
from pypdf import PdfReader

ALVOS = ["docs/Crypto101.pdf", "docs/SEv3.pdf", "docs/cyber security.pdf"]

print("=== metadados embutidos em PDF publicado ===")
for rel in ALVOS:
    caminho = Path(r"C:/Dev/cybersecurity-app") / rel
    if not caminho.exists():
        continue
    meta = PdfReader(caminho).metadata or {}
    print(f"--- {caminho.name}")
    for chave in ("/Title", "/Author", "/Creator", "/Producer", "/CreationDate", "/ModDate"):
        if chave in meta:
            print(f"  {chave:<14} {str(meta[chave])[:70]}")
print()
print("Cada campo desses viaja com o arquivo publicado no site da empresa.")
print("Ferramenta de escritorio grava nome de usuario, caminho e versao sem avisar.")
