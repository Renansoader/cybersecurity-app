# -*- coding: utf-8 -*-
"""Laboratorio 5.1 -- por que a mesma correcao custa mais quanto mais tarde
ela acontece.

Nao cita nenhum multiplicador de industria pronto (o classico "1x/10x/100x"
e contestado e varia por contexto -- citar um numero fixo seria decorar,
nao entender). Em vez disso, modela o mecanismo: cada fase do
desenvolvimento acrescenta dependentes reais sobre uma decisao already
tomada, e o custo de mudar essa decisao e proporcional a quantos
dependentes precisam ser tocados tambem.

Roda com: python custo_por_fase.py
"""


class Decisao:
    def __init__(self, nome):
        self.nome = nome
        self.dependentes = []  # outras decisoes/artefatos construidos em cima desta

    def adicionar_dependente(self, nome):
        self.dependentes.append(nome)

    def custo_de_mudar(self, custo_por_dependente=1):
        # mudar a decisao exige revisar/ajustar cada coisa que foi construida
        # assumindo que ela era daquele jeito -- 1 (a propria decisao) + dependentes
        return 1 + len(self.dependentes) * custo_por_dependente


def simular_fase_design():
    d = Decisao("formato do identificador de usuario")
    # em design, nada mais foi construido ainda
    return d


def simular_fase_codigo(d):
    d.adicionar_dependente("funcao de validacao de entrada")
    d.adicionar_dependente("esquema da tabela no banco")
    return d


def simular_fase_teste(d):
    d.adicionar_dependente("suite de testes automatizados")
    d.adicionar_dependente("dados de exemplo usados em outros testes")
    return d


def simular_fase_producao(d):
    d.adicionar_dependente("integracao com sistema de terceiro (API publica)")
    d.adicionar_dependente("dados reais ja gravados no formato antigo")
    d.adicionar_dependente("documentacao publicada para integradores externos")
    return d


def main():
    print("=== mesma decisao, custo de mudar medido em cada fase ===")

    d_design = simular_fase_design()
    print(f"  design:    {len(d_design.dependentes)} dependentes -> "
          f"custo de mudar = {d_design.custo_de_mudar()}")

    d_codigo = simular_fase_codigo(Decisao("formato do identificador de usuario"))
    print(f"  codigo:    {len(d_codigo.dependentes)} dependentes -> "
          f"custo de mudar = {d_codigo.custo_de_mudar()}")

    d_teste = simular_fase_teste(simular_fase_codigo(Decisao("formato do identificador de usuario")))
    print(f"  teste:     {len(d_teste.dependentes)} dependentes -> "
          f"custo de mudar = {d_teste.custo_de_mudar()}")

    d_prod = simular_fase_producao(simular_fase_teste(simular_fase_codigo(
        Decisao("formato do identificador de usuario"))))
    print(f"  producao:  {len(d_prod.dependentes)} dependentes -> "
          f"custo de mudar = {d_prod.custo_de_mudar()}")

    print("\n=== leitura ===")
    print("  a decisao em si nao mudou de fase para fase -- o que mudou foi")
    print("  quanta coisa real foi construida em cima dela, assumindo que")
    print("  ela nao ia mudar. o custo de mudar nao vem de a correcao ser")
    print("  mais dificil tecnicamente: vem de precisar tocar em cada")
    print("  dependente que so existe porque a decisao original parecia")
    print("  definitiva. em producao, alguns desses dependentes (integracao")
    print("  externa, dado ja gravado) nem estao sob o controle de quem")
    print("  precisa corrigir.")


if __name__ == "__main__":
    main()
