# -*- coding: utf-8 -*-
"""Laboratorio 3.8 -- o custo real de uma tentativa de senha.

Nao acessa rede nem usa hash de terceiro: mede, nesta maquina, quantas
tentativas por segundo um hash rapido (sha256) e um hash lento calibrado
(pbkdf2_hmac com 600.000 iteracoes, o minimo recomendado pela OWASP citado
em 2.4.t5) permitem, e projeta quanto tempo cada um leva para esgotar um
espaco de busca de exemplo. Nenhuma senha real, nenhuma lista de senhas
comuns: os candidatos sao gerados por contador, nao adivinhados.

Roda com: python custo_da_tentativa.py
"""

import hashlib
import time


def taxa_hash_rapido(n_amostras=200_000):
    alvo = hashlib.sha256(b"alvo-de-exemplo").hexdigest()
    inicio = time.perf_counter()
    for i in range(n_amostras):
        hashlib.sha256(f"tentativa{i}".encode()).hexdigest()
    duracao = time.perf_counter() - inicio
    return n_amostras / duracao


def taxa_hash_lento(n_amostras=20, iteracoes=600_000):
    sal = b"sal-de-exemplo-fixo-so-para-medir-taxa"
    inicio = time.perf_counter()
    for i in range(n_amostras):
        hashlib.pbkdf2_hmac(
            "sha256", f"tentativa{i}".encode(), sal, iteracoes
        )
    duracao = time.perf_counter() - inicio
    return n_amostras / duracao


def tempo_para_esgotar(espaco, tentativas_por_segundo):
    segundos = espaco / tentativas_por_segundo
    return segundos


def formatar_duracao(segundos):
    unidades = [
        ("segundos", 1),
        ("minutos", 60),
        ("horas", 3600),
        ("dias", 86400),
        ("anos", 86400 * 365),
        ("seculos", 86400 * 365 * 100),
    ]
    escolhida = unidades[0]
    for nome, tamanho in unidades:
        if segundos >= tamanho:
            escolhida = (nome, tamanho)
    nome, tamanho = escolhida
    return f"{segundos / tamanho:,.1f} {nome}"


def main():
    print("=== taxa medida nesta maquina ===")
    rapido = taxa_hash_rapido()
    print(f"  hash rapido (sha256):                 {rapido:,.0f} tentativas/s")

    lento = taxa_hash_lento()
    print(f"  hash lento (pbkdf2_hmac, 600.000 it): {lento:,.1f} tentativas/s")

    razao = rapido / lento
    print(f"\n  o hash lento custa {razao:,.0f}x mais por tentativa.")
    print("  nenhuma das duas funcoes mudou de forma; o que muda e o custo")
    print("  que a propria funcao impoe a cada chamada.")

    # espaco de exemplo: 8 caracteres entre minusculas e digitos (36^8)
    espaco = 36 ** 8
    print(f"\n=== projecao para esgotar um espaco de {espaco:,} combinacoes ===")
    print(f"  com hash rapido: {formatar_duracao(tempo_para_esgotar(espaco, rapido))}")
    print(f"  com hash lento:  {formatar_duracao(tempo_para_esgotar(espaco, lento))}")

    print("\n=== leitura ===")
    print("  o custo de tentar e tentativas-por-segundo vezes tamanho do")
    print("  espaco de busca. a funcao lenta age no primeiro lado da conta;")
    print("  comprimento e diversidade de caractere agem no segundo. as duas")
    print("  se multiplicam -- e e por isso que o modulo 2.4 recomenda")
    print("  Argon2id/PBKDF2 e o modulo 2.5 recomenda 15+ caracteres: cada um")
    print("  encarece um lado diferente da mesma equacao.")


if __name__ == "__main__":
    main()
