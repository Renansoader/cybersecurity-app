# -*- coding: utf-8 -*-
"""Laboratorio 3.5 — a mesma string, segura num canal, perigosa em outro.

Usa duas strings — uma com apostrofo, uma com tags HTML — e testa cada
uma nos dois canais (SQL por concatenacao, HTML sem escape) para provar
que "perigoso" nao e uma propriedade da string, e sim uma relacao entre
a string e o canal que a recebe. Banco SQLite em memoria; nenhum
servidor de rede, nenhum host de terceiro.

Roda com: python mesma_string_dois_contextos.py
"""

import html
import sqlite3


def testa_no_sql(con, texto):
    try:
        consulta = f"SELECT 1 WHERE 'x' = '{texto}'"
        con.execute(consulta)
        return "executou sem erro"
    except sqlite3.OperationalError as erro:
        return f"ERRO DE SINTAXE: {erro}"


def testa_no_html(texto):
    bruto = f"<p>{texto}</p>"
    seguro = f"<p>{html.escape(texto)}</p>"
    tag_sobrevive = texto in bruto and "<" in texto
    return bruto, seguro, tag_sobrevive


def main():
    con = sqlite3.connect(":memory:")

    casos = {
        "nome com apóstrofo (O'Brien)": "O'Brien",
        "comentário com tag HTML (<b>oi</b>)": "<b>oi</b>",
    }

    for rotulo, texto in casos.items():
        print(f"=== caso: {rotulo} ===")

        resultado_sql = testa_no_sql(con, texto)
        print(f"  no canal SQL (concatenado):  {resultado_sql}")

        bruto, seguro, sobrevive = testa_no_html(texto)
        print(f"  no canal HTML (sem escape):  {bruto!r}  (tag preservada: {sobrevive})")
        print()

    print("=== leitura ===")
    print("  'O'Brien' quebra o canal SQL (o apóstrofo é o delimitador de string ali)")
    print("  mas é só texto inofensivo no canal HTML — nenhum caractere dele tem")
    print("  significado especial em marcação. '<b>oi</b>' faz o oposto: é só um")
    print("  texto estranho para o SQL (sem delimitador nenhum dele em jogo), mas")
    print("  vira uma instrução de formatação real no HTML. Perigoso não é uma")
    print("  propriedade da string — é uma relação entre o que ela contém e o que")
    print("  o canal de destino trata como caractere especial. É por isso que a")
    print("  defesa certa depende do contexto de saída, não de uma lista fixa de")
    print("  'caracteres proibidos' que valeria igual em qualquer lugar.")

    con.close()


if __name__ == "__main__":
    main()
