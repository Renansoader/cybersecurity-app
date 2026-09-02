# -*- coding: utf-8 -*-
"""Laboratorio 4.7 — notificacao em cadeia (serial) x em leque (paralela).

Nao acessa rede nem sistema nenhum. Modelo declarado: a mesma lista de
partes interessadas, notificada de duas formas — uma pessoa avisa a
proxima, que avisa a proxima (serial), ou uma pessoa aciona todo mundo ao
mesmo tempo (paralela). O prazo externo (o que a lei exige) NAO e
recalculado aqui — e so um numero de referencia que o 0.4 ja ensinou,
usado como teto para comparar contra o tempo interno.

Roda com: python cadeia_de_comunicacao.py
"""

PARTES = [
    ("lider tecnico confirma o incidente",        5),
    ("gerente de seguranca avaliado",             15),
    ("juridico avaliado",                         20),
    ("diretoria avisada",                         10),
    ("comunicacao/RP prepara posicionamento",     30),
    ("encarregado de dados (LGPD) aciona ANPD",   15),
]

PRAZO_EXTERNO_DIAS_UTEIS = 3  # referencia: ja estabelecido no 0.4 (Resolucao CD/ANPD no 15/2024) —
# nao recalculado aqui. Fica em dias uteis mesmo, sem converter para horas: "3 dias uteis" nao e
# "72 horas corridas" (dia util exclui fim de semana, entao 3 dias uteis quase sempre passa de 72h
# corridas) — inventar uma equivalencia em hora seria precisao falsa que o 0.4 nao afirma.


def tempo_serial(partes):
    return sum(minutos for _, minutos in partes)


def tempo_paralelo(partes):
    """Paralelo real tem uma restricao: quem depende de informacao de
    outro (juridico e comunicacao dependem do que a diretoria decidiu
    liberar) nao pode comecar antes. Aqui simplificamos com duas ondas:
    onda 1 roda em paralelo, onda 2 depende do fim da onda 1."""
    onda1 = ["lider tecnico confirma o incidente", "gerente de seguranca avaliado", "diretoria avisada"]
    onda2 = ["juridico avaliado", "comunicacao/RP prepara posicionamento", "encarregado de dados (LGPD) aciona ANPD"]
    tempo_onda1 = max(m for nome, m in partes if nome in onda1)
    tempo_onda2 = max(m for nome, m in partes if nome in onda2)
    return tempo_onda1 + tempo_onda2


def main():
    print("=== partes a notificar, minutos estimados para cada etapa ===")
    for nome, minutos in PARTES:
        print(f"  {minutos:3} min  {nome}")

    serial = tempo_serial(PARTES)
    paralelo = tempo_paralelo(PARTES)

    print(f"\n=== tempo total ===")
    print(f"  serial (um avisa o proximo):        {serial} min ({serial/60:.1f} h)")
    print(f"  paralelo em duas ondas dependentes: {paralelo} min ({paralelo/60:.1f} h)")
    print(f"  prazo externo de referencia (0.4):  {PRAZO_EXTERNO_DIAS_UTEIS} dias uteis")

    print("\n=== folga ate o prazo externo ===")
    print(f"  as duas formas terminam em menos de {max(serial, paralelo)/60:.1f} h — uma fracao")
    print(f"  pequena de {PRAZO_EXTERNO_DIAS_UTEIS} dias uteis, mesmo sem converter dia util em hora")
    print("  corrida (a conversao exata depende de cair ou nao em fim de semana)")

    print("\n=== leitura ===")
    print("  As duas formas cabem dentro do prazo externo neste exemplo — a folga")
    print("  existe porque a cadeia interna e curta comparada ao prazo legal, medido")
    print("  em dias, nao em minutos. O ponto nao e o numero exato de horas de folga:")
    print("  e que o prazo legal comeca a contar da")
    print("  CIENCIA do incidente, e a cadeia interna so comeca depois que alguem")
    print("  primeiro reconhece que ha um incidente. Um lider tecnico que demora")
    print("  a escalar consome a folga antes de qualquer aprovador entrar na conta.")


if __name__ == "__main__":
    main()
