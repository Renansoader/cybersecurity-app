# -*- coding: utf-8 -*-
"""Laboratorio 4.4 — triagem estatica de arquivo suspeito.

NENHUMA AMOSTRA REAL DE MALWARE. O script cria os proprios arquivos de exemplo,
todos benignos, num diretorio temporario, e os apaga no fim. Nenhum deles e
executavel: sao um PNG, um ZIP, um PDF e um texto. O objetivo e a TECNICA de
triagem — identificar tipo real, calcular resumo, extrair cadeias — e a
distincao entre indicador e coincidencia.

Nada aqui executa o arquivo examinado. Triagem estatica e, por definicao, o que
se faz sem rodar nada.

Roda com: python triagem_estatica.py
"""

import hashlib
import re
import shutil
import tempfile
from pathlib import Path

# Assinaturas de inicio de arquivo (magic bytes) de formatos benignos comuns.
ASSINATURAS = [
    (b"\x89PNG\r\n\x1a\n", "imagem PNG"),
    (b"PK\x03\x04", "arquivo ZIP (ou formato baseado em ZIP)"),
    (b"%PDF-", "documento PDF"),
    (b"\x1f\x8b", "arquivo GZIP"),
]

# O que cada extensao promete. O xlsx moderno E um ZIP, entao o par bate.
PROMETIDO = {
    ".pdf": {"documento PDF"},
    ".xlsx": {"arquivo ZIP (ou formato baseado em ZIP)"},
    ".txt": {"texto legivel"},
    ".png": {"imagem PNG"},
}

# Conteudo dos exemplos. Tudo benigno e escrito pelo proprio script.
EXEMPLOS = {
    # PNG minimo valido: assinatura + um bloco IHDR truncado. Nao e imagem util,
    # e serve para o que interessa aqui: o inicio do arquivo.
    "relatorio_final.pdf": b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + b"\x00" * 40,
    "planilha_orcamento.xlsx": b"PK\x03\x04" + b"\x14\x00\x06\x00" + b"\x00" * 40,
    "manual.pdf": b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog >>\nendobj\n" + b"\x00" * 20,
    "notas.txt": (
        "reuniao de 12/03\n"
        "contato: suporte@example.com\n"
        "servidor de teste: 192.0.2.10\n"
        "lembrete: renovar certificado em abril\n"
    ).encode("utf-8"),
}


def tipo_real(dados):
    for assinatura, nome in ASSINATURAS:
        if dados.startswith(assinatura):
            return nome
    if all(32 <= b < 127 or b in (9, 10, 13) for b in dados[:256]):
        return "texto legivel"
    return "desconhecido"


def cadeias(dados, minimo=6):
    """Sequencias legiveis de tamanho minimo — o `strings` em cinco linhas."""
    return re.findall(rb"[\x20-\x7e]{%d,}" % minimo, dados)


INDICADORES = [
    (re.compile(rb"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "endereco IP"),
    (re.compile(rb"https?://[^\s\"']+"), "endereco web"),
    (re.compile(rb"[\w.+-]+@[\w-]+\.[\w.]{2,}"), "endereco de e-mail"),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="triagem_"))
    try:
        for nome, dados in EXEMPLOS.items():
            (tmp / nome).write_bytes(dados)

        print("=== 1. extensao declarada contra tipo real ===")
        print(f"  {'arquivo':<26} {'extensao':<10} tipo real pelos primeiros bytes")
        for nome in EXEMPLOS:
            dados = (tmp / nome).read_bytes()
            ext = Path(nome).suffix
            real = tipo_real(dados)
            bate = "" if real in PROMETIDO.get(ext, set()) else "  <-- NAO BATE"
            print(f"  {nome:<26} {ext:<10} {real}{bate}")

        print("\n=== 2. resumo criptografico de cada arquivo ===")
        for nome in EXIBIR_ORDEM:
            dados = (tmp / nome).read_bytes()
            print(f"  {nome:<26} sha256 {hashlib.sha256(dados).hexdigest()[:32]}...")

        print("\n=== 3. cadeias legiveis e o que elas sugerem ===")
        for nome in EXIBIR_ORDEM:
            dados = (tmp / nome).read_bytes()
            achadas = cadeias(dados)
            print(f"  {nome}: {len(achadas)} cadeia(s) com 6 caracteres ou mais")
            for padrao, rotulo in INDICADORES:
                for m in padrao.findall(dados):
                    print(f"      {rotulo}: {m.decode('utf-8', 'replace')}")

        print("\n=== leitura ===")
        print("  O primeiro arquivo se chama .pdf e comeca com a assinatura de PNG:")
        print("  extensao e nome sao escolhidos por quem entrega o arquivo, e nao")
        print("  descrevem o conteudo. Os primeiros bytes descrevem.")
        print("  O .txt traz um endereco IP e um e-mail, que um leitor apressado")
        print("  chamaria de indicador. Nenhum dos dois e indicio aqui: sao os")
        print("  dados de uma reuniao. Indicador precisa de contexto:")
        print("  o mesmo IP dentro de um binario sem motivo para falar em rede")
        print("  significa uma coisa; num arquivo de notas, significa outra.")
        print("  O resumo nao diz se o arquivo e malicioso. Ele serve para comparar")
        print("  com o que ja se conhece e para nomear o arquivo sem ambiguidade.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n  (diretorio temporario removido)")


EXIBIR_ORDEM = list(EXEMPLOS)

if __name__ == "__main__":
    main()
