# -*- coding: utf-8 -*-
"""Laboratorio 4.8 — hash como prova demonstravel de integridade.

Cria tres arquivos proprios dentro de uma pasta temporaria: o original, uma
copia identica (o que uma copia forense deveria produzir) e uma copia
alterada em um unico byte (o que qualquer adulteracao, por menor que seja,
produziria). Nao toca em nenhum arquivo real da maquina.

A pergunta: "cadeia de custodia" costuma virar um formulario assinado —
mas o que realmente prova que o arquivo de hoje e o mesmo de ontem?

Roda com: python hash_de_integridade.py
"""

import hashlib
import tempfile
from pathlib import Path


def sha256_de(caminho):
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def main():
    with tempfile.TemporaryDirectory(prefix="lab48_hash_") as tmp:
        pasta = Path(tmp)
        original = pasta / "original.bin"
        copia_identica = pasta / "copia_identica.bin"
        copia_alterada = pasta / "copia_alterada.bin"

        conteudo = bytes(range(256)) * 40  # 10.240 bytes, deterministico
        original.write_bytes(conteudo)
        copia_identica.write_bytes(conteudo)

        alterado = bytearray(conteudo)
        alterado[5000] ^= 0x01  # inverte um unico bit, no meio do arquivo
        copia_alterada.write_bytes(bytes(alterado))

        h_original = sha256_de(original)
        h_copia = sha256_de(copia_identica)
        h_alterada = sha256_de(copia_alterada)

        print("=== tamanho dos três arquivos (bytes) ===")
        print(f"  original:        {original.stat().st_size}")
        print(f"  copia identica:  {copia_identica.stat().st_size}")
        print(f"  copia alterada:  {copia_alterada.stat().st_size}  (mesmo tamanho — só 1 bit mudou)")

        print("\n=== sha256 de cada arquivo ===")
        print(f"  original:        {h_original}")
        print(f"  copia identica:  {h_copia}")
        print(f"  copia alterada:  {h_alterada}")

        print("\n=== comparação ===")
        print(f"  original == copia identica: {h_original == h_copia}")
        print(f"  original == copia alterada: {h_original == h_alterada}")

        print("\n=== leitura ===")
        print("  A copia alterada tem o MESMO tamanho do original — nada no")
        print("  metadado (tamanho, nome, data) denuncia a alteração de um único")
        print("  bit em 10.240 bytes. O hash muda por completo mesmo assim: é a")
        print("  função criptográfica, não uma inspeção visual ou um formulário")
        print("  assinado, que torna a integridade uma propriedade verificável —")
        print("  qualquer pessoa com os dois arquivos e uma calculadora de hash")
        print("  confirma a integridade sozinha, sem confiar na palavra de quem")
        print("  coletou.")


if __name__ == "__main__":
    main()
