# -*- coding: utf-8 -*-
"""Laboratorio 4.3 — o que cada classe de controle alcanca.

Nao toca em rede, disco nem processo. Passa a MESMA cadeia de ataque por tres
conjuntos de controle e mostra, passo a passo, o que cada conjunto impede, o que
apenas observa e o que consegue desfazer depois.

A cadeia e sintetica e declarada aqui: seis passos, do phishing a exfiltracao.

Roda com: python classes_de_controle.py
"""

CADEIA = [
    "1. e-mail com anexo malicioso chega a caixa do usuario",
    "2. usuario abre o anexo e o codigo executa na estacao",
    "3. codigo coleta credencial guardada no navegador",
    "4. credencial e usada para entrar no servidor de arquivos",
    "5. 40 GB sao copiados do servidor para a estacao",
    "6. 40 GB saem da rede para um endereco externo",
]

# controle -> (classe, passos que ele IMPEDE, passos que ele OBSERVA,
#              passos que ele consegue DESFAZER)
CONTROLES = {
    "filtro de anexo":            ("preventivo", {1}, set(), set()),
    "bloqueio de macro":          ("preventivo", {2}, set(), set()),
    "cofre de senhas":            ("preventivo", {3}, set(), set()),
    "multiplo fator no servidor": ("preventivo", {4}, set(), set()),
    "registro de autenticacao":   ("detectivo",  set(), {4}, set()),
    "alerta de volume de leitura": ("detectivo", set(), {5}, set()),
    "alerta de saida de dados":   ("detectivo",  set(), {6}, set()),
    "backup isolado":             ("corretivo",  set(), set(), {5}),
    "revogacao de credencial":    ("corretivo",  set(), set(), {4}),
}

CONJUNTOS = {
    "so preventivo": [c for c, v in CONTROLES.items() if v[0] == "preventivo"],
    "so detectivo":  [c for c, v in CONTROLES.items() if v[0] == "detectivo"],
    "as tres classes": ["filtro de anexo", "multiplo fator no servidor",
                        "registro de autenticacao", "revogacao de credencial"],
}


def avalia(nomes):
    impede, observa, desfaz = set(), set(), set()
    for n in nomes:
        _, i, o, d = CONTROLES[n]
        impede |= i
        observa |= o
        desfaz |= d
    return impede, observa, desfaz


def main():
    print("=== cadeia de ataque (sintetica, declarada no proprio script) ===")
    for passo in CADEIA:
        print("  " + passo)

    for rotulo, nomes in CONJUNTOS.items():
        impede, observa, desfaz = avalia(nomes)
        print(f"\n=== conjunto: {rotulo} ({len(nomes)} controles) ===")
        for n in nomes:
            print(f"    - {n} ({CONTROLES[n][0]})")
        # o ataque para no primeiro passo impedido
        parada = min(impede) if impede else None
        alcance = (parada - 1) if parada else len(CADEIA)
        print(f"  passos que o ataque completa: {alcance} de {len(CADEIA)}")
        if parada:
            print(f"  primeira parada: passo {parada}")
        else:
            print("  primeira parada: nenhuma — a cadeia vai ate o fim")
        tentado = parada if parada else len(CADEIA)
        vistos = sorted(p for p in observa if p <= tentado)
        print(f"  passos observados: {vistos if vistos else 'nenhum'}")
        recuperaveis = sorted(p for p in desfaz if p <= tentado)
        print(f"  passos que dao para desfazer depois: "
              f"{recuperaveis if recuperaveis else 'nenhum'}")

    # o caso que interessa: uma camada preventiva falha
    print("\n=== conjunto: as tres classes, com o filtro de anexo falhando ===")
    nomes = [n for n in CONJUNTOS["as tres classes"] if n != "filtro de anexo"]
    for n in nomes:
        print(f"    - {n} ({CONTROLES[n][0]})")
    print("    - filtro de anexo (preventivo) — FALHOU nesta rodada")
    impede, observa, desfaz = avalia(nomes)
    parada = min(impede) if impede else None
    alcance = (parada - 1) if parada else len(CADEIA)
    print(f"  passos que o ataque completa: {alcance} de {len(CADEIA)}")
    print(f"  primeira parada: passo {parada}" if parada else "  primeira parada: nenhuma")
    tentado = parada if parada else len(CADEIA)
    vistos = sorted(p for p in observa if p <= tentado)
    print(f"  passos observados: {vistos if vistos else 'nenhum'}")
    rec = sorted(p for p in desfaz if p <= tentado)
    print(f"  passos que dao para desfazer depois: {rec if rec else 'nenhum'}")

    print("\n=== leitura ===")
    print("  Com tudo funcionando, dois dos tres conjuntos param a cadeia no")
    print("  passo 1, e a contagem de controles nao distingue nada: 4, 3 e 4.")
    print("  A diferenca aparece quando uma camada falha. Sem o filtro de anexo,")
    print("  o conjunto misto deixa o ataque completar 3 dos 6 passos, para no 4,")
    print("  e esse passo 4 sai observado e revogavel. So detectivo nunca para:")
    print("  completa os 6 e observa os passos 4, 5 e 6 de um estrago consumado.")


if __name__ == "__main__":
    main()