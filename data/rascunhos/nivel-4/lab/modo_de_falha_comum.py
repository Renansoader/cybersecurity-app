# -*- coding: utf-8 -*-
"""Laboratorio 4.3 — camadas que caem juntas.

Nao toca em rede, disco nem processo: e aritmetica de confiabilidade sobre um
modelo declarado. A pergunta que ele responde: quanto vale acrescentar camadas
quando elas compartilham uma dependencia?

Duas pilhas com as MESMAS quatro camadas e as MESMAS probabilidades de falha
individual. Na primeira, as falhas sao independentes. Na segunda, tres das
quatro dependem do mesmo diretorio de identidade — se ele cair, as tres caem
com ele.

Roda com: python modo_de_falha_comum.py
"""

# Probabilidade de a camada falhar SOZINHA, por tentativa de ataque.
CAMADAS = [
    ("filtro de borda",            0.30),
    ("autenticacao multiplo fator", 0.10),
    ("controle de acesso por papel", 0.20),
    ("deteccao de comportamento",   0.40),
]

# Probabilidade de o diretorio de identidade estar comprometido.
P_DIRETORIO = 0.05
# Camadas que deixam de valer quando o diretorio cai.
DEPENDEM = {"autenticacao multiplo fator", "controle de acesso por papel",
            "deteccao de comportamento"}


def falha_independente():
    """Todas as camadas falham por motivos proprios e nao relacionados."""
    p = 1.0
    for _, pf in CAMADAS:
        p *= pf
    return p


def falha_com_dependencia():
    """Decompoe em dois mundos: com o diretorio de pe, e com ele comprometido.

    Com o diretorio comprometido, as camadas que dependem dele falham com
    certeza, e sobra apenas o produto das independentes.
    """
    resto = 1.0
    for nome, pf in CAMADAS:
        if nome not in DEPENDEM:
            resto *= pf
    p_de_pe = 1.0
    for nome, pf in CAMADAS:
        p_de_pe *= pf
    return (1 - P_DIRETORIO) * p_de_pe + P_DIRETORIO * resto


def linha(rotulo, p):
    print(f"  {rotulo:<34} {p:.6f}   1 em {1/p:,.0f}".replace(",", "."))


def main():
    print("=== camadas declaradas ===")
    for nome, pf in CAMADAS:
        marca = "  (depende do diretorio)" if nome in DEPENDEM else ""
        print(f"  {nome:<30} falha sozinha em {pf:.0%}{marca}")
    print(f"\n  diretorio de identidade comprometido: {P_DIRETORIO:.0%}")

    ind = falha_independente()
    dep = falha_com_dependencia()
    print("\n=== probabilidade de o ataque atravessar TODAS as camadas ===")
    linha("supondo independencia", ind)
    linha("com a dependencia comum", dep)
    print(f"\n  a pilha real e {dep/ind:.0f}x mais permissiva do que a contagem de")
    print("  camadas sugere, com as MESMAS quatro camadas")

    print("\n=== o que cada camada acrescenta, uma a uma (caso dependente) ===")
    ordem = [n for n, _ in CAMADAS]
    acumulado = 1.0
    for i, nome in enumerate(ordem, start=1):
        parcial = [(n, p) for n, p in CAMADAS if n in ordem[:i]]
        resto = 1.0
        for n, p in parcial:
            if n not in DEPENDEM:
                resto *= p
        de_pe = 1.0
        for _, p in parcial:
            de_pe *= p
        atual = (1 - P_DIRETORIO) * de_pe + P_DIRETORIO * resto
        ganho = acumulado / atual if atual else float("inf")
        print(f"  +{nome:<32} {atual:.6f}   ganho {ganho:>5.2f}x")
        acumulado = atual
    print("\n  o ganho de cada camada dependente cai rapido — 6,90x, 2,10x, 1,20x —")
    print("  porque as tres dividem o mesmo motivo de morte: o piso de todas")
    print("  elas juntas e o que sobra quando o diretorio cai")


if __name__ == "__main__":
    main()
