# -*- coding: utf-8 -*-
"""Laboratorio 4.8 — o proprio ato de examinar uma evidencia pode altera-la.

So cria e le um arquivo proprio, dentro de uma pasta temporaria criada por
este script. Nao toca em nenhum arquivo real da maquina, nao altera nenhum
timestamp de proposito — so demonstra, com fatos reais de sistema de
arquivos, que LER um arquivo ja e uma acao que o sistema operacional
registra.

A pergunta: um perito que abre um arquivo "so para olhar" deixa rastro?

Roda com: python custo_da_captura.py
"""

import os
import tempfile
import time
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory(prefix="lab48_") as tmp:
        caminho = Path(tmp) / "evidencia.txt"
        caminho.write_text("conteudo de exemplo, criado por este laboratorio\n", encoding="utf-8")

        antes = caminho.stat()
        print("=== metadados logo apos criar o arquivo ===")
        print(f"  tamanho:            {antes.st_size} bytes")
        print(f"  modificado (mtime): {time.ctime(antes.st_mtime)}")
        print(f"  acessado  (atime):  {time.ctime(antes.st_atime)}")

        time.sleep(1.2)  # garante que o relogio do sistema avance o suficiente pra diferenca aparecer

        print("\n=== abrindo o arquivo só para leitura (nenhuma escrita) ===")
        with open(caminho, "r", encoding="utf-8") as f:
            f.read()

        depois = caminho.stat()
        print("\n=== metadados depois da leitura ===")
        print(f"  tamanho:            {depois.st_size} bytes  (mudou: {depois.st_size != antes.st_size})")
        print(f"  modificado (mtime): {time.ctime(depois.st_mtime)}  (mudou: {depois.st_mtime != antes.st_mtime})")
        print(f"  acessado  (atime):  {time.ctime(depois.st_atime)}  (mudou: {depois.st_atime != antes.st_atime})")

        print("\n=== leitura ===")
        print("  O conteudo e o mtime nao mudaram — ninguem escreveu no arquivo.")
        print("  O atime, quando o sistema de arquivos o mantem, muda so de LER.")
        print("  Um perito que abre um arquivo suspeito num sistema ao vivo, sem")
        print("  write-blocker nem copia forense antes, corre o risco de ele mesmo")
        print("  produzir a alteracao que depois vira objeto de duvida sobre a")
        print("  integridade da evidencia. A ordem certa e sempre copiar primeiro,")
        print("  examinar a copia depois — nunca o inverso.")


if __name__ == "__main__":
    main()
