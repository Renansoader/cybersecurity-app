# -*- coding: utf-8 -*-
"""Laboratorio 5.1 -- 100% de cobertura de linha nao prova ausencia de falha.

Uma funcao de regra de negocio (calculo de desconto), uma suite de testes
que executa toda linha dela (cobertura de linha real, medida, nao
estimada), e um caso de entrada que a suite nunca imaginou -- a mesma linha
roda, o resultado esta errado, e a cobertura continua em 100%.

Roda com: python cobertura_nao_e_correcao.py
"""


def calcular_desconto(valor_total, quantidade_itens):
    """Regra pretendida: 10% de desconto para 5 ou mais itens,
    NUNCA um desconto que deixe o valor final negativo ou maior
    que o valor original."""
    desconto = 0.0
    if quantidade_itens >= 5:
        desconto = valor_total * 0.10
    valor_final = valor_total - desconto
    return valor_final


def linhas_executadas():
    """Registra manualmente quais ramos da função rodaram, para medir
    cobertura de linha sem depender de ferramenta externa."""
    executadas = set()

    def calcular_com_rastro(valor_total, quantidade_itens):
        executadas.add("entrada_da_funcao")
        desconto = 0.0
        executadas.add("inicializa_desconto")
        if quantidade_itens >= 5:
            executadas.add("ramo_com_desconto")
            desconto = valor_total * 0.10
            executadas.add("calcula_desconto")
        else:
            executadas.add("ramo_sem_desconto")
        valor_final = valor_total - desconto
        executadas.add("calcula_valor_final")
        return valor_final, executadas

    return calcular_com_rastro


def main():
    testes = [
        (100.0, 2, 100.0),   # menos de 5 itens: sem desconto
        (100.0, 5, 90.0),    # 5 itens: 10% de desconto
        (200.0, 10, 180.0),  # muitos itens: 10% de desconto
    ]

    calcular_com_rastro = linhas_executadas()
    todas_linhas = set()
    print("=== suite de testes existente ===")
    for valor, qtd, esperado in testes:
        resultado, linhas = calcular_com_rastro(valor, qtd)
        todas_linhas |= linhas
        ok = abs(resultado - esperado) < 0.01
        print(f"  valor={valor}, itens={qtd} -> {resultado} "
              f"(esperado {esperado}): {'passou' if ok else 'FALHOU'}")

    total_ramos_possiveis = 6  # entrada, inicializa, ramo-com, ramo-sem, calcula-desconto, calcula-final
    print(f"\n  linhas/ramos executados pela suite: {sorted(todas_linhas)}")
    print(f"  cobertura: {len(todas_linhas)}/{total_ramos_possiveis} ramos = "
          f"{len(todas_linhas)/total_ramos_possiveis:.0%}")

    print("\n=== caso que a suite nunca imaginou ===")
    valor_negativo = -50.0
    resultado_final = calcular_desconto(valor_negativo, 10)
    print(f"  valor_total={valor_negativo}, itens=10 -> {resultado_final}")
    print("  a regra pretendida proibia valor final negativo ou maior que")
    print("  o original -- nenhuma das duas checagens existe no codigo.")
    print("  esse caso passa exatamente pelos MESMOS ramos que os três")
    print("  testes existentes já cobrem (entrada, inicializa, ramo com")
    print("  desconto, calcula desconto, calcula valor final) -- cobertura")
    print("  de linha continua em 100%, e o resultado ainda está errado.")

    print("\n=== leitura ===")
    print("  cobertura de linha prova que todo caminho do código FOI")
    print("  executado por algum teste -- nunca prova que o valor que saiu")
    print("  era o valor certo para aquela entrada. a regra de negócio que")
    print("  faltou (nunca aceitar valor de entrada inválido) não é um ramo")
    print("  de código que a cobertura pudesse ter avisado que faltava --")
    print("  é uma regra que ninguém escreveu no código nem no teste.")


if __name__ == "__main__":
    main()
