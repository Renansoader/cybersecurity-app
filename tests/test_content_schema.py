"""Um módulo malformado não pode chegar à tela — e o erro tem que dizer onde está."""

import copy
import json

import pytest

from app import content

MODULO_EXEMPLO = content.PASTA_DADOS / "modulos" / "00-01-o-que-e-ciberseguranca.json"


@pytest.fixture
def modulo_valido():
    with open(MODULO_EXEMPLO, encoding="utf-8") as arq:
        return json.load(arq)


def escrever(tmp_path, dados, nome="modulo-teste.json"):
    caminho = tmp_path / nome
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return caminho


# --- o conteúdo que já existe carrega ---

def test_niveis_json_carrega_e_valida():
    niveis = content.carregar_niveis()
    assert [n["id"] for n in niveis] == [0, 1, 2, 3, 4, 5]
    assert niveis[0]["desbloqueio"]["tipo"] == "aberto"
    assert niveis[5]["desbloqueio"] == {"tipo": "dominio", "niveis": [3, 4], "minimo": 0.6}


def test_todos_os_modulos_de_data_carregam_sem_erro():
    modulos, erros = content.carregar_modulos()
    assert erros == []
    assert "0.1" in modulos


def test_modulo_exemplo_usa_pelo_menos_quatro_tipos(modulo_valido):
    tipos = {q["tipo"] for q in modulo_valido["questoes"]}
    assert len(tipos) >= 4
    assert tipos <= set(content.CAMPOS_POR_TIPO)


def test_modulo_exemplo_testa_todos_os_objetivos_que_declara(modulo_valido):
    cobertos = {i for q in modulo_valido["questoes"] for i in q["objetivos"]}
    assert cobertos == set(range(len(modulo_valido["objetivos"])))


# --- cobertura dos objetivos ---

def test_objetivo_sem_questao_reprova_o_modulo(tmp_path, modulo_valido):
    modulo_valido["objetivos"].append("Objetivo que nenhuma questão testa")
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "objetivos"
    assert "Objetivo que nenhuma questão testa" in erro.value.detalhe


def test_questao_apontando_objetivo_inexistente_e_recusada(tmp_path, modulo_valido):
    modulo_valido["questoes"][0]["objetivos"] = [7]
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes[0.1.q1].objetivos"


def test_questao_sem_campo_objetivos_e_recusada(tmp_path, modulo_valido):
    del modulo_valido["questoes"][0]["objetivos"]
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes[0].objetivos"


# --- o que precisa falhar, falha apontando arquivo e campo ---

def test_campo_obrigatorio_ausente_diz_qual_arquivo_e_qual_campo(tmp_path, modulo_valido):
    del modulo_valido["objetivos"]
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.arquivo == "modulo-teste.json"
    assert erro.value.campo == "modulo.objetivos"


def test_indice_correta_fora_da_lista_de_alternativas(tmp_path, modulo_valido):
    modulo_valido["questoes"][0]["correta"] = 9
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes[0.1.q1].correta"


def test_distrator_sem_justificativa_e_recusado(tmp_path, modulo_valido):
    """Se não dá para justificar o distrator, o distrator está ruim."""
    modulo_valido["questoes"][0]["por_que_erradas"].pop("2")
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes[0.1.q1].por_que_erradas"
    assert "faltando" in erro.value.detalhe


def test_questao_sem_pergunta_socratica_e_recusada(tmp_path, modulo_valido):
    del modulo_valido["questoes"][0]["pergunta_socratica"]
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes[0].pergunta_socratica"


def test_tipo_desconhecido_e_recusado(tmp_path, modulo_valido):
    modulo_valido["questoes"][0]["tipo"] = "quiz"
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes[0.1.q1].tipo"


def test_mais_de_oito_blocos_de_teoria_e_recusado(tmp_path, modulo_valido):
    bloco = modulo_valido["teoria"][0]
    modulo_valido["teoria"] = [
        {**copy.deepcopy(bloco), "id": f"0.1.t{i}"} for i in range(9)
    ]
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "teoria"


def test_ids_repetidos_sao_recusados(tmp_path, modulo_valido):
    modulo_valido["questoes"][1]["id"] = modulo_valido["questoes"][0]["id"]
    caminho = escrever(tmp_path, modulo_valido)

    with pytest.raises(content.ErroDeConteudo) as erro:
        content.carregar_modulo(caminho)

    assert erro.value.campo == "questoes.id"


def test_json_quebrado_vira_erro_de_conteudo_e_nao_derruba_a_carga(tmp_path, modulo_valido):
    escrever(tmp_path, modulo_valido, "bom.json")
    (tmp_path / "quebrado.json").write_text("{ isso não é json", encoding="utf-8")

    modulos, erros = content.carregar_modulos(tmp_path)

    assert "0.1" in modulos          # o módulo bom carregou
    assert len(erros) == 1
    assert "quebrado.json" in erros[0]
