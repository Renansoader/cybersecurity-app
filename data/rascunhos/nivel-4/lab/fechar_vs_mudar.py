# -*- coding: utf-8 -*-
"""Laboratorio 4.7 — encerrar o chamado x mudar o sistema.

Nao acessa rede nem sistema nenhum. Mesmo padrao de restaurar_nao_encerra.py
(4.4), aplicado ao pos-incidente em vez de a contencao: uma lista de itens
de acao depois de um incidente, cada um marcado como "chamado fechado" ou
como "verificado como mudado de fato" — e a lacuna entre os dois.

Roda com: python fechar_vs_mudar.py
"""

ITENS = [
    ("credencial comprometida trocada",                    True,  True),
    ("regra de deteccao criada para o padrao usado",        True,  False),  # criada, nunca testada
    ("caminho de entrada (VPN sem MFA) corrigido",          True,  False),  # ticket fechado, config nao mudou
    ("relatorio de incidente arquivado",                    True,  True),
    ("playbook atualizado com o que faltou desta vez",      False, False),  # nem chegou a virar tarefa
    ("acesso de terceiro revisado apos o incidente",        True,  True),
]


def main():
    print("=== itens de acao pos-incidente ===")
    print(f"{'item':<50} {'chamado fechado':>16} {'mudanca verificada':>20}")
    for nome, fechado, verificado in ITENS:
        print(f"{nome:<50} {'sim' if fechado else 'nao':>16} {'sim' if verificado else 'nao':>20}")

    fechados = [n for n, f, v in ITENS if f]
    verificados = [n for n, f, v in ITENS if v]
    lacuna = [n for n, f, v in ITENS if f and not v]

    print(f"\n=== contagem ===")
    print(f"  chamados fechados:      {len(fechados)} de {len(ITENS)}")
    print(f"  mudancas verificadas:   {len(verificados)} de {len(ITENS)}")
    print(f"  lacuna (fechado sem verificar mudanca): {len(lacuna)}")
    for n in lacuna:
        print(f"    - {n}")

    print("\n=== leitura ===")
    print("  'Fechado' e um estado do sistema de chamados, preenchido por quem")
    print("  registra. 'Verificado' exige uma segunda acao independente que")
    print("  confirma que o sistema mudou de fato — testar a regra, tentar a VPN")
    print("  sem MFA de novo, reler o playbook contra o incidente. A lacuna e")
    print("  exatamente os itens que alguem marcou como prontos sem essa segunda")
    print("  checagem: o mesmo padrao de risco de 'regra nunca testada de proposito'")
    print("  que o 4.5 ja ensinou, aplicado ao processo em vez de a deteccao.")


if __name__ == "__main__":
    main()
