"""O chutador_de_forma: cada estratégia é uma heurística pura, sem ler `correta`.
Este arquivo garante que a lógica de decisão (aplica / abstém / índice certo)
não quebra silenciosamente — é o que a terceira rodada de medição da regra 7
depende para não virar tautologia despercebida."""

from ferramentas.chutador_de_forma import (
    evita_absoluto,
    mais_curta,
    mais_longa,
    unica_com_digito,
    unica_com_negacao,
    unica_sem_digito,
    unica_sem_negacao,
    wilson,
)


def test_mais_longa_escolhe_a_de_mais_caracteres():
    assert mais_longa(["curta", "a mais longa de todas", "média", "outra"]) == 1


def test_mais_curta_escolhe_a_de_menos_caracteres():
    assert mais_curta(["curta", "a mais longa de todas", "média", "outra"]) == 0


def test_unica_com_negacao_acha_a_marcada():
    assert unica_com_negacao(["não faz X", "faz Y", "faz Z", "faz W"]) == 0


def test_unica_com_negacao_abstem_com_duas_marcadas():
    assert unica_com_negacao(["não faz X", "não faz Y", "faz Z", "faz W"]) is None


def test_unica_sem_negacao_acha_a_desmarcada():
    assert unica_sem_negacao(["faz X", "não faz Y", "nunca faz Z", "nenhum faz W"]) == 0


def test_unica_com_digito_acha_a_marcada():
    assert unica_com_digito(["usa 42 unidades", "sem número", "sem número", "sem número"]) == 0


def test_unica_sem_digito_acha_a_desmarcada():
    assert unica_sem_digito(["sem número", "usa 1", "usa 2", "usa 3"]) == 0


def test_evita_absoluto_elimina_e_pega_a_mais_longa_do_resto():
    alternativas = ["sempre funciona", "curta", "a mais longa das que sobraram", "nunca falha"]
    assert evita_absoluto(alternativas) == 2


def test_evita_absoluto_abstem_se_todas_forem_absolutas():
    assert evita_absoluto(["sempre X", "nunca Y", "qualquer Z", "todo W"]) is None


def test_wilson_contem_a_taxa_observada():
    baixo, alto = wilson(76, 82)
    assert baixo <= 76 / 82 <= alto
