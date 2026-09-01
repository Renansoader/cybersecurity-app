"""A regra 6 do validador: o molde "Pergunte ⟨…⟩" nas dicas.

A regra é de forma, e a forma mora inteira numa expressão regular com
lookbehind. Se ela parar de casar, a regra vira um laço que nunca acusa nada e
ninguém percebe. Este arquivo é o que falha nesse caso.
"""

import pytest

from ferramentas.validar_modulo import MOLDE_PERGUNTE

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
