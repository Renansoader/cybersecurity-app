"""A resposta não pode chegar à tela antes de o usuário confirmar uma tentativa."""

import pytest

from app import content, pedagogy

MODULO = content.carregar_modulo(
    content.PASTA_DADOS / "modulos" / "00-01-o-que-e-ciberseguranca.json")
QUESTOES = {q["id"]: q for q in MODULO["questoes"]}


@pytest.fixture
def multipla():
    return QUESTOES["0.1.q1"]


# --- nada de gabarito antes da hora ---

@pytest.mark.parametrize("questao", MODULO["questoes"], ids=lambda q: q["id"])
def test_questao_para_exibir_nao_leva_a_resposta(questao):
    visivel = pedagogy.questao_para_exibir(questao)
    assert set(visivel) & set(pedagogy.CAMPOS_DE_RESPOSTA) == set()


def test_questao_para_exibir_mantem_o_que_a_tela_precisa(multipla):
    visivel = pedagogy.questao_para_exibir(multipla)
    assert visivel["enunciado"] == multipla["enunciado"]
    assert visivel["alternativas"] == multipla["alternativas"]
    assert visivel["dicas_disponiveis"] == len(multipla["dicas"])
    assert "dicas" not in visivel, "as dicas saem uma a uma, sob pedido"


def test_pareamento_nao_entrega_o_gabarito_nas_colunas():
    visivel = pedagogy.questao_para_exibir(QUESTOES["0.1.q6"])
    assert "pares" not in visivel
    assert len(visivel["coluna_esquerda"]) == 3
    assert len(visivel["coluna_direita"]) == 3
    # as colunas não podem sair pareadas na mesma ordem
    pares_originais = QUESTOES["0.1.q6"]["pares"]
    assert visivel["coluna_direita"] != [par[1] for par in pares_originais]


def test_ordenacao_nao_entrega_a_ordem_correta():
    visivel = pedagogy.questao_para_exibir(QUESTOES["0.1.q4"])
    assert "ordem_correta" not in visivel
    assert len(visivel["itens"]) == 5


# --- dicas ---

def test_dica_so_libera_depois_de_vinte_segundos(multipla):
    assert pedagogy.dica_liberada(19, 0, multipla) is False
    assert pedagogy.dica_liberada(20, 0, multipla) is True


def test_dicas_saem_na_ordem_e_acabam(multipla):
    assert pedagogy.proxima_dica(multipla, 0) == multipla["dicas"][0]
    assert pedagogy.proxima_dica(multipla, 2) == multipla["dicas"][2]
    assert pedagogy.proxima_dica(multipla, len(multipla["dicas"])) is None
    assert pedagogy.dica_liberada(300, len(multipla["dicas"]), multipla) is False


# --- feedback ---

def test_quem_errou_ve_primeiro_por_que_a_escolha_dele_estava_errada(multipla):
    blocos = pedagogy.feedback(multipla, escolha=2, acertou=False)

    assert blocos[0][0] == "sua_escolha"
    assert blocos[0][1] == multipla["por_que_erradas"]["2"]
    assert blocos[1][0] == "explicacao"


def test_quem_acertou_ve_a_explicacao_e_depois_os_distratores(multipla):
    blocos = pedagogy.feedback(multipla, escolha=multipla["correta"], acertou=True)

    assert blocos[0] == ("explicacao", multipla["explicacao"])
    assert [rotulo for rotulo, _ in blocos[1:]] == ["por_que_errada"] * 3


def test_feedback_de_questao_sem_alternativas_nao_quebra():
    blocos = pedagogy.feedback(QUESTOES["0.1.q4"], escolha=None, acertou=False)
    assert blocos == [("explicacao", QUESTOES["0.1.q4"]["explicacao"])]
