# -*- coding: utf-8 -*-
"""Laboratorio 4.7 — o custo de nao ter dono da decisao antes do incidente.

Nao acessa rede nem sistema nenhum. E um modelo declarado neste arquivo:
uma cadeia de aprovacao, com e sem autoridade pre-combinada, medida em
tempo ate a decisao sair.

A pergunta: quanto tempo a ausencia de um dono da decisao custa, quando
cada aprovador precisa ser convencido em vez de apenas confirmado?

Roda com: python autoridade_pre_combinada.py
"""

import random

random.seed(7)

# Cada aprovador tem um tempo de resposta (minutos) quando so precisa
# CONFIRMAR uma decisao ja combinada, e um tempo maior quando precisa
# primeiro ser CONVENCIDO — avaliar o caso do zero, pedir mais contexto,
# hesitar por nao ter mandato claro.
APROVADORES = [
    ("gerente de TI",            (2, 5),   (15, 40)),
    ("diretor de operacoes",     (3, 8),   (30, 90)),
    ("juridico",                 (5, 10),  (45, 120)),
]


def tempo_cadeia(faixas, n_simulacoes=2000):
    """Soma o tempo de cada aprovador na cadeia (serial — decisao de
    autoridade dividida nao se paraleliza, cada um depende do anterior ter
    concordado). Devolve a media sobre n_simulacoes rodadas."""
    total = 0.0
    for _ in range(n_simulacoes):
        soma = sum(random.uniform(*faixa) for faixa in faixas)
        total += soma
    return total / n_simulacoes


def main():
    print("=== cadeia de aprovacao, minutos por etapa ===")
    for nome, com_mandato, sem_mandato in APROVADORES:
        print(f"  {nome:<20} com autoridade pre-combinada: {com_mandato[0]}-{com_mandato[1]} min"
              f"   sem: {sem_mandato[0]}-{sem_mandato[1]} min")

    faixas_com = [c for _, c, _ in APROVADORES]
    faixas_sem = [s for _, _, s in APROVADORES]

    media_com = tempo_cadeia(faixas_com)
    media_sem = tempo_cadeia(faixas_sem)

    print("\n=== tempo medio ate a decisao sair (simulacao, 2000 rodadas) ===")
    print(f"  com autoridade pre-combinada: {media_com:6.1f} min")
    print(f"  sem autoridade pre-combinada: {media_sem:6.1f} min")
    print(f"  razao sem/com:                {media_sem / media_com:6.2f}x")

    print("\n=== leitura ===")
    print("  A cadeia de aprovadores e a mesma nos dois casos. O que muda e")
    print("  se cada um so CONFIRMA algo ja decidido de antemao (quem pode")
    print("  autorizar o que, sob quais condicoes) ou se precisa ser")
    print("  CONVENCIDO do zero durante o incidente. A diferenca nao vem de")
    print("  um aprovador ser mais lento — vem de decisao sem dono virar")
    print("  negociacao, e negociacao nao tem teto de tempo.")


if __name__ == "__main__":
    main()
