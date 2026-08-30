# -*- coding: utf-8 -*-
"""Laboratorio 4.4 — o que a restauracao resolve, e o que ela nao toca.

Nao cifra, nao restaura e nao toca em arquivo nenhum. E um modelo declarado
neste arquivo: um incidente de ransomware descrito como uma lista de fatos, e
tres respostas possiveis avaliadas contra essa lista.

A pergunta: pagar ou restaurar devolve os arquivos. Isso encerra o incidente?

Roda com: python restaurar_nao_encerra.py
"""

# Fatos do incidente. Cada um e uma consequencia que existe independentemente
# das outras — e a lista e o que precisa ser zerado para o caso fechar.
FATOS = [
    ("arquivos de producao cifrados",              "disponibilidade"),
    ("copia dos dados saiu da rede antes da cifra", "confidencialidade"),
    ("credenciais de administrador coletadas",      "acesso"),
    ("mecanismo de persistencia instalado",         "acesso"),
    ("caminho de entrada continua aberto",          "acesso"),
    ("relacao de confianca com um parceiro usada",  "acesso"),
]

# O que cada resposta resolve, pelo rotulo do fato.
RESPOSTAS = {
    "pagar o resgate": {"arquivos de producao cifrados"},
    "restaurar do backup": {"arquivos de producao cifrados"},
    "restaurar + resposta a incidente": {
        "arquivos de producao cifrados",
        "credenciais de administrador coletadas",
        "mecanismo de persistencia instalado",
        "caminho de entrada continua aberto",
        "relacao de confianca com um parceiro usada",
    },
}


def main():
    print("=== fatos do incidente ===")
    for f, eixo in FATOS:
        print(f"  [{eixo:<16}] {f}")

    print("\n=== o que sobra depois de cada resposta ===")
    for nome, resolve in RESPOSTAS.items():
        resta = [(f, e) for f, e in FATOS if f not in resolve]
        print(f"\n  {nome}")
        print(f"    resolve {len(resolve)} de {len(FATOS)} fatos")
        if resta:
            for f, e in resta:
                print(f"    fica: [{e}] {f}")
        else:
            print("    fica: nada da lista")

    print("\n=== o eixo que nenhuma das tres resolve ===")
    conf = [f for f, e in FATOS if e == "confidencialidade"]
    for f in conf:
        quem = [n for n, r in RESPOSTAS.items() if f in r]
        print(f"  {f}: resolvido por {quem if quem else 'nenhuma das respostas'}")

    print("\n=== leitura ===")
    print("  Pagar e restaurar resolvem o mesmo unico fato: os arquivos voltam.")
    print("  A diferenca entre os dois e de custo e de risco, nao de alcance.")
    print("  Cinco dos seis fatos continuam de pe depois de qualquer um dos dois.")
    print("  A copia que saiu antes da cifra e o unico fato que NENHUMA resposta")
    print("  desfaz: dado exfiltrado nao volta. E dai que vem a dupla extorsao —")
    print("  a segunda cobranca nao depende de a vitima ter restaurado ou nao.")
    print("  Restaurar sem resposta a incidente devolve os arquivos para dentro")
    print("  de um ambiente em que o acesso do adversario continua valido.")


if __name__ == "__main__":
    main()
