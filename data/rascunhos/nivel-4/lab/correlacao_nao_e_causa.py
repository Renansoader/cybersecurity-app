# -*- coding: utf-8 -*-
"""Laboratorio 4.8 — o que uma evidencia sustenta, e o que ela nao sustenta.

Duas demonstracoes, com dados sinteticos gerados por este script (nenhum
dado real). Nao acessa rede nem sistema nenhum.

1. Correlacao temporal por acaso: dois processos aleatorios e
   independentes, medidos juntos por tempo suficiente, produzem picos
   coincidentes de vez em quando so pela matematica — sem nenhuma relacao
   causal entre eles.
2. Ausencia de log nao e ausencia de acao: um evento real acontece fora
   da janela que o sistema de log cobre, e o relatorio "nao ha registro"
   nao vira "nao aconteceu".

Roda com: python correlacao_nao_e_causa.py
"""

import random

random.seed(11)


def coincidencias_por_acaso(n_dias=90, prob_evento_a=0.15, prob_evento_b=0.15):
    """Dois processos independentes. Quantos dias os dois eventos caem no
    mesmo dia, so por acaso, com as probabilidades dadas?"""
    dias_a = [random.random() < prob_evento_a for _ in range(n_dias)]
    dias_b = [random.random() < prob_evento_b for _ in range(n_dias)]
    coincidencias = sum(1 for a, b in zip(dias_a, dias_b) if a and b)
    esperado = n_dias * prob_evento_a * prob_evento_b
    return coincidencias, esperado, dias_a, dias_b


def main():
    print("=== demonstração 1: coincidência temporal sem causa ===")
    coincidencias, esperado, dias_a, dias_b = coincidencias_por_acaso()
    print(f"  90 dias, dois processos independentes (15% de chance cada, por dia)")
    print(f"  coincidências observadas (os dois no mesmo dia): {coincidencias}")
    print(f"  coincidências esperadas só pelo acaso:           {esperado:.1f}")
    print("  Os dois processos foram sorteados de forma totalmente independente")
    print("  neste script — nenhum influencia o outro. Ainda assim, coincidem")
    print("  em vários dias, porque coincidência ocasional é o comportamento")
    print("  ESPERADO de dois eventos independentes, não uma anomalia.")

    print("\n=== demonstração 2: ausência de log não é ausência de ação ===")
    janela_log = set(range(8, 20))  # log so cobre das 8h as 19h (rotacao/retencao configurada assim)
    hora_do_evento_real = 3  # o evento aconteceu de fato às 3h da manhã
    print(f"  janela coberta pelo log: horas {min(janela_log)}h–{max(janela_log)}h")
    print(f"  hora real em que o evento aconteceu: {hora_do_evento_real}h")
    print(f"  o log tem registro dessa hora? {hora_do_evento_real in janela_log}")
    print("  Um relatório que diz 'nenhum log mostra esse evento' está descrevendo")
    print("  a cobertura do sistema de coleta, não o mundo real. A pergunta certa")
    print("  não é 'o log mostra?', é 'o log SEQUER COBRIA esse horário e essa fonte?'.")

    print("\n=== leitura ===")
    print("  As duas demonstrações minam o mesmo tipo de conclusão apressada:")
    print("  tratar uma correlação como prova de causa, e tratar um log vazio")
    print("  como prova de ausência. As duas exigem a mesma disciplina —")
    print("  perguntar o que a evidência de fato cobre antes de decidir o que")
    print("  ela sustenta.")


if __name__ == "__main__":
    main()
