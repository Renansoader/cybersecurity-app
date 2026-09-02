# -*- coding: utf-8 -*-
"""Laboratorio 4.7 — agir agora com informacao incompleta x esperar confirmar.

Nao acessa rede nem sistema nenhum. Modelo declarado: o custo de um
incidente cresce enquanto ele nao e contido; o custo de agir cedo demais
(falso positivo, container que nao precisava) e fixo. O modelo calcula o
ponto de equilibrio — a partir de qual confianca na hipotese vale a pena
agir sem esperar confirmacao total.

Roda com: python custo_de_esperar.py
"""


def custo_esperado_de_agir(prob_incidente_real, custo_falso_positivo):
    """Agir: se for falso alarme, paga o custo fixo do falso positivo.
    Se for incidente real, o custo de agir e considerado zero de referencia
    (contido a tempo)."""
    return (1 - prob_incidente_real) * custo_falso_positivo


def custo_esperado_de_esperar(prob_incidente_real, custo_por_minuto, minutos_de_espera):
    """Esperar: se for incidente real, o custo cresce com cada minuto de
    espera. Se for falso alarme, esperar nao custa nada (o tempo perdido
    em confirmar nao entra no modelo — e custo de analista, nao de
    incidente)."""
    return prob_incidente_real * custo_por_minuto * minutos_de_espera


def ponto_de_equilibrio(custo_falso_positivo, custo_por_minuto, minutos_de_espera):
    """Probabilidade de incidente real a partir da qual agir custa menos
    que esperar. Resolve agir(p) = esperar(p) para p."""
    denom = custo_falso_positivo + custo_por_minuto * minutos_de_espera
    return custo_falso_positivo / denom


def main():
    custo_falso_positivo = 5_000      # ex.: hora de equipe revertendo isolamento desnecessario
    custo_por_minuto = 800            # ex.: exfiltracao ou cifra continuando
    minutos_de_espera = 20            # tempo tipico para confirmar com certeza

    print("=== parametros do modelo ===")
    print(f"  custo de um falso positivo (agir sem precisar): R$ {custo_falso_positivo:,}")
    print(f"  custo por minuto de incidente real em curso:    R$ {custo_por_minuto:,}")
    print(f"  minutos que esperar por confirmacao total leva:  {minutos_de_espera}")

    print("\n=== custo esperado por probabilidade de ser incidente real ===")
    print(f"{'P(real)':>8} {'agir agora':>12} {'esperar confirmar':>20}")
    for p10 in range(0, 11):
        p = p10 / 10
        agir = custo_esperado_de_agir(p, custo_falso_positivo)
        esperar = custo_esperado_de_esperar(p, custo_por_minuto, minutos_de_espera)
        print(f"{p:8.1f} {agir:12,.0f} {esperar:20,.0f}")

    eq = ponto_de_equilibrio(custo_falso_positivo, custo_por_minuto, minutos_de_espera)
    print(f"\n=== ponto de equilibrio ===")
    print(f"  a partir de P(real) = {eq:.1%}, agir agora custa menos, em esperanca,")
    print(f"  do que esperar os {minutos_de_espera} minutos de confirmacao total.")

    print("\n=== leitura ===")
    print("  O ponto de equilibrio nao e 50% nem 100% — depende da razao entre o")
    print("  custo de errar por excesso de cautela e o custo de errar por excesso")
    print("  de pressa. 'Espere ter certeza' so e a resposta certa quando o custo")
    print("  por minuto de espera e baixo comparado ao custo do falso positivo;")
    print("  quando a razao inverte, esperar certeza total e a decisao mais cara,")
    print("  nao a mais segura.")


if __name__ == "__main__":
    main()
