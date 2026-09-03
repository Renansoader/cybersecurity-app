# -*- coding: utf-8 -*-
"""Laboratorio 3.5 — dado que vira instrucao: consulta a banco.

Banco SQLite em memoria, criado e destruido por este script — nenhum
banco real e tocado. Compara concatenar a entrada diretamente na string
da consulta contra usar parametro (placeholder `?`), com a MESMA
entrada nos dois casos.

A entrada usada nao e um payload de ataque: e um nome real e comum,
"O'Brien", que contem um apostrofo por acidente de ortografia, nao por
intencao maliciosa. O objetivo e mostrar que o problema nao depende de
um atacante esperto — dado legitimo ja quebra a concatenacao.

Roda com: python sql_concatenacao_vs_parametros.py
"""

import sqlite3


def montar_banco():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE usuarios (nome TEXT, email TEXT)")
    con.executemany(
        "INSERT INTO usuarios VALUES (?, ?)",
        [("ana", "ana@exemplo.local"), ("O'Brien", "obrien@exemplo.local"), ("carla", "carla@exemplo.local")],
    )
    con.commit()
    return con


def busca_por_concatenacao(con, nome_buscado):
    """Constroi a consulta colando a entrada diretamente na string —
    dado e instrução no mesmo canal, sem fronteira nenhuma entre eles."""
    consulta = f"SELECT nome, email FROM usuarios WHERE nome = '{nome_buscado}'"
    return consulta, con.execute(consulta).fetchall()


def busca_por_parametro(con, nome_buscado):
    """A entrada vai num parâmetro separado — o driver do banco manda o
    valor e o comando por canais diferentes, então o valor nunca é
    interpretado como parte do comando."""
    consulta = "SELECT nome, email FROM usuarios WHERE nome = ?"
    return consulta, con.execute(consulta, (nome_buscado,)).fetchall()


def main():
    con = montar_banco()

    print("=== busca normal, por concatenação (nome sem caractere especial) ===")
    consulta, resultado = busca_por_concatenacao(con, "ana")
    print(f"  consulta: {consulta}")
    print(f"  resultado: {resultado}")

    nome_legitimo = "O'Brien"  # nome real, com apóstrofo — não é ataque, é ortografia comum

    print(f"\n=== busca por concatenação, agora pelo nome legítimo {nome_legitimo!r} ===")
    consulta = f"SELECT nome, email FROM usuarios WHERE nome = '{nome_legitimo}'"
    print(f"  consulta montada: {consulta}")
    try:
        con.execute(consulta).fetchall()
        print("  executou sem erro")
    except sqlite3.OperationalError as erro:
        print(f"  ERRO DE SINTAXE: {erro}")
        print("  o apóstrofo do próprio nome fechou a string cedo demais — o banco")
        print("  não consegue mais distinguir onde o dado termina e o comando continua")

    print(f"\n=== a mesma busca, agora por parâmetro ===")
    consulta, resultado = busca_por_parametro(con, nome_legitimo)
    print(f"  consulta: {consulta}")
    print(f"  parâmetro enviado separadamente: {nome_legitimo!r}")
    print(f"  resultado: {resultado}")

    print("\n=== leitura ===")
    print("  O nome 'O'Brien' não é um ataque — é um sobrenome real, comum em países")
    print("  de língua inglesa. Por concatenação, mesmo esse dado legítimo já quebra a")
    print("  consulta, porque o apóstrofo do dado é indistinguível do apóstrofo que")
    print("  delimita a instrução. Por parâmetro, a mesma pessoa é encontrada")
    print("  normalmente — o dado nunca compete com a sintaxe do comando. Um atacante")
    print("  não precisa inventar nada sofisticado: só precisa saber que o mesmo")
    print("  caractere que quebra por acidente também pode ser usado de propósito.")

    con.close()


if __name__ == "__main__":
    main()
