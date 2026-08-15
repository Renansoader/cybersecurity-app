"""Controle de qualidade do conteúdo (especificação 10.1).

O esquema em content.py já garante que os campos pedagógicos existem. Aqui
ficam as regras de quantidade e de consistência que só fazem sentido sobre
conteúdo real: mínimo de questões por módulo, variedade de tipos, e nenhuma
questão com mais de uma alternativa defensável.

Roda sobre todos os módulos de data/modulos/, então módulo novo entra no teste
sozinho.
"""

import pytest

from app import content

MIN_QUESTOES = 35
MAX_QUESTOES = 60
MIN_TIPOS = 4
MIN_BLOCOS_TEORIA = 4

MODULOS, ERROS_DE_CARGA = content.carregar_modulos()
IDS = sorted(MODULOS)


def modulo(mid):
    return MODULOS[mid]


def test_todos_os_modulos_carregam():
    assert ERROS_DE_CARGA == []
    assert IDS, "nenhum módulo encontrado em data/modulos/"


@pytest.mark.parametrize("mid", IDS)
def test_modulo_tem_entre_35_e_60_questoes(mid):
    total = len(modulo(mid)["questoes"])
    assert MIN_QUESTOES <= total <= MAX_QUESTOES, (
        f"módulo {mid} tem {total} questões")


@pytest.mark.parametrize("mid", IDS)
def test_modulo_usa_pelo_menos_quatro_tipos(mid):
    tipos = {q["tipo"] for q in modulo(mid)["questoes"]}
    assert len(tipos) >= MIN_TIPOS, f"módulo {mid} usa só {sorted(tipos)}"


@pytest.mark.parametrize("mid", IDS)
def test_modulo_tem_entre_quatro_e_oito_blocos_de_teoria(mid):
    total = len(modulo(mid)["teoria"])
    assert MIN_BLOCOS_TEORIA <= total <= content.MAX_BLOCOS_TEORIA, (
        f"módulo {mid} tem {total} blocos de teoria")


@pytest.mark.parametrize("mid", IDS)
def test_nenhuma_questao_tem_alternativa_repetida(mid):
    """Duas alternativas iguais seriam duas respostas igualmente defensáveis."""
    for questao in modulo(mid)["questoes"]:
        alternativas = questao.get("alternativas")
        if not alternativas:
            continue
        repetidas = {a for a in alternativas if alternativas.count(a) > 1}
        assert not repetidas, f"{questao['id']}: alternativas repetidas {repetidas}"


@pytest.mark.parametrize("mid", IDS)
def test_indice_correta_existe_na_lista_de_alternativas(mid):
    for questao in modulo(mid)["questoes"]:
        alternativas = questao.get("alternativas")
        if not alternativas:
            continue
        assert 0 <= questao["correta"] < len(alternativas), questao["id"]


@pytest.mark.parametrize("mid", IDS)
def test_todo_distrator_tem_justificativa(mid):
    for questao in modulo(mid)["questoes"]:
        alternativas = questao.get("alternativas")
        if not alternativas:
            continue
        esperadas = {str(i) for i in range(len(alternativas)) if i != questao["correta"]}
        assert set(questao["por_que_erradas"]) == esperadas, questao["id"]


@pytest.mark.parametrize("mid", IDS)
def test_toda_questao_traz_dicas_pergunta_socratica_explicacao_e_fonte(mid):
    for questao in modulo(mid)["questoes"]:
        assert len(questao["dicas"]) >= 2, f"{questao['id']}: poucas dicas"
        assert questao["pergunta_socratica"].strip(), questao["id"]
        assert questao["explicacao"].strip(), questao["id"]
        assert questao["fonte"].strip(), questao["id"]


@pytest.mark.parametrize("mid", IDS)
def test_todo_objetivo_do_modulo_e_testado(mid):
    dados = modulo(mid)
    cobertos = {i for q in dados["questoes"] for i in q["objetivos"]}
    assert cobertos == set(range(len(dados["objetivos"]))), (
        f"módulo {mid}: objetivos sem questão")


@pytest.mark.parametrize("mid", IDS)
def test_ids_de_questao_e_teoria_seguem_o_id_do_modulo(mid):
    dados = modulo(mid)
    for questao in dados["questoes"]:
        assert questao["id"].startswith(dados["id"] + "."), questao["id"]
    for bloco in dados["teoria"]:
        assert bloco["id"].startswith(dados["id"] + "."), bloco["id"]


@pytest.mark.parametrize("mid", IDS)
def test_pre_requisitos_apontam_para_modulos_que_existem(mid):
    for pre in modulo(mid)["pre_requisitos"]:
        assert pre in MODULOS, f"módulo {mid} depende de {pre}, que não existe"


def test_niveis_declarados_batem_com_o_arquivo_de_niveis():
    ids_de_nivel = {n["id"] for n in content.carregar_niveis()}
    for mid, dados in MODULOS.items():
        assert dados["nivel"] in ids_de_nivel, f"módulo {mid} em nível inexistente"
