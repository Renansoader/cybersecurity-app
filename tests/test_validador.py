"""As regras 6 e 7 do validador.

Regra 6: o molde "Pergunte ⟨…⟩" nas dicas — forma pura, mora inteira numa
expressão regular com lookbehind. Se ela parar de casar, a regra vira um laço
que nunca acusa nada e ninguém percebe.

Regra 7: a alternativa correta estruturalmente única entre as quatro (única
com dígito, única com negação) — mesmo defeito da "correta é a mais longa",
por outro canal. Medida contra os 27 módulos publicados antes de virar regra:
ver o comentário de EIXOS_UNICIDADE em ferramentas/validar_modulo.py para os
números e para "interrogativa" ter ficado de fora por zero ocorrência.
"""

import pytest

from ferramentas.validar_modulo import (
    MOLDE_PERGUNTE,
    achar_gabarito_entregue,
    _unicidade_estrutural,
)

ACUSA = [
    "Pergunte o que acontece com o tráfego.",
    "Pergunte-se qual dos dois sente o número primeiro.",
    "Se pergunte o que a marcação carrega.",
    "Pergunta-se onde o equipamento está.",
    "Questione a premissa do enunciado.",
    "Indague o motivo da segunda seção.",
    "O artefato tem duas seções. Pergunte por que a segunda existe.",
    "Releia o enunciado; pergunte-se o que mudou.",
]

PASSA = [
    "Compare a porta de destino com a das linhas anteriores.",
    "A pergunta certa aqui é outra.",
    "Separe os dois assuntos antes de escolher.",
    # limite conhecido: o molde no meio da frase não é o que a regra proíbe
    "Pense em mil conversas simultâneas e pergunte qual sente esse número primeiro.",
]


@pytest.mark.parametrize("dica", ACUSA)
def test_molde_e_acusado(dica):
    assert MOLDE_PERGUNTE.search(dica), dica


@pytest.mark.parametrize("dica", PASSA)
def test_dica_legitima_passa(dica):
    assert not MOLDE_PERGUNTE.search(dica), dica


# --------------------------------------------------------------------------
# Regra 7: unicidade estrutural (dígito, negação)
# --------------------------------------------------------------------------

def test_correta_unica_com_digito_e_acusada():
    alternativas = [
        "A correta cita 42 unidades",
        "Distratora sem número",
        "Outra distratora sem número",
        "Mais uma sem número",
    ]
    achados = _unicidade_estrutural(alternativas, 0)
    assert ("dígito", "presente") in achados


def test_correta_unica_sem_digito_e_acusada():
    alternativas = [
        "A correta não cita nenhum número",
        "Distratora com 10 unidades",
        "Outra distratora com 20 unidades",
        "Mais uma com 30 unidades",
    ]
    achados = _unicidade_estrutural(alternativas, 0)
    assert ("dígito", "ausente") in achados


def test_digito_espalhado_por_todas_nao_acusa():
    # Três ou quatro alternativas com dígito, mas nenhuma "sozinha" nos dois
    # extremos — duas com número e duas sem não é nem "só a correta tem" nem
    # "só a correta não tem".
    alternativas = [
        "A correta cita 42 unidades",
        "Distratora cita 7 unidades",
        "Outra distratora sem número",
        "Mais uma sem número",
    ]
    achados = _unicidade_estrutural(alternativas, 0)
    assert not any(nome == "dígito" for nome, _ in achados)


def test_correta_unica_com_negacao_e_acusada():
    alternativas = [
        "A correta não é o mesmo que a alternativa parecida",
        "Distratora afirma algo direto",
        "Outra distratora afirma outra coisa",
        "Mais uma distratora afirma mais uma coisa",
    ]
    achados = _unicidade_estrutural(alternativas, 0)
    assert ("negação", "presente") in achados


def test_correta_unica_sem_negacao_e_acusada():
    alternativas = [
        "A correta afirma algo direto",
        "Distratora nunca faz isso",
        "Outra distratora não faz aquilo",
        "Mais uma nenhuma vez faz isso",
    ]
    achados = _unicidade_estrutural(alternativas, 0)
    assert ("negação", "ausente") in achados


def test_negacao_em_metade_nao_acusa():
    alternativas = [
        "A correta não é o mesmo que a outra",
        "Distratora também não é a mesma coisa",
        "Outra distratora afirma algo direto",
        "Mais uma afirma outra coisa direta",
    ]
    achados = _unicidade_estrutural(alternativas, 0)
    assert not any(nome == "negação" for nome, _ in achados)


def _questao_mc(qid, correta_idx, alternativas):
    return {
        "id": qid, "tipo": "conceitual", "correta": correta_idx,
        "alternativas": alternativas,
        "enunciado": "Enunciado neutro sobre um assunto qualquer do módulo.",
        "dicas": ["Pense com calma no que foi pedido.",
                  "Compare as quatro opções entre si.",
                  "Releia o enunciado antes de responder."],
    }


def test_regra_7_roda_sobre_modulo_com_pareamento_e_ordenacao_sem_quebrar():
    """Regressão: a regra 6 nasceu só dentro do laço gated por `alternativas` e
    ficou cega para pareamento e ordenação, porque os dois não têm esse campo.
    A regra 7 é, por natureza, sobre "correta contra três distratoras" — algo
    que pareamento (quatro pares igualmente certos) e ordenação (uma
    permutação, sem distrator nenhum) não têm. O teste garante que o laço da
    regra 7 não quebra ao encontrar esses dois tipos misturados no mesmo
    módulo, e que ele não inventa um aviso onde não há "alternativas" para
    julgar — não que ele os avalie, porque estruturalmente não há o que
    avaliar neles.
    """
    dados = {
        "id": "9.9",
        "questoes": [
            _questao_mc("9.9.q1", 0, [
                "A correta cita 42 unidades",
                "Distratora sem número",
                "Outra distratora sem número",
                "Mais uma sem número",
            ]),
            {
                "id": "9.9.q2", "tipo": "pareamento",
                "pares": [["Esquerda 1", "Direita 1"], ["Esquerda 2", "Direita 2"]],
                "dicas": ["Pense na relação entre os dois lados.",
                          "Compare os pares um a um.",
                          "Releia as definições antes de ligar."],
            },
            {
                "id": "9.9.q3", "tipo": "ordenacao",
                "itens": ["Primeiro passo", "Segundo passo", "Terceiro passo", "Quarto passo"],
                "dicas": ["Pense na sequência lógica do processo.",
                          "Compare a ordem proposta com a real.",
                          "Releia os passos antes de decidir."],
            },
        ],
    }
    avisos = []
    achar_gabarito_entregue(dados, avisos)  # não pode lançar exceção

    unicidade = [a for a in avisos if "único" in a or "única" in a]
    assert any(a.startswith("9.9.q1") for a in unicidade), avisos
    assert not any(a.startswith("9.9.q2") for a in unicidade), avisos
    assert not any(a.startswith("9.9.q3") for a in unicidade), avisos
