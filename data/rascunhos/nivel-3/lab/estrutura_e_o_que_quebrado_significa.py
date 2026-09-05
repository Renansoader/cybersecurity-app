# -*- coding: utf-8 -*-
"""Laboratorio 3.8 -- estrutura bate forca bruta, e o que "quebrado" significa.

Nenhuma lista de senhas comuns reproduzida: as palavras-base abaixo sao
inventadas para este script, nao extraidas de nenhum vazamento real. Nenhum
hash de terceiro: todo hash e calculado aqui, sobre senha tambem inventada
aqui. O objetivo e mostrar duas coisas com execucao real, nao com
afirmacao: (1) um ataque estruturado (dicionario + regra de transformacao)
alcanca senha de "formato humano" com uma fracao minuscula do espaco de
busca teorico; (2) "quebrar" uma senha e recuperar aquela entrada
especifica dentro da estrategia usada -- nao e quebrar o algoritmo de hash,
e o tempo medio do lote esconde o pior caso.

Roda com: python estrutura_e_o_que_quebrado_significa.py
"""

import hashlib
import itertools
import secrets
import string
import time


PALAVRAS_BASE = [
    "futebol", "cachorro", "verao", "familia", "musica", "viagem", "trabalho",
]
SUFIXOS_DIGITO = [""] + [str(n) for n in range(0, 100)]
SUFIXOS_SIMBOLO = ["", "!", "@", "#", "123"]


def gerar_candidatos_estruturados():
    for palavra in PALAVRAS_BASE:
        for forma in (palavra, palavra.capitalize()):
            for sufixo_digito in SUFIXOS_DIGITO:
                for sufixo_simbolo in SUFIXOS_SIMBOLO:
                    yield forma + sufixo_digito + sufixo_simbolo


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def atacar(hash_alvo, candidatos, limite=None):
    inicio = time.perf_counter()
    tentativas = 0
    for candidato in candidatos:
        tentativas += 1
        if hash_senha(candidato) == hash_alvo:
            duracao = time.perf_counter() - inicio
            return candidato, tentativas, duracao
        if limite is not None and tentativas >= limite:
            break
    duracao = time.perf_counter() - inicio
    return None, tentativas, duracao


def gerar_senha_aleatoria(tamanho=12):
    alfabeto = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(secrets.choice(alfabeto) for _ in range(tamanho))


def main():
    candidatos_estruturados = list(gerar_candidatos_estruturados())
    tamanho_lista = len(candidatos_estruturados)
    print(f"=== lista estruturada gerada: {tamanho_lista:,} candidatos ===")
    print(f"  {len(PALAVRAS_BASE)} palavras-base x 2 capitalizacoes x "
          f"{len(SUFIXOS_DIGITO)} sufixos de digito x {len(SUFIXOS_SIMBOLO)} "
          f"sufixos de simbolo")

    espaco_teorico = (len(string.ascii_letters + string.digits + "!@#$%&*")) ** 10
    print(f"  espaco de busca teorico para 10 caracteres livres: "
          f"{espaco_teorico:,.2e}")
    print(f"  a lista estruturada e {espaco_teorico / tamanho_lista:,.2e}x "
          f"menor que o espaco teorico")

    alvos = {
        "senha de formato humano (1)": hash_senha("Futebol23!"),
        "senha de formato humano (2)": hash_senha("Verao7!"),
        "senha aleatoria, fora da estrutura": hash_senha(gerar_senha_aleatoria()),
    }

    print("\n=== ataque estruturado contra cada hash ===")
    duracoes = []
    for rotulo, hash_alvo in alvos.items():
        achado, tentativas, duracao = atacar(hash_alvo, candidatos_estruturados)
        duracoes.append(duracao)
        if achado:
            print(f"  {rotulo}: recuperada em {tentativas:,} tentativas "
                  f"({duracao*1000:.1f} ms) -> {achado!r}")
        else:
            print(f"  {rotulo}: NAO recuperada apos {tentativas:,} tentativas "
                  f"({duracao*1000:.1f} ms) -- fora da lista estruturada")

    media = sum(duracoes) / len(duracoes)
    print(f"\n  tempo medio do lote: {media*1000:.1f} ms")

    print("\n=== leitura ===")
    print("  as duas senhas de formato humano caem quase de imediato, porque")
    print("  a estrutura (palavra + capitalizacao + sufixo) e exatamente o que")
    print("  uma pessoa tende a escolher -- nao e forca bruta, e adivinhar com")
    print("  hipotese. a senha aleatoria nao cai, porque nunca esteve na lista")
    print("  gerada -- e o sha256 dela continua tao intacto quanto o das outras")
    print("  duas: nada aqui quebrou o algoritmo de hash, so encontrou (ou nao)")
    print("  a entrada certa dentro da estrategia escolhida.")
    print("  o 'tempo medio do lote' acima e enganoso por construcao: ele mistura")
    print("  dois casos que caem em milissegundos com um caso que nunca cairia,")
    print("  mesmo rodando essa lista para sempre -- reportar so a media esconde")
    print("  exatamente a senha que a defesa mais precisa proteger.")


if __name__ == "__main__":
    main()
